cyrustek-multimeter
===================

Python Module for Communicating with Multimeters with Cyrustek Chips.

This module works with many low cost multimeters that have an RS232 interface.  These multimeters send packets of data
over the serial port in binary format representing the state of the individual LCD segments lit.  There is a sole function, read_meter.

read_meter(port)
----------------
  Read a CyrusTek compatible multimeter on on a serial port port.  Returns
  (digit_string, indicators)

  port -> The serial port device to read from
  
  digit_string <- A string representation of the digits on the display usually
  suitable for passing to float().  If the measured value is off-scale low,
  digit_string will be 'L'.

  indicators <- A list of strings in the set:
  ['DegC', 'Batt', 'Hz', 'V', 'A', 'Hold', 'REL', 'Ohm', 'F', 'Sound', 'M', '%',
  'm', 'Diode', 'k', 'n', 'u', 'RS232', 'AUTO', 'DC', 'AC']
  representing the LCD indicators that are currently lit on the multimeter's
  display.