import sys
import json
import pandas as pd
import openpyxl

def Json_to_XLSX(importFile):
    import json
    import pandas as pd
    
    try:
        data = json.load(open(importFile))
        df = pd.DataFrame(data['data'])
        filename = 'export.xlsx'
        with pd.ExcelWriter(filename, engine='openpyxl') as xlWriter:
            df.to_excel(xlWriter,sheet_name='json', index=False)
        print(f'criado arquivo {filename}')
        sys.exit(0)
    except:
        sys.exit(1)

importFile = sys.argv[1]
Json_to_XLSX(importFile)