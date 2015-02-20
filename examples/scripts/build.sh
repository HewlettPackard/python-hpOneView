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
ENC_PASS=${ENC_PASS:=OV_PASSWORD}
# 3PAR hostname or IP Address
STO_ADDR=${STO_ADDR:=172.18.11.11}
# Enclosure OA username
STO_USR=${STO_USR:=Administrator}
# Enclosure OA password
STO_PASS=${STO_PASS:=OV_PASSWORD}

echo  -- Defining Ethernet Logical Networks
for AA in A B
do
  for vlan in 10 20 30 40 50 60
  do
    ./define-ethernet-network.py -a $OV_HOST -u $OV_USER -p $OV_PASS -n VLAN-$vlan"-"$AA -v $vlan
  done
done

echo  -- Defining Fibre Channel  Logical Networks
./define-fibrechannel-network.py -a $OV_HOST -u $OV_USER -p $OV_PASS -n "3PAR SAN A" -e
./define-fibrechannel-network.py -a $OV_HOST -u $OV_USER -p $OV_PASS -n "3PAR SAN B" -e
echo  -- Defining Logical Interconnect Groups
./define-logical-interconnect-group.py -a $OV_HOST -u $OV_USER -p $OV_PASS -n "VC FlexFabric Production" -i 1:Flex2040f8 2:Flex2040f8
echo  -- Defining Uplink Set Groups in Logical Interconnect Group
./define-uplink-set.py -a $OV_HOST -u $OV_USER -p $OV_PASS -n "3PAR SAN A" -i "VC FlexFabric Production" -t FibreChannel -l "3PAR SAN A"  -o 1:3 1:4
./define-uplink-set.py -a $OV_HOST -u $OV_USER -p $OV_PASS -n "3PAR SAN B" -i "VC FlexFabric Production" -t FibreChannel -l "3PAR SAN B"  -o 2:3 2:4
./define-uplink-set.py -a $OV_HOST -u $OV_USER -p $OV_PASS -n "Uplink Set 1-A" -i "VC FlexFabric Production" -t Ethernet  -l VLAN-10-A VLAN-20-A VLAN-30-A VLAN-40-A VLAN-50-A VLAN-60-A -o 1:7 1:8
./define-uplink-set.py -a $OV_HOST -u $OV_USER -p $OV_PASS -n "Uplink Set 1-B" -i "VC FlexFabric Production" -t Ethernet  -l VLAN-10-B VLAN-20-B VLAN-30-B VLAN-40-B VLAN-50-B VLAN-60-B -o 2:7 2:8
echo  -- Defining Enclosure Groups
./define-enclosure-group.py -a $OV_HOST -u $OV_USER -p $OV_PASS -n "Prod VC FlexFabric Group 1" -l "VC FlexFabric Production"
echo  -- Import Enclosures
./import-enclosure.py -a $OV_HOST -u $OV_USER -p $OV_PASS -eu $ENC_USR -ep $ENC_PASS -e $ENC_ADDR -n "Prod VC FlexFabric Group 1"
echo  -- Add Storage System
./add-storage-system.py -a $OV_HOST -u $OV_USER -p $OV_PASS -s $STO_ADDR -su $STO_USR -sp $STO_PASS
echo  -- Defining Storage Pools
./add-storage-pool.py -a $OV_HOST -u $OV_USER -p $OV_PAS -s ThreePAR7200-4446S -n SND_CPG1
echo  -- Defining Volume Templates
./add-volume-template.py -a $OV_HOST -u $OV_USER -p $OV_PASS -n "ESX Boot"
echo  -- Defining volumes
./add-volume.py -a $OV_HOST -u $OV_USER -p $OV_PASS -n vol1
echo  -- Defining profiles
./define-profile.py -a $OV_HOST -u $OV_USER -p $OV_PASS
