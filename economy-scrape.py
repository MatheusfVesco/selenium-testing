from selenium import webdriver
from selenium.webdriver.common.by import By

driver = webdriver.Firefox() #seleciona web-driver(Firefox)

#abre navegador na página de indicadores do IBGE
driver.get("https://ibge.gov.br/indicadores")

#lista de nomes de IDs relacionados a dados economicos
lista_ids_total = ['ipca','inpc','ipca-15','ipp','custo-do-m','variacao-do-pib','pib-per-capita','industria','comercio','servicos']

#lista de dados economicos no formato "valor mês ano"
lista_ids = ['ipca','inpc','ipca-15','ipp','custo-do-m','industria','comercio','servicos']

#seleciona tabela de dados economicos
indicadores_economicos = driver.find_element(By.CLASS_NAME,'indicadores-table-container')

#armazena todos elementos da coluna "Último" em um dicionário
all_elements = {}
for id in lista_ids:
    all_elements[id] = indicadores_economicos.find_element(By.ID,f'indicador-{id}').find_element(By.CLASS_NAME,"ultimo")

#A partir da lista gerada anteriormente, gera novo dicionário no formato
#{'Indicador economico':{
#   'value': valor float,
#   'month': mês string,
#   'year': ano int,
# }
#}
valores_porcent = {}
for id in all_elements:
    string_list = all_elements[id].text.split()
    id_dict = {}
    for i in range(3):
        id_dict['value'] = float(string_list[0].replace(',','.'))
        id_dict['month'] = string_list[1]
        id_dict['year'] = int(string_list[2])
    valores_porcent[id] = id_dict

print(valores_porcent)
#fecha navegador
driver.close()

