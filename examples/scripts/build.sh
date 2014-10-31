# OneView Appliance hostname or IP address
HOST=${HOST:=oneview}
# OneView Appliance username
USER=${USER:=Administrator}
# OneView Appliance password
PASS=${PASS:=PASSWORD}
# Enclosure OA hostname or IP address
ENC_ADDR=${ENC_ADDR:=172.18.1.11}
# Enclosure OA username
ENC_USR=${ENC_USR:=Administrator}
# Enclosure OA password
ENC_PASS=${ENC_PASS:=PASSWORD}
# 3PAR hostname or IP Address
STO_ADDR=${STO_ADDR:=172.18.11.11}
# Enclosure OA username
STO_USR=${STO_USR:=Administrator}
# Enclosure OA password
STO_PASS=${STO_PASS:=PASSWORD}

echo  -- Defining Logical Networks
./define-networks.py -a $HOST -u $USER -p $PASS
echo  -- Defining Logical Interconnect Groups
./define-lig.py -a $HOST -u $USER -p $PASS
echo  -- Defining Enclosure Groups
./define-enclosure-group.py -a $HOST -u $USER -p $PASS -n "Prod VC FlexFabric Group 1" -l "VC FlexFabric Production"
echo  -- Import Enclosures
./import-enclosure.py -a $HOST -u $USER -p $PASS -eu $ENC_USR -ep $ENC_PASS -e $ENC_ADDR
echo  -- Add Storage System
./add-storage-system.py -a $HOST -u $USER -p $PASS -s $STO_ADDR -su $STO_USR -sp $STO_PASS
echo  -- Defining Storage Pools
./add-storage-pool.py -a $HOST -u $USER -p $PASS -n SND_CPG1
echo  -- Defining Volume Templates
./add-volume-template.py -a $HOST -u $USER -p $PASS -n "ESX Boot"
echo  -- Defining volumes
./add-volume.py -a $HOST -u $USER -p $PASS -n vol1
echo  -- Defining profiles
./define-profile.py -a $HOST -u $USER -p $PASS
