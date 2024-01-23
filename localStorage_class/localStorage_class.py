import csv
import os
from typing import Literal

class localStor:
    def __init__(self, storage_name: str, talkative = True):
        self.storage_name = storage_name
        self.talkative = talkative
        
    def create_storage(self, fields: list, data: list = []) -> bytes:
        try:
            if os.path.exists(f'{self.storage_name}.csv'):
                raise Exception(f'Storage {self.storage_name} already exists!')
            
            with open(self.storage_name + '.csv', 'w', newline='') as f:

                writer = csv.writer(f)
                
                if len(fields) != 0:
                    writer.writerow(fields)

                if len(data) != 0:
                    if type(data[0]) != list:
                        writer.writerow(data)
                    else:
                        writer.writerows(data)
                if self.talkative == True:
                    print(f'{self.storage_name}.csv were created.')
            
        except Exception as e:
            print(f'Creation failed: {e}')

    def storage_info(self, option: Literal['full', 'fields'] = 'full'):
        try:
            if option == 'full':
                with open(self.storage_name + '.csv', 'r') as f:
                    lines = f.readlines()
                    objResult = []
                    for currLine in reader:
                        line = currLine.split(',')
                        objResult.append(line)

            elif option == 'fields':
                with open(self.storage_name + '.csv', 'r') as f:
                    reader = csv.DictReader(f)
                    return reader.fieldnames.__str__()
            else:
                raise Exception('Either choose "full" or "fields"')
            
        except Exception as e:
            print(f'Could not show {self.storage_name} info: {e}')