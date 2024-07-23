# Product Recommendation System

Este projeto é um sistema de recomendação de produtos baseado em uma API web, utilizando dados de vendas de produtos. A recomendação é feita com base em dados de vendas e pode ser aprimorada em versões futuras para incluir dados de compras de usuários e autenticação.

Dentro do seguinte path: product_recomendation_system/db/analise_dados.ipynb tem uma breve análise dos dados


## Versão 0 (V.0)

### API
- **Framework:** FastAPI
- **Endpoint:** `GET /recommendation/{user_id}`
- **Descrição:** Retorna uma lista dos 5 produtos recomendados para o usuário com base nas vendas.

### Banco de Dados
- **Tipo:** CSV Estático
- **Arquivo:** `xpto_sales_products_mar_may_2024.csv`

### Algoritmo de Recomendação de Produto
- **Análise:** Processa e analisa o CSV de vendas.
- **Categorização:** Classificação de produtos por categoria.
- **Agrupamento:** Analise das vendas por dia da semana.

## Versão 1 (V.1)

### API
- **Autenticação:** Implementar autenticação de usuários para rotas personalizadas.

### Banco de Dados
- **Banco de Dados:** Migrar para um banco de dados relacional. Pode conter usuários e vendas consolidadas

### Algoritmo de Recomendação de Produto
- **Dados de Compras de Usuário:** Utilizar dados históricos de compras para recomendações personalizadas.

Segue imagem com o escopo do System Design iniciais do projeto:

![Alt text](/img/ProductRecommender.png?raw=true "Title")



## Ambiente de Desenvolvimento

### Pré-requisitos
Certifique-se de ter o Python 3.8 ou superior instalado.

### Instalação

1. **Clone o repositório:**

    ```bash
    git clone https://github.com/AAntunesNDS/product_recommendation_system.git
    cd product_recommendation_system
    ```

2. **Crie um ambiente virtual:**

    ```bash
    python -m venv venv
    source venv/bin/activate  # No Windows use `venv\Scripts\activate`
    ```

3. **Instale as dependências:**

    ```bash
    pip install -r requirements.txt
    ```

4. **Execute a aplicação:**

    ```bash
    uvicorn main:app --reload --host 0.0.0.0 --port 8000
    ```

    A documentação e o os usos da rotas estão  disponíveis em `http://127.0.0.1:8000/docs`.

![Alt text](/img/API.png?raw=true "Title")

## Docker

### Construir a Imagem

1. **Crie um arquivo `Dockerfile` no diretório raiz com o seguinte conteúdo:**

    ```dockerfile
    # Usar uma imagem base do FastAPI com Uvicorn e Gunicorn
    FROM tiangolo/uvicorn-gunicorn-fastapi:python3.9

    # Definir o diretório de trabalho
    WORKDIR /app

    # Copiar o arquivo de dependências
    COPY requirements.txt ./
    RUN pip install --no-cache-dir -r requirements.txt

    # Copiar o restante dos arquivos do projeto
    COPY . .

    # Definir o comando para iniciar a aplicação
    CMD ["uvicorn", "main:app", "--reload", "--host", "0.0.0.0", "--port", "80"]
    ```

2. **Construa a imagem Docker:**

    ```bash
    docker build -t produto-recomendacao .
    ```

3. **Execute o contêiner Docker:**

    ```bash
    docker run -d -p 80:80 produto-recomendacao
    ```

    A aplicação estará disponível em `http://localhost` no seu navegador.

## Versões futuras

Para versões futuras podem ser considerados Jobs que alimentem os bancos de dados para realizar predições mais precisas

Dependendo do número de requisições para api, também podem ser criados Load Balancers e/ou Filas de Mensageria, como SQS, para garantir que todas as requisições gerem resultados e sejam expostos em um endpoint separado.
