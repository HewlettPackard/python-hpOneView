@echo off
chcp 65001

rem OneView Appliance hostname or IP address
set HOST=oneview
rem OneView Appliance username
set USER=Administrator
rem OneView Appliance password
set PASS=PASSWORD
rem Enclosure OA hostname or IP address
set ENC_ADDR=172.18.1.11
rem Enclosure OA username
set ENC_USR=Administrator
rem Enclosure OA password
set ENC_PASS=PASSWORD

echo  -- Defining Logical Networks
python define-networks.py -a %HOST% -u %USER% -p %PASS%
echo  -- Defining Logical Interconnect Groups
python define-lig.py -a %HOST% -u %USER% -p %PASS%
echo  -- Defining Enclosure Groups
python define-eg.py -a %HOST% -u %USER% -p %PASS%
echo  -- Import Enclosures
python import-enclosure.py -a %HOST% -u %USER% -p %PASS% -eu %ENC_USR% -ep %ENC_PASS% -e %ENC_ADDR%
echo  -- Defining Storage Pools
python add-storage-pools.py -a %HOST% -u %USER% -p %PASS% -n SND_CPG1
echo  -- Defining Volume Templates
echo  -- Defining volumes
python add-volume.py -a %HOST% -u %USER% -p %PASS% -n vol1
echo  -- Defining profiles
python define-profile.py -a %HOST% -u %USER% -p %PASS%
