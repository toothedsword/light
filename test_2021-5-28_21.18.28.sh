
echo '-----start scp-----'
date
mkdir /home/ads/ADS_cma2loc_2021-5-28_21.18.28/
cd /home/ads/ADS_cma2loc_2021-5-28_21.18.28
echo "`date`" > README
scp -r   10.24.237.31:/mnt/swapdata/ADSCODE/ADS/light/figure/_small_topocth_lt-37_n2/molave_1028.dat__small_topocth_lt-37_n2_20201028_000000.24.png-molave_1028.dat__small_topocth_lt-37_n2_20201029_000000.11.png_out.gif /home/ads/ADS_cma2loc_2021-5-28_21.18.28/
echo '-----start git init-----'
date
git init
git remote add origin ssh://git@git.piesat.cn:10002/QXYG/algorithm/ADS/ADS_cma2loc.git
git checkout -b 2021-5-28_21.18.28
echo '-----start git add-----'
date
git add .
git commit -am 'init commit'
echo '-----start push-----'
date
git push origin 2021-5-28_21.18.28
echo '-----end push-----'
date
sleep 60
date
echo 'will remove ADS_cma2loc_2021-5-28_21.18.28 in 540 seconds'
sleep 60
date
echo 'will remove ADS_cma2loc_2021-5-28_21.18.28 in 480 seconds'
sleep 60
date
echo 'will remove ADS_cma2loc_2021-5-28_21.18.28 in 420 seconds'
sleep 60
date
echo 'will remove ADS_cma2loc_2021-5-28_21.18.28 in 360 seconds'
sleep 60
date
echo 'will remove ADS_cma2loc_2021-5-28_21.18.28 in 300 seconds'
sleep 60
date
echo 'will remove ADS_cma2loc_2021-5-28_21.18.28 in 240 seconds'
sleep 60
date
echo 'will remove ADS_cma2loc_2021-5-28_21.18.28 in 180 seconds'
sleep 60
date
echo 'will remove ADS_cma2loc_2021-5-28_21.18.28 in 120 seconds'
sleep 60
date
echo 'will remove ADS_cma2loc_2021-5-28_21.18.28 in 60 seconds'
sleep 60
date
echo 'will remove ADS_cma2loc_2021-5-28_21.18.28 in 0 seconds'

echo 'rmING /home/ads/ADS_cma2loc_2021-5-28_21.18.28/'
rm -rf /home/ads/ADS_cma2loc_2021-5-28_21.18.28/
date
echo '-----end rm-----'
