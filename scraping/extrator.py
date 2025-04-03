from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
import pandas as pd

def extrair_dados(driver):
    wait = WebDriverWait(driver, 10)
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

    return pd.DataFrame(lista_imoveis)
