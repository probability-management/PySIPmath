# PySIPmath
Package containing the export and import functions for using/making SIP libraries:

## PySIP3library
Converts pandas DataFrames cotaining data or SIPs into SIPmath 3.0 libraries 
in a .json or .xlsx format.

### Usage
```python
import PySIP
import pandas

PySIP.Json(pandas.read_csv("input.csv"), "output.json", "Abraham Lincoln")
```

### Example

To see it in action, execute `./example.py` in the project root, and observe the example `Dev_Time_Lib.SIPmath` generated from `./example/Dev_Time_Lib.csv`.

## PySIP2library
Used for outputting pandas DataFrames as SIPmath 2.0 libraries in an .xlsx format.


## chanceCalc
Import function for SIPlibraries; for use in monte carlo simulation or data imports..

*metalog package can be found at https://pypi.org/project/metalog/
