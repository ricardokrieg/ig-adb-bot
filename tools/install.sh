adb disconnect $1
adb connect $1

adb install resources/ADBKeyboard.apk
adb shell ime set com.android.adbkeyboard/.AdbIME
adb install resources/instagram.apk
adb push resources/ig_image.jpeg /sdcard/Download/
