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
rem 3PAR hostname or IP Address
set STO_ADDR=172.18.11.11
rem Enclosure OA username
set STO_USR=Administrator
rem Enclosure OA password
set STO_PASS=PASSWORD


echo  -- Defining Logical Networks
FOR %%A IN (A B) DO FOR %%V IN (10 20 30 40 50 60) DO python define-ethernet-network.py -a %HOST% -u %USER% -p %PASS% -n VLAN-%%V-%%A -v %%V
echo  -- Defining Logical Interconnect Groups
python define-logical-interconnect-group.py -a %HOST% -u %USER% -p %PASS% -n "VC FlexFabric Production" -i 1:Flex2040f8 2:Flex2040f8
echo  -- Defining Uplink Set Groups in Logical Interconnect Group
python define-uplink-set.py -a %HOST% -u %USER% -p %PASS% -n "3PAR SAN A" -i "VC FlexFabric Production" -t FibreChannel -l "3PAR   SAN A"  -o 1:3 1:4
python define-uplink-set.py -a %HOST% -u %USER% -p %PASS% -n "3PAR SAN B" -i "VC FlexFabric Production" -t FibreChannel -l "3PAR   SAN B"  -o 2:3 2:4
python define-uplink-set.py -a %HOST% -u %USER% -p %PASS% -n "Uplink Set 1-A" -i "VC FlexFabric Production" -t Ethernet  -l VLAN-  10-A VLAN-20-A VLAN-30-A VLAN-40-A VLAN-50-A VLAN-60-A -o 1:7 1:8
python define-uplink-set.py -a %HOST% -u %USER% -p %PASS% -n "Uplink Set 1-B" -i "VC FlexFabric Production" -t Ethernet  -l VLAN-  10-B VLAN-20-B VLAN-30-B VLAN-40-B VLAN-50-B VLAN-60-B -o 2:7 2:8
echo  -- Defining Enclosure Groups
python define-enclosure-group.py -a %HOST% -u %USER% -p %PASS% -n "Prod VC FlexFabric Group 1" -l "VC FlexFabric Production"
echo  -- Import Enclosures
python import-enclosure.py -a %HOST% -u %USER% -p %PASS% -eu %ENC_USR% -ep %ENC_PASS% -e %ENC_ADDR%
echo  -- Add Storage System
python add-storage-system.py -a %HOST% -u %USER% -p %PASS% -s %STO_ADDR% -su %STO_USR% -sp %STO_PASS%
echo  -- Defining Storage Pools
python add-storage-pool.py -a %HOST% -u %USER% -p %PASS% -n SND_CPG1
echo  -- Defining Volume Templates
python add-volume-template.py -a %HOST% -u %USER% -p %PASS% -n "ESX BOOT"
echo  -- Defining volumes
python add-volume.py -a %HOST% -u %USER% -p %PASS% -n vol1
echo  -- Defining profiles
python define-profile.py -a %HOST% -u %USER% -p %PASS%
