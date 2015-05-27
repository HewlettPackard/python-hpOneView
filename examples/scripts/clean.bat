@echo off
chcp 65001

rem OneView Appliance hostname or IP address
set HOST=oneview
rem OneView Appliance username
set USER=Administrator
rem OneView Appliance password
set PASS=PASSWORD

echo ================================================================
echo                       Removing Profiles
echo ================================================================
python del-profile.py -a %HOST% -u %USER% -p %PASS% -d -f

echo.
echo ================================================================
echo                       Removing Volumes
echo ================================================================
python del-volume.py -a %HOST% -u %USER% -p %PASS% -d

echo.
echo ================================================================
echo                    Removing Volume Templates
echo ================================================================
python del-volume-template.py -a %HOST% -u %USER% -p %PASS% -d

echo.
echo ================================================================
echo                    Removing Storage Pools
echo ================================================================
python del-storage-pool.py -a %HOST% -u %USER% -p %PASS% -d

echo.
echo ================================================================
echo                    Removing Storage Systems
echo ================================================================
python del-storage-system.py -a %HOST% -u %USER% -p %PASS% -d

echo.
echo ================================================================
echo                       Removing Enclosure
echo ================================================================
python del-enclosure.py -a %HOST% -u %USER% -p %PASS% -d

echo.
echo ================================================================
echo                    Removing Standalone Servers
echo ================================================================
python del-server.py -a %HOST% -u %USER% -p %PASS% -d

echo.
echo ================================================================
echo                    Removing Enclosure Groups
echo ================================================================
python del-enclosure-group.py -a %HOST% -u %USER% -p %PASS% -d

echo.
echo ================================================================
echo                Removing Logical Interconnect Groups
echo ================================================================
python del-logical-interconnect-groups.py -a %HOST% -u %USER% -p %PASS% -d

echo.
echo ================================================================
echo                       Removing Network Sets
echo ================================================================
python del-network-set.py -a %HOST% -u %USER% -p %PASS% -d

echo.
echo ================================================================
echo                       Removing Networks
echo ================================================================
python del-network.py -a %HOST% -u %USER% -p %PASS% -d

echo.
echo ================================================================
echo                    Removing Power Devices
echo ================================================================
python del-powerdevices.py -a %HOST% -u %USER% -p %PASS% -d
