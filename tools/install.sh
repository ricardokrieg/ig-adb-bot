curl \
  -k \
  -X POST \
  -u genymotion:$2 \
  -H "Content-Type: application/json" \
  -d '{"active": true, "active_on_reboot": true}' \
  https://$3/api/v1/configuration/adb

curl \
  -k \
  -X POST \
  -u genymotion:$2 \
  -H "Content-Type: application/json" \
  -d '{"commands": ["settings put secure show_ime_with_hard_keyboard 1"], "timeout_in_seconds": 5}' \
  https://$3/api/v1/android/shell

adb disconnect $1
adb connect $1

adb -s $1 install resources/ADBKeyboard.apk
adb -s $1 shell ime set com.android.adbkeyboard/.AdbIME
adb -s $1 install resources/instagram.apk
#adb -s $1 install resources/instagram_192.apk
#adb -s $1 push resources/ig_image.jpeg /sdcard/Download/
#adb -s $1 push resources/iphone.png /sdcard/Download/
#adb -s $1 push resources/clevelandclinic.jpeg /sdcard/Download/
#adb -s $1 push resources/holagos.jpeg /sdcard/Download/
#adb -s $1 push resources/sorteios_insta.png /sdcard/Download/
adb -s $1 push resources/casasbahia.jpeg /sdcard/Download/
