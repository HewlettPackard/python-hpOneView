#!/bin/bash

# OneView Appliance hostname or IP address
OV_HOST=${OV_HOST:=oneview}
# OneView Appliance username
OV_USER=${OV_USER:=Administrator}
# OneView Appliance password
OV_PASS=${OV_PASS:=OV_PASSWORD}
# Enclosure OA hostname or IP address
ENC_ADDR=${ENC_ADDR:=172.18.1.11}
# Enclosure OA username
ENC_USR=${ENC_USR:=Administrator}
# Enclosure OA password
ENC_PASS=${ENC_PASS:=PASSWORD}
# 3PAR hostname or IP Address
STO_ADDR=${STO_ADDR:=172.18.11.11}
# 3PAR username
STO_USR=${STO_USR:=Administrator}
# 3PAR password
STO_PASS=${STO_PASS:=PASSWORD}
# 3PAR Storage Domain
STO_DOM=${STO_DOM:=NewDomain}
# 3PAR CPG
STO_CPG=${STO_CPG:=SND_CPG1}
# Standalone Server iLO hostname or IP address
SRV_ADDR=${SRV_ADDR:=172.18.6.15}
# Standalone Server iLO username
SRV_USR=${SRV_USR:=Administrator}
# Standalone Server iLO password
SRV_PASS=${SRV_PASS:=PASSWORD}
# Firmware Baseline
FW_BASE=${FW_BASE:=HP_Service_Pack_for_ProLiant_2015.10.0-SPP2015100.2015_0921.6.iso}
# Server boot order (dependent on server hardware type)
BOOT_G78=${BOOT_G78:="HardDisk PXE USB CD Floppy"}
BOOT_G9_LEGACY=${BOOT_G9_LEGACY:="HardDisk PXE USB CD"}
BOOT_G9_UEFI=${BOOT_G9_UEFI:="HardDisk"}


# Securely create a temporary directory and temporary connection listfile
OV_TMP=${TMPDIR-/tmp}
OV_TMP=$OV_TMP/hpOneView_temporary_files.$RANDOM.$RANDOM.$RANDOM.$$
(umask 077 && mkdir $OV_TMP) || {
	echo "Could not create temporary directory! Exiting." 1>&2
	exit 1
}

CONN_LIST=$OV_TMP/CONN-$RANDOM.$RANDOM.$$
CONN_LIST_BFS=$OV_TMP/CONN-BFS-$RANDOM.$RANDOM.$$
SAN_LIST1=$OV_TMP/SAN-1-$RANDOM.$RANDOM.$$
SAN_LIST2=$OV_TMP/SAN-2-$RANDOM.$RANDOM.$$

echo ================================================================
echo "            Defining Ethernet Logical Networks                "
echo ================================================================
for AA in A B
do
  for vlan in 10 20 30 40 50 60
  do
    ./define-ethernet-network.py -a $OV_HOST -u $OV_USER -p $OV_PASS -n VLAN-$vlan"-"$AA -v $vlan
  done
done

echo ================================================================
echo "                 Defining Network Sets                        "
echo ================================================================
./define-network-set.py -a $OV_HOST -u $OV_USER -p $OV_PASS \
  -n "Production-A" -l VLAN-20-A VLAN-30-A VLAN-40-A VLAN-50-A
./define-network-set.py -a $OV_HOST -u $OV_USER -p $OV_PASS \
  -n "Production-B" -l VLAN-20-B VLAN-30-B VLAN-40-B VLAN-50-B


echo
echo ================================================================
echo "         Defining Fibre Channel  Logical Networks             "
echo ================================================================
./define-fibrechannel-network.py -a $OV_HOST -u $OV_USER -p $OV_PASS -n "3PAR SAN A" -d
./define-fibrechannel-network.py -a $OV_HOST -u $OV_USER -p $OV_PASS -n "3PAR SAN B" -d

echo
echo ================================================================
echo "            Defining Logical Interconnect Groups              "
echo ================================================================
./define-logical-interconnect-group.py -a $OV_HOST -u $OV_USER -p $OV_PASS -n "VC FlexFabric Production" -i 1:Flex2040f8 2:Flex2040f8

echo
echo ================================================================
echo "   Defining Uplink Set Groups in Logical Interconnect Group   "
echo ================================================================
./define-uplink-set.py -a $OV_HOST -u $OV_USER -p $OV_PASS -n "3PAR SAN A" -i "VC FlexFabric Production" -t FibreChannel -l "3PAR SAN A"  -o 1:3 1:4
./define-uplink-set.py -a $OV_HOST -u $OV_USER -p $OV_PASS -n "3PAR SAN B" -i "VC FlexFabric Production" -t FibreChannel -l "3PAR SAN B"  -o 2:3 2:4
./define-uplink-set.py -a $OV_HOST -u $OV_USER -p $OV_PASS -n "Uplink Set 1-A" -i "VC FlexFabric Production" -t Ethernet  -l VLAN-10-A VLAN-20-A VLAN-30-A VLAN-40-A VLAN-50-A VLAN-60-A -o 1:7 1:8
./define-uplink-set.py -a $OV_HOST -u $OV_USER -p $OV_PASS -n "Uplink Set 1-B" -i "VC FlexFabric Production" -t Ethernet  -l VLAN-10-B VLAN-20-B VLAN-30-B VLAN-40-B VLAN-50-B VLAN-60-B -o 2:7 2:8

echo
echo ================================================================
echo "                 Defining Enclosure Groups                    "
echo ================================================================
./define-enclosure-group.py -a $OV_HOST -u $OV_USER -p $OV_PASS -n "Prod VC FlexFabric Group 1" -l "VC FlexFabric Production"

echo
echo ================================================================
echo "                      Add Enclosures                          "
echo ================================================================
./add-enclosure.py -a $OV_HOST -u $OV_USER -p $OV_PASS -eu $ENC_USR -ep $ENC_PASS -oa $ENC_ADDR -eg "Prod VC FlexFabric Group 1"

echo
echo ================================================================
echo "                     Add Storage System                       "
echo ================================================================
./add-storage-system.py -a $OV_HOST -u $OV_USER -p $OV_PASS -sh $STO_ADDR -su $STO_USR -sp $STO_PASS -sd $STO_DOM

echo
echo ================================================================
echo "                    Add Standalone Server                     "
echo ================================================================
./add-server.py -a $OV_HOST -u $OV_USER -p $OV_PASS -sh $SRV_ADDR -su $SRV_USR -sp $SRV_PASS

echo
echo ================================================================
echo "                     Add Storage Pools                        "
echo ================================================================
./add-storage-pool.py -a $OV_HOST -u $OV_USER -p $OV_PASS -f -sp $STO_CPG

echo
echo ================================================================
echo "                     Add Volume Templates                     "
echo ================================================================
./add-volume-template.py -a $OV_HOST -u $OV_USER -p $OV_PASS -n "ESX Boot" -f -sp $STO_CPG -cap 50

echo
echo ================================================================
echo "                        Add  Volumes                          "
echo ================================================================
./add-volume.py -a $OV_HOST -u $OV_USER -p $OV_PASS -n boot1 -sp $STO_CPG -cap 10
./add-volume.py -a $OV_HOST -u $OV_USER -p $OV_PASS -n boot2 -sp $STO_CPG -cap 10
./add-volume.py -a $OV_HOST -u $OV_USER -p $OV_PASS -n boot3 -sp $STO_CPG -cap 10
./add-volume.py -a $OV_HOST -u $OV_USER -p $OV_PASS -n datastore1 -sp $STO_CPG -cap 500 -sh

echo
echo ================================================================
echo "                   Defining Connection List                   "
echo ================================================================
# Define a BFS connection list using single networks for Mgmt and network
# sets for production
./define-connection-list.py -a $OV_HOST -u $OV_USER -p $OV_PASS -n "Mgmt-A" \
  -net "VLAN-10-A" -func Ethernet -gbps 1 -cl $CONN_LIST_BFS -i 1
./define-connection-list.py -a $OV_HOST -u $OV_USER -p $OV_PASS -n "Mgmt-B" \
  -net "VLAN-10-B" -func Ethernet -gbps 1 -cl $CONN_LIST_BFS -i 2 -app
./define-connection-list.py -a $OV_HOST -u $OV_USER -p $OV_PASS -n "Prod-A" \
  -net "Production-A" -func Ethernet -gbps 2.5 -cl $CONN_LIST_BFS -i 3 -ns -app
./define-connection-list.py -a $OV_HOST -u $OV_USER -p $OV_PASS -n "Prod-B" \
  -net "Production-B" -func Ethernet -gbps 2.5 -cl $CONN_LIST_BFS -i 4 -ns -app
./define-connection-list.py -a $OV_HOST -u $OV_USER -p $OV_PASS -n "FC-A" \
  -net "3PAR SAN A" -func FibreChannel -bp "Primary" -cl $CONN_LIST_BFS -i 5 -app
./define-connection-list.py -a $OV_HOST -u $OV_USER -p $OV_PASS -n "FC-B" \
  -net "3PAR SAN B" -func FibreChannel -bp "Secondary" -cl $CONN_LIST_BFS -i 6 -app
# Define a local boot connection list with no FC connections
./define-connection-list.py -a $OV_HOST -u $OV_USER -p $OV_PASS -n "Mgmt-A" \
  -net "VLAN-10-A" -func Ethernet -gbps 1 -cl $CONN_LIST -i 1
./define-connection-list.py -a $OV_HOST -u $OV_USER -p $OV_PASS -n "Mgmt-B" \
  -net "VLAN-10-B" -func Ethernet -gbps 1 -cl $CONN_LIST -i 2 -app
./define-connection-list.py -a $OV_HOST -u $OV_USER -p $OV_PASS -n "Prod-A" \
  -net "Production-A" -func Ethernet -gbps 2.5 -cl $CONN_LIST -i 3 -ns -app
./define-connection-list.py -a $OV_HOST -u $OV_USER -p $OV_PASS -n "Prod-B" \
  -net "Production-B" -func Ethernet -gbps 2.5 -cl $CONN_LIST -i 4 -ns -app

echo
echo ================================================================
echo "                   Defining SAN Storage List                  "
echo ================================================================
echo 'Create a SAN connection list using the private volume "boot1" and the'
echo 'shared volume "datastore"'
./define-san-storage-list.py -a $OV_HOST -u $OV_USER -p $OV_PASS -o VMware \
    -n boot1 -sl $SAN_LIST1 -cl $CONN_LIST_BFS
./define-san-storage-list.py -a $OV_HOST -u $OV_USER -p $OV_PASS -o VMware \
    -n datastore1 -sl $SAN_LIST1 -cl $CONN_LIST_BFS -app
echo 'Create a SAN connection list using the private volume "boot2" and the'
echo 'shared volume "datastore"'
./define-san-storage-list.py -a $OV_HOST -u $OV_USER -p $OV_PASS -o VMware \
    -n boot2 -sl $SAN_LIST2 -cl $CONN_LIST_BFS
./define-san-storage-list.py -a $OV_HOST -u $OV_USER -p $OV_PASS -o VMware \
    -n datastore1 -sl $SAN_LIST2 -cl $CONN_LIST_BFS -app

echo
echo ================================================================
echo "                     Defining profiles                        "
echo ================================================================
echo "Define profiles with network and SAN storage connections"
./define-profile.py -a $OV_HOST -u $OV_USER -p $OV_PASS -n "Profile-Enc1Bay1" \
  -s "Encl1, bay 1" -cl $CONN_LIST_BFS -sl $SAN_LIST1
./define-profile.py -a $OV_HOST -u $OV_USER -p $OV_PASS -n "Profile-Enc1Bay2" \
  -s "Encl1, bay 2" -cl $CONN_LIST_BFS -sl $SAN_LIST2
echo "Define profile with network and local storage"
./define-profile.py -a $OV_HOST -u $OV_USER -p $OV_PASS -n "Profile-Enc1Bay4" \
  -s "Encl1, bay 4" -cl $CONN_LIST -rl RAID1 -pn 2 -is
echo "Define profile with firmware base line and managed boot order using Gen 7 & 8 ordering"
./define-profile.py -a $OV_HOST -u $OV_USER -p $OV_PASS -n "Profile-1" \
  -s $SRV_ADDR -fw $FW_BASE -bo $BOOT_G78
echo "Define an unassigned server profile"
./define-profile.py -a $OV_HOST -u $OV_USER -p $OV_PASS -n "Unassigned-1" \
  -s UNASSIGNED -sh 'DL360p Gen8 1' -fw $FW_BASE -bo $BOOT_G78

echo
echo ================================================================
echo "                     Copy profile                             "
echo ================================================================
./copy-profile.py -a $OV_HOST -u $OV_USER -p $OV_PASS -n "Profile-Enc1Bay4" \
  -s "Encl1, bay 5" -d "Profile-Enc1Bay5"
./copy-profile.py -a $OV_HOST -u $OV_USER -p $OV_PASS -n "Profile-Enc1Bay4" \
  -s "Encl1, bay 6" -d "Profile-Enc1Bay6"

# Clean up temporary files
if [ -d $OV_TMP ]; then
  rm -Rf $OV_TMP
fi
