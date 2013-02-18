from serial import Serial
from binascii import b2a_hex, a2b_hex

digit_table = {'05' : ('1', False),
             '85' : ('1', True),
             '5B' : ('2', False),
             'DB' : ('2', True),
             '1F' : ('3', False),
             '9F' : ('3', True),
             '27' : ('4', False),
             'A7' : ('4', True),
             '3E' : ('5', False),
             'BE' : ('5', True),
             '7E' : ('6', False),
             'FE' : ('6', True),
             '15' : ('7', False),
             '95' : ('7', True),
             '7F' : ('8', False),
             'FF' : ('8', True),
             '3F' : ('9', False),
             'BF' : ('9', True),
             '7D' : ('0', False),
             'FD' : ('0', True),
             '00' : ('', False),
             '80' : ('', True),
             '68' : ('L', False),
             'E8' : ('L', True)
             }

indicators = [None, None, 'DegC', None,
            'Batt', 'Hz', 'V', 'A',
            'Hold', 'REL', 'Ohm', 'F',
            'Sound', 'M', '%', 'm',
            'Diode', 'k', 'n', 'u'] + \
            [None] * 32 + \
            ['RS232', 'AUTO', 'DC', 'AC']

def read_meter(port):
  ser = Serial(port, 2400)
  try:
      byte = ser.read()
      while b2a_hex(byte)[0] != '1':
          # Keep reading until we get to the beginning of the next packet
          byte = ser.read()
      rawdata = byte + ser.read(13)
      # Strip out the sequencing data and convert to hex
      hexdata = b2a_hex(rawdata)[1::2].upper()

      digits = [digit_table.get(hexdata[i:i+2], ('X', False)) \
                for i in (1, 3, 5, 7)]

      digitstr = ''
      if digits[0][1]:
          digitstr += '-'
      digitstr += digits[0][0]
      for digit in digits[1:]:
          if digit[1]:
              digitstr += '.'
          digitstr += digit[0]

      long_data = long(hexdata, 16)
      active_indicators = [indicators[bit_pos] for bit_pos in range(56) \
                           if (long_data >> bit_pos) & 1 \
                           and indicators[bit_pos] is not None]
      return digitstr, active_indicators
  finally:
      ser.close()
 
for i in range(100):
  print read_meter('/dev/cu.usbserial')
