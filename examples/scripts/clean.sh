# OneView Appliance hostname or IP address
OV_HOST=${OV_HOST:=oneview}
# OneView Appliance username
OV_USER=${OV_USER:=Administrator}
# OneView Appliance password
OV_PASS=${OV_PASS:=OV_PASSWORD}

echo ================================================================
echo "                    Removing Profiles                         "
echo ================================================================
./del-profile.py -a $OV_HOST -u $OV_USER -p $OV_PASS -d -f

echo
echo ================================================================
echo "                    Removing Volumes                          "
echo ================================================================
./del-volume.py -a $OV_HOST -u $OV_USER -p $OV_PASS -d

echo
echo ================================================================
echo "                 Removing Volume Templates                    "
echo ================================================================
./del-volume-template.py -a $OV_HOST -u $OV_USER -p $OV_PASS -d

echo
echo ================================================================
echo "                 Removing Storage Pools                       "
echo ================================================================
./del-storage-pool.py -a $OV_HOST -u $OV_USER -p $OV_PASS -d

echo
echo ================================================================
echo "                 Removing Storage Systems                     "
echo ================================================================
./del-storage-system.py -a $OV_HOST -u $OV_USER -p $OV_PASS -d

echo
echo ================================================================
echo "                    Removing Enclosure                        "
echo ================================================================
./del-enclosure.py -a $OV_HOST -u $OV_USER -p $OV_PASS -d

echo
echo ================================================================
echo "                 Removing Standalone Servers                  "
echo ================================================================
./del-server.py -a $OV_HOST -u $OV_USER -p $OV_PASS -d

echo
echo ================================================================
echo "                 Removing Enclosure Groups                    "
echo ================================================================
./del-enclosure-group.py -a $OV_HOST -u $OV_USER -p $OV_PASS -d

echo
echo ================================================================
echo "             Removing Logical Interconnect Groups             "
echo ================================================================
./del-logical-interconnect-groups.py -a $OV_HOST -u $OV_USER -p $OV_PASS -d

echo
echo ================================================================
echo "                    Removing Network Sets                     "
echo ================================================================
./del-network-set.py -a $OV_HOST -u $OV_USER -p $OV_PASS -d

echo
echo ================================================================
echo "                    Removing Networks                         "
echo ================================================================
./del-network.py -a $OV_HOST -u $OV_USER -p $OV_PASS -d

echo
echo ================================================================
echo "                Removing Power Devices                        "
echo ================================================================
./del-powerdevices.py -a $OV_HOST -u $OV_USER -p $OV_PASS -d
