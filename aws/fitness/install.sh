while [ -z "$CURL_OUTPUT" ]
do
    sleep 30
    echo "Trying to connect..."
    CURL_OUTPUT=$(curl \
        -k \
        -s \
        -i \
        --connect-timeout 5 \
        -X POST \
        -u genymotion:$1 \
        -H "Content-Type: application/json" \
        -d '{"active": true, "active_on_reboot": true}' \
        https://$2/api/v1/configuration/adb)
done

~/platform-tools/adb disconnect $2:5555
~/platform-tools/adb connect $2:5555

~/platform-tools/adb -s $2:5555 install ./ig-adb-bot/resources/instagram.apk

i=1
ls ./ig-adb-bot/aws/fitness/images |sort -R |tail -3 |while read file; do
  cp ./ig-adb-bot/aws/fitness/images/$file $i.jpg
  ~/platform-tools/adb -s $2:5555 push $i.jpg /sdcard/Download/
  rm $i.jpg
  ((i++))
done
