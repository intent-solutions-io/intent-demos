#!/usr/bin/env bash
# Install an immutable reviewed source artifact; never run from a mutable checkout.
set -euo pipefail
mode="${1:?publisher or monitor required}"
case "$mode" in publisher|monitor) ;; *) exit 64 ;; esac
repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
packaged=0
if [ -f "$repo_root/.publisher-revision" ]; then
  packaged=1
  revision="$(cat "$repo_root/.publisher-revision")"
  (cd "$repo_root" && sha256sum --status --check artifact.sha256)
else
  revision="$(git -C "$repo_root" rev-parse HEAD)"
fi
[[ "$revision" =~ ^[0-9a-f]{40}$ ]] || { echo "Invalid artifact revision" >&2; exit 1; }
if [ "$packaged" = 0 ] && [ -n "$(git -C "$repo_root" status --porcelain --untracked-files=no)" ]; then
  echo "Refused: tracked tree dirty; install only reviewed committed sources" >&2
  exit 1
fi
install_root="${MC_INSTALL_ROOT:-$HOME/.local/lib/intentsolutions/mission-control-public}"
artifact="$install_root/releases/$revision"
mkdir -p "$install_root/releases"
if [ ! -d "$artifact" ]; then
  stage="$(mktemp -d "$install_root/releases/.install.XXXXXX")"
  if [ "$packaged" = 1 ]; then
    cp -a "$repo_root/." "$stage/"
  else
    git -C "$repo_root" archive "$revision" | tar -x -C "$stage"
  fi
  printf '%s\n' "$revision" > "$stage/.publisher-revision"
  (cd "$stage" && find .publisher-revision scripts site/mission-control -type f -print0 | sort -z | xargs -0 sha256sum > artifact.sha256)
  mv -T "$stage" "$artifact"
fi
(cd "$artifact" && sha256sum --status --check artifact.sha256)
pending="$install_root/.current.next"
if [ -L "$pending" ]; then
  resolved="$(readlink -f "$pending")"
  [[ "$resolved" == "$install_root/releases/"* ]] || { echo "Unexpected install candidate" >&2; exit 1; }
  rm -f "$pending"
elif [ -e "$pending" ]; then
  echo "Unexpected install candidate" >&2; exit 1
fi
ln -s "$artifact" "$pending"
mv -Tf "$install_root/.current.next" "$install_root/current"
units="$HOME/.config/systemd/user"
mkdir -p "$units"
command=check
[ "$mode" != publisher ] || command=publish
job="intent-mc-public-$command"
cat > "$units/$job.service" <<EOF
[Unit]
Description=Mission Control public $command from reviewed immutable source
After=network-online.target

[Service]
Type=oneshot
ExecStart=/bin/bash $install_root/current/scripts/mission_control_job.sh $command
TimeoutStartSec=150
UMask=0022
EOF
cat > "$units/$job.timer" <<EOF
[Unit]
Description=Mission Control public $command every 15 minutes

[Timer]
OnCalendar=*:0/15
Persistent=true
RandomizedDelaySec=30

[Install]
WantedBy=timers.target
EOF
systemctl --user daemon-reload
systemctl --user enable --now "$job.timer"
systemctl --user start "$job.service"
systemctl --user show "$job.service" -p Result -p ExecMainStatus
echo "Installed $mode artifact $revision; verify user lingering for reboot recovery."
