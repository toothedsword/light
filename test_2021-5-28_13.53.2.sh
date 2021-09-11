
echo '-----start scp-----'
date
mkdir /home/ads/ADS_cma2loc_2021-5-28_13.53.2/
cd /home/ads/ADS_cma2loc_2021-5-28_13.53.2
echo "`date`" > README
scp -r   10.24.237.31:/mnt/swapdata/ADSCODE/ADS/light/figure/L1/FDI/DISK/2021/20210528/FY4B-_AGRI--_N_DISK_1047E_L1-_FDI-_MULT_NOM_20210528001500_20210528002959_4000M_V0001.TIFF /home/ads/ADS_cma2loc_2021-5-28_13.53.2/
echo '-----start git init-----'
date
git init
git remote add origin ssh://git@git.piesat.cn:10002/QXYG/algorithm/ADS/ADS_cma2loc.git
git checkout -b 2021-5-28_13.53.2
echo '-----start git add-----'
date
git add .
git commit -am 'init commit'
echo '-----start push-----'
date
git push origin 2021-5-28_13.53.2
echo '-----end push-----'
date
sleep 60
date
echo 'will remove ADS_cma2loc_2021-5-28_13.53.2 in 540 seconds'
sleep 60
date
echo 'will remove ADS_cma2loc_2021-5-28_13.53.2 in 480 seconds'
sleep 60
date
echo 'will remove ADS_cma2loc_2021-5-28_13.53.2 in 420 seconds'
sleep 60
date
echo 'will remove ADS_cma2loc_2021-5-28_13.53.2 in 360 seconds'
sleep 60
date
echo 'will remove ADS_cma2loc_2021-5-28_13.53.2 in 300 seconds'
sleep 60
date
echo 'will remove ADS_cma2loc_2021-5-28_13.53.2 in 240 seconds'
sleep 60
date
echo 'will remove ADS_cma2loc_2021-5-28_13.53.2 in 180 seconds'
sleep 60
date
echo 'will remove ADS_cma2loc_2021-5-28_13.53.2 in 120 seconds'
sleep 60
date
echo 'will remove ADS_cma2loc_2021-5-28_13.53.2 in 60 seconds'
sleep 60
date
echo 'will remove ADS_cma2loc_2021-5-28_13.53.2 in 0 seconds'

echo 'rmING /home/ads/ADS_cma2loc_2021-5-28_13.53.2/'
rm -rf /home/ads/ADS_cma2loc_2021-5-28_13.53.2/
date
echo '-----end rm-----'
