class Print2:
    def __init__(self, log_file = 'Print2.log'):
        self.log_file = log_file

    def print_and_log(self, data_to_print):
        import datetime as dt
        import os
        
        log_file = self.log_file

        if os.path.exists(log_file):
           mode = 'a'
        else:
           mode = 'w'

        if type(data_to_print) != list:
           data_to_print = [data_to_print]
        
        dateAndTime = dt.datetime.now()
        logTime = dateAndTime.strftime('%d-%m-%Y %H:%M:%S')

        try:
            with open(log_file, mode, encoding='UTF-8') as file:
                if mode == 'w':
                   texto = f'LOG GERADO PELO ROBÔ PYTHON NO DIA E HORA: {dateAndTime.strftime("%d-%m-%Y")}'
                   print(texto)
                   file.write(texto)

                for data in data_to_print:
                    texto = f'{logTime}: {data}'
                    if file.closed:
                        with open(log_file, 'a', encoding='UTF-8') as file:

                            print(texto)

                            if isinstance(data, str):
                                file.write('\n' + texto)
                            else:
                                print("Tipo não suportado. Somente texto é suportado.")
                            file.close()            
                    else:
                        
                        print(texto)

                        if isinstance(data, str):
                            file.write('\n' + texto)
                        else:
                            print("Tipo não suportado. Somente texto é suportado.")
                        file.close()
        except Exception as Exp:
            print(f'Erro para logar os dados {Exp}')

print2 = Print2()
print2.log_file = 'teste.log'
print2.print_and_log('teste')