#!/bin/bash

FILE_PATH=/home/zunair/Downloads/reports_benign/*

for file in $FILE_PATH
    do
        mv -i "${file}" "${file/.corrupt}"
        
    done
ls $FILE_PATH
