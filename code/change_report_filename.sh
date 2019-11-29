#!/bin/bash

FILE_PATH=/home/zunair/Downloads/reports_benign/*
KEYWORD=benign

for file in $FILE_PATH
    
    do

        mv -i "${file}" "$( dirname $file )/benign_$( basename $file)"
    
    done

ls $FILE_PATH
        
