# Project_Wallet_API
Projeto Wallet API


#### 💻 Pré-requisitos

Antes de começar, verifique se você atendeu aos seguintes requisitos:

- Python 
- Django
- Django REST Framework
- GIT 
- PostgreSQL
- Docker
- Docker Compose
- Postman (opcional)


#### 🛠️ Instalação

Faça o clone do projeto:
```bash
git clone git@github.com:pedro-hnrq/Project_Wallet_API.git
```

Após clonar o repositório acesse o diretório:
```bash
cd Project_Wallet_API
``` 

Crie uma maquina virtual  para rodar o projeto.

```python
python -m venv .venv
```
Uma vez criado seu ambiente virtual, você deve ativá-lo.

No Unix ou no MacOS, executa:

```bash
source .venv/bin/activate
```

No Windows, execute:

```bash
.venv\Scripts\activate.bat
```

Com o ambiente virtual ativo instale as dependências

```python
pip install -r requirements.txt
```

execute os comandos abaixo para criar arquivo de _variáveis de ambiente_ a partir de exemplos. (Lembre-se de modificá-los)

```bash
mv env .env
```

Na primeira vez é necessário executar esse comando para aplicar as migrações do banco de dados
```python
python manage.py migrate
```

Script de Popular Banco de Dados:

- Para popular o banco de dados com 10 usuários por padrão
    ```python
    python manage.py populate_db
    ```
- Para popular o banco de dados com 15 usuários execute o comando abaixo
    ```python
    python manage.py populate_db --users 15
    ```

Criando super usuário para acessar o painel administrativo
```python
python manage.py createsuperuser
```

Executando o Projeto
```python
python manage.py runserver
```

Linter - Flake8
```python
flake8
```

🧪 Teste Unitário 

```python
python manage.py test
```

#### 🗺️ APIs

Este guia detalhado irá te mostrar como usar a API de Carros e Marcas, desde a autenticação até a realização de operações com carros e marcas.

🔐 Autenticação - JWT
 
 Antes de começarmos a interagir com a API, precisamos obter um token de acesso JWT (JSON Web Token). Esse token é como uma chave que garante que você tenha permissão para acessar os recursos protegidos da API.

 Existem três maneiras de obter um token:

 1. Criar um usuário: Você pode criar um usuário diretamente pela API. 
 Endpoint: `POST /api/accounts/register`
    ```
      {
        "email": "user@example.com",
        "password": "your_password",
        "first_name": "John",
        "last_name": "Doe"
      }
    ```
    Sucesso da resposta (201 Created)
    ```
      {
        "email": "user@example.com",
        "first_name": "John",
        "last_name": "Doe"
      }
    ```

 2. Superusuário: Utilize o comando `python manage.py createsuperuser` no terminal para criar um superusuário com acesso total.
 3. Painel Admin: Acesse o painel de administração do Django e crie um usuário.

Após criar o usuário, você pode obter o token JWT usando login, fornecendo o email e a senha do usuário.

Endpoint: `POST /api/accounts/login`
```
{
    "email": "user@example.com",
    "password": "string"
}
```
Sucesso da resposta (200 OK)
```
{
  "access_token": "your_jwt_token",
  "refresh_token": "your_refresh_token",
  "type": "Bearer",
  "expiration_at": 1741130263,
  "issued_at": 1741043863,
  "user": {
    "id": 1,
    "email": "user@example.com"
  }
}
```

_Lembre-se_:

- O token JWT tem validade de um dia e duração de 60 minutos. Após esse período, você precisará renová-lo usando o endpoint `POST /api/accounts/token/refresh/`.
- Você pode verificar se o token expirou usando o endpoint POST `/api/accounts/token/verify/`



🧩 Swagger e Redoc

A API de Carros e Marcas também oferece documentação interativa através do Swagger e do Redoc.

- Swagger: `http://localhost:8000/api/swagger`
- Redoc: `http://localhost:8000/api/redoc`


_Dica_: No Swagger, você pode simplesmente colar o access_token no campo "Authorize" sem precisar adicionar "Bearer" antes.


👨🏻‍🚀 Postman


#### 🦫 Dbeaver | 🐘 PostgreSQL

Para visualizar as as tabelas no banco de dados no `PostgreSQL`, poderá usar a ferramenta `DBeaver Communty`, com as seguintes configurações: 

- Host: localhost
- Port: 5432
- Banco de dados: wallet
- Nome de usuário: dev
- Senha: Dev1234@


#### 🐋 DOCKER

Para facilitar a execução e o desenvolvimento da API REST, utilizamos o Docker para criar um ambiente isolado e consistente. Siga os passos abaixo para colocar a API para rodar em um contêiner:

1. Configurando o `.env`:

    Altere a variável `POSTGRES_HOST` de `localhost` para `db`.

2. Iniciando os Contêineres:

    ```bash
    docker compose up --build
    ```
3. Aplicando as Migrações:

    Após iniciar os contêineres, execute o seguinte comando para aplicar as migrações do banco de dados PostgreSQL:

    ```bash
    docker compose exec app python manage.py migrate
    ```
4. Criando um Superusuário:
    
    Para acessar o painel administrativo do Django, crie um superusuário com o seguinte comando:
    ```bash
    docker compose exec app python manage.py createsuperuser
    ```

5. Iniciando o Servidor de Desenvolvimento:

    Inicie o servidor de desenvolvimento do Django com o seguinte comando:

    ```bash
    docker compose exec app python manage.py runserver 0.0.0.0:8000
    ```

6. Outros Comandos Úteis:

    Para iniciar novamente:
    ```bash
    docker compose up -d
    ```
    Iniciar somente o Banco de Dados:

    ```bash
    docker compose up -d db
    ```

    Para poder **Parar** a aplicação no docker basta executar
    ```bash
    docker compose down
    ```