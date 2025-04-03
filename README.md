# 🏘️ Scraper de Imóveis - DFImóveis | Lucas Rodor

Este projeto realiza a **coleta automática de imóveis à venda** no portal [DFImoveis.com.br](https://www.dfimoveis.com.br), usando **Selenium + Pandas**, trata os dados com expressões regulares e salva os resultados em:

- ✅ Um arquivo Excel (com timestamp)
- ✅ Um banco de dados MySQL (**apenas novos registros**, evitando duplicatas)

Esse projeto foi uma avaliação da disciplina Projeto em Ciência de Dados II do curso Ciência de Dados & Inteligência Artificial | IBMEC - DF, ministrada pelo professor [Laerte Jun Takeuti](https://www.linkedin.com/in/laertejt/)

---
## 👤 Autor

Desenvolvido por **Lucas Rodor**:
- [LinkedIn](https://www.linkedin.com/in/lucasrodor)
- [GitHub](https://github.com/lucasrodor)
---

## 🧠 Principais funcionalidades

- 🧭 Filtra imóveis por:
  - Tipo de operação (ex: venda)
  - Tipo de imóvel (ex: apartamento)
  - Localização, cidade, bairro
  - Número de quartos
  - Preço médio
  - Palavra-chave (endereço ou empreendimento)

- 📄 Extrai:
  - Título, preço, endereço
  - Detalhes (tamanho, quartos, vagas, suítes, plantas)
  - Descrição do anúncio
  - Link do imóvel

- 🧹 Trata os dados:
  - Normaliza acentuação
  - Extrai dados estruturados dos detalhes usando Regex
  - Preenche campo `data_extracao` com timestamp

- 💾 Salva:
  - Em planilha Excel (pasta `/data`)
  - Em banco de dados MySQL (**evitando duplicatas via link**)

---

## 🚀 Tecnologias utilizadas

- Python 3.10+
- Selenium
- Pandas
- SQLAlchemy
- PyMySQL
- python-dotenv
- openpyxl
- re (regex)

---

## 📦 Estrutura do projeto

```
├── main.py
├── scraping/
│   ├── navegador.py
│   ├── filtros.py
│   ├── extrator.py
│   └── tratamento.py
├── utils/
│   ├── banco.py
│   └── excel.py
├── data/                # arquivos Excel salvos
├── .env
├── README.md
└── requirements.txt
```

---

## ⚙️ Como rodar localmente

### 1. Clone o repositório
```bash
git clone https://github.com/lucasrodor/AP1_LucasRodor_webScrapping.git
cd AP1_LucasRodor_webScrapping
```

### 2. Instale as dependências
```bash
pip install -r requirements.txt
```

### 3. Crie um arquivo `.env` com suas credenciais do MySQL:
```
MYSQL_USER=seu_usuario
MYSQL_PASSWORD=sua_senha
```

### 4. Configure o banco de dados e tabela
```sql
CREATE DATABASE db_imoveis;
USE db_imoveis;

CREATE TABLE imoveis (
    id INT AUTO_INCREMENT PRIMARY KEY,
    titulo VARCHAR(255),
    preco DECIMAL(15,2),
    endereco VARCHAR(255),
    detalhes TEXT,
    descricao TEXT,
    link VARCHAR(500) UNIQUE,
    tamanho VARCHAR(20),
    quartos VARCHAR(20),
    vagas VARCHAR(20),
    suites VARCHAR(20),
    plantas VARCHAR(20),
    data_extracao DATETIME
);
```

### 5. Execute o script
```bash
python main.py
```

---

## ✅ Exemplo de uso no código
```python
from scraping.navegador import iniciar_navegador
from scraping.filtros import aplicar_filtros
from scraping.extrator import extrair_dados
from scraping.tratamento import tratar_dataframe
from utils.banco import salvar_mysql
from utils.excel import salvar_excel

# pipeline manual
navegador = iniciar_navegador()
aplicar_filtros(navegador, tipo_operacao="VENDA", tipo_imovel="APARTAMENTO", cidade="AGUAS CLARAS")
df = extrair_dados(navegador)
navegador.quit()

df = tratar_dataframe(df)
salvar_excel(df)
salvar_mysql(df)
```

---


---

## 📌 Observações
- O script usa o navegador Chrome. Certifique-se de ter o **Google Chrome** e o **ChromeDriver** compatível instalados.
- Para rodar em modo invisível (sem abrir o navegador), ative a opção `headless=True` ao chamar `iniciar_navegador()`.

