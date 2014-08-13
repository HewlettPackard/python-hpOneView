# OneView Appliance hostname or IP address
HOST=oneview
# OneView Appliance username
USER=Administrator
# OneView Appliance password
PASS=PASSWORD
# Enclosure OA hostname or IP address
ENC_ADDR=172.18.1.11
# Enclosure OA username
ENC_USR=Administrator
# Enclosure OA password
ENC_PASS=PASSWORD

echo  -- Defining Logical Networks
./define-networks.py -a $HOST -u $USER -p $PASS
echo  -- Defining Logical Interconnect Groups
./define-lig.py -a $HOST -u $USER -p $PASS
echo  -- Defining Enclosure Groups
./define-eg.py -a $HOST -u $USER -p $PASS
echo  -- Import Enclosures
./import-enclosure.py -a $HOST -u $USER -p $PASS -eu $ENC_USR -ep $ENC_PASS -e $ENC_ADDR
echo  -- Defining Storage Pools
./add-storage-pools.py -a $HOST -u $USER -p $PASS -n SND_CPG1
echo  -- Defining Volume Templates
echo  -- Defining volumes
./add-volume.py -a $HOST -u $USER -p $PASS -n vol1
echo  -- Defining profiles
./define-profile.py -a $HOST -u $USER -p $PASS
