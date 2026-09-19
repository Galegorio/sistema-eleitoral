# 🗳️ Sistema Eleitoral em Python com Tkinter

Projeto de um sistema de votação desenvolvido em **Python**, com interface gráfica em **Tkinter** e persistência de dados utilizando **SQLite**.

> Projeto desenvolvido com foco em estudo, prática, aprendizado de banco de dados e construção de portfólio.

---

## 📌 Sobre

A ideia deste projeto é desenvolver um **sistema eleitoral local simulado**, permitindo identificar eleitores, registrar votos e consultar os resultados da votação.

O projeto está sendo desenvolvido de forma incremental, dividido em etapas:

1. **Fase 1 — Funcionalidades básicas**

   * Estrutura inicial do sistema
   * Identificação do eleitor
   * Seleção de candidatos
   * Votos em branco e nulos
   * Confirmação do voto
   * Apuração básica

2. **Fase 2 — Banco de dados**

   * Integração com SQLite
   * Armazenamento de candidatos
   * Armazenamento de eleitores
   * Armazenamento dos votos
   * Bloqueio de votação duplicada
   * Persistência dos resultados

3. **Fase 3 — Refinamento**

   * Melhorias na interface
   * Organização do código
   * Melhorias de validação
   * Novos recursos

---

## 🚀 Tecnologias

* **Python 3**
* **Tkinter** — interface gráfica
* **SQLite3** — banco de dados
* **SQL** — criação e consulta das tabelas

---

## ⚙️ Funcionalidades atuais

### Identificação do eleitor

* [x] Solicitação de identificação
* [x] Identificação com apenas números
* [x] Bloqueio de espaços na identificação
* [x] Identificação com no mínimo 6 dígitos
* [x] Bloqueio de identificação já utilizada

### Votação

* [x] Exibição dos candidatos
* [x] Seleção de candidato
* [x] Voto em branco
* [x] Voto nulo
* [x] Tela de confirmação
* [x] Possibilidade de corrigir a escolha antes da confirmação
* [x] Registro do voto no banco de dados

### Apuração

* [x] Contagem de votos por candidato
* [x] Contagem de votos brancos
* [x] Contagem de votos nulos
* [x] Cálculo do percentual de votos
* [x] Exibição do total de votos
* [x] Identificação do vencedor
* [x] Identificação de empate

### Banco de dados

* [x] Criação automática do banco SQLite
* [x] Tabela de candidatos
* [x] Tabela de eleitores
* [x] Tabela de votos
* [x] Persistência dos dados após fechar o programa

---

## 📂 Estrutura atual

```text
sistema-eleitoral/
├── main.py
├── banco.py
├── eleicoes.db
└── README.md
```

### 📄 `main.py`

Responsável pela execução do sistema e pela interface gráfica desenvolvida com Tkinter.

Contém, entre outras partes:

* telas do sistema;
* identificação do eleitor;
* seleção do voto;
* confirmação;
* exibição dos resultados.

### 📄 `banco.py`

Responsável pela comunicação com o banco de dados SQLite.

Contém funções para:

* conectar ao banco;
* criar as tabelas;
* inserir candidatos;
* consultar candidatos;
* verificar se um eleitor já votou;
* cadastrar eleitores;
* registrar votos;
* contar votos;
* contar votos brancos e nulos.

### 🗄️ `eleicoes.db`

Arquivo do banco de dados SQLite utilizado pelo sistema.

Armazena os dados das tabelas:

* `candidatos`
* `eleitores`
* `votos`

> O arquivo é criado automaticamente pelo programa caso ainda não exista.

### 📄 `README.md`

Documentação do projeto.

---

## 🗃️ Banco de dados

O projeto utiliza **SQLite** para armazenar os dados da votação.

### Tabela `candidatos`

Armazena os candidatos cadastrados no sistema.

Principais informações:

* `id`
* `numero`
* `nome`

### Tabela `eleitores`

Armazena as identificações dos eleitores que já participaram da votação.

Principais informações:

* `id`
* `identificacao`

A identificação é única, impedindo que a mesma identificação seja cadastrada novamente.

### Tabela `votos`

Armazena os votos registrados.

Principais informações:

* `id`
* `eleitor_id`
* `candidato_numero`
* `tipo`

O campo `tipo` diferencia:

* `candidato`
* `branco`
* `nulo`

---

## ▶️ Como executar

### 1. Verifique se o Python está instalado

No terminal:

```bash
python --version
```

### 2. Execute o programa

Dentro da pasta do projeto:

```bash
python main.py
```

O banco de dados `eleicoes.db` será criado automaticamente caso ainda não exista.

---

## 🧪 Testes realizados

Durante o desenvolvimento, o sistema foi testado para verificar:

* identificação válida e inválida;
* identificação duplicada;
* votação para candidatos;
* voto branco;
* voto nulo;
* confirmação e cancelamento da votação;
* contagem dos votos;
* cálculo dos percentuais;
* identificação do vencedor;
* persistência dos dados após fechar e abrir o programa novamente.

---

## 🎯 Objetivos de aprendizado

Este projeto está sendo desenvolvido para praticar:

* lógica de programação;
* programação orientada a objetos;
* Python;
* criação de interfaces gráficas com Tkinter;
* SQL;
* SQLite;
* operações CRUD;
* organização de código;
* persistência de dados;
* desenvolvimento incremental de software.

---

## 🔮 Próximas etapas

### Fase 3 — Refinamento

* [ ] Melhorar a interface gráfica
* [ ] Organizar melhor os elementos da interface
* [ ] Melhorar mensagens e validações
* [ ] Revisar a organização do código
* [ ] Adicionar melhorias de usabilidade

### Futuras possibilidades

* [ ] Login de administrador
* [ ] Exportação dos resultados
* [ ] Relatórios de votação
* [ ] Criação de versão web
* [ ] Utilização de Flask ou FastAPI
* [ ] Integração com dados públicos de eleições para fins de estudo

---

## ⚠️ Aviso

Este projeto é uma **simulação educacional** desenvolvida para fins de estudo e portfólio.

Ele **não foi desenvolvido para utilização em eleições reais** e não deve ser utilizado como sistema eleitoral oficial.

---

## 📌 Status

🚧 **Em desenvolvimento**

**Fase 1 — Funcionalidades básicas:** ✅ Concluída

**Fase 2 — Banco de dados SQLite:** ✅ Concluída

**Fase 3 — Refinamento:** ⏳ Próxima etapa

