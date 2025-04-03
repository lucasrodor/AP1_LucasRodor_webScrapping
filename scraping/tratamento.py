import re
import unicodedata
from datetime import datetime

def normalizar(texto):
    texto = str(texto)
    texto = unicodedata.normalize('NFKD', texto).encode('ASCII', 'ignore').decode('ASCII')
    return texto.lower()

padrao = r'(\d+\s*(?:a\s*\d+)?)\s*(m2|quartos?|vagas?|suites?|plantas?)'

def extrair(detalhe, tipo_alvo):
    detalhe = normalizar(detalhe)
    matches = re.findall(padrao, detalhe)
    for valor, tipo in matches:
        if tipo_alvo in tipo:
            return valor.strip()
    return ''

def tratar_dataframe(df):
    df['preco'] = df['preco'].apply(
        lambda x: float(
            re.search(r'R\\$[\\s]*([\\d\\.\\,]+)', x).group(1).replace('.', '').replace(',', '.')
        ) if isinstance(x, str) and re.search(r'R\\$[\\s]*([\\d\\.\\,]+)', x) else None
    )

    df['detalhes'] = df['detalhes'].fillna('').apply(lambda x: x.replace('\\n', ',  '))
    df['tamanho']  = df['detalhes'].apply(lambda x: extrair(x, 'm2'))
    df['quartos']  = df['detalhes'].apply(lambda x: extrair(x, 'quarto'))
    df['vagas']    = df['detalhes'].apply(lambda x: extrair(x, 'vaga'))
    df['suites']   = df['detalhes'].apply(lambda x: extrair(x, 'suite'))
    df['plantas']  = df['detalhes'].apply(lambda x: extrair(x, 'planta'))

    return df
