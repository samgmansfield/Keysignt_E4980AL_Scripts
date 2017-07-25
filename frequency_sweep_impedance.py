# frequency_sweep_impedance.py
#
# Sends SCPI commands to Keysight E4980AL LCR meter to measure
# impedance over a logarithmic frequency sweep. The results
# are graphed.
#
# Author: Sam Mansfield

import visa
import numpy as np
from matplotlib import pyplot as plt
import re
import sys
import os

def print_usage():
  print("Correct usage:")
  print("  default:")
  print("    frequency_sweep_impedance.py file_name")
  print("      file_name: name of file to store data")
  print("  custom:")
  print("    frequency_sweep_impedance.py file_name fi ff voltage num_of_samples")
  print("      file_name: name of file to store data")
  print("      fi: initial frequency")
  print("      ff: final frequency")
  print("      voltage: fixed voltage")
  print("      num_of_samples: number of samples to average")
  exit()

if len(sys.argv) != 2 and len(sys.argv) != 6:
  print_usage()

file_name = sys.argv[1]
if os.path.exists(file_name):
  print("File already exists: " + file_name)
  exit()

# Lowest frequency is 20Hz, highest frequency is 2MHz
fi = 20
ff = 2000
voltage = 0.1
num_of_samples = 1

if len(sys.argv) == 6:
  fi = int(sys.argv[2])
  ff = int(sys.argv[3])
  voltage = float(sys.argv[4])
  num_of_samples = int(sys.argv[5])

rm = visa.ResourceManager()
inst = rm.open_resource(rm.list_resources()[0])
print("Connected to: ")
print(inst.query("*IDN?"))

samples_per_decade = 30
log_fi = np.log10(fi)
log_ff = np.log10(ff)
decades = log_ff - log_fi
freq_list = np.logspace(log_fi, log_ff, num = decades*samples_per_decade)  

print("Starting a frequency sweep from " + str(freq_list[0]) + "-" + str(freq_list[-1]))

inst.write(":VOLTage:LEVel " + str(voltage))
print("Voltage set to: " + str(voltage))

r_list = []
x_list = []
z_list = []
d_list = []
for freq in freq_list:
  r_samples = []
  x_samples = []
  z_samples = []
  d_samples = []
  for i in range(num_of_samples):
    inst.write(":FREQuency:CW " + str(freq))
    inst.write(":FUNCtion:IMPedance:TYPE RX")
    inst.write(":TRIGger:IMMediate")
    #imped = inst.query(":FETCh:IMPedance:CORRected?")
    rx = inst.query(":FETCh:IMPedance:FORMatted?")
    #print(imped)
    m = re.search("(.+),(.+),.+", rx)
    if m:
      # By experimentation units are in ohms
      r = float(m.group(1))
      x = float(m.group(2))
      r_samples.append(r)
      x_samples.append(x)
    else:
      print("Unrecognized output: " + str(rx))
      exit()

    inst.write(":FUNCtion:IMPedance:TYPE ZTD")
    inst.write(":TRIGger:IMMediate")
    ztd = inst.query(":FETCh:IMPedance:FORMatted?")
    #print(imped)
    m = re.search("(.+),(.+),.+", ztd)
    if m:
      # By experimentation units are in ohms
      z = float(m.group(1))
      d = float(m.group(2))
      z_samples.append(z)
      d_samples.append(d)
    else:
      print("Unrecognized output: " + str(ztd))
      exit()

  r_list.append(np.mean(r_samples))
  x_list.append(np.mean(x_samples))
  z_list.append(np.mean(z_samples))
  d_list.append(np.mean(d_samples))

f = open(file_name, "w")
f.write("Frequency, R, X, Z, Phase\n")
for i in range(len(freq_list)):
  f.write(str(freq_list[i]) + ", " + str(r_list[i]) + ", " + str(x_list[i]) + ", " + str(z_list[i]) + ", " + str(d_list[i]) + "\n")
f.close()

# Graph the impedance vs. frequency
plt.plot(freq_list, r_list, label = "real")
plt.xlim(fi, ff)
plt.xscale("log")
plt.xlabel("Frequency (Hz)")
plt.ylabel("Impedance (Ohms)")
#plt.plot(freq_list, x_list, label = "imaginary")

plt.legend()
plt.show()

# Two sets of axes example
#fig, ax1 = plt.subplots()
#t = np.arange(0.01, 10.0, 0.01)
#s1 = np.exp(t)
#ax1.plot(t, s1, 'b-')
#ax1.set_xlabel('time (s)')
## Make the y-axis label, ticks and tick labels match the line color.
#ax1.set_ylabel('exp', color='b')
#ax1.tick_params('y', colors='b')
#
#ax2 = ax1.twinx()
#s2 = np.sin(2 * np.pi * t)
#ax2.plot(t, s2, 'r.')
#ax2.set_ylabel('sin', color='r')
#ax2.tick_params('y', colors='r')