#!/bin/perl
#
my $infile = '/mnt/fy4data/AGRI/L1/FDI/DISK/2021/20210910/FY4A-_AGRI--_N_DISK_1047E_L1-_FDI-_MULT_NOM_20210910000000_20210910001459_4000M_V0001.HDF';
my $res = '4';
my $outdir = './';
my $cthfile = '/mnt/fy4data/AGRI/L2/CTH/DISK/NOM/2021/20210910/FY4A-_AGRI--_N_DISK_1047E_L2-_CTH-_MULT_NOM_20210910000000_20210910001459_4000M_V0001.NC';
my $logfile = './1.log';
my $jsonfile = './1.json';

system("sh disk_light_topo_tb.sh $infile $cthfile $res $outdir $logfile $jsonfile");
