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
rem Standalone server iLO hostname or IP Address
set SRV_ADDR=172.18.6.15
rem Enclosure OA username
set SRV_USR=Administrator
rem Enclosure OA password
set SRV_PASS=PASSWORD

set CONN_LIST=%TMP%\oneview_conn_list-%RANDOM%-%TIME:~6,5%.tmp

echo ================================================================
echo "            Defining Ethernet Logical Networks                "
echo ================================================================
FOR %%A IN (A B) DO FOR %%V IN (10 20 30 40 50 60) DO python define-ethernet-network.py -a %HOST% -u %USER% -p %PASS% -n VLAN-%%V-%%A -v %%V

echo
echo ================================================================
echo "         Defining Fibre Channel  Logical Networks             "
echo ================================================================
python define-fibrechannel-network.py -a %HOST% -u %USER% -p %PASS% -n "3PAR SAN A" -e
python define-fibrechannel-network.py -a %HOST% -u %USER% -p %PASS% -n "3PAR SAN B" -e

echo
echo ================================================================
echo "            Defining Logical Interconnect Groups              "
echo ================================================================
python define-logical-interconnect-group.py -a %HOST% -u %USER% -p %PASS% -n "VC FlexFabric Production" -i 1:Flex2040f8 2:Flex2040f8

echo
echo ================================================================
echo "   Defining Uplink Set Groups in Logical Interconnect Group   "
echo ================================================================
python define-uplink-set.py -a %HOST% -u %USER% -p %PASS% -n "3PAR SAN A" -i "VC FlexFabric Production" -t FibreChannel -l "3PAR   SAN A"  -o 1:3 1:4
python define-uplink-set.py -a %HOST% -u %USER% -p %PASS% -n "3PAR SAN B" -i "VC FlexFabric Production" -t FibreChannel -l "3PAR   SAN B"  -o 2:3 2:4
python define-uplink-set.py -a %HOST% -u %USER% -p %PASS% -n "Uplink Set 1-A" -i "VC FlexFabric Production" -t Ethernet  -l VLAN-  10-A VLAN-20-A VLAN-30-A VLAN-40-A VLAN-50-A VLAN-60-A -o 1:7 1:8
python define-uplink-set.py -a %HOST% -u %USER% -p %PASS% -n "Uplink Set 1-B" -i "VC FlexFabric Production" -t Ethernet  -l VLAN-  10-B VLAN-20-B VLAN-30-B VLAN-40-B VLAN-50-B VLAN-60-B -o 2:7 2:8

echo
echo ================================================================
echo "                 Defining Enclosure Groups                    "
echo ================================================================
python define-enclosure-group.py -a %HOST% -u %USER% -p %PASS% -n "Prod VC FlexFabric Group 1" -l "VC FlexFabric Production"

echo
echo ================================================================
echo "                      Add Enclosures                          "
echo ================================================================
python add-enclosure.py -a %HOST% -u %USER% -p %PASS% -eu %ENC_USR% -ep %ENC_PASS% -oa %ENC_ADDR% -eg "Prod VC FlexFabric Group 1"

echo
echo ================================================================
echo "                     Add Storage System                       "
echo ================================================================
python add-storage-system.py -a %HOST% -u %USER% -p %PASS% -s %STO_ADDR% -su %STO_USR% -sp %STO_PASS%

echo
echo ================================================================
echo "                    Add Standalone Server                     "
echo ================================================================
python add-server.py -a %HOST% -u %USER% -p %PASS% -sh %SRV_ADDR% -su %SRV_USR% -sp %SRV_PASS%

echo
echo ================================================================
echo "                   Add Storage Pools                          "
echo ================================================================
python add-storage-pool.py -a %HOST% -u %USER% -p %PASS% -f -sp SND_CPG1

echo
echo ================================================================
echo "                  Add Volume Templates                        "
echo ================================================================
python add-volume-template.py -a %HOST% -u %USER% -p %PASS% -n "ESX Boot" -f -sp SND_CPG1 -cap 50

echo
echo ================================================================
echo "                        Add  Volumes                          "
echo ================================================================
python add-volume.py -a %HOST% -u %USER% -p %PASS% -n vol1 -sp SND_CPG1 -cap 50

echo
echo ================================================================
echo "                   Defining Connection List                   "
echo ================================================================
python define-connection-list.py -a %HOST% -u %USER% -p %PASS% -n "VLAN-10-A" -func Ethernet -gbps 1.5 -cl %CONN_LIST%
python define-connection-list.py -a %HOST% -u %USER% -p %PASS% -n "VLAN-10-B" -func Ethernet -gbps 1.5 -cl %CONN_LIST% -app
python define-connection-list.py -a %HOST% -u %USER% -p %PASS% -n "VLAN-20-A" -func Ethernet -gbps 1.5 -cl %CONN_LIST% -app
python define-connection-list.py -a %HOST% -u %USER% -p %PASS% -n "VLAN-20-B" -func Ethernet -gbps 1.5 -cl %CONN_LIST% -app
python define-connection-list.py -a %HOST% -u %USER% -p %PASS% -n "3PAR SAN A" -func FibreChannel -bp "Primary" -cl %CONN_LIST% -app
python define-connection-list.py -a %HOST% -u %USER% -p %PASS% -n "3PAR SAN B" -func FibreChannel -bp "Secondary" -cl %CONN_LIST% -app

echo
echo ================================================================
echo "                     Defining profiles                        "
echo ================================================================
python define-profile.py -a %HOST% -u %USER% -p %PASS% -n "Profile-Enc1Bay1" -s "Encl1, bay 1" -cl %CONN_LIST%
