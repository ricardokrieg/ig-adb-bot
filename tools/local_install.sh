adb disconnect $1
adb connect $1

adb -s $1 install resources/ADBKeyboard.apk
adb -s $1 shell ime set com.android.adbkeyboard/.AdbIME
adb -s $1 install resources/instagram.apk
adb -s $1 push resources/casasbahia.jpeg /sdcard/Download/
