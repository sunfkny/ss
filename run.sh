if [ -e '/data/data/com.termux/files/home/ss/profile.db' ] ; then
echo '清理db缓存'
rm -f '/data/data/com.termux/files/home/ss/profile.db'
fi;

if [ -e '/data/data/com.termux/files/home/ss/profile.db-shm' ] ; then
echo '清理db-shm缓存'
rm -f '/data/data/com.termux/files/home/ss/profile.db-shm'
fi;

if [ -e '/data/data/com.termux/files/home/ss/profile.db-wal' ] ; then
echo '清理db-wal缓存'
rm -f '/data/data/com.termux/files/home/ss/profile.db-wal'
fi;

if [ -e '/data/data/com.termux/files/home/ss/getVpsInfo.json' ] ; then
echo '清理getVpsInfo缓存'
rm -f '/data/data/com.termux/files/home/ss/getVpsInfo.json'
fi;

if [ -e '/data/data/com.termux/files/home/ss/info.json' ] ; then
echo '清理info缓存'
rm -f '/data/data/com.termux/files/home/ss/info.json'
fi;

if [ -e '/data/data/com.termux/files/home/ss/time.json' ] ; then
echo '清理time缓存'
rm -f '/data/data/com.termux/files/home/ss/time.json'
fi;

echo "复制数据库"
tsudo cp /data/data/com.galaxylab.ss/databases/profile.db /data/data/com.termux/files/home/ss/profile.db

echo "执行Python脚本"
tsudo python /data/data/com.termux/files/home/ss/main.py


echo "自动上传github"
cd /data/data/com.termux/files/home/ss/
git add .
git commit -m 'upload'
git push



tsudo cp /data/data/com.termux/files/home/ss/info.json /sdcard/.android/info.json
tsudo cp /data/data/com.termux/files/home/ss/time.json /sdcard/.android/time.json
echo "开始本地预览"
tsudo am start -n com.mixplorer/com.mixplorer.activities.ContentViewerActivity -d "/sdcard/.android/index.html" > /dev/null


echo "执行完成，任意键退出......"
get_char()
{
    SAVEDSTTY=`stty -g`
    stty -echo
    stty cbreak
    dd if=/dev/tty bs=1 count=1 2> /dev/null
    stty -raw
    stty echo
    stty $SAVEDSTTY
}
char=`get_char`