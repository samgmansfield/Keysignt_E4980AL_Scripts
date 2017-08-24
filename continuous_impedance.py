# continuous_impedance.py
#
# Sends SCPI commands to Keysight E4980AL LCR meter to measure
# impedance at a set frequency over time. The results are written
# to a file.
#
# Author: Sam Mansfield

import visa
import numpy as np
import re
import sys
import os
import datetime

def print_usage():
  print("Correct usage:")
  print("  continuous_impedance.py frequency file_name")
  print("    file_name: name of file to store data")
  exit()

if len(sys.argv) != 3:
  print_usage()

freq = sys.argv[1]

# Do not overwrite a file if it already exists
file_name = sys.argv[2]
if os.path.exists(file_name):
  print("File already exists: " + file_name)
  overwrite = raw_input("Overwrite? (y/n) ")
  if overwrite != "y":
    exit()

voltage = 0.1
num_of_samples = 1

rm = visa.ResourceManager()
inst = rm.open_resource(rm.list_resources()[0])
print("Connected to: ")
print(inst.query("*IDN?"))

inst.write(":VOLTage:LEVel " + str(voltage))
print("Voltage set to: " + str(voltage))

#inst.write(":FREQuency:CW " + freq)
#print("Frequency set to: " + freq)

# Set sweep mode to sequence, set by default

# Generate a frequency string of values as an input to :LIST:FREQuency
freq_str = freq
for i in range(200):
  freq_str += "," + freq
inst.write(":LIST:FREQuency " + freq_str)

inst.write(":FUNCtion:IMPedance:TYPE RX")

r_samples = []
x_samples = []
# Open file for writing
f = open(file_name, "w")
f.write("Timestamp, R, X\n")
# Loops forever, must be killed using ^C
while True:
  inst.write(":TRIGger:IMMediate")
  #imped = inst.query(":FETCh:IMPedance:CORRected?")
  rx = inst.query(":FETCh:IMPedance:FORMatted?")
  #print(imped)
  print(rx)
  #m = re.search("(.+),(.+),.+", rx)
  #if m:
  #  # By experimentation units are in ohms
  #  r = float(m.group(1))
  #  x = float(m.group(2))
  #  r_samples.append(r)
  #  x_samples.append(x)
  #else:
  #  print("Unrecognized output: " + str(rx))
  #  exit()
  #
  ## Write timestamp
  #f.write(str(datetime.datetime.now()))
  #f.write(", ")
  #f.write(str(np.mean(r_samples)))
  #f.write(", ")
  #f.write(str(np.mean(x_samples)))
  #f.write("\n")

# This will never happen in the current implementation
f.close()
