from selenium import webdriver
from selenium.webdriver.common.by import By
from datetime import datetime
from time import sleep

txt_filepath = 'fsr-scrape/fsr-games.txt'

# Quais tipos de export deseja?
export_txt = True
export_csv = True #WIP
export_thumbnail = False
if export_thumbnail:
    images_per_wait = 10

driver = webdriver.Firefox() #seleciona web-driver(Firefox)
driver.implicitly_wait(5) #espera por até 5 segundos para encontrar elemento

# função para ler linhas do arquivo
def readlines(filepath):
    file = open(filepath,'r')
    file_list = file.readlines()
    file.close()
    return file_list

# função para deletar linhas do arquivo
# mantendo estrutura de newlines
def delete_lines(filepath,lines):
    file_list = readlines(txt_filepath)

    try:
        if type(lines) == type(list()):
            for line in lines:
                file_list[line] = ''
        else:
            file_list[lines] = ''
    except:
        print('Não foi possível apagar todas as linhas desejadas!')
    
    file = open(filepath,'w')
    file.writelines(file_list)
    file.close()

# função de teste se arquivo de texto já possui header
def contain_header(filepath):
    file_list = readlines(filepath)
    if len(file_list) > 0:
        if 'Last execution of the program:' in file_list[0]:
            return True
        else:
            return False
    else:
        return False

# função para adicionar header no arquivo txt
# 
def txt_header(filepath,new_games,last_exec):
    if contain_header(filepath):
        try:
            delete_lines(filepath,[0,1])
        except:
            pass

    file_list=readlines(filepath)

    file = open(filepath,'w')
    file.write(f'Last execution of the program: {last_exec.day}-{last_exec.month}-{last_exec.year} | {last_exec.hour}:{last_exec.minute}')
    file.write('\n')
    file.write(f'Newly added games detected on last execution: {new_games}')
    file.write('\n')
    file.writelines(file_list)
    file.close()

# abre navegador na página do AMD FSR
driver.get("https://www.amd.com/en/technologies/fidelityfx-super-resolution")

# acha container de jogos com FSR implementado
fsr_games = driver.find_element(By.ID,'paragraph-1396016')

# Acha container com a lista de jogos com FSR implementados
fsr_games_list = fsr_games.find_elements(By.CLASS_NAME,'field__item')

if export_thumbnail:
    try: #tenta fechar banner de cookies para todas as screenshots ficarem visíveis
        cookie_banner = driver.find_element(By.ID,'onetrust-banner-sdk')
        cookie_banner_close_container = cookie_banner.find_element(By.ID,'onetrust-close-btn-container')
        cookie_banner_close = cookie_banner_close_container.find_element(By.TAG_NAME,'button')
        cookie_banner_close.click()
    except:
        pass

if export_txt:
    # Tenta criar arquivo se arquivo ainda não existe
    try:
        file = open(txt_filepath,'x')
        file.close()
        print('Arquivo criado com sucesso!')
    except:
        print('O arquivo já existe!')
        pass

    # abre arquivo de texto e armazena nomes dos jogos já detectados
    # na ultima execução do programa em uma lista
    # para fácil checagem posteriormente
    file = open(txt_filepath,'r')
    file_list = []
    for line in file:
        file_list.append(line.replace('\n',''))
    file.close()


# este bloco é responsável por armazenar os jogos ainda
# não armazenados no arquivo de texto, indicando a quantidade
# de jogos detectados desde a última execução
if export_txt:
    file = open(txt_filepath,'a')
if export_thumbnail:
    i = 0
new_game_count = 0
for fsr_game in fsr_games_list:    
    if fsr_game.text != '':
        if fsr_game.text not in file_list:
            print(f'New game detected: {fsr_game.text}')
            if export_txt:
                file.write(fsr_game.text)
                file.write('\n')
            if export_csv:
                pass
            new_game_count += 1
    else:
        if export_thumbnail:
            if i == 0: #se primeira execução do loop
                fsr_game.screenshot(f'fsr-scrape/game_image/{i}.png')
                sleep(5) #espera imagens carregarem
            else:
                if (i % images_per_wait) == 0: #se 'images_per_wait' imagens sem espera para carregar...
                    sleep(0.4) #espera 0.4 segundos para carregar
            fsr_game.screenshot(f'fsr-scrape/game_image/{i}.png')
            i += 1
print(f'Newly added games: {new_game_count}')
last_exec = datetime.now()
print(f'Last program execution: {last_exec.day}-{last_exec.month}-{last_exec.year} | {last_exec.hour}:{last_exec.minute}')
if export_txt:
    file.close()

if export_txt:
    # chama função para adicionar header no arquivo de texto
    txt_header(txt_filepath,new_game_count,last_exec)

driver.close()