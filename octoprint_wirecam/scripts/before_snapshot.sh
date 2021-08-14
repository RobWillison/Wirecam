#!/bin/sh
# Put the arguments sent by Octolapse into variables for easy use
SNAPSHOT_NUMBER=$1
DELAY_SECONDS=$2
DATA_DIRECTORY=$3
SNAPSHOT_DIRECTORY=$4
SNAPSHOT_FILENAME=$5
SNAPSHOT_FULL_PATH=$6

API_KEY=`cat ~/.octoprint-api-key`

curl 0.0.0.0:5000/plugin/wirecam/next_position -H "X-Api-Key: $API_KEY" 2> /dev/null

echo 0
