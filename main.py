from scraping.navegador import iniciar_navegador
from scraping.filtros import aplicar_filtros
from scraping.extrator import extrair_dados
from scraping.tratamento import tratar_dataframe
from utils.banco import salvar_mysql
from utils.excel import salvar_excel

def main():
    driver = iniciar_navegador()
    aplicar_filtros(driver, tipo_operacao="VENDA", tipo_imovel="APARTAMENTO",
                    localizacao="DF", cidade="AGUAS CLARAS", bairro="SUL",
                    quartos="", preco_medio="3000000", palavra_chave="")

    df = extrair_dados(driver)
    driver.quit()

    df = tratar_dataframe(df)

    #Opcionais, caso não queira é só comentar a linha
    salvar_excel(df)
    salvar_mysql(df)

if __name__ == "__main__":
    main()