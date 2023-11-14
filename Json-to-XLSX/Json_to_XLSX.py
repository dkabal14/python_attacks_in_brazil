import sys
import json
import pandas as pd
import openpyxl

importFile = sys.argv[1]

data = json.load(open(importFile))

df = pd.DataFrame(data['data'])

with pd.ExcelWriter('export.xlsx', engine='openpyxl') as xlWriter:
    df.to_excel(xlWriter,sheet_name='json', index=False)