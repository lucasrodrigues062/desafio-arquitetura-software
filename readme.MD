
# Solução

Aluno: Lucas Rodrigues

## Entidades
    
### Customers (Clientes)

entidade composta pelas seguintes propriedades
- id (Inteiro, Chave Primária)
- name (String)
- email (String, unique)
- phone_number  (String)
- address = (String)
- deleted = (Boolean)

## Funcionalidades

Deverão ser disponibilizadas seguindo padrão RESTful com combinação de verbos HTTP (GET, POST, PUT, PATCH, DELETE) e padrões de URL

### Endpoints

Caso prefira pode baixar o arquivo de especificação OpenApi [Aqui](https://github.com/lucasrodrigues062/desafio-arquitetura-software/blob/main/docs/OpenApi.json)

#### POST /api/v1/customers - Criação de Cliente

Request
```
{
  "name": "string",
  "email": "user@example.com",
  "phone_number": "string",
  "address": "string"
}
```

Response - 201
```
{
  "id": 0,
  "name": "string",
  "email": "user@example.com",
  "phone_number": "string",
  "address": "string"
}
```

#### GET /api/v1/customers - Consulta de Clientes

- Possibilidade de uso de query parameter `name`. Quando informado a aplicação só irá retornar registros com o nome informado

Response - 200
```
[
  {
    "id": 0,
    "name": "string",
    "email": "user@example.com",
    "phone_number": "string",
    "address": "string"
  }
]
```
Response - 404
```
{
  "detail": "Customer not found"
}
```

#### GET /api/v1/customers/{customer_id} - Consulta de Cliente por id

- deve ser informado a `PATH VARIABLE` `customer_id`

Response - 200
```
  {
    "id": 0,
    "name": "string",
    "email": "user@example.com",
    "phone_number": "string",
    "address": "string"
  }

```
Response - 404
```
{
  "detail": "Customer not found"
}
```

#### PATCH /api/v1/customers/{customer_id} - Atualiza dados do cliente

- deve ser informado a `PATH VARIABLE` `customer_id`. campos que não devem ser atualizados, não devem ser informados

Request
```
{
  "name": "string",
  "phone_number": "string",
  "address": "string"
}
```
Response - 200
```
  {
    "id": 0,
    "name": "string",
    "email": "user@example.com",
    "phone_number": "string",
    "address": "string"
  }

```
Response - 404
```
{
  "detail": "Customer not found"
}
```


#### DELETE /api/v1/customers/{customer_id} - Exclui dados do cliente

- deve ser informado a `PATH VARIABLE` `customer_id`.
- Aplicação faz um "soft delete", somente alterando o status do cliente para deletado. Entretanto, o cliente não é retornado em nenhuma busca 

Response - 200
```
  {}

```
Response - 404
```
{
  "detail": "Customer not found"
}
```

#### GET /api/v1/count/customers - Consulta contagem de clientes


Response - 200
```
{
  "customers_quantity": 0
}
```

### Persistência de dados

Banco de dados escolhido foi o SqLite devido a sua praticidade de implementação

### Implementação

Escolhido a linguagem Python com o "framework" FastApi. A decisão aqui foi somente aprender uma nova tecnologia

### Arquitetura da solução

Foi utilizado o padrão MVC (Model View Control) em quase a sua totalidade, visto que não temos nada para "mostrar" ao consumidor da API então as respostas ficaram diretamente na camada "Controller"

![Estrutura de pastas](https://github.com/lucasrodrigues062/desafio-arquitetura-software/blob/main/docs/img/estrutura-de-pastas.jpg)

1. root - raíz do monorepo
   1. model - camada de domínio. Contém regras de negócio da aplicação.
      1. entities - entidades do domínio
      2. services - Regras de negócio da aplicação
   2. configuration - Módulo com configurações inerentes a infra e tecnologias utilizadas
   3. controller - Módulo responsável pelos pontos de entrada da aplicação 
      1. schemas - Contém os nossos módelos de validação também conhecido como "DTO"
      2. customer-controller.py - Contém os endpoints da API
               

#### Controller

Responsável por fazer a comunicação entre os adaptadores externos (endpoints) e a camada de domínio (model)

```
@customer_router.post('/api/v1/customers', tags=["customer"],  status_code=status.HTTP_201_CREATED, include_in_schema=True, response_model=CustomerView)
def create(customer: CustomerCreate):
    return create_customer(customer)

@customer_router.patch('/api/v1/customers/{customer_id}', tags=["customer"],  status_code=status.HTTP_200_OK, include_in_schema=True, response_model=CustomerView)
def update(customer_id: int, customer: CustomerUpdate):
    return update_customer(customer, customer_id)


@customer_router.get('/api/v1/customers/{customer_id}', tags=["customer"],  status_code=status.HTTP_200_OK, include_in_schema=True, response_model=CustomerView)
def get_by_id(customer_id: int):
    return get_customer_by_id(customer_id)

@customer_router.get('/api/v1/customers', tags=["customer"],  status_code=status.HTTP_200_OK, include_in_schema=True, response_model=list[CustomerView])
def get(name: str | None = None):
    if name is not None:
        return get_customer_by_name(name)
    return get_customers()

@customer_router.get('/api/v1/count/customers', tags=["customer"],  status_code=status.HTTP_200_OK, include_in_schema=True, response_model=CustomerCount )
def count():
    return count_customers()

@customer_router.delete('/api/v1/customers/{customer_id}', tags=["customer"],  status_code=status.HTTP_200_OK, include_in_schema=True )
def delete(customer_id: int):
    return delete_customer(customer_id)
```

#### Service

Responsável por toda a nossa regra de négocio

```
def create_customer(cliente: CustomerCreate):
    with Session(engine) as db:
        db_cliente = Customer(name=cliente.name, email=cliente.email, phone_number=cliente.phone_number, address=cliente.address)
        db.add(db_cliente)
        db.commit()
        db.refresh(db_cliente)
        return db_cliente

def update_customer(cliente: CustomerUpdate, customer_id: int):
    with Session(engine) as db:
        customer = db.get(Customer, customer_id)
        if not customer or customer.deleted == True:
            raise HTTPException(status_code=404, detail="Customer not found")
        if cliente.address is not None:
            customer.address = cliente.address
        if cliente.phone_number is not None:
            customer.phone_number = cliente.phone_number
        if cliente.name is not None:
            customer.name = cliente.name
        db.add(customer)
        db.commit()
        db.refresh(customer)
        return customer

def get_customer_by_id(customer_id: int):
    with Session(engine) as db:
        customer = db.get(Customer, customer_id)
        if not customer or customer.deleted == True:
            raise HTTPException(status_code=404, detail="Customer not found")
        return customer

def get_customers():
    with Session(engine) as db:
        customers = db.query(Customer).filter(Customer.deleted == False).all()
        return customers

def count_customers():
    with Session(engine) as db:
        customers = db.query(Customer).filter(Customer.deleted == False).all()
        print(len(customers))
        return CustomerCount(customers_quantity=len(customers))

def get_customer_by_name(name: str):
    with Session(engine) as db:
        customer = db.query(Customer).filter(Customer.name == name).filter(Customer.deleted == False).first()
        if not customer:
            raise HTTPException(status_code=404, detail="Customer not found")
        return customer

def delete_customer(customer_id: int):
    with Session(engine) as db:
        customer = db.get(Customer,customer_id)
        if not customer:
            raise HTTPException(status_code=404, detail="Customer not found")
        customer.deleted = True
        db.add(customer)
        db.commit()
        db.refresh(customer)
        return
```

### C4 Model

Caso prefira o arquivo draw.io ele pode ser baixado [aqui](https://github.com/lucasrodrigues062/desafio-arquitetura-software/blob/main/docs/c4model.xml)

Nível 1
![C4 de Nível 1](https://github.com/lucasrodrigues062/desafio-arquitetura-software/blob/main/docs/c4/c4-1.jpg)

Nível 3
![C4 de Nível 3](https://github.com/lucasrodrigues062/desafio-arquitetura-software/blob/main/docs/c4/c4-3.jpg)
