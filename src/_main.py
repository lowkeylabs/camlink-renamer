"""
"""
import sys
import winreg
import click
from loguru import logger
from .utils import rename_device_driver, get_camlink_devices

logger.remove()
logger.add(sys.stderr, level="SUCCESS")


@click.group()
@click.pass_context
def cli(ctx):
    """ Change friendly (user facing) names for CamLink 4K USB video capture device.
    """
    pass

@cli.command()
@click.option("--all", help="Show all CamLinks ever connected to system.")
@click.option("-v","--verbose", help="Provide detailed / verbose output")
@click.pass_context
def list(ctx,all,verbose):
    """ Lists Elgato CamLink devices and provides a simple reference id.
    """
    print("list")
#    device_instance_path_to_search = "USB#VID_0FD9&PID_0066&MI_00#8&2764D13E&0&0000"

    camlink_list = get_camlink_devices()
    i = 0
    for camlink in camlink_list.keys():
        print( f"{i:2} : {camlink_list[camlink]['device_id']:8} : {camlink_list[camlink]['friendly_name']}" )
        i = i + 1

@cli.command()
@click.pass_context
@click.option("--sid",help="The list-ID of CamLink from previous list command")
@click.option("--name", help="The friendly name to associate with this CamLink")
def rename(ctx,sid,name):
    """ Renames CamLink device using reference id
    """
    print("rename")
#    device_instance_path_to_search = "USB#VID_0FD9&PID_0066&MI_00#8&2764D13E&0&0000"
#    keylist = search_registry_for_device_instance(device_instance_path_to_search)
#    rename_device_instance("Cam Link 4K-Canon R10",keylist)
#    rename_device_driver( device_instance_path_to_search )

if __name__ == '__main__':
    cli()
    