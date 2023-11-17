import sys
import subprocess

liLibs = [
    'openpyxl',
    'pandas'
]

for lib in liLibs:
    try:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '--upgrade', '--no-warn-script-location', '--disable-pip-version-check', '--no-warn-script-location', '--no-warn-conflicts', '--quiet', lib])
    except:
        print(f"Não foi possível atualizar a biblioteca {lib}")

    
jsonFile = 'C:/users/Trabalho/JSON_TESTE.json'
jsonScript = 'C:/Users/Trabalho/VSCode_GIT_Workspaces/python_attacks_in_brazil/Json-to-XLSX/Json_to_XLSX.py'
Response = subprocess.check_call([sys.executable, jsonScript, jsonFile])
sys.exit(Response)