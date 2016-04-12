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
rem 3PAR username
set STO_USR=Administrator
rem 3PAR password
set STO_PASS=PASSWORD
rem 3PAR Storage Domain
set STO_DOM=STORAGE_DOMAIN
rem 3PAR CPG
set STO_CPG=STORAGE_CPG
rem Standalone server iLO hostname or IP Address
set SRV_ADDR=172.18.6.15
rem Standalone Server iLO username
set SRV_USR=Administrator
rem Standalone Server iLO password
set SRV_PASS=PASSWORD
rem Firmware Baseline
set FW_BASE=HP_Service_Pack_for_ProLiant_2015.10.0-SPP2015100.2015_0921.6.iso
rem Server boot order (dependent on server hardware type)
set BOOT_G78=HardDisk PXE USB CD Floppy
set BOOT_G9_LEGACY=HardDisk PXE USB CD
set BOOT_G9_UEFI=HardDisk


set CONN_LIST_BFS=%TMP%\oneview_conn_list_bfs-%RANDOM%-%TIME:~6,5%.tmp
set CONN_LIST=%TMP%\oneview_conn_list-%RANDOM%-%TIME:~6,5%.tmp
set CONN_LIST_TEMPLATE=%TMP%\oneview_conn_list-template-%RANDOM%-%TIME:~6,5%.tmp
set SAN_LIST1=%TMP%\oneview_san_list1-%RANDOM%-%TIME:~6,5%.tmp
set SAN_LIST2=%TMP%\oneview_san_list2-%RANDOM%-%TIME:~6,5%.tmp

echo ================================================================
echo              Defining Ethernet Logical Networks
echo ================================================================
FOR %%A IN (A B) DO FOR %%V IN (10 20 30 40 50 60) DO python define-ethernet-network.py -a %HOST% -u %USER% -p %PASS% -n VLAN-%%V-%%A -v %%V

echo ================================================================
echo                    Defining Network Sets
echo ================================================================
python define-network-set.py -a %HOST% -u %USER% -p %PASS% -n "Production-A" -l VLAN-20-A VLAN-30-A VLAN-40-A VLAN-50-A
python define-network-set.py -a %HOST% -u %USER% -p %PASS% -n "Production-B" -l VLAN-20-B VLAN-30-B VLAN-40-A VLAN-50-B

echo.
echo ================================================================
echo           Defining Fibre Channel  Logical Networks
echo ================================================================
python define-fibrechannel-network.py -a %HOST% -u %USER% -p %PASS% -n "3PAR SAN A" -d
python define-fibrechannel-network.py -a %HOST% -u %USER% -p %PASS% -n "3PAR SAN B" -d

echo.
echo ================================================================
echo              Defining Logical Interconnect Groups
echo ================================================================
python define-logical-interconnect-group.py -a %HOST% -u %USER% -p %PASS% -n "VC FlexFabric Production" -i 1:Flex2040f8 2:Flex2040f8

echo.
echo ================================================================
echo     Defining Uplink Set Groups in Logical Interconnect Group
echo ================================================================
python define-uplink-set.py -a %HOST% -u %USER% -p %PASS% -n "3PAR SAN A" -i "VC FlexFabric Production" -t FibreChannel -l "3PAR SAN A" -o 1:3 1:4
python define-uplink-set.py -a %HOST% -u %USER% -p %PASS% -n "3PAR SAN B" -i "VC FlexFabric Production" -t FibreChannel -l "3PAR SAN B" -o 2:3 2:4
python define-uplink-set.py -a %HOST% -u %USER% -p %PASS% -n "Uplink Set 1-A" -i "VC FlexFabric Production" -t Ethernet -l VLAN-10-A VLAN-20-A VLAN-30-A VLAN-40-A VLAN-50-A VLAN-60-A -o 1:7 1:8
python define-uplink-set.py -a %HOST% -u %USER% -p %PASS% -n "Uplink Set 1-B" -i "VC FlexFabric Production" -t Ethernet -l VLAN-10-B VLAN-20-B VLAN-30-B VLAN-40-B VLAN-50-B VLAN-60-B -o 2:7 2:8


echo ================================================================
echo                   Defining Enclosure Groups
echo ================================================================
python define-enclosure-group.py -a %HOST% -u %USER% -p %PASS% -n "Prod VC FlexFabric Group 1" -l "VC FlexFabric Production"

echo.
echo ================================================================
echo                        Add Enclosures
echo ================================================================
python add-enclosure.py -a %HOST% -u %USER% -p %PASS% -eu %ENC_USR% -ep %ENC_PASS% -oa %ENC_ADDR% -eg "Prod VC FlexFabric Group 1"

echo.
echo ================================================================
echo                       Add Storage System
echo ================================================================
python add-storage-system.py -a %HOST% -u %USER% -p %PASS% -sh %STO_ADDR% -su %STO_USR% -sp %STO_PASS% -sd %STO_DOM%

echo.
echo ================================================================
echo                      Add Standalone Server
echo ================================================================
python add-server.py -a %HOST% -u %USER% -p %PASS% -sh %SRV_ADDR% -su %SRV_USR% -sp %SRV_PASS%

echo.
echo ================================================================
echo                     Add Storage Pools
echo ================================================================
python add-storage-pool.py -a %HOST% -u %USER% -p %PASS% -f -sp %STO_CPG%

echo.
echo ================================================================
echo                    Add Volume Templates
echo ================================================================
python add-volume-template.py -a %HOST% -u %USER% -p %PASS% -n "ESX Boot" -f -sp %STO_CPG% -cap 50

echo.
echo ================================================================
echo                          Add  Volumes
echo ================================================================
python add-volume.py -a %HOST% -u %USER% -p %PASS% -n boot1 -sp %STO_CPG% -cap 10
python add-volume.py -a %HOST% -u %USER% -p %PASS% -n boot2 -sp %STO_CPG% -cap 10
python add-volume.py -a %HOST% -u %USER% -p %PASS% -n boot3 -sp %STO_CPG% -cap 10
python add-volume.py -a %HOST% -u %USER% -p %PASS% -n datastore1 -sp %STO_CPG% -cap 500 -sh

echo.
echo ================================================================
echo                     Defining Connection List
echo ================================================================
rem Define a BFS connection list using single networks for Mgmt and network sets
rem for production
python define-connection-list.py -a %HOST% -u %USER% -p %PASS% -n "Mgmt-A" -net "VLAN-10-A" -func Ethernet -gbps 1 -cl %CONN_LIST_BFS% -i 1
python define-connection-list.py -a %HOST% -u %USER% -p %PASS% -n "Mgmt-B" -net "VLAN-10-B" -func Ethernet -gbps 1 -cl %CONN_LIST_BFS% -i 2 -app
python define-connection-list.py -a %HOST% -u %USER% -p %PASS% -n "Prod-A" -net "Production-A" -func Ethernet -gbps 2.5 -cl %CONN_LIST_BFS% -i 3 -ns -app
python define-connection-list.py -a %HOST% -u %USER% -p %PASS% -n "Prod-B" -net "Production-B" -func Ethernet -gbps 2.5 -cl %CONN_LIST_BFS% -i 4 -ns -app
python define-connection-list.py -a %HOST% -u %USER% -p %PASS% -n "FC-A" -net "3PAR SAN A" -func FibreChannel -bp "Primary" -cl %CONN_LIST_BFS% -i 5 -app
python define-connection-list.py -a %HOST% -u %USER% -p %PASS% -n "FC-B" -net "3PAR SAN B" -func FibreChannel -bp "Secondary" -cl %CONN_LIST_BFS% -i 6 -app
rem Define a local boot connection list with no FC connections
python define-connection-list.py -a %HOST% -u %USER% -p %PASS% -n "Mgmt-A" -net "VLAN-10-A" -func Ethernet -gbps 1 -cl %CONN_LIST% -i 1
python define-connection-list.py -a %HOST% -u %USER% -p %PASS% -n "Mgmt-B" -net "VLAN-10-B" -func Ethernet -gbps 1 -cl %CONN_LIST% -i 2 -app
python define-connection-list.py -a %HOST% -u %USER% -p %PASS% -n "Prod-A" -net "Production-A" -func Ethernet -gbps 2.5 -cl %CONN_LIST% -i 3 -ns -app
python define-connection-list.py -a %HOST% -u %USER% -p %PASS% -n "Prod-B" -net "Production-B" -func Ethernet -gbps 2.5 -cl %CONN_LIST% -i 4 -ns -app

echo.
echo ================================================================
echo                     Defining Connection Lists (templates)
echo ================================================================
rem Define a connection list with no FC connections (for profile templates)
python define-connection-list.py -a %HOST% -u %USER% -p %PASS% -n "Mgmt-A" -net "VLAN-10-A" -func Ethernet -gbps 1 -cl %CONN_LIST_TEMPLATE% -i 1 -spt
python define-connection-list.py -a %HOST% -u %USER% -p %PASS% -n "Mgmt-B" -net "VLAN-10-B" -func Ethernet -gbps 1 -cl %CONN_LIST_TEMPLATE% -i 2 -spt -app

echo.
echo ================================================================
echo                     Defining SAN Storage List
echo ================================================================
rem Create a SAN connection list using the private volume "boot1" and the
rem shared volume "datastore"
python define-san-storage-list.py -a %HOST% -u %USER% -p %PASS% -o VMware -n boot1 -sl %SAN_LIST1% -cl %CONN_LIST_BFS%
python define-san-storage-list.py -a %HOST% -u %USER% -p %PASS% -o VMware -n datastore1 -sl %SAN_LIST1% -cl %CONN_LIST_BFS% -app
rem Create a SAN connection list using the private volume "boot2" and the
rem shared volume "datastore"
python define-san-storage-list.py -a %HOST% -u %USER% -p %PASS% -o VMware -n boot2 -sl %SAN_LIST2% -cl %CONN_LIST_BFS%
python define-san-storage-list.py -a %HOST% -u %USER% -p %PASS% -o VMware -n datastore1 -sl %SAN_LIST2% -cl %CONN_LIST_BFS% -app

echo.
echo ================================================================
echo                       Defining profiles
echo ================================================================
echo "Define profiles with network and SAN storage connections"
python define-profile.py -a %HOST% -u %USER% -p %PASS% -n "Profile-Enc1Bay1" -s "Encl1, bay 1" -cl %CONN_LIST_BFS% -sl %SAN_LIST1%
python define-profile.py -a %HOST% -u %USER% -p %PASS% -n "Profile-Enc1Bay2" -s "Encl1, bay 2" -cl %CONN_LIST_BFS% -sl %SAN_LIST2%
echo "Define profile with network and local storage"
python define-profile.py -a %HOST% -u %USER% -p %PASS% -n "Profile-Enc1Bay4" -s "Encl1, bay 4" -cl %CONN_LIST% -rl RAID1 -pn 2 -is
echo "Define profile with firmware base line and managed boot order using Gen 7 & 8 ordering"
python define-profile.py -a %HOST% -u %USER% -p %PASS% -n "Profile-1" -s %SRV_ADDR% -fw %FW_BASE% -bo %BOOT_G78%
echo "Define n unassigned server profile"
python define-profile.py -a %HOST% -u %USER% -p %PASS% -n "Unassigned-1" -s UNASSIGNED -sh "DL360p Gen8 1" -fw %FW_BASE% -bo %BOOT_G78%

echo.
echo ================================================================
echo                       Copy profile
echo ================================================================
python define-profile.py -a %HOST% -u %USER% -p %PASS% -n "Profile-Enc1Bay4" -s "Encl1, bay 5" -d "Profile-Enc1Bay5"
python define-profile.py -a %HOST% -u %USER% -p %PASS% -n "Profile-Enc1Bay4" -s "Encl1, bay 6" -d "Profile-Enc1Bay6"

echo.
echo ================================================================
echo                       Defining profile templates
echo ================================================================
echo "Define profile templates with no network connections"
python define-profile-template.py -a %HOST% -u %USER% -p %PASS% -n "BL460c Gen9 1" -d "A server profile template" -spd "Server profile description" -sht "BL460c Gen9 1" -eg "Prod VC FlexFabric Group 1" -af "BayAndServer" -hn false
echo "Define profile templates with network connections"
python define-profile-template.py -a %HOST% -u %USER% -p %PASS% -n "BL460c Gen8 1" -d "A server profile template" -spd "Server profile description" -sht "BL460c Gen8 1" -eg "Prod VC FlexFabric Group 1" -af "Bay" -hn false -cl %CONN_LIST_TEMPLATE%
python define-profile-template.py -a %HOST% -u %USER% -p %PASS% -n "BL660c Gen8 1" -sht "BL660c Gen8 1" -eg "Prod VC FlexFabric Group 1" -af "Bay" -cl %CONN_LIST_TEMPLATE%
