#!/bin/bash
#
#@sviaro
#This script copies and overwrites the necessary files to run CRYOWRF for the testcase
#

#variables
DEST1=/home/viaro/cryos/softwares/cryowrf/CRYOWRF-WRF/test/em_real/input
DEST2=/home/viaro/cryos/softwares/cryowrf/CRYOWRF-WRF/test/em_real
DEST3=/home/viaro/cryos/softwares/cryowrf/CRYOWRF-WRF/phys
DEST4=/home/viaro/cryos/softwares/cryowrf/CRYOWRF-WRF/test/em_real/wpsout
DIR1=/home/viaro/cryos/softwares/cryowrf/CRYOWRF-WRF/test/em_real/outhist

#copy DEST1
cp COSMO.smet $DEST1
cp make_sno_for_sam.py $DEST1

#copy DEST2
cp io.ini $DEST2
cp namelist.input $DEST2
cp outhist_variables_ALPS.txt $DEST2
cp tslist $DEST2
cp WRF.job $DEST2
cp WRF_REAL.job $DEST2

#copy DEST3: compare this file with the local first
cp module_sf_snowpacklsm_TESTCASE.F $DEST3

#copy DEST4
DIR=$DEST4
if [ -d "$DIR" ]; then
    # If it exists, remove everything inside but keep the folder
    rm -rf "${DIR:?}"/*
    echo "Directory '$DIR' cleaned."
else
    # If it doesn't exist, create it
    mkdir "$DIR"
    echo "Directory '$DIR' created."
fi
cp metFiles/met_em* $DEST4

#create directories
mkdir "$DIR1"






