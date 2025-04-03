<h1 align="center"> Project_Wallet_API </h1>

<p align="center">
<a href="#-prévia">Prévia</a>&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;
  <a href="#-objetivo">Objetivo</a>&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;
  <a href="#-pré-requisitos">Instalação</a>&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;
  <a href="#️-apis">APIs</a>&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;
  <a href="#-dbeaver---postgresql">Banco de Dados</a>&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;
  <a href="#-docker">Docker</a>&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;
  <a href="#-conclusão">Conclusão</a>&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;
  <a href="#licença">Licença</a>
</p>



### 📷 Prévia


![image](https://github.com/user-attachments/assets/43c6ae1e-8ea0-4a45-ab2e-193c406a058b)



### 🎯 Objetivo

O objetivo deste projeto, desenvolvido em resposta ao desafio proposto, foi demonstrar proficiência em desenvolvimento backend, seguindo rigorosamente as diretrizes estabelecidas. A API Wallet foi construída utilizando o framework Django em Python e PostgreSQL, como solicitado, com foco na implementação de autenticação segura via JWT, aderência aos padrões RESTful e organização clara do código. Além disso, foram incluídas funcionalidades essenciais como criação de usuários, gestão de saldos de carteira e transferências entre usuários, com a opção de filtrar transações por período. O projeto buscou não apenas cumprir os requisitos básicos, mas também incorporar boas práticas de segurança, arquitetura limpa e documentação abrangente, visando a entrega de uma solução robusta e de alta qualidade.


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

1. Executar os testes na aplicação `accounts`:
    ```python
    python manage.py test accounts
    ```
2. Executar os testes na aplicação `wallets`:
    ```python
    python manage.py test wallets
   ```

#### 🗺️ APIs

Este guia detalhado irá te mostrar como usar a API de Carros e Marcas, desde a autenticação até a realização de operações com carros e marcas.

🔐 Autenticação - JWT
 
 Antes de começarmos a interagir com a API, precisamos obter um token de acesso JWT (JSON Web Token). Esse token é como uma chave que garante que você tenha permissão para acessar os recursos protegidos da API.

 | **Método**   | **Endpoint** | **Descrição** |  **Autenticação** |
|------------|-----------|------------------|------------------|
| POST       |  `/api/v1/accounts/login` | Realizar login   |  NÃO  |
|  POST | `/api/v1/accounts/register/`   | Registar na plataforma   |  NÃO |
| POST     | `/api/v1/accounts/token/refresh/`   | Obter access_token |  NÃO |
|  POST | `/api/v1/accounts/token/verify/`   | Verificar se já expirou o access_token  | NÃO  |


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
  "jti": "e4f550ee0e1840269813f25e55c2b2e5",
  "user": {
    "id": 1,
    "email": "user@example.com"
  }
}
```

_Lembre-se_:

- O token JWT tem validade de um dia e duração de 30 minutos. Após esse período, você precisará renová-lo usando o endpoint `POST /api/accounts/token/refresh/`.
- Você pode verificar se o token expirou usando o endpoint POST `/api/accounts/token/verify/`

🪪 Wallet Endpoint 

 | **Método**   | **Endpoint** | **Descrição** |  **Autenticação** |
|------------|-----------|------------------|------------------|
| GET       |  `/api/v1/wallets/` | Listar somente a carteira    |  SIM  |
|  GET | `/api/v1/wallets/:id/`   | Obter com ID a carteira   |  SIM |
| POST     | `/api/v1/wallets/`   | Criar novo carteira |  SIM |
|  PUT | `/api/v1/wallets/:id/`   | Atualizar registro completo do carteira   | SIM  |
| PATCH     | `/api/v1/wallets/:id`   | Atualização parcial | SIM  |
| DELETE     | `/api/v1/wallets/:id/`   | Deleta registro do carteira | SIM  |

Necessita está autenticado para acessar os endpoints. Pois o retorno da resposta status (401 Unauthorized).

```
{
    "detail": "As credenciais de autenticação não foram fornecidas."
}
```

Etapas: 

1. Crie uma carteira:
Endpoint: `POST /api/v1/wallets/`
    ```
    {
      "balance": "7445.95"
    }
    ```
    Sucesso da resposta (201 Created)
    ```
    {
        "id": 1,
        "user_email": "dev@mail.com",
        "balance": "7445.95",
        "created_at": "2025-04-03T09:29:58.742892-03:00",
        "updated_at": "2025-04-03T09:29:58.742938-03:00"
    }
    ```
2. Listar as informações da carteira ou passando o ID especifico da carteira do usuário. 

    Endpoints: `GET /api/v1/wallets/` status (200 OK)

    ```
    {
    "count": 1,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": 1,
            "user_email": "dev@mail.com",
            "balance": "7445.95",
            "created_at": "2025-04-03T09:29:58.742892-03:00",
            "updated_at": "2025-04-03T09:29:58.742938-03:00"
        }
      ]
    }

    ```

    Endpoint: `GET /api/v1/wallets/:id/`, id = 1, status (200 OK)
    
    ```
    {
    "id": 1,
    "user_email": "dev@mail.com",
    "balance": "7445.95",
    "created_at": "2025-04-03T09:29:58.742892-03:00",
    "updated_at": "2025-04-03T09:29:58.742938-03:00"
    }
    ```
3. Atulizar total metodo PUT ou Parcial PATCH a informação da carteira.

    Endpoint: `PUT /api/v1/wallets/:id/`, id = 1
    ```
    {
    "balance": "20591.34"
    }
    ```
    Sucesso da resposta (200 OK)
    ```
    {
    "id": 1,
    "user_email": "dev@mail.com",
    "balance": "20591.34",
    "created_at": "2025-04-03T09:29:58.742892-03:00",
    "updated_at": "2025-04-03T09:40:41.614292-03:00"
    }
    ```

4. Delata o registro da carteira

    Endpoint: `DEL /api/v1/wallets/:id/`, id = 6, passar um ID que não é sua carteira, retornará com mensagem.

    ```
    {
    "detail": "Você não tem permissão para deletar esta carteira."
    }
    ```
    
    Agora se passar o id = 1, a resposta (204 No Content)


🔁 Transaction Endpoint 

 | **Método**   | **Endpoint** | **Descrição** |  **Autenticação** |
|------------|-----------|------------------|------------------|
| GET       |  `/api/v1/transactions/` | Listar somente a transição    |  SIM  |
|  GET | `/api/v1/transactions/:id/`   | Obter com ID a transição   |  SIM |
| POST     | `/api/v1/transactions/`   | Criar novo transição |  SIM |
|  PUT | `/api/v1/transactions/:id/`   | Atualizar registro completo do transição   | SIM  |
| PATCH     | `/api/v1/transactions/:id`   | Atualização parcial | SIM  |
| DELETE     | `/api/v1/transactions/:id/`   | Deleta registro do transição | SIM  |

Necessita está autenticado para acessar os endpoints. Pois o retorno da resposta status (401 Unauthorized).

```
{
    "detail": "As credenciais de autenticação não foram fornecidas."
}
```

Etapas: 

1. Para realizar transferências entre usuários, cada um deve possuir uma carteira individual, e o remetente precisa estar autenticado com um token válido, garantindo a segurança e rastreabilidade da transação destinatário.
    
    Endpoint: `POST /api/v1/transactions/`
    ```
    {
    "receiver_wallet": 6,
    "amount": "138",
    "note": "Hello at Transaction"
    }
    ```
    Sucesso da resposta (201 Created)
    ```
    {
    "id": 51,
    "sender_wallet": 13,
    "sender_email": "dev@mail.com",
    "receiver_email": "fvieira@example.org",
    "receiver_wallet": 6,
    "amount": "138.00",
    "status": "completed",
    "timestamp": "2025-04-03T09:55:41.097555-03:00",
    "note": "Hello at Transaction"
    }
    ```
2. Listar as informações da carteira ou passando o ID especifico da carteira do usuário. 

    Endpoints: `GET /api/v1/transactions/` status (200 OK)

    ```
    {
    "count": 1,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": 1,
            "user_email": "dev@mail.com",
            "balance": "7445.95",
            "created_at": "2025-04-03T09:29:58.742892-03:00",
            "updated_at": "2025-04-03T09:29:58.742938-03:00"
        }
      ]
    }

    ```

    Endpoint: `GET /api/v1/transactions/:id/`, id = 51, status (200 OK)
    
    ```
    {
    "id": 51,
    "sender_wallet": 13,
    "sender_email": "dev@mail.com",
    "receiver_email": "fvieira@example.org",
    "receiver_wallet": 6,
    "amount": "138.00",
    "status": "completed",
    "timestamp": "2025-04-03T09:55:41.097555-03:00",
    "note": "Hello at Transaction"
    }
    ```
3. Use os métodos PUT ou PATCH para atualizar informações de transações existentes, especificando o `id` da transação no endpoint.

    Endpoint: `PUT /api/v1/transactions/:id/`, id = 51
    ```
    {
      "receiver_wallet": 3,
      "amount": "300",
      "note": "Good Morning"
    }
    ```
    Sucesso da resposta (200 OK)
    ```
    {
    "id": 51,
    "sender_wallet": 13,
    "sender_email": "dev@mail.com",
    "receiver_email": "gabrielly53@example.com",
    "receiver_wallet": 3,
    "amount": "300.00",
    "status": "completed",
    "timestamp": "2025-04-03T09:55:41.097555-03:00",
    "note": "Good Morning"
    }
    ```

    Obs.: Se o valor da transferência exceder o saldo da carteira do remetente, a transação será marcada como status "failed" e não será realizada.

    ```
    {
      "receiver_wallet": 2,
      "amount": "7000",
      "note": "Good"
    }
    ```
    Sucesso da resposta (200 OK)
    ```
    {
    "id": 51,
    "sender_wallet": 13,
    "sender_email": "dev@mail.com",
    "receiver_email": "fonsecajulia@example.com",
    "receiver_wallet": 2,
    "amount": "7000.00",
    "status": "failed",
    "timestamp": "2025-04-03T09:55:41.097555-03:00",
    "note": "Good"
    }
    ```

4. Delata o registro da carteira

    Endpoint: `DEL /api/v1/transactions/:id/`, id = 51
    
    A resposta (204 No Content)

🧩 Swagger e Redoc

A API de Carros e Marcas também oferece documentação interativa através do Swagger e do Redoc.

- Swagger: `http://localhost:8000/api/swagger`
- Redoc: `http://localhost:8000/api/redoc`


_Dica_: No Swagger, você pode simplesmente colar o access_token no campo "Authorize" sem precisar adicionar "Bearer" antes.


👨🏻‍🚀 Postman

Navegue até o diretório `Postman` para obter a coleção Postman, dentro do Postman no Import adicione a coleção `Wallet.postman_collection.json`. 

Estrutura da coleção:
```
Wallet
├── Accounts
│   ├── Login
|   ├── Register
|   ├── Refresh
│   └── Verify
├── Wallets
│   ├── List 
│   ├── Get Single
│   ├── Create
│   ├── Update
│   └── Delete
└── Transactions
    ├── List All
    ├── Get Single
    ├── Create
    ├── Update
    └── Delete
```

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

Melhorias

Para aprimorar ainda mais o sistema, planejo implementar o Celery ou RabbitMQ para processamento assíncrono de transações, melhorando o desempenho e a escalabilidade.Além disso, implementa controle de acesso baseado em roles, onde administradores têm acesso completo a todas as informações e usuários comuns só conseguem visualizar suas próprias carteiras e transações.


#### 📓 Conclusão

Este projeto implementa uma API robusta para gestão de carteiras e transações financeiras, com autenticação JWT e endpoints para criação, leitura, atualização e exclusão de carteiras e transações. O sistema garante a segurança das transações, exigindo autenticação para todas as operações e validando o saldo disponível antes de cada transferência. 

## Licença
[MIT License](LICENSE)
