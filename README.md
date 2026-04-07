# Sistema de Votação Eletrônica
# Descrição 
Este projeto consiste no desenvolvimento de um sistema de votação eletrônica, capaz de organizar o processo da votação, desde o cadastro de novos eleitores e candidatos até o registro e apuração dos votos.

O sistema foi projetado com foco em segurança e organização.
# Funcionalidades
## Gerenciamento
-Cadastro de eleitores


-Validação de CPF e título de eleitor


-Criação da chave de acesso


-Update e Delete de eleitores


-Cadastro de candidatos


-Listagem e busca de dados

## Módulo de Votação
-Abertura da votação por mesário


-Zerézima


-Identificação do eleitor


-Registro de voto


-Protocolo de Votação


-Controle de voto único

## Resultados
-Boletim da urna


-Apuração dos votos


-Votos por partido

## Auditória
-Registro de logs do sistema


-Exibição de eventos (abertura, erros, votos, encerramento)


-Validação de integridade

## Integrantes (Grupo 1-2)
-Eduardo Martins Colmati

-Enzo Carleti Teixeira

-Gustavo de Oliveira de Santana

-José Gabriel Bedani


## Tecnologias Utilizadas
-Python 3.14

-MySQL

-MySQL Connector-Python

-Datetime

-Git

-Github


## Segurança e Criptografia
Nosso sistema,a partir da Cifra De Hill, utiliza da criptografia para proteger dados sensíveis, como:

-CPF dos Eleitores

-Chave de acesso

-Protocolo de votação

# Como executar nosso sistema
## Pré-Requisitos
- Python 3.14
- MySQL instalado e configurado
- mysql-connector-python
- datetime (biblioteca padrão do Python)
- Git
- GitHub

## Passo a Passo
1. No Github, clique em "Code", e faça o Download do projeto
2. Abra o VSCode ou PyCharm, clique em File > Open Folder, e selecione a pasta do projeto.
3. Abra o terminal dentro do VSCode ou PyCharm. Menu terminal > New Terminal, e digite: "pip install mysql-connector-python".
4. Abra o MySQL Workbench (ou outro gerenciador de banco de dados) e crie um banco de dados para o projeto (ex: sistema_votacao).
5. No código do projeto, localize as configurações de conexão com o banco de dados (host, user, password) e insira suas credenciais do MySQL.
6. Ainda no terminal do VSCode ou PyCharm, execute o sistema com o comando: "python main.py".
7. O sistema irá iniciar no terminal e estará pronto para uso.




