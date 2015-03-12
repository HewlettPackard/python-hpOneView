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

echo  -- Removing profiles
./del-profile.py -a $OV_HOST -u $OV_USER -p $OV_PASS -d -f
echo  -- Removing volumes
./del-volume.py -a $OV_HOST -u $OV_USER -p $OV_PASS -d
echo  -- Removing Volume Templates
./del-volume-template.py -a $OV_HOST -u $OV_USER -p $OV_PASS -d
echo  -- Removing Storage Pools
./del-storage-pool.py -a $OV_HOST -u $OV_USER -p $OV_PASS -d
echo  -- Removing Storage Systems
./del-storage-system.py -a $OV_HOST -u $OV_USER -p $OV_PASS -d
echo  -- Removing Enclosures
./del-enclosure.py -a $OV_HOST -u $OV_USER -p $OV_PASS -d
echo  -- Removing Enclosure Groups
./del-enclosure-group.py -a $OV_HOST -u $OV_USER -p $OV_PASS -d
echo  -- Removing Logical Interconnect Groups
./del-logical-interconnect-groups.py -a $OV_HOST -u $OV_USER -p $OV_PASS -d
echo  -- Removing Network Sets
./del-network-set.py -a $OV_HOST -u $OV_USER -p $OV_PASS -d
echo  -- Removing Logical Networks
./del-network.py -a $OV_HOST -u $OV_USER -p $OV_PASS -d
