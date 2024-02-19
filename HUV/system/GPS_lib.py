# SPDX-FileCopyrightText: 2017 Tony DiCola for Adafruit Industries
# SPDX-FileCopyrightText: 2021 James Carr
#
# SPDX-License-Identifier: MIT

"""
`adafruit_gps`
====================================================
GPS parsing module.  Can parse simple NMEA data sentences from serial GPS
modules to read latitude, longitude, and more.
* Author(s): Tony DiCola, James Carr
Implementation Notes
--------------------
**Hardware:**
* Adafruit `Ultimate GPS Breakout <https://www.adafruit.com/product/746>`_
* Adafruit `Ultimate GPS FeatherWing <https://www.adafruit.com/product/3133>`_
**Software and Dependencies:**
* Adafruit CircuitPython firmware for the ESP8622 and M0-based boards:
  https://github.com/adafruit/circuitpython/releases
"""
import time
#from micropython import const

__version__ = "0.0.0-auto.0"
__repo__ = "https://github.com/adafruit/Adafruit_CircuitPython_GPS.git"




_GLL = 0
_RMC = 1
_GGA = 2
_GSA = 3
_GSA_4_11 = 4
_GSV7 = 5
_GSV11 = 6
_GSV15 = 7
_GSV19 = 8
_RMC_4_1 = 9
_ST_MIN = _GLL
_ST_MAX = _RMC_4_1

_SENTENCE_PARAMS = (
    # 0 - _GLL
    "dcdcfcC",
    # 1 - _RMC
    "fcdcdcffiDCC",
    # 2 - _GGA
    "fdcdciiffsfsIS",
    # 3 - _GSA
    "ciIIIIIIIIIIIIfff",
    # 4 - _GSA_4_11
    "ciIIIIIIIIIIIIfffS",
    # 5 - _GSV7
    "iiiiiiI",
    # 6 - _GSV11
    "iiiiiiIiiiI",
    # 7 - _GSV15
    "iiiiiiIiiiIiiiI",
    # 8 - _GSV19
    "iiiiiiIiiiIiiiIiiiI",
    # 9 - _RMC_4_1
    "fcdcdcffiDCCC",
)


# Internal helper parsing functions.
# These handle input that might be none or null and return none instead of
# throwing errors.
def _parse_degrees(nmea_data):
    # Parse a NMEA lat/long data pair 'dddmm.mmmm' into a pure degrees value.
    # Where ddd is the degrees, mm.mmmm is the minutes.
    if nmea_data is None or len(nmea_data) < 3:
        return None
    raw = float(nmea_data)
    deg = raw // 100
    minutes = raw % 100
    return deg + minutes / 60


def _parse_int(nmea_data):
    if nmea_data is None or nmea_data == "":
        return None
    return int(nmea_data)


def _parse_float(nmea_data):
    if nmea_data is None or nmea_data == "":
        return None
    return float(nmea_data)


def _parse_str(nmea_data):
    if nmea_data is None or nmea_data == "":
        return None
    return str(nmea_data)


def _read_degrees(data, index, neg):
    x = data[index]
    if data[index + 1].lower() == neg:
        x *= -1.0
    return x


def _parse_talker(data_type):
    # Split the data_type into talker and sentence_type
    if data_type[0] == b"P":  # Proprietary codes
        return (data_type[:1], data_type[1:])

    return (data_type[:2], data_type[2:])


def _parse_data(sentence_type, data):
    """Parse sentence data for the specified sentence type and
    return a list of parameters in the correct format, or return None.
    """
    # pylint: disable=too-many-branches

    if not _ST_MIN <= sentence_type <= _ST_MAX:
        # The sentence_type is unknown
        return None

    param_types = _SENTENCE_PARAMS[sentence_type]

    if len(param_types) != len(data):
        # The expected number does not match the number of data items
        return None

    params = []
    try:
        for i, dti in enumerate(data):
            pti = param_types[i]
            len_dti = len(dti)
            nothing = dti is None or len_dti == 0
            if pti == "c":
                # A single character
                if len_dti != 1:
                    return None
                params.append(dti)
            elif pti == "C":
                # A single character or Nothing
                if nothing:
                    params.append(None)
                elif len_dti != 1:
                    return None
                else:
                    params.append(dti)
            elif pti == "d":
                # A number parseable as degrees
                params.append(_parse_degrees(dti))
            elif pti == "D":
                # A number parseable as degrees or Nothing
                if nothing:
                    params.append(None)
                else:
                    params.append(_parse_degrees(dti))
            elif pti == "f":
                # A floating point number
                params.append(_parse_float(dti))
            elif pti == "i":
                # An integer
                params.append(_parse_int(dti))
            elif pti == "I":
                # An integer or Nothing
                if nothing:
                    params.append(None)
                else:
                    params.append(_parse_int(dti))
            elif pti == "s":
                # A string
                params.append(dti)
            elif pti == "S":
                # A string or Nothing
                if nothing:
                    params.append(None)
                else:
                    params.append(dti)
            else:
                raise TypeError(f"GPS: Unexpected parameter type '{pti}'")
    except ValueError:
        # Something didn't parse, abort
        return None

    # Return the parsed data
    return params


# lint warning about too many attributes disabled
# pylint: disable-msg=R0902


class GPS:
    """GPS parsing module.  Can parse simple NMEA data sentences from serial
    GPS modules to read latitude, longitude, and more.
    """

    def __init__(self, uart, debug=False):
        self._uart = uart
        # Initialize null starting values for GPS attributes.
        self.timestamp_utc = None
        self.latitude = None
        self.longitude = None
        self.fix_quality = 0
        self.fix_quality_3d = 0
        self.satellites = None
        self.satellites_prev = None
        self.horizontal_dilution = None
        self.altitude_m = None
        self.height_geoid = None
        self.speed_knots = None
        self.track_angle_deg = None
        self._sats = None  # Temporary holder for information from GSV messages
        self.sats = None  # Completed information from GSV messages
        self.isactivedata = None
        self.true_track = None
        self.mag_track = None
        self.sat_prns = None
        self.sel_mode = None
        self.pdop = None
        self.hdop = None
        self.vdop = None
        self.total_mess_num = None
        self.mess_num = None
        self._raw_sentence = None
        self._mode_indicator = None
        self._magnetic_variation = None
        self.debug = debug

    def update(self):
        """Check for updated data from the GPS module and process it
        accordingly.  Returns True if new data was processed, and False if
        nothing new was received.
        """
        # Grab a sentence and check its data type to call the appropriate
        # parsing function.

        try:
            
            sentence = self._parse_sentence()
            
        except UnicodeError:
            return None
        if sentence is None:
            return False
        data_type, args = sentence
        if len(data_type) < 5:
            return False
        data_type = bytes(data_type.upper(), "ascii")
        (talker, sentence_type) = _parse_talker(data_type)
        #print(_parse_talker(data_type))
        # Check for all currently known GNSS talkers
        # GA - Galileo
        # GB - BeiDou Systems
        # GI - NavIC
        # GL - GLONASS
        # GP - GPS
        # GQ - QZSS
        # GN - GNSS / More than one of the above
        if talker not in (b"GA", b"GB", b"GI", b"GL", b"GP", b"GQ", b"GN"):
            # It's not a known GNSS source of data
            # Assume it's a valid packet anyway
            return True

        result = True
        args = args.split(",")
        #print(sentence)
        if sentence_type == b"RMC":  # Minimum location info
            #print(sentence)
            result = self._parse_rmc(args)
            
        elif sentence_type == b"GGA":  # 3D location fix
            #print(sentence)
            result = self._parse_gga(args)

        return result

    def send_command(self, command, add_checksum=True):
        """Send a command string to the GPS.  If add_checksum is True (the
        default) a NMEA checksum will automatically be computed and added.
        Note you should NOT add the leading $ and trailing * to the command
        as they will automatically be added!
        """
        self.write(b"$")
        print(b"$")
        self.write(command)
        print(command)
        if add_checksum:
            checksum = 0
            for char in command:
                checksum ^= char
            self.write(b"*")
            self.write(bytes("{:02x}".format(checksum).upper(), "ascii"))
        self.write(b"\r\n")

    @property
    def has_fix(self):
        return self.fix_quality is not None and self.fix_quality >= 1#True if a current fix for location information is available."""

    @property
    def has_3d_fix(self):
        return self.fix_quality_3d is not None and self.fix_quality_3d >= 2 #"""Returns true if there is a 3d fix available. use has_fix to determine if a 2d fix is available, passing it the same data"""

    @property
    def datetime(self):
        return self.timestamp_utc#"""Return struct_time object to feed rtc.set_time_source() function"""

    @property
    def nmea_sentence(self):
        return self._raw_sentence #"""Return raw_sentence which is the raw NMEA sentence read from the GPS"""

    def read(self, num_bytes):
        return self._uart.read(num_bytes)#"""Read up to num_bytes of data from the GPS directly, without parsing.Returns a bytearray with up to num_bytes or None if nothing was read"""

    def write(self, bytestr):
        return self._uart.write(bytestr)#"""Write a bytestring data to the GPS directly, without parsingor checksums"""
    

    @property
    def in_waiting(self):
        return self._uart.in_waiting #"""Returns number of bytes available in UART read buffer"""

    def readline(self):
        return self._uart.readline()#"""Returns a newline terminated bytearray, must have timeout set for the underlying UART or this will block forever!"""

    def _read_sentence(self):
        # Parse any NMEA sentence that is available. pylint: disable=len-as-condition This needs to be refactored when it can be tested.
        if self.in_waiting : # Only continue if we have at least 11 bytes in the input buffer
            sentence = self.readline()
            
            if sentence is None or sentence == b"" or len(sentence) < 1:
                return None
            try:
                sentence = str(sentence, "ascii").strip()
            except UnicodeError:
                return None
            if len(sentence) > 7 and sentence[-3] == "*":        # Look for a checksum and validate it if present.
                expected = int(sentence[-2:], 16)# Get included checksum, then calculate it and compare.
                actual = 0
                for i in range(1, len(sentence) - 3):
                    actual ^= ord(sentence[i])
                if actual != expected:
                    return None  # Failed to validate checksum.
                self._raw_sentence = sentence# copy the raw sentence

                return sentence
            # At this point we don't have a valid sentence
            return None

    def _parse_sentence(self):
        sentence = self._read_sentence()
        if sentence is None: # sentence is a valid NMEA with a valid checksum
            return None
        sentence = sentence[:-3] # Remove checksum once validated.
        delimiter = sentence.find(",")# Parse out the type of sentence (first string after $ up to comma and then grab the rest as data within the sentence.
        if delimiter == -1:
            return None  # Invalid sentence, no comma after data type.
        data_type = sentence[1:delimiter]
        return (data_type, sentence[delimiter + 1 :])

    def _update_timestamp_utc(self, time_utc, date=None):
        hours = time_utc // 10000
        mins = (time_utc // 100) % 100
        secs = time_utc % 100
        if date is None:
            if self.timestamp_utc is None:
                day, month, year = 0, 0, 0
            else:
                day = self.timestamp_utc.tm_mday
                month = self.timestamp_utc.tm_mon
                year = self.timestamp_utc.tm_year
        else:
            day = date // 10000
            month = (date // 100) % 100
            year = 2000 + date % 100

        self.timestamp_utc = time.struct_time((year, month, day, hours, mins, secs, 0, 0, -1))

 
    def _parse_rmc(self, data):
        # RMC - Recommended Minimum Navigation Information

        if data is None or len(data) not in (12, 13):
            return False  # Unexpected number of params.
        data = _parse_data({12: _RMC, 13: _RMC_4_1}[len(data)], data)
        if data is None:
            return False  # Params didn't parse

        self._update_timestamp_utc(int(data[0]), data[8]) # UTC time of position and date

        self.isactivedata = data[1] # Status Valid(A) or Invalid(V)
        if data[1].lower() == "a":
            if self.fix_quality == 0:
                self.fix_quality = 1
        else:
            self.fix_quality = 0

        self.latitude = _read_degrees(data, 2, "s") # Latitude
        self.longitude = _read_degrees(data, 4, "w") # Longitude
        self.speed_knots = data[6]  # Speed over ground, knots
        self.track_angle_deg = data[7]  # Track made good, degrees true
        if data[9] is None or data[10] is None: # Magnetic variation
            self._magnetic_variation = None
        else:
            self._magnetic_variation = _read_degrees(data, 9, "w")
        self._mode_indicator = data[11] # Parse FAA mode indicator

        return True

    def _parse_gga(self, data):
        # GGA - Global Positioning System Fix Data

        if data is None or len(data) != 14:
            return False  # Unexpected number of params.
        data = _parse_data(_GGA, data)
        if data is None:
            return False  # Params didn't parse

        self._update_timestamp_utc(int(data[0])) # UTC time of position
        self.latitude = _read_degrees(data, 1, "s") # Latitude
        self.longitude = _read_degrees(data, 3, "w") # Longitude

        # GPS quality indicator
        # 0 - fix not available,
        # 1 - GPS fix,
        # 2 - Differential GPS fix (values above 2 are 2.3 features)
        # 3 - PPS fix
        # 4 - Real Time Kinematic
        # 5 - Float RTK
        # 6 - estimated (dead reckoning)
        # 7 - Manual input mode
        # 8 - Simulation mode
        
        self.fix_quality = data[5]
        self.satellites = data[6]               # Number of satellites in use, 0 - 12
        self.horizontal_dilution = data[7]      # Horizontal dilution of precision
        self.altitude_m = _parse_float(data[8]) # Antenna altitude relative to mean sea level
        # data[9] - antenna altitude unit, always 'M' ? 
        self.height_geoid = _parse_float(data[10]) # Geoidal separation relative to WGS 84
        # data[11] - geoidal separation unit, always 'M' ???
        # data[12] - Age of differential GPS data, can be null
        # data[13] - Differential reference station ID, can be null

        return True