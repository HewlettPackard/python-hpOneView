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

echo  -- Removing profiles
./define-profile.py -a $HOST -u $USER -p $PASS -d
echo  -- Removing volumes
./add-volume.py -a $HOST -u $USER -p $PASS -d
echo  -- Removing Volume Templates
echo  -- Removing Storage Pools
./add-storage-pools.py -a $HOST -u $USER -p $PASS -d
echo  -- Removing Enclosures
./import-enclosure.py -a $HOST -u $USER -p $PASS -eu $ENC_USR -ep $ENC_PASS -d
echo  -- Removing Enclosure Groups
./define-eg.py -a $HOST -u $USER -p $PASS -d
echo  -- Removing Logical Interconnect Groups
./define-lig.py -a $HOST -u $USER -p $PASS -d
echo  -- Removing Logical Networks
./define-networks.py -a $HOST -u $USER -p $PASS -d
