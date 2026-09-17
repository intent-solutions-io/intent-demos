#!/usr/bin/env bash
# System-level independent monitors from a verified packaged release, not a checkout.
set -euo pipefail
[ "$(id -u)" = 0 ] || { echo "Run as root on the independent monitoring host" >&2; exit 1; }
repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
revision="$(cat "$repo_root/.publisher-revision")"
[[ "$revision" =~ ^[0-9a-f]{40}$ ]] || exit 1
(cd "$repo_root" && sha256sum --status --check artifact.sha256)
monitor_user="${MC_MONITOR_USER:-intentsolutions}"
id "$monitor_user" >/dev/null
credentials="${MC_MONITOR_ENV:-/etc/intentsolutions/scorecardecho-observer.env}"
[ -f "$credentials" ] || { echo "Governed notifier environment missing" >&2; exit 1; }
[ -x /usr/local/lib/intentsolutions/buzz-notify.sh ]
[ -f /usr/local/lib/intentsolutions/alert-floor.sh ]
install_root=/usr/local/lib/intentsolutions/mission-control-public
artifact="$install_root/releases/$revision"
mkdir -p "$install_root/releases"
if [ ! -d "$artifact" ]; then
  stage="$(mktemp -d "$install_root/releases/.install.XXXXXX")"
  cp -a "$repo_root/." "$stage/"
  chown -R root:root "$stage"
  chmod -R a+rX,go-w "$stage"
  mv -T "$stage" "$artifact"
fi
(cd "$artifact" && sha256sum --status --check artifact.sha256)
runuser -u "$monitor_user" -- test -r "$artifact/scripts/mission_control_job.sh"
for mode in check regional; do
  job=intent-mc-public-check
  calendar='*:0/5'
  timeout=90
  [ "$mode" != regional ] || { job=tonsofskills-regional; calendar='*-*-* *:07:00'; timeout=210; }
  cat > "/etc/systemd/system/$job.service" <<UNIT
[Unit]
Description=Independent public $mode monitor from $revision
Wants=network-online.target
After=network-online.target
OnFailure=$job-failure.service

[Service]
Type=oneshot
User=$monitor_user
StateDirectory=$job
StateDirectoryMode=0700
Environment=HOME=/var/lib/$job
Environment=MC_JOB_STATE=/var/lib/$job
Environment=AF_STATE_DIR=/var/lib/$job/alert-floor
Environment=MC_ALERT_FLOOR=/usr/local/lib/intentsolutions/alert-floor.sh
Environment=AF_BUZZ_CMD=/usr/local/lib/intentsolutions/buzz-notify.sh
Environment=BUZZ_NOTIFY_BIN=/usr/local/bin/buzz
EnvironmentFile=$credentials
ExecStart=/bin/bash $artifact/scripts/mission_control_job.sh $mode
# A bad product sample already has an accepted governed alert; delivery errors fail.
SuccessExitStatus=1
TimeoutStartSec=$timeout
UMask=0077
NoNewPrivileges=true
PrivateTmp=true
ProtectSystem=strict
ProtectHome=true
MemoryMax=256M
TasksMax=64
UNIT
  cat > "/etc/systemd/system/$job-failure.service" <<UNIT
[Unit]
Description=Governed $job execution failure alert

[Service]
Type=oneshot
User=$monitor_user
Environment=HOME=/var/lib/$job
Environment=AF_STATE_DIR=/var/lib/$job/alert-floor
Environment=AF_BUZZ_CMD=/usr/local/lib/intentsolutions/buzz-notify.sh
Environment=BUZZ_NOTIFY_BIN=/usr/local/bin/buzz
Environment=AF_HC_URL=
EnvironmentFile=$credentials
ExecStart=/bin/bash /usr/local/lib/intentsolutions/alert-floor.sh dispatch "$job execution or alert delivery failed" "$job monitor failure" high sys-automation
TimeoutStartSec=60
UMask=0077
NoNewPrivileges=true
PrivateTmp=true
ProtectSystem=strict
ProtectHome=true
ReadWritePaths=/var/lib/$job
UNIT
  cat > "/etc/systemd/system/$job.timer" <<UNIT
[Unit]
Description=Persistent independent public $mode checks

[Timer]
OnCalendar=$calendar
Persistent=true
RandomizedDelaySec=20

[Install]
WantedBy=timers.target
UNIT
  systemd-analyze verify "/etc/systemd/system/$job.service" "/etc/systemd/system/$job.timer" "/etc/systemd/system/$job-failure.service"
done
systemctl daemon-reload
systemctl enable --now intent-mc-public-check.timer tonsofskills-regional.timer
systemctl start intent-mc-public-check.service
systemctl start --no-block tonsofskills-regional.service
systemctl show intent-mc-public-check.service -p Result -p ExecMainStatus
printf 'Independent monitors installed from %s\n' "$revision"
