#!/usr/bin/env bash
# The same deployed immutable code handles the publisher and outside-in monitor.
set -euo pipefail
repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
if [ -f "$repo_root/artifact.sha256" ]; then
  (cd "$repo_root" && sha256sum --status --check artifact.sha256) || { echo "Artifact integrity failure" >&2; exit 2; }
fi
mode="${1:?publish, check or regional required}"
case "$mode" in publish|check|regional) ;; *) exit 64 ;; esac
state_root="${MC_JOB_STATE:-$HOME/.local/state/intent-mc-public}"
mkdir -p "$state_root"
exec 9>"$state_root/$mode.job.lock"
flock -n 9 || exit 0
log_file="$state_root/$mode.log"
set +e
if [ "$mode" = regional ]; then
  python3 "$repo_root/scripts/regional_reachability.py" --target tonsofskills.com > "$log_file.tmp" 2>&1
  first_result=$?
  python3 "$repo_root/scripts/regional_reachability.py" --target www.tonsofskills.com >> "$log_file.tmp" 2>&1
  second_result=$?
  result=0
  [ "$first_result" = 0 ] && [ "$second_result" = 0 ] || result=1
elif [ "$mode" = check ]; then
  python3 "$repo_root/scripts/mission_control.py" check --url "${MC_CHECK_URL:-https://demos.intentsolutions.io/mission-control/}" > "$log_file.tmp" 2>&1
  result=$?
else
  python3 "$repo_root/scripts/mission_control.py" publish > "$log_file.tmp" 2>&1
  result=$?
fi
set -e
mv -f "$log_file.tmp" "$log_file"
cat "$log_file"
if [ "$result" -ne 0 ]; then
  af_cli="${MC_ALERT_FLOOR:-$HOME/bin/lib/alert-floor.sh}"
  if [ ! -f "$af_cli" ]; then
    echo "Mission Control $mode failed; governed alert transport missing" >&2
    exit 2
  fi
  subject="Mission Control public $mode failed"
  [ "$mode" != regional ] || subject="Tons of Skills regional HTTPS check failed or unverified"
  AF_BUZZ_TOPIC=sys-automation AF_HC_URL="" bash "$af_cli" dispatch \
    "$subject. Check the timestamped snapshot and installed job log." \
    "$subject" high sys-automation || {
      echo "Governed alert receipt failed; transport owns its durable spool" >&2
      exit 2
    }
fi
exit "$result"
