import time # Para aguardar o download antes de fechar
import getpass as gp # Para pegar a senha do usuário (não funciona no robô Highbond)
import datetime as dt # Para pegar a data atual
import glob # para pegar o arquivo mais novo na pasta (ainda não implementado)
import os # para alterar os arquivos baixados (ainda não implementado)

# Importações de métodos da library do selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

# ##########################################
# ############### VARIAVEIS ################
# ##########################################
username = input('E-mail: ')
password = gp.getpass('Senha: ')
mainURL = 'https://accounts.highbond.com/orgs/26690'
ProcessamentoPath = f'c:\\teste\\Processamento'
ResultadoPath = f'c:\\teste\\Download'
# currDate = dt.datetime.now().strftime('%d_%m_%Y')

# Implementar para a alteração dos arquivos
# ========================================
# if not os.path.exists(ProcessamentoPath):
#     os.mkdir(ProcessamentoPath)

# if not os.path.exists(ResultadoPath):
#     os.mkdir(ResultadoPath)

print('='*60)
print(f'Os arquivos serão baixados para {ProcessamentoPath}')
print('='*60)


print('Configurando as opções do Edge')

try:
    EdgeOptions = webdriver.EdgeOptions()
    EdgeOptions.add_experimental_option(name='prefs', value={"download.default_directory": ProcessamentoPath}) # Altera a pasta de download do arquivo
    EdgeOptions.add_experimental_option(name='excludeSwitches', value=['enable-logging']) #Desativa os avisos causados pelo bug do Edge na versão 4.15.2 do Selenium
except:
    print('---> Não foi possível definir as preferências')
    print('='*60)
    exit()
else:
    print('---> Configrações Definidas com Sucesso!')
    print('='*60)


print('Iniciando a automação do Edge: ')
try:
    #keep_alive = True mantém o navegador aberto para auxiliar no debug do código.
    objNavigator = webdriver.Edge(options=EdgeOptions, keep_alive=True)
except:
    print('---> Não foi possível iniciar a automação')
    print('='*60)
    exit()
else:
    print('---> Automação iniciada com sucesso')
    print('='*60)

# Acessando a página de login

print('Acessando a página de login: ')
try:
    objNavigator.get(mainURL)
except:
    print('---> Não foi possível acessar a página de login')
    print('='*60)
    exit()
else:
    print('---> Página acessada com sucesso!')
    print('='*60)


print('Autenticando no portal: ')
try:
    # Insere Usuário
    objNavigator.find_element(By.ID, "user_email").send_keys(username)
    # Insere Senha
    objNavigator.find_element(By.ID, "user_password").send_keys(password)
    #Autentica no portal
    objNavigator.find_element(By.NAME, "commit").click()
    
except:
    print('---> Não foi possível definir as preferências')
    print('='*60)
    exit()
else:
    print('---> Autenticação efetuada com sucesso!')
    print('='*60)

# Clica no link de relatórios

print('Entrando na página de relatórios: ')
try:
    objNavigator.find_element(By.LINK_TEXT, "Relatórios").click()
except:
    print('---> Não foi possível acessar a página de relatórios')
    print('='*60)
    exit()
else:
    print('---> Página de relatórios acessada com sucesso!')
    print('='*60)


print('Aguardando o relatório de planos de ação ficar visível e acessando-o:')
try:
    # Espera 30 segundos até que o link do relatório "Relatório de Planos de Ação" esteja visível na página
    WebDriverWait(objNavigator, 30000).until(expected_conditions.visibility_of_element_located((By.XPATH, "//div[@title='Relatório de Planos de Ação']")))
    # Clica uma vez sobre o div para permitir a ação de clique duplo
    objNavigator.find_element(By.XPATH, "//div[@title='Relatório de Planos de Ação']").click()
    # Faz um clique duplo no div do relatório
    element = objNavigator.find_element(By.XPATH, "//div[@title='Relatório de Planos de Ação']")
    actions = ActionChains(objNavigator)
    actions.double_click(element).perform()
except:
    print('---> O relatório de planos de ação não está disponível ou a execução falhou')
    print('='*60)
    exit()
else:
    print('---> Relatório acessado com sucesso!')
    print('='*60)


# Espera 2 minutos até que o filtro do dashboard esteja visível (indicando que o relatório terminou de carregar)

print('Aguardando o carregamento do relatório: ')
try:
    WebDriverWait(objNavigator, 120000).until(expected_conditions.visibility_of_element_located((By.CSS_SELECTOR, ".filterList")))
except:
    print('---> A automação não identificou o carregamento do relatório')
    print('='*60)
    exit()
else:
    print('---> Relatório carregado!')
    print('='*60)

# Clica no botão exportar para abrir o menu de exportação e depois clica no primeiro item do menu (se Deus quiser é a opção de csv)

print('Abrindo dropdownlist de exportação e selecionando a opção de Excel')
try:
    objNavigator.find_element(By.XPATH, "//img[@title='Exportar']").click()
    # objNavigator.find_element(By.XPATH, "//ul/li[1]").click() # Clica em CSV
    # objNavigator.find_element(By.XPATH, "//ul/li[2]").click() # Clica em PDF
    # objNavigator.find_element(By.XPATH, "//ul/li[3]").click() # Clica em Texto
    objNavigator.find_element(By.XPATH, "//ul/li[4]").click() # Clica em XLSX
    # objNavigator.find_element(By.XPATH, "//ul/li[6]").click() # Clica em Impressão
except:
    print('---> Não foi possível abrir as preferências de exportação de XLSX:')
    print('='*60)
    exit()
else:
    print('---> Janela de preferências de exportação aberta!')
    print('='*60)

# Aguarda até que o botão de exportação esteja disponível e depois clica nele
# Obs.: Como o botão possui uma classe dinâmica que muda com a ação "mouse_over", foi preciso clicar nela utilizando o caminho de XML dele, se o caminho mudar, o sistema não funciona

print('Aguardando o carregamento do menu de exportação e iniciando o download: ')

try:
    # WebDriverWait(objNavigator, 30000).until(expected_conditions.presence_of_element_located((By.XPATH, "//div[7]/table/tbody/tr/td/div/table/tbody/tr/td[2]/span")))
    WebDriverWait(objNavigator, 30000).until(expected_conditions.presence_of_element_located((By.XPATH, "//div[@class='exportBtn']/*//span[@class='submitMidHighlightText']")))
    time.sleep(5)

    # toggle1 = objNavigator.find_element(By.XPATH, "//div[@class='optionListMain']/div[1]/*//*[@id='toggle']") # Botão de Pular citações
    # if toggle1.get_attribute('class') == 'rounded-toggle toggle-off': # Marca se estiver desmarcado
    #     toggle1.click()
    #     print('---> Executado clique para marcar "Incluir Cabeçalhos"')

    # toggle2 = objNavigator.find_element(By.XPATH, "//div[@class='optionListMain']/div[2]/*//*[@id='toggle']") # Botão Incluir cabeçalhos
    # if toggle2.get_attribute('class') == 'rounded-toggle toggle-off': # Marca se estiver desmarcado
    #     toggle2.click() # Clica na opção incluir cabeçalhos
    #     print('---> Executado clique para marcar "Incluir Cabeçalhos"')
    
    # dropdownlist1 = objNavigator.find_element(By.XPATH, "//div[@class='optionListMain']/div[3]/*//select") # dropdownlist de Conjunto de caracteres
    # dropdownlist1.find_element(By.XPATH, "option[@value='UTF-8']").click() # Não importa qual a opção, sempre marca UTF-8
    # print('---> Marcada a opção UTF-8 na opção Conjunto de Caracteres')

    # dropdownlist2 = objNavigator.find_element(By.XPATH, "//div[@class='optionListMain']/div[4]/*//select") # dropdownlist de Separador de campos
    # dropdownlist2.find_element(By.XPATH, "option[@value='COMMA']").click() # Não importa qual a opção, sempre marca UTF-8
    # print('---> Marcada a opção Vírgula na opção Vírgula')

    # toggle3 = objNavigator.find_element(By.XPATH, "//div[@class='optionListMain']/div[7]/*//*[@id='toggle']") # Botão Citar todos os valores
    # if toggle3.get_attribute('class') == 'rounded-toggle toggle-off': # Marca se estiver desmarcado
    #     toggle3.click()
    #     print('---> Executado clique para marcar "Citar Todos os Valores"')

    # dropdownlist3 = objNavigator.find_element(By.XPATH, "//div[@class='optionListMain']/div[8]/*//select") # dropdownlist Fechamento de Campo
    # dropdownlist3.find_element(By.XPATH, "option[@value='DOUBLEQUOTE']").click()
    # print('---> Marcada a opção Vírgula na opção Vírgula')

    # time.sleep(5)

    # Clica no botão de download
    objNavigator.find_element(By.XPATH, "//div[@class='exportBtn']/*//span[@class='submitMidHighlightText']").click()
except:
    print('---> Não foi possível abrir o menu de exportação ou iniciar o download')
    print('='*60)
    exit()
else:
    print('---> Download iniciado com sucesso!')
    print('='*60)

# Esperando o download terminar
time.sleep(10)

# Implementar para a alteração dos arquivos
# ========================================
# files_to_rename = os.listdir(ProcessamentoPath)
# i = 0
# for file in files_to_rename:
#     filepath = ProcessamentoPath + f'\\' + file
#     filename = ResultadoPath + f'\\Plano de Ação {currDate}.txt'
    
#     sair = False
#     while sair != True:
#         if not os.path.exists(filename):
#             sair = True
#         else:
#             i = i + 1
                
#     os.replace(filepath, filename)
#     i = i + 1

objNavigator.quit()