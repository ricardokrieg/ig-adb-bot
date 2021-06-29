curl \
  -k \
  -X POST \
  -u genymotion:$1 \
  -H "Content-Type: application/json" \
  -d '{"active": true, "active_on_reboot": true}' \
  https://$2/api/v1/configuration/adb

# curl \
#   -k \
#   -X POST \
#   -u genymotion:$1 \
#   -H "Content-Type: application/json" \
#   -d '{"commands": ["settings put secure show_ime_with_hard_keyboard 1"], "timeout_in_seconds": 5}' \
#   https://$2/api/v1/android/shell

~/platform-tools/adb disconnect $2:5555
~/platform-tools/adb connect $2:5555

# ~/platform-tools/adb -s $2:5555 install ../resources/ADBKeyboard.apk
# ~/platform-tools/adb -s $2:5555 shell ime set com.android.adbkeyboard/.AdbIME
~/platform-tools/adb -s $2:5555 install ../resources/instagram.apk
~/platform-tools/adb -s $2:5555 push ../resources/casasbahia.jpeg /sdcard/Download/
~/platform-tools/adb -s $2:5555 reboot

sleep 60

~/platform-tools/adb devices
~/platform-tools/adb disconnect $2:5555
~/platform-tools/adb connect $2:5555

sleep 20

~/platform-tools/adb devices
~/platform-tools/adb disconnect $2:5555
~/platform-tools/adb connect $2:5555

sleep 60

~/platform-tools/adb devices
~/platform-tools/adb disconnect $2:5555
~/platform-tools/adb connect $2:5555
