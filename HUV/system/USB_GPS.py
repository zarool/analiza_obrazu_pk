from time import sleep
import serial
from serial.tools import list_ports

# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

# Simple GPS module demonstration.
# Will wait for a fix and print a message every second with the current location
# and other details.
import time
import board


import GPS_lib


# Create a serial connection for the GPS connection using default speed and
# a slightly higher timeout (GPS modules typically update once a second).
# These are the defaults you should use for the GPS FeatherWing.
# For other boards set RX = GPS module TX, and TX = GPS module RX pins.
def GPS_communication(nie_potrzebne,magazyn):
    device_list = list_ports.comports()

    for device in device_list:
            if (device.vid == magazyn.GPS_VID) and (device.pid == magazyn.GPS_PID):
                port_USB = device.device
                print(port_USB)
    try:
        port = serial.Serial(port=port_USB, baudrate=9600, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, bytesize=serial.EIGHTBITS, timeout=0.1, xonxoff=False, rtscts=False, write_timeout=None, dsrdtr=True, inter_byte_timeout=None, exclusive=None) # w razie problemów z komunikacją podmień na 0  
        magazyn.GPSUsbAddress = port
        if magazyn.GPS != 1:
                magazyn.GPS = 1
        magazyn.status = 'IDLE'
    except:
        print("No GPS")
        magazyn.GPS = 0
        magazyn.status = 'IDLE'
    if magazyn.GPS == 1:
        # Create a GPS module instance.
        gps = GPS_lib.GPS(magazyn.GPSUsbAddress, debug=False)  # Use UART/pyserial

        #Turn on the basic GGA and RMC info (what you typically want)
        gps.send_command(b"PMTK314,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0")

        # Set update rate to once a second (1hz) which is what you typically want.
        gps.send_command(b"PMTK220,3000")

        sleep(1)
        # Main loop runs forever printing the location, etc. every second.
        last_print = time.monotonic()

        while True:

            gps.update()
            # Every second print out current location details if there's a fix.
            current = time.monotonic()
    #     if current - last_print >= 1.0:
#         last_print = current
#         if not gps.has_fix:
#             # Try again if we don't have a fix yet.
#             print("Waiting for fix...")
#             continue
#         # We have a fix! (gps.has_fix is true)
#         # Print out details about the fix like location, date, etc.
#         print("=" * 40)  # Print a separator line.
#         print(
#             "Fix timestamp: {}/{}/{} {:02}:{:02}:{:02}".format(
#                 gps.timestamp_utc.tm_mon,  # Grab parts of the time from the
#                 gps.timestamp_utc.tm_mday,  # struct_time object that holds
#                 gps.timestamp_utc.tm_year,  # the fix time.  Note you might
#                 gps.timestamp_utc.tm_hour,  # not get all data like year, day,
#                 gps.timestamp_utc.tm_min,  # month!
#                 gps.timestamp_utc.tm_sec,
#             )
#         )
#         print("Latitude: {0:.6f} degrees".format(gps.latitude))
#         print("Longitude: {0:.6f} degrees".format(gps.longitude))
#         print("Fix quality: {}".format(gps.fix_quality))
#         # Some attributes beyond latitude, longitude and timestamp are optional
#         # and might not be present.  Check if they're None before trying to use!
#         if gps.satellites is not None:
#             print("# satellites: {}".format(gps.satellites))
#         if gps.altitude_m is not None:
#             print("Altitude: {} meters".format(gps.altitude_m))
#         if gps.speed_knots is not None:
#             print("Speed: {} knots".format(gps.speed_knots))
#         if gps.track_angle_deg is not None:
#             print("Track angle: {} degrees".format(gps.track_angle_deg))
#         if gps.horizontal_dilution is not None:
#             print("Horizontal dilution: {}".format(gps.horizontal_dilution))
#         if gps.height_geoid is not None:
#             print("Height geoid: {} meters".format(gps.height_geoid))