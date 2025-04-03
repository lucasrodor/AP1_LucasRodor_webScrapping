from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import pandas as pd
import re
import unicodedata
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os
from urllib.parse import quote_plus
from datetime import datetime

# Normaliza acentuação e caixa (pra evitar erros com "Suítes", "quartos", etc)
def normalizar(texto):
    texto = str(texto)
    texto = unicodedata.normalize('NFKD', texto).encode('ASCII', 'ignore').decode('ASCII')
    return texto.lower()

# Expressão que pega valores tipo "94 a 98 m²", "286 m²", "2 Quartos", etc
padrao = r'(\d+\s*(?:a\s*\d+)?)\s*(m2|quartos?|vagas?|suites?|plantas?)'

# Função para extrair um tipo específico
def extrair(detalhe, tipo_alvo):
    detalhe = normalizar(detalhe)
    matches = re.findall(padrao, detalhe)
    for valor, tipo in matches:
        if tipo_alvo in tipo:
            return valor.strip()
    return ''

def buscar_imoveis(tipo_operacao="", tipo_imovel="", localizacao="", cidade="", bairro="", quartos ="", preco_medio="", palavra_chave=""):
    # Configurações do navegador
    options = Options()
    # options.add_argument("--headless")  # Ativa modo invisível se quiser
    driver = webdriver.Chrome(options=options)

    url = 'https://dfimoveis.com.br'
    driver.get(url)

    wait = WebDriverWait(driver, 10)

    # === 1. Tipo de operação ===
    if tipo_operacao:
        campo_operacao = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "select2-selection--single")))
        campo_operacao.click()
        campo_busca = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "select2-search__field")))
        campo_busca.send_keys(tipo_operacao)
        campo_busca.send_keys(Keys.ENTER)
        sleep(1)

    # === 2. Tipo de imóvel ===
    if tipo_imovel:
        todos_os_seletores = driver.find_elements(By.CLASS_NAME, "select2-selection--single")
        todos_os_seletores[1].click()
        campo_tipo = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "select2-search__field")))
        campo_tipo.send_keys(tipo_imovel)
        campo_tipo.send_keys(Keys.ENTER)
        sleep(1)

    # === 3. Localização ===
    if localizacao:
        todos_os_seletores = driver.find_elements(By.CLASS_NAME, "select2-selection--single")
        todos_os_seletores[2].click()
        campo_localizacao = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "select2-search__field")))
        campo_localizacao.send_keys(localizacao)
        campo_localizacao.send_keys(Keys.ENTER)
        sleep(1)

    # === 4. Cidade ===
    if cidade:
        todos_os_seletores = driver.find_elements(By.CLASS_NAME, "select2-selection--single")
        todos_os_seletores[3].click()
        campo_cidade = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "select2-search__field")))
        campo_cidade.send_keys(cidade)
        campo_cidade.send_keys(Keys.ENTER)
        sleep(1)

    # === 5. Bairro ===
    if bairro:
        todos_os_seletores = driver.find_elements(By.CLASS_NAME, "select2-selection--single")
        todos_os_seletores[4].click()
        campo_bairro = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "select2-search__field")))
        campo_bairro.send_keys(bairro)
        campo_bairro.send_keys(Keys.ENTER)
        sleep(1)

    # === 6. Quartos ===
    if quartos:
        todos_os_seletores = driver.find_elements(By.CLASS_NAME, "select2-selection--single")
        todos_os_seletores[5].click()
        sleep(1)
        opcoes_quartos = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "select2-results__option")))

        for opcao in opcoes_quartos:
            texto = opcao.text.strip()
            if texto.startswith(quartos):
                opcao.click()
                break
        sleep(1)

    # === 7. Preço médio ===
    if preco_medio:
        campo_preco = wait.until(EC.element_to_be_clickable((By.ID, "valorMedio")))
        campo_preco.clear()
        campo_preco.send_keys(preco_medio)
        sleep(1)
        
    # === 8. Palavra-chave (endereço ou empreendimento) ===
    if palavra_chave:
        campo_palavra = wait.until(EC.element_to_be_clickable((By.ID, "palavraChave")))
        campo_palavra.clear()
        campo_palavra.send_keys(palavra_chave)
        sleep(1)

    # === 9. Buscar ===
    botao_buscar = wait.until(EC.element_to_be_clickable((By.ID, "botaoDeBusca")))
    botao_buscar.click()
    sleep(7)

    # === 10. Coleta de dados ==+
    lista_imoveis = []

    while True:
        print("Coletando página...")

        resultados_container = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="resultadoDaBuscaDeImoveis"]')))
        cards = resultados_container.find_elements(By.TAG_NAME, 'a')

        for card in cards:
            imovel = {}
            try:
                imovel['titulo'] = card.find_element(By.CLASS_NAME, 'new-title').text
            except:
                imovel['titulo'] = "N/A"

            try:
                imovel['preco'] = card.find_element(By.CLASS_NAME, 'new-price').text
            except:
                imovel['preco'] = "N/A"

            try:
                imovel['endereco'] = card.find_element(By.CLASS_NAME, 'new-subtitle').text
            except:
                imovel['endereco'] = "N/A"

            try:
                imovel['detalhes'] = card.find_element(By.CLASS_NAME, 'new-details-ul').text
            except:
                imovel['detalhes'] = "N/A"

            try:
                imovel['descricao'] = card.find_element(By.CLASS_NAME, 'new-simple').text
            except:
                imovel['descricao'] = "N/A"

            try:
                imovel['link'] = card.get_attribute("href")
            except:
                imovel['link'] = "N/A"

            lista_imoveis.append(imovel)

        # Verifica botão "Próximo"
        try:
            botao_proximo = driver.find_element(By.CSS_SELECTOR, ".btn.next")
            if "disabled" in botao_proximo.get_attribute("class"):
                print("Última página.")
                break
            botao_proximo.click()
            sleep(4)
        except:
            print("Paginação encerrada.")
            break

    driver.quit()

    # DataFrame e tratamento
    df = pd.DataFrame(lista_imoveis)

    # Preço limpo
    df['preco'] = df['preco'].apply(
        lambda x: float(
            re.search(r'R\$[\s]*([\d\.\,]+)', x).group(1).replace('.', '').replace(',', '.')
        ) if isinstance(x, str) and re.search(r'R\$[\s]*([\d\.\,]+)', x) else None
    )

    # Extração dos detalhes
    df['detalhes'] = df['detalhes'].fillna('').apply(lambda x: x.replace('\n', ',  '))
    df['tamanho']  = df['detalhes'].apply(lambda x: extrair(x, 'm2'))
    df['quartos']  = df['detalhes'].apply(lambda x: extrair(x, 'quarto'))
    df['vagas']    = df['detalhes'].apply(lambda x: extrair(x, 'vaga'))
    df['suites']   = df['detalhes'].apply(lambda x: extrair(x, 'suite'))
    df['plantas']  = df['detalhes'].apply(lambda x: extrair(x, 'planta'))

    return df

def salvar_imoveis(df, salvar_excel=True, salvar_mysql=False):
    if salvar_excel:
        data_str = datetime.now().strftime("%Y-%m-%d_%H-%M")
        filename = f"imoveis_{data_str}.xlsx"
        df.to_excel(filename, index=False)
        print(f"Excel salvo como: {filename}")

    if salvar_mysql:
        load_dotenv()

        host = 'localhost'
        port = '3306'
        user = os.getenv("MYSQL_USER")
        senha = quote_plus(os.getenv("MYSQL_PASSWORD"))
        database_name = 'db_imoveis'

        DATABASE_URL = f'mysql+pymysql://{user}:{senha}@{host}:{port}/{database_name}'
        engine = create_engine(DATABASE_URL)
        df['data_extracao'] = datetime.now()
        # Padroniza os nomes das colunas para bater com o banco
        df = df.rename(columns={
            'titulo': 'titulo',
            'preco': 'preco',
            'endereco': 'endereco',
            'detalhes': 'detalhes',
            'descricao': 'descricao',
            'link': 'link',
            'tamanho': 'tamanho',
            'quartos': 'quartos',
            'vagas': 'vagas',
            'suites': 'suites',
            'plantas': 'plantas'
        })
        #Evitar registros duplicados, só cadastra os novos verificando pelo link de cada um
        try:    
            with engine.begin() as connection:
                links_existentes = pd.read_sql('SELECT link FROM imoveis', con=connection)['link'].tolist()
                novos_df = df[~df['link'].isin(links_existentes)]
                # print("\nPré-visualização dos dados a serem inseridos:")
                # print(novos_df[['titulo', 'link', 'preco', 'data_extracao']].head(10))
                # print("\nTipos das colunas:")
                # print(novos_df.dtypes)
                # print(f"\nTotal de registros novos detectados: {len(novos_df)}\n")


                #Se não tiver vazio, da insert na tabela imoveis o que ta no data frame
                if not novos_df.empty:
                    novos_df.to_sql(name='imoveis', con=connection, if_exists='append', index=False)
                    print(f"{len(novos_df)} novos registros inseridos no banco.")
                else:
                    print("Nenhum novo registro para inserir (todos já estavam no banco).")

        except Exception as e:
            print("Erro ao inserir no banco:", e)



df = buscar_imoveis(tipo_operacao="VENDA", tipo_imovel="APARTAMENTO", localizacao="DF", cidade = "AGUAS CLARAS", bairro ="SUL", quartos="", preco_medio="3000000", palavra_chave ="")
salvar_imoveis(df, False, True)
