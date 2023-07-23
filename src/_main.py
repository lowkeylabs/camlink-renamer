"""
"""
import sys
import winreg
import click
from loguru import logger
from .utils import rename_device_instance, search_registry_for_device_instance, rename_device_driver

logger.remove()
logger.add(sys.stderr, level="INFO")


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
def list(ctx):
    """ List CamLink devices and provides simple ID (sid).
    """
    print("list")
#    device_instance_path_to_search = "USB#VID_0FD9&PID_0066&MI_00#8&2764D13E&0&0000"
#    keylist = search_registry_for_device_instance(device_instance_path_to_search)
#    rename_device_instance("Cam Link 4K-Canon R10",keylist)
#    rename_device_driver( device_instance_path_to_search )

@cli.command()
@click.pass_context
@click.option("--sid",help="The list-ID of CamLink from previous list command")
@click.option("--name", help="The friendly name to associate with this CamLink")
def rename(ctx):
    """ Rename CamLink device using simple ID (sid).
    """
    print("rename")
#    device_instance_path_to_search = "USB#VID_0FD9&PID_0066&MI_00#8&2764D13E&0&0000"
#    keylist = search_registry_for_device_instance(device_instance_path_to_search)
#    rename_device_instance("Cam Link 4K-Canon R10",keylist)
#    rename_device_driver( device_instance_path_to_search )

if __name__ == '__main__':
    cli()
    