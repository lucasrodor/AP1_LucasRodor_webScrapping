# 🏘️ Projeto: Scraper de Imóveis - DFImóveis

Este projeto realiza a **coleta automática de imóveis à venda** no portal [DFImoveis.com.br](https://www.dfimoveis.com.br), usando **Selenium + Pandas**, trata os dados com expressões regulares e salva os resultados em:
- ✅ Um arquivo Excel
- ✅ Um banco de dados MySQL

Esse projeto foi um avaliação da disciplina Projeto em Ciência de Dados II do curso 
Ciência de Dados & Inteligência Artificial | IBMEC - DF, Ministrada pelo professor [Laerte Jun Takeuti](https://www.linkedin.com/in/laertejt/)
---


## 🧑‍💻 Autor

Desenvolvido por **Lucas Rodor**:
-Linkedin: [Lucas Rodor](https://www.linkedin.com/in/lucasrodor)
-Github: [Lucas Rodor](https://www.github.com/lucasrodor)

## 🚀 Tecnologias utilizadas

- Python 3.10+
- Selenium
- Pandas
- re (expressões regulares)
- SQLAlchemy
- MySQL + pymysql
- python-dotenv
- openpyxl

---

## 📦 Funcionalidades

- 🧭 Filtra imóveis por:
  - Tipo de operação (ex: venda)
  - Tipo de imóvel (ex: apartamento)
  - Localização, cidade, bairro
  - Número de quartos
  - Preço médio
  - Palavra-chave (endereço ou empreendimento)

- 📄 Extrai:
  - Título, preço, endereço
  - Detalhes (como tamanho, número de quartos, vagas, suítes, plantas)
  - Descrição do anúncio
  - Link direto

- 🧹 Trata os dados:
  - Normaliza acentuação
  - Remove duplicatas
  - Extrai detalhes com regex (área, quartos etc.)

- 💾 Salva:
  - Em Excel com timestamp
  - No banco de dados MySQL, **apenas registros novos**

---

## ⚙️ Como rodar

### 1. Clone o repositório

```bash
git clone https://github.com/seu-usuario/imoveis-scraper.git
cd imoveis-scraper
```

### 2. Instale os pacotes

```bash
pip install -r requirements.txt
```

### 3. Crie o arquivo `.env` com suas credenciais do MySQL

```
MYSQL_USER=root
MYSQL_PASSWORD=sua_senha_aqui
```

### 4. Crie o banco de dados e a tabela:

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

## 🧠 Exemplos de uso no código

```python
df = buscar_imoveis(
    tipo_operacao="VENDA",
    tipo_imovel="APARTAMENTO",
    cidade="AGUAS CLARAS",
    bairro="SUL",
    preco_medio="3000000"
)

salvar_imoveis(df, salvar_excel=True, salvar_mysql=True)
```

---

## 📂 Estrutura do projeto

```
├── main.py
├── requirements.txt
├── .env
```

---

## 📌 Observações

- O script usa o navegador Chrome, então você deve ter o **Google Chrome** e o **ChromeDriver** compatível instalados.
- Se quiser rodar em modo invisível, descomente a linha `options.add_argument("--headless")`.

---