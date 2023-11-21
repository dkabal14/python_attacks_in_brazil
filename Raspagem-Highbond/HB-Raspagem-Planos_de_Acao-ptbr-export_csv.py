# ############################################
# ################ BIBLIOTECAS ###############
# ############################################

# import logging
import time # Para aguardar o download antes de fechar
import getpass as gp # Para pegar a senha do usuário (não funciona no robô Highbond)
import datetime as dt # Para pegar a data atual
import sys # Para retornar 0 na saída
import glob # para pegar o arquivo mais novo na pasta (ainda não implementado)
import os # para alterar os arquivos baixados (ainda não implementado)
import win32api # para pegar a propriedade de versão de arquivos (Especificamente para o Edge)
import shutil # para copiar o arquivo de resultado
from selenium import webdriver # Para iniciar o navegador e a navegação
from selenium.webdriver.common.by import By # Coleção de métodos para encontrar os webelements
from selenium.webdriver.common.action_chains import ActionChains # Para utilizar ações complexas como double_click e mouse_over
from selenium.webdriver.support import expected_conditions # Para iniciar condicionais de webelements
from selenium.webdriver.support.wait import WebDriverWait # Para aguardar a conclusão de um bloco condicional

# ##########################################
# ############### VARIAVEIS ################
# ##########################################

username = input('E-mail: ')
password = gp.getpass('Senha: ')

# username = sys.argv[1]
# password = sys.argv[2]

mainURL = 'https://accounts.highbond.com/orgs/26690'
relatorio = 'Relatório de Planos de Ação' # - SUCESSO
currDate = dt.datetime.now().strftime('%d_%m_%Y')
arquivoLog = f'c:\\teste\\HB-Raspagem-{currDate}.log'
pasta_raiz = f'c:\\teste\\'
ProcessamentoPath = f'{pasta_raiz}Download'
ResultadoPath = f'{pasta_raiz}Resultado'

# #########################################
# ############ BLOOCO DE DEBUG ############
# #########################################

# logging.basicConfig(filename="log.txt", level=logging.DEBUG, )
# root = logging.getLogger()
# root.setLevel(logging.DEBUG)
# handler = logging.StreamHandler(sys.stdout)
# handler.setLevel(logging.DEBUG)
# formatter = logging.Formatter('%(asctime)s - %(name)s: \n%(message)s')
# handler.setFormatter(formatter)
# root.addHandler(handler)

# #########################################
# ################ CLASSES ################
# #########################################

class Print2:
    def __init__(self, log_file2):
        self.log_file = log_file2

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

# #########################################
# ################ FUNÇÕES ################
# #########################################

def get_file_version(path): # Pega a propriedade de versão de um arquivo executável
    info = win32api.GetFileVersionInfo(path, '\\')
    ms = info['FileVersionMS']
    ls = info['FileVersionLS']
    version = f'{win32api.HIWORD(ms)}.{win32api.LOWORD(ms)}.{win32api.HIWORD(ls)}.{win32api.LOWORD(ls)}'
    return version

def altPrint(data): # Gera um log dos prints e ao mesmo tempo joga pra tela
    cfgPrint.print_and_log(data)

# #########################################
# ############ DESENVOLVIMENTO ############
# #########################################

if not os.path.exists(ProcessamentoPath): # Cria a pasta de download se ela não existir
    os.mkdir(ProcessamentoPath)

if not os.path.exists(ResultadoPath): # Cria a pasta de resultados se ela não existir
    os.mkdir(ResultadoPath)

cfgPrint = Print2(arquivoLog) # Define o arquivo de log

altPrint('='*60)
altPrint('Variáveis nessa sessão:')
altPrint('='*60)
altPrint(f'E-mail utilizado: {username}')
altPrint(f'URL da Organização: {mainURL}')
altPrint(f'Relatório Alvo: {relatorio}')
altPrint(f'Pasta de Resultado: {ResultadoPath}')
altPrint(f'Pasta de Download: {ProcessamentoPath}')
altPrint(f'Arquivo de log gerado em: {arquivoLog}')
altPrint(f'Versão do Selenium Webdriver: {webdriver.__version__}')
altPrint(f'Versão do Microsoft Edge: {get_file_version("C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe")}')
altPrint('='*60)

altPrint('Configurando as opções do Edge: ')

try:
    EdgeOptions = webdriver.EdgeOptions()
    EdgeOptions.add_experimental_option(name='prefs', value={"download.default_directory": ProcessamentoPath}) # Altera a pasta de download do arquivo
    EdgeOptions.add_experimental_option(name='excludeSwitches', value=['enable-logging']) #Desativa os avisos causados pelo bug do Edge na versão 4.15.2 do Selenium
except:
    altPrint('---> Não foi possível definir as preferências')
    altPrint('='*60)
    sys.exit(1)
else:
    altPrint('---> Configrações Definidas com Sucesso!')
    altPrint('='*60)


altPrint('Iniciando a automação do Edge: ')
try:
    #keep_alive = True mantém o navegador aberto para auxiliar no debug do código.
    objNavigator = webdriver.Edge(options=EdgeOptions, keep_alive=True)
except:
    altPrint('---> Não foi possível iniciar a automação')
    altPrint('='*60)
    sys.exit(1)
else:
    altPrint('---> Automação iniciada com sucesso')
    altPrint('='*60)

# Acessando a página de login

altPrint('Acessando a página de login: ')
try:
    objNavigator.get(mainURL)
except:
    altPrint('---> Não foi possível acessar a página de login')
    altPrint('='*60)
    objNavigator.quit()
    sys.exit(1)
else:
    altPrint('---> Página acessada com sucesso!')
    altPrint('='*60)


altPrint('Autenticando no portal: ')
try:
    # Aguarda os campos ficarem visíveis
    WebDriverWait(objNavigator, 30000).until(expected_conditions.visibility_of_element_located((By.ID, "user_email")))
    # Insere Usuário
    objNavigator.find_element(By.ID, "user_email").send_keys(username)
    # Insere Senha
    objNavigator.find_element(By.ID, "user_password").send_keys(password)
    # Autentica no portal
    objNavigator.find_element(By.NAME, "commit").click()
    # Checa o sucesso do logon, se não identificar um objeto que só aparece quando logado, levanta um erro do selenium.
    element = objNavigator.find_element(By.XPATH, "//a[@href='/orgs/26690/apps/21']")

except:
    altPrint(f'---> Não foi possível autenticar no portal para o usuário: {username}')
    altPrint('='*60)
    objNavigator.quit()
    sys.exit(1)
else:
    altPrint(f'---> Autenticação efetuada com sucesso para o usuário: {username}!')
    altPrint('='*60)

# Clica no link de relatórios

altPrint('Entrando na página de relatórios: ')
try:
    objNavigator.find_element(By.XPATH, "//a[@href='/orgs/26690/apps/21']").click()
except:
    altPrint('---> Não foi possível acessar a página de relatórios')
    altPrint('='*60)
    objNavigator.quit()
    sys.exit(1)
else:
    altPrint('---> Página de relatórios acessada com sucesso!')
    altPrint('='*60)


altPrint(f'Aguardando o relatório "{relatorio}" ficar visível e acessando-o:')
try:
    # Espera 30 segundos até que o link do relatório "Relatório de Planos de Ação" esteja visível na página
    WebDriverWait(objNavigator, 30000).until(expected_conditions.visibility_of_element_located((By.XPATH, f"//div[@title='{relatorio}']")))
    # Clica uma vez sobre o div para permitir a ação de clique duplo
    objNavigator.find_element(By.XPATH, f"//div[@title='{relatorio}']").click()
    # Faz um clique duplo no div do relatório
    element = objNavigator.find_element(By.XPATH, f"//div[@title='{relatorio}']")
    actions = ActionChains(objNavigator)
    actions.double_click(element).perform()
except:
    altPrint(f'---> O {relatorio} não está disponível ou a execução falhou')
    altPrint('='*60)
    objNavigator.quit()
    sys.exit(1)
else:
    altPrint('---> Relatório acessado com sucesso!')
    altPrint('='*60)


# Espera 2 minutos até que o filtro do dashboard esteja visível (indicando que o relatório terminou de carregar)

altPrint('Aguardando o carregamento do relatório: ')
try:
     # O botão "undo" nem sempre está visível, mas o webelement sempre aparece assim que os relatórios carregam.
    WebDriverWait(objNavigator, 90000).until(expected_conditions.presence_of_element_located((By.XPATH, "//div[@class='undo']")))
except:
    altPrint('---> A automação não identificou o carregamento do relatório')
    altPrint('='*60)
    objNavigator.quit()
    sys.exit(1)
else:
    altPrint('---> Relatório carregado!')
    altPrint('='*60)

# Clica no botão exportar para abrir o menu de exportação e depois clica no primeiro item do menu (se Deus quiser é a opção de csv)

altPrint('Abrindo dropdownlist de exportação e selecionando a opção de CSV')
try:
    objNavigator.find_element(By.XPATH, "//td[@id='reportexport']").click()
    objNavigator.find_element(By.XPATH, "//ul/li[1]").click() # Clica em CSV
    # objNavigator.find_element(By.XPATH, "//ul/li[2]").click() # Clica em PDF
    # objNavigator.find_element(By.XPATH, "//ul/li[3]").click() # Clica em Texto
    # objNavigator.find_element(By.XPATH, "//ul/li[4]").click() # Clica em XLSX
    # objNavigator.find_element(By.XPATH, "//ul/li[6]").click() # Clica em Impressão
except:
    altPrint('---> Não foi possível abrir as preferências de exportação de CSV:')
    altPrint('='*60)
    objNavigator.quit()
    sys.exit(1)
else:
    altPrint('---> Janela de preferências de exportação aberta!')
    altPrint('='*60)

# Aguarda até que o botão de exportação esteja disponível e depois clica nele
# Obs.: Como o botão possui uma classe dinâmica que muda com a ação "mouse_over", foi preciso clicar nela utilizando o caminho de XML dele, se o caminho mudar, o sistema não funciona

altPrint('Aguardando o carregamento do menu de exportação e iniciando o download: ')

try:
    
    WebDriverWait(objNavigator, 30000).until(expected_conditions.presence_of_element_located((By.XPATH, "//div[@class='exportBtn']/*//span[@class='submitMidHighlightText']")))

    # Todo esse bloco foi construído para os botões do menu de exportação CSV, mas podem ser facilmente trocados para as outras opções
    # Se esse bloco for comentado ou removido, a exportação ainda acontecerá, porém com o padrão que estiver no momento da execução
    # ================================================================================================================================
    time.sleep(5)

    toggle1 = objNavigator.find_element(By.XPATH, "//div[@class='optionListMain']/div[1]/*//*[@id='toggle']") # Botão de Pular citações
    if toggle1.get_attribute('class') == 'rounded-toggle toggle-off': # Marca se estiver desmarcado
        toggle1.click()
        altPrint('---> Executado clique para marcar "Incluir Cabeçalhos"')

    toggle2 = objNavigator.find_element(By.XPATH, "//div[@class='optionListMain']/div[2]/*//*[@id='toggle']") # Botão Incluir cabeçalhos
    if toggle2.get_attribute('class') == 'rounded-toggle toggle-off': # Marca se estiver desmarcado
        toggle2.click() # Clica na opção incluir cabeçalhos
        altPrint('---> Executado clique para marcar "Incluir Cabeçalhos"')
    
    dropdownlist1 = objNavigator.find_element(By.XPATH, "//div[@class='optionListMain']/div[3]/*//select") # dropdownlist de Conjunto de caracteres
    dropdownlist1.find_element(By.XPATH, "option[@value='UTF-8']").click() # Não importa qual a opção, sempre marca UTF-8
    altPrint('---> Marcada a opção UTF-8 na opção Conjunto de Caracteres')

    dropdownlist2 = objNavigator.find_element(By.XPATH, "//div[@class='optionListMain']/div[4]/*//select") # dropdownlist de Separador de campos
    dropdownlist2.find_element(By.XPATH, "option[@value='COMMA']").click() # Não importa qual a opção, sempre marca UTF-8
    altPrint('---> Marcada a opção Vírgula em "Separador de Campos"')

    toggle3 = objNavigator.find_element(By.XPATH, "//div[@class='optionListMain']/div[7]/*//*[@id='toggle']") # Botão Citar todos os valores
    if toggle3.get_attribute('class') == 'rounded-toggle toggle-off': # Marca se estiver desmarcado
        toggle3.click()
        altPrint('---> Executado clique para marcar "Citar Todos os Valores"')

    dropdownlist3 = objNavigator.find_element(By.XPATH, "//div[@class='optionListMain']/div[8]/*//select") # dropdownlist Fechamento de Campo
    dropdownlist3.find_element(By.XPATH, "option[@value='DOUBLEQUOTE']").click()
    altPrint('---> Marcada a opção Aspas Duplas em "Fechamento de Campo"')
    # ================================================================================================================================
    time.sleep(5)

    # Clica no botão de download
    objNavigator.find_element(By.XPATH, "//div[@class='exportBtn']/*//span[@class='submitMidHighlightText']").click()
except:
    altPrint('---> Não foi possível abrir o menu de exportação ou iniciar o download')
    altPrint('='*60)
    objNavigator.quit()
    sys.exit(1)
else:
    altPrint('---> Download iniciado com sucesso!')
    altPrint('='*60)

# Esperando o download terminar
time.sleep(10)

# Implementar para a alteração dos arquivos
# ========================================
ProcessamentoPathRec = f'{ProcessamentoPath}\\*'

arquivosBaixados = glob.glob(ProcessamentoPathRec)
ultimoArquivoBaixado = max(arquivosBaixados, key=os.path.getctime)

arquivoOrigem = os.path.basename(ultimoArquivoBaixado).split('/')[-1]
extensaoArquivo = arquivoOrigem.split('.')[-1]

nomeAntigo = f'{ResultadoPath}\\{arquivoOrigem}'
nomeNovoBase = f'{ResultadoPath}\\Planos de Ação {currDate}.{extensaoArquivo}'

i = 2
sair = False
if os.path.exists(nomeNovoBase):
    # Esse bloco deleta o arquivo do dia se existir para criar um atualizado
    os.remove(nomeNovoBase)
    nomeNovo = nomeNovoBase

    # Substituindo o algoritmo de cima por esse, faz com que os arquivos de resultados não sejam substituídos durante a cópia do arquivo baixado durante a rotina
    #=============================================================================
    # while sair != True:
    #     if os.path.exists(f'{ResultadoPath}\\Planos de Ação {currDate} ({i}).{extensaoArquivo}'):
    #         i = i + 1
    #     else:
    #         nomeNovo = f'{ResultadoPath}\\Planos de Ação {currDate} ({i}).{extensaoArquivo}'
    #         sair = True
else:
    nomeNovo = nomeNovoBase
    
shutil.copy(ultimoArquivoBaixado, ResultadoPath)
os.replace(nomeAntigo, nomeNovo)
altPrint(f'---> Último arquivo baixado foi copiado da pasta {ProcessamentoPath} para a pasta {ResultadoPath}')
altPrint(f'---> O nome do arquivo foi alterado de {arquivoOrigem} para Planos de Ação {nomeNovo}')
altPrint('='*60)
altPrint('---> Fim do script')
objNavigator.quit()
sys.exit(0)