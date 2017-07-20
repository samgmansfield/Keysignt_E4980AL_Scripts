This directory contains Python scripts that can be used to send SCPI commands using PyVisa
to the Keysight E4980AL LCR Meter.

Dependencies: PyVisa
Install pyVisa:
  https://pyvisa.readthedocs.io/en/stable/
  PyVisa is the SCPI command python library. To install via conda type:
	  >> conda install -c conda-forge pyvisa=1.8

Install NI-VISA:
  The pyVisa library uses the NI-VSA library, so it also must be installed.
  https://pyvisa.readthedocs.io/en/stable/getting_nivisa.html#getting-nivisa
