# frequency_sweep_impedance.py
#
# Sends SCPI commands to Keysight E4980AL LCR meter to measure
# impedance over a logarithmic frequency sweep. The results
# are graphed.
#
# Author: Sam Mansfield

#import visa
import numpy as np
from matplotlib import pyplot as plt
import re
import sys

def print_usage():
  print("Correct usage:")
  print("  default:")
  print("    frequency_sweep_impedance.py")
  print("  custom:")
  print("    frequency_sweep_impedance.py fi ff voltage num_of_samples")
  print("      fi: initial frequency")
  print("      ff: final frequency")
  print("      voltage: fixed voltage")
  print("      num_of_samples: number of samples to average")
  exit()

if len(sys.argv) != 1 and len(sys.argv) != 5:
  print_usage()

# Lowest frequency is 20Hz, highest frequency is 2MHz
fi = 20
ff = 2000
voltage = 0.1
num_of_samples = 1

if len(sys.argv) == 5:
  fi = int(sys.argv[1])
  ff = int(sys.argv[2])
  voltage = float(sys.argv[3])
  num_of_samples = int(sys.argv[4])

rm = visa.ResourceManager()
inst = rm.open_resource(rm.list_resources()[0])
print("Connected to: ")
print(inst.query("*IDN?"))

samples_per_decade = 30
log_fi = np.log10(fi)
log_ff = np.log10(ff)
decades = log_ff - log_fi
freq_list = np.logspace(np.log10(fi), np.log10(ff), num = decades*samples_per_decade)  

print("Starting a frequency sweep from " + str(freq_list[0]) + "-" + str(freq_list[-1]))

inst.write(":VOLTage:LEVel " + str(voltage))
print("Voltage set to: " + str(voltage))
r_list = []
x_list = []
for freq in freq_list:
  r_samples = []
  x_samples = []
  for i in range(num_of_samples):
    inst.query(":FREQuency:CW " + str(freq))
    inst.write(":TRIGger:IMMediate")
    imped = inst.query(":FETCh:IMPedance:CORRected?")
    imped = "1e7-40"
    m = re.search("(.+)-(.+)", imped)
    if m:
      # By experimentation units are in ohms
      r = float(m.group(1))
      x = float(m.group(2))
      r_samples.append(r)
      x_samples.append(x)
    else:
      print("Unrecognized output: " + str(imped))
      exit()
  r_list.append(np.mean(r_samples))
  x_list.append(np.mean(x_samples))

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

