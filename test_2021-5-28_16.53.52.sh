
echo '-----start scp-----'
date
mkdir /home/ads/ADS_cma2loc_2021-5-28_16.53.52/
cd /home/ads/ADS_cma2loc_2021-5-28_16.53.52
echo "`date`" > README
scp -r   10.24.237.31:/mnt/fy4data/AGRI/L2/CTH/REGC/NOM/2020/20201028/FY4A-_AGRI--_N_REGC_1047E_L2-_CTH-_MULT_NOM_20201028225336_20201028225753_4000M_V0001.NC /home/ads/ADS_cma2loc_2021-5-28_16.53.52/
echo '-----start git init-----'
date
git init
git remote add origin ssh://git@git.piesat.cn:10002/QXYG/algorithm/ADS/ADS_cma2loc.git
git checkout -b 2021-5-28_16.53.52
echo '-----start git add-----'
date
git add .
git commit -am 'init commit'
echo '-----start push-----'
date
git push origin 2021-5-28_16.53.52
echo '-----end push-----'
date
sleep 60
date
echo 'will remove ADS_cma2loc_2021-5-28_16.53.52 in 540 seconds'
sleep 60
date
echo 'will remove ADS_cma2loc_2021-5-28_16.53.52 in 480 seconds'
sleep 60
date
echo 'will remove ADS_cma2loc_2021-5-28_16.53.52 in 420 seconds'
sleep 60
date
echo 'will remove ADS_cma2loc_2021-5-28_16.53.52 in 360 seconds'
sleep 60
date
echo 'will remove ADS_cma2loc_2021-5-28_16.53.52 in 300 seconds'
sleep 60
date
echo 'will remove ADS_cma2loc_2021-5-28_16.53.52 in 240 seconds'
sleep 60
date
echo 'will remove ADS_cma2loc_2021-5-28_16.53.52 in 180 seconds'
sleep 60
date
echo 'will remove ADS_cma2loc_2021-5-28_16.53.52 in 120 seconds'
sleep 60
date
echo 'will remove ADS_cma2loc_2021-5-28_16.53.52 in 60 seconds'
sleep 60
date
echo 'will remove ADS_cma2loc_2021-5-28_16.53.52 in 0 seconds'

echo 'rmING /home/ads/ADS_cma2loc_2021-5-28_16.53.52/'
rm -rf /home/ads/ADS_cma2loc_2021-5-28_16.53.52/
date
echo '-----end rm-----'
