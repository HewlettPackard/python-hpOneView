# 5.0.0
#### Notes
Extends support of the SDK to OneView Rest API version 800 (OneView v4.1).

#### Major changes
 1. Extended support of SDK to API800.
 2. Designed a base class to keep all the common operations available for the resources.
 3. Introduced mixin classes to include the optional features of the resources.
 4. Resource data will be available with the resource object. This enhancement helps to
  add helper methods and avoid passing uri/name to call the resource methods.

#### Breaking
  Enhancement made in this version breaks the previous version of the SDK.
  Resource object should be created to call a resource method.

  E.g.
     Get an existing FC network or create one and use the
       returned object to call the other methods.

       oneview_client = OneViewClient(config)
       fc_networks = oneview_client.fc_networks

       fc_network = fc_networks.get_by_name(name) / create
       fc_network.update(update_data)
       fc_network.delete()

  Refer example files of the updated resources for more details.

#### Features supported with current release
- Connection template
- Enclosure
- Enclosure group
- Ethernet network
- FC network
- FCOE network
- Interconnect type
- Internal link set
- Logical enclosure
- Logical interconnect
- Logical interconnect group
- Logical switch group
- Managed SAN
- OS deployment plan
- SAS interconnect
- SAS interconnect type
- SAS logical interconnect
- SAS logical interconnect group
- Server hardware
- Server hardware type
- Server profile
- Server profile template
- Switch type
- Uplink set

# 4.8.0
#### Notes
Added the capability to handle OneView Appliance SNMP Settings
Extends support of the SDK to OneView Rest API version 800 (OneView v4.1).

#### Features supported with current release:
- Appliance Device Read Community
- Appliance Device SNMP v1 Trap Destinations
- Appliance Device SNMP v3 Trap Destinations
- Appliance Device SNMP v3 Users

#### Bug fixes
- [#364] (https://github.com/HewlettPackard/python-hpOneView/issues/364) Bug in index_resources.get_all()

# 4.7.0
#### Notes
Extends support of the SDK to OneView Rest API version 600 (OneView v4.0).

#### Features supported with current release:
- Alert

#### New Resource:
- License

# 4.6.0
#### Notes
Extends support of the SDK to OneView Rest API version 600 (OneView v4.0).
Updated support for HPE Synergy Image Streamer REST API 500 and 600.

#### Features supported with current release:
- Deployment plan
- Golden image
- Interconnect
- Network set
- OS deployment plan
- OS volume
- Plan script
- Storage pool
- Storage system
- Storage volume

# 4.5.0
#### Notes
Added the capability to set a connection timeout when connecting to the HPE OneView Appliance

Extends support of the SDK to OneView Rest API version 600 (OneView v4.0).

#### Features supported with current release:
- Connection template
- Enclosure
- Enclosure group
- Ethernet network
- FC network
- FCoE network
- Interconnect type
- Internal link set
- Logical enclosure
- Logical interconnect
- Logical interconnect group
- Logical switch
- Logical switch group
- Managed SAN
- OS Build Plan
- SAS interconnect
- SAS interconnect type
- SAS logical interconnect
- SAS logical interconnect group
- Server hardware
- Server profile
- Server profile template
- Storage volume template
- Switch
- Switch type
- Task
- Uplink set

# 4.4.0
#### Notes
Enabled usage of a CA Certificate file for establishing a SSL connection to the HPE OneView Appliance.

#### New Resources:
- Version

#### Bug fixes & Enhancements
- [#332](https://github.com/HewlettPackard/python-hpOneView/issues/332) example scmb.py is broken with v4.x libray
- [#339](https://github.com/HewlettPackard/python-hpOneView/issues/339) Validate secure connection to OneView using a certificate file

# 4.3.0
#### Notes
Added endpoints-support.md to track the supported and tested endpoints for the different HPE OneView REST APIs

#### New Resources:
- Login details

#### Bug fixes & Enhancements
- [#273](https://github.com/HewlettPackard/python-hpOneView/issues/273) OneViewClient doesn't allow using a token (sessionId)
- [#317](https://github.com/HewlettPackard/python-hpOneView/issues/317) Resource "Roles" should be under "Security" instead of "Uncategorized"
- [#320](https://github.com/HewlettPackard/python-hpOneView/issues/320) Issue with pickling HPOneViewException
- [#324](https://github.com/HewlettPackard/python-hpOneView/issues/324) Is it possible to login with session token?
- [#330](https://github.com/HewlettPackard/python-hpOneView/issues/330) Remove unused/legacy code from connection.py

# v4.2.0
#### New Resources:
- Index resource

#### Bug fixes & Enhancements
- [#312](https://github.com/HewlettPackard/python-hpOneView/issues/312) Could not find mappings for OneView's Index Resources

# v4.1.0
#### New Resources:
- Appliance node information

#### Bug fixes & Enhancements
- [#309](https://github.com/HewlettPackard/python-hpOneView/issues/309) HPOneViewException not raised when connection with paused VM fails

# v4.0.0
#### Notes
Major release which extends support of the SDK to OneView Rest API version 500 (OneView v3.10).

#### Major changes
 1. Extended support of SDK to API500.
 2. Officially adopted [Semantic Versioning](http://semver.org/) for the SDK.
 3. Updated example files for most resources for improved readability and usability.
 4. General cleanup and removal of deprecated methods and classes.

#### Breaking changes
Legacy code under hpOneView which was marked as deprecated has been removed. This will cause scripts which still use legacy code to stop working. HPE recommends switching to the new modules, which are actively maintained.

#### Bug fixes & Enhancements
- [#300](https://github.com/HewlettPackard/python-hpOneView/issues/300) Unable to unassign Server Hardware from a Server Profile

#### Features supported with current release:
- Connection template
- Datacenter
- Drive enclosure
- Enclosure
- Enclosure group
- Ethernet network
- Fabric
- FC network
- FCOE network
- Firmware bundle
- Firmware driver
- Interconnect
- Interconnect link topology
- Interconnect type
- Internal link set
- Logical downlink
- Logical enclosure
- Logical interconnect
- Logical interconnect group
- Logical switch
- Logical switch group
- Managed SAN
- Network set
- OS deployment plan
- Rack
- SAN manager
- SAS interconnect
- SAS interconnect type
- SAS logical interconnect
- SAS logical interconnect group
- SAS logical JBOD
- SAS logical JBOD attachment
- Scope
- Server hardware
- Server hardware type
- Server profile
- Server profile template
- Storage pool
- Storage system
- Storage volume
- Storage volume attachment
- Storage volume template
- Switch
- Switch type
- Uplink set
- User

# v3.3.0
### Version highlights:
1. Added CHANGELOG to track versions, issues and improvements.

### New features:
- User

# v3.2.2
#### Notes
Minor fixes. Changed raise exception in case of unsupported Python version for warning to allow users that have TTL backported to run the SDK.

# v3.2.1
#### Notes
Improvements and refactoring.

# v3.1.1
#### Notes
Bugfixes and corrections.


# v3.1.0
#### Major changes
 1. Updated support for OneView API V300 and HPE Synergy.
 2. Updated support for HPE Synergy Image Streamer REST API.

# v3.0.0
#### Major changes
 1. Added support for OneView API300 and HPE Synergy to resources previously supported.
 2. Added support for new HPE Synergy exclusive resources.
 3. Partial support for HPE Synergy Image Streamer REST API.

# v2.0.0
#### Major changes
 1. HPE Rebranding
 2. Core Architecture Refactoring
   - PEP8 compliant
   - Support for both Python 2.7 and 3.x
   - Developer friendly interface
   - Standardization for building new endpoint clients
   - Core client implementation
   - Support for Python's logging library
   - Added possibility to load connection settings from configuration file
   - Simple access to OneView API endpoints through OneViewClient module
 3. Added developer-focused samples
 4. Continuous Integration
   - Integration with Travis-CI Server
   - Automatized build / unit test execution on every Pull Request

# v1.0.0
#### Notes
 This is the first release of the OneView SDK in Python and it adds support to core features listed bellow.
 This version of the SDK supports OneView appliances with versions 2.00.00 or higher, using the OneView Rest API version 120 or 200.

#### Features supported
 - Ethernet network
 - FC network
 - FCOE network
 - Network set
 - Connection template
 - Fabric
 - SAN manager
 - Managed SAN
 - Interconnect
 - Logical interconnect
 - Logical interconnect group
 - Uplink set
 - Logical downlink
 - Enclosure
 - Logical enclosure
 - Enclosure group
 - Firmware bundle
 - Firmware driver
 - Storage system
 - Storage pool
 - Volume
 - Volume template
 - Datacenter
 - Racks
 - Logical switch group
 - Logical switch
 - Switch
 - Power devices
 - Server profile
 - Server profile template
 - Server hardware
 - Server hardware type
 - Unmanaged devices
