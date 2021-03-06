# Check File

Projeto para a disciplina de Cloud Computing da Universidade Federal do Ceará.

Esse projeto consiste em uma implementação de um servidor, com API REST, utilizando `Django` e `Django Rest Framework`, que terá como propósito servir e encapsular regras de negócio para um cliente especificado [nesse outro repositório](https://github.com/pyduh/cloud-check-file.front).


## Instalação

Há duas formas de preparar o ambiente dessa aplicação: utilizando o [Docker Compose](https://docs.docker.com/compose/) ou instalando manualmente as dependências e iniciando manualmente o serviço.

Sempre será necessário a configuração de um arquivo de variáveis de ambiente, `.env`. 


### Docker Compose

Para iniciar o projeto utilizando essa ferramenta, verifique se ela já se encontra [devidamente instalada](https://docs.docker.com/get-docker/). Depois, garanta que o repositório da [aplicação cliente](https://github.com/pyduh/cloud-check-file.front) esteja devidamente clonado. Copie o arquivo `local.env` para um arquivo `.env` e o preencha devidamente, adicionando as credenciais de acesso para o provedor escolhido.

Execute, então:

```
$ docker-compose up
```

E entre, com seu navegador, no seguinte endereço `http://localhost:8080` para ter acesso ao sistema.


### Instalação Manual

Para fazer a instalação das dependências desse projeto, aconselho a utilização de alguma biblioteca para isolar ambientes virtuais, como o [virtualenv](https://pypi.org/project/virtualenv/). Para instalar as dependências, execute:

```
$ pip install -r requirements.txt
$ cd cloud_check_file
$ python manage.py migrate
$ python manage.py runserver
```

Essa série de instruções será responsável por instanciar um servidor de desenvolvimento. Essa aplicação não é a responsável por servir o seu [cliente](https://github.com/pyduh/cloud-check-file.front). Verifique no README desse projeto como inicializá-lo


## Autores

**Eduardo Neto** 
