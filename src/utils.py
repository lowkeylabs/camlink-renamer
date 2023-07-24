"""
"""
import os
import sys
import winreg
from loguru import logger

def search_registry_for_device_instance( substring ):
    """ Search registry """
    registry_path = "SYSTEM\\ControlSet001\\Control\\DeviceClasses"

    logger.debug("opening key")
    try:
        key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, registry_path)
    except FileNotFoundError:
        print("Could not open registry. Do you have admin rights?")
        sys.exit(1)
    except Exception as e:
        print(f"An error occured: {e}")
        sys.exit(1)

    logger.debug("searching subkeys")
    key_list = {}
    try:
        count = winreg.QueryInfoKey(key)[0]

        for i in range(count):
            subkey_name = winreg.EnumKey(key, i)
#            if substring in subkey_name:
#                print(f"Substring found in: {registry_path}\\{subkey_name}")

            subkey_path = f"{registry_path}\\{subkey_name}"
            try:
                subkey = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, subkey_path)
                subkey_count = winreg.QueryInfoKey(subkey)[0]

                for j in range(subkey_count):
                    subsubkey_name = winreg.EnumKey(subkey, j)
#                    logger.debug(f"{registry_path}\\{subkey_name}\\{subsubkey_name}")
#                    logger.debug(f"{subsubkey_name}")
                    if substring.upper() in subsubkey_name.upper():
#                        logger.info(f"subsubkey: {subsubkey_name}")

                        try:
                            searchkey_path = f"{registry_path}\\{subkey_name}\\{subsubkey_name}\\#GLOBAL\\Device Parameters"
                            logger.debug(f"{searchkey_path}")
                            searchkey = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE,searchkey_path)
                            friendly_name, itype = winreg.QueryValueEx( searchkey,"FriendlyName")
                            logger.info(f"{friendly_name} found in found in: {subsubkey_name}")
            
                            parts = searchkey_path.split("\\")
                            moreparts = parts[5].split("#")
                            device_instance_path = f"{moreparts[3]}#{moreparts[4]}#{moreparts[5]}"
                            device_identifier = moreparts[5]
                            moremoreparts = device_identifier.split("&")
                            device_id = moremoreparts[1]

                            if not device_id in key_list.keys():
                                key_list[device_id] = {"device_id":device_id,"friendly_name":friendly_name,"searchkey_paths":[]}
                            key_list[device_id]["searchkey_paths"].append({"searchkey_path":searchkey_path,
                                                        "friendly_name":friendly_name,
                                                        "subsubkey_name":subsubkey_name,
                                                        "device_instance_path":device_instance_path,
                                                        "device_identifier":device_identifier,
                                                        "device_id":device_id})
                            winreg.CloseKey( searchkey )
                        except Exception as e:
                            logger.debug(f"Error with search: {e}")

#                if subkey_count > 0:
#                    search_registry_for_substring(substring, subkey_path)

                winreg.CloseKey(subkey)
            except Exception as e:
                logger.debug(f"Error accessing subkey '{subkey_path}': {e}")

        winreg.CloseKey(key)
    except FileNotFoundError:
        logger.info("Registry key not found.")
    except Exception as e:
        logger.warning(f"An error occurred: {e}")
    return key_list

def rename_device_instance( new_name, keylist ):
    """ Given a list of keys, rename device """
    for subkey_path in keylist:
        try:
            subkey = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, subkey_path, 0, winreg.KEY_SET_VALUE)
            winreg.SetValueEx(subkey, "FriendlyName", 0, winreg.REG_SZ, new_name)
            winreg.CloseKey(subkey)
            print(f"Key value 'FriendlyName' has been updated to '{new_name}' in: {subkey_path}")
        except FileNotFoundError:
            print("Registry key not found.")
        except Exception as e:
            print(f"An error occurred: {e}")

def rename_device_driver( long_path ):
    print(f"{long_path}")
    # split on \# character. Create 3 pieces.
    # driver friendly name is here: Computer\HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Enum\#1\#2\#3\FriendlyName


def get_camlink_devices():
    """ return list of camlink devices
    """

# USB\VID_0FD9&PID_0067&MI_00\8&298320BB&0&0000
# USB\VID_0FD9&PID_0066&MI_00\6&1D3A44BA&0&0000
# USB\VID_0FD9&PID_0066&MI_00\6&86946DA&0&0000

    device_instance_path_to_search = "USB#VID_0FD9&PID_0066"
    keylist1 = search_registry_for_device_instance(device_instance_path_to_search)
    device_instance_path_to_search = "USB#VID_0FD9&PID_0067"
    keylist2 = search_registry_for_device_instance(device_instance_path_to_search)

    for key in keylist2.keys():
        keylist1[key] = keylist2[key]

#    rename_device_instance("Cam Link 4K-Canon R10",keylist)
#    rename_device_driver( device_instance_path_to_search )

    return keylist1
