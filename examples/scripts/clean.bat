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

echo  -- Removing profiles
python define-profile.py -a %HOST% -u %USER% -p %PASS% -d
echo  -- Removing volumes
python add-volume.py -a %HOST% -u %USER% -p %PASS% -d
echo  -- Removing Volume Templates
python add-volume-template.py -a %HOST% -u %USER% -p %PASS% -d
echo  -- Removing Storage Pools
python add-storage-pool.py -a %HOST% -u %USER% -p %PASS% -d
echo  -- Removing Storage Systems
python add-storage-system.py -a %HOST% -u %USER% -p %PASS% -d
echo  -- Removing Enclosures
python import-enclosure.py -a %HOST% -u %USER% -p %PASS% -eu %ENC_USR% -ep %ENC_PASS% -d
echo  -- Removing Enclosure Groups
python define-enclosure-group.py -a %HOST% -u %USER% -p %PASS% -d
echo  -- Removing Logical Interconnect Groups
python del-logical-interconnect-groups.py -a %HOST% -u %USER% -p %PASS% -d
echo  -- Removing Network Sets
python del-network-set.py -a %HOST% -u %USER% -p %PASS% -d
echo  -- Removing Logical Networks
python del-network.py -a %HOST% -u %USER% -p %PASS% -d
