sleep 150

curl \
  -k \
  -X POST \
  -u genymotion:$1 \
  -H "Content-Type: application/json" \
  -d '{"active": true, "active_on_reboot": true}' \
  https://$2/api/v1/configuration/adb

~/platform-tools/adb disconnect $2:5555
~/platform-tools/adb connect $2:5555

~/platform-tools/adb -s $2:5555 install ./ig-adb-bot/resources/instagram.apk
