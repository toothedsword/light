#!/usr/bin/env perl
# /**---------------------------------------------------------------------------
#
#         File: gengif.pl
#
#        Usage: ./gengif.pl  
#
#  Description: 
#
#      Options: ---
# Requirements: ---
#         Bugs: ---
#        Notes: ---
#       Author: Liang Peng (...), pengliang@piesat
# Organization: ...
#      Version: 1.0
#      Created: 2021年02月24日 12时17分23秒
#     Revision: ---
# ----------------------------------------------------------------------------*/

use strict;
use warnings;
use utf8;

my $file = shift;
my $opt = shift;

my @file = glob($file);

my $files = '';
my $i = 0;
my $j = 0;
for my $file (@file) {
    chomp($file);
    $files = " $files $file ";
    $i++;
    if ($i >= 10) {
        $j++;
        my $cmd = "convert $opt $files out".sprintf("%03d",$j).".gif";
        print($cmd,"\n");
        system($cmd);
        $files = '';
        $i = 0;
    }
}
if ($i > 0) {
    $j++;
    system("convert $opt $files out".sprintf("%03d",$j).".gif");
}
system("convert  out???.gif out.gif")
