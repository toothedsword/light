#!/bin/bash

work_dir=$(cd $(dirname $0); pwd)
cd ${work_dir}
echo ${work_dir}

file_4000M=$1
file_cth=$2
resolution=$3
output_path=$4
json_file=$5
log_file=$6

script_name='/disk_light_topo_tb.py'
script_path=${work_dir}${script_name}
echo ${script_path}

python3 ${script_path} ${file_4000M} ${output_path} ${resolution} ${json_file} ${log_file}
