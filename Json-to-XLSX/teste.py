import sys
import subprocess

jsonFile = 'C:/Users/Trabalho/VSCode_GIT_Workspaces/python_attacks_in_brazil/Json-to-XLSX/files/Sign_offs_1.json'
jsonScript = 'C:/Users/Trabalho/VSCode_GIT_Workspaces/python_attacks_in_brazil/Json-to-XLSX/Json_to_XLSX.py'
subprocess.check_call([sys.executable, jsonScript, jsonFile])