import json
import pandas as pd

# series like column
data = {"Math": 90, "English": 85, "Science": 95}
s = pd.Series(data)

fruits = ["蘋果", "橘子", "梨子", "櫻桃"]
quantities = [15, 33, 45, 55]
ss = pd.Series(quantities, index=fruits)
print(ss)
print(ss.index)
print(ss.values)

print(pd.show_versions())