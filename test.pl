#!/usr/bin/env perl
# /**---------------------------------------------------------------------------
#
#         File: test.pl
#
#        Usage: ./test.pl  
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
#      Created: 2021年01月20日 10时12分14秒
#     Revision: ---
# ----------------------------------------------------------------------------*/

use strict;
use warnings;
use utf8;
use Shell;

use PDL;
use PDL::NiceSlice;

system("python3 -m numpy.f2py -c light.f90 -m light");
system("python3 -m numpy.f2py -c griddata.f90 -m griddata");

