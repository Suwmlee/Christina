# !/bin/usr

deamo='python userbot.py'
for pid in `ps -ef|grep $deamo|awk '{print $2}'`
do
    echo $pid
    kill -9 $pid
done
nohup python userbot.py > christina.log 2>&1 &
echo OK
