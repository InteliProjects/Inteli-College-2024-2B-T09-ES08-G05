# Inteli - Instituto de Tecnologia e Liderança 

<p align="center">
<a href= "https://www.inteli.edu.br/"><img src="docs/assets/inteli.png" alt="Inteli - Instituto de Tecnologia e Liderança" border="0" width=40% height=40%></a>
</p>

<br>

# Arquitetura de software

## Grupo Ecto-One

## 👨‍🎓 Integrantes: 
- <a href="https://www.linkedin.com/in/breno-santana7/">Breno Santana</a>
- <a href="https://www.linkedin.com/in/claramohammad/">Clara Mohammad</a>
- <a href="https://www.linkedin.com/in/heitorprudente/">Heitor Prudente</a>
- <a href="https://www.linkedin.com/in/joselitojunior/">Joselito Carvalho</a>
- <a href="https://www.linkedin.com/in/paulapiva03/">Paula Piva</a>

## 👩‍🏫 Professores:
### Orientador(a) 
- Hermano Peixoto

### Instrutores
- Reginaldo Arakaki
- José Romualdo 
- Hermano Peixoto
- Francisco Escobar
- Geraldo Magela
- Lisane Valdo
- Ana Cristina dos Santos

## 📜 Descrição

# Descrição do projeto
 O projeto consiste em uma arquitetura de software para inspeção predial, desenvolvida para o Instituto de Pesquisas Tecnológicas (IPT), focada nos atributos de qualidade de software de integridade e disponibilidade. O objetivo é automatizar e centralizar o processo de inspeção de edificações, permitindo que os técnicos coletem, organizem e gerem relatórios de inspeção de forma mais segura. A solução proposta visa substituir o sistema manual atualmente utilizado pelo IPT, que apresenta limitações em termos de escalabilidade, rastreabilidade e integridade dos dados. Com a nova arquitetura, o parceiro poderá aumentar a produtividade, melhorar a qualidade dos relatórios e garantir a conformidade com normas e regulamentações do setor.

## 📁 Estrutura de pastas

```
(raiz do projeto)
├── docs
│   └── assets
|   └── README.md
├── src
│   └── backend
│       └── auth-api
│       └── database_manager
│       └── heartbeat
│       └── home
│       └── trend_model
├── README.md 
```

Dentre os arquivos e pastas presentes na raiz do projeto, definem-se:

- <b>docs</b>: aqui estão todos os documentos do projeto. Há também um arquivo README para o registro de cada artefato produzido.

- <b>src</b>: aqui estão os códigos fonte do projeto. A pasta backend contém os códigos relacionados ao backend da aplicação, como a API de autenticação, o gerenciador de banco de dados e o heartbeat.

- <b>README.md</b>: arquivo que serve como guia e explicação geral sobre o projeto (o mesmo que você está lendo agora).

## 🔧 Instalação

&emsp;&emsp;Para instalar o projeto exibido, primeiro clone o repositório utilizando `git clone https://github.com/Inteli-College/2024-2A-T09-ES08-G05`. Em seguida, navegue até a pasta do projeto e instale as dependências.

&emsp;&emsp;No backend, em cada um dos serviços, execute `pip install -r requirements.txt` para instalar as bibliotecas necessárias em cada serviço. Certifique-se de que o Python está instalado corretamente em sua máquina.

&emsp;&emsp;Após configurar as dependências, execute os serviços separadamente. Para isso execute:

- Para rodar o serviço de database_manager: `uvicorn manager:app --reload` na raiz do serviço
- Para rodar o auth_api, execute: `uvicorn app.main:app --reload` na raiz do serviço
- Para rodar o trend_model: `python -m backend.trend_model.run_model` na raiz do projeto
- Para rodar o heartbeat: `python heartbeat.py` na raiz do serviço
- Para rodar o main: `uvicorn app.main:app --reload` na raiz do serviço

## 🗃 Histórico de lançamentos
* 0.1.0 - 28/10/2024
    * Entendimento de negócios
* 0.2.0 - 08/11/2024
    * Simulações arquiteturais
* 0.3.0 - 22/11/2024
    * Desenvolvimento das táticas arquiteturais
* 0.4.0 - 06/12/2024
    *  Ajustes de implementação
* 0.5.0 - 19/12/2024
    * Entrega final

## 📋 Licença/License

Ecto-One by Inteli, Breno Santana, Clara Mohammad, Heitor Prudente, Joselito Carvalh and Paula Piva is licensed under <a href="http://creativecommons.org/licenses/by/4.0/?ref=chooser-v1" target="_blank" rel="license noopener noreferrer" style="display:inline-block;">Attribution 4.0 International<img style="height:22px!important;margin-left:3px;vertical-align:text-bottom;" src="https://mirrors.creativecommons.org/presskit/icons/cc.svg?ref=chooser-v1"><img style="height:22px!important;margin-left:3px;vertical-align:text-bottom;" src="https://mirrors.creativecommons.org/presskit/icons/by.svg?ref=chooser-v1"></a></p>
