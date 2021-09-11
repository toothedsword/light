
echo '-----start scp-----'
date
mkdir /home/ads/ADS_cma2loc_2021-5-28_16.18.22/
cd /home/ads/ADS_cma2loc_2021-5-28_16.18.22
echo "`date`" > README
scp -r   10.24.237.31:/mnt/swapdata/ADSCODE/ADS/light/figure/small_topo_/molave_1028.dat_small_topo__20201028_000000.100.png-molave_1028.dat_small_topo__20201029_000000.100.png_out.gif /home/ads/ADS_cma2loc_2021-5-28_16.18.22/
echo '-----start git init-----'
date
git init
git remote add origin ssh://git@git.piesat.cn:10002/QXYG/algorithm/ADS/ADS_cma2loc.git
git checkout -b 2021-5-28_16.18.22
echo '-----start git add-----'
date
git add .
git commit -am 'init commit'
echo '-----start push-----'
date
git push origin 2021-5-28_16.18.22
echo '-----end push-----'
date
sleep 60
date
echo 'will remove ADS_cma2loc_2021-5-28_16.18.22 in 540 seconds'
sleep 60
date
echo 'will remove ADS_cma2loc_2021-5-28_16.18.22 in 480 seconds'
sleep 60
date
echo 'will remove ADS_cma2loc_2021-5-28_16.18.22 in 420 seconds'
sleep 60
date
echo 'will remove ADS_cma2loc_2021-5-28_16.18.22 in 360 seconds'
sleep 60
date
echo 'will remove ADS_cma2loc_2021-5-28_16.18.22 in 300 seconds'
sleep 60
date
echo 'will remove ADS_cma2loc_2021-5-28_16.18.22 in 240 seconds'
sleep 60
date
echo 'will remove ADS_cma2loc_2021-5-28_16.18.22 in 180 seconds'
sleep 60
date
echo 'will remove ADS_cma2loc_2021-5-28_16.18.22 in 120 seconds'
sleep 60
date
echo 'will remove ADS_cma2loc_2021-5-28_16.18.22 in 60 seconds'
sleep 60
date
echo 'will remove ADS_cma2loc_2021-5-28_16.18.22 in 0 seconds'

echo 'rmING /home/ads/ADS_cma2loc_2021-5-28_16.18.22/'
rm -rf /home/ads/ADS_cma2loc_2021-5-28_16.18.22/
date
echo '-----end rm-----'
