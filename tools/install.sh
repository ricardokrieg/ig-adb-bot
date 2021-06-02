curl \
  -k \
  -X POST \
  -u genymotion:$2 \
  -H "Content-Type: application/json" \
  -d '{"active": true, "active_on_reboot": true}' \
  https://$3/api/v1/configuration/adb

adb disconnect $1
adb connect $1

adb install resources/ADBKeyboard.apk
adb shell ime set com.android.adbkeyboard/.AdbIME
adb install resources/instagram.apk
adb push resources/ig_image.jpeg /sdcard/Download/
