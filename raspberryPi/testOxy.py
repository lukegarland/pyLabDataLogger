#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
    Test device support.
    
    @author Daniel Duke <daniel.duke@monash.edu>
    @copyright (c) 2018-2023 LTRAC
    @license GPL-3.0+
    @version 1.3.0
    @date 23/12/2022
        __   ____________    ___    ______
       / /  /_  ____ __  \  /   |  / ____/
      / /    / /   / /_/ / / /| | / /
     / /___ / /   / _, _/ / ___ |/ /_________
    /_____//_/   /_/ |__\/_/  |_|\__________/

    Laboratory for Turbulence Research in Aerospace & Combustion (LTRAC)
    Monash University, Australia
    
    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

import time
from termcolor import cprint
from pyLabDataLogger.device.i2c import i2cDevice
from pyLabDataLogger.device import usbDevice
from pyLabDataLogger.logger import globalFunctions

if __name__ == '__main__':

    globalFunctions.banner()
    devices=[]
    
    # I2C setup
    found = i2cDevice.scan_for_devices(bus=1)
    devices = i2cDevice.load_i2c_devices(found) 
    if len(devices)==0: 
        cprint( "No I2C devices found.", 'red',attrs=['bold'])
    

    # USB setup
    usbDevicesFound = usbDevice.search_for_usb_devices(debugMode=True)
    special_args={'debugMode':True, 'live_preview':True, 'quiet':False}
    devices.extend( usbDevice.load_usb_devices(usbDevicesFound, **special_args) )

    # Serial device on the Pi's UART
    from pyLabDataLogger.device import serialDevice
    devices.append( serialDevice.serialDevice({'driver':'serial/hpma', 'port':'/dev/serial0'}) )

    try:
        while True:
            for d in devices:
                cprint( d.name, 'magenta', attrs=['bold'] )
                d.query()
                d.pprint()
            time.sleep(1)
            print("")
    except KeyboardInterrupt:
        cprint( "Stopped.", 'red',attrs=['bold'])
    except: # all other errors
        raise
     

