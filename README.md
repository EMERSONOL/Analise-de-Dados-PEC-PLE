# 📊 Sistema de Análise de Dados PEC-G

## 📌 1. Introdução

O sistema de **Análise de Dados do Programa de Estudantes-Convênio de Graduação (PEC-G)** tem como objetivo **centralizar, organizar e visualizar** os dados 📂 dos alunos estrangeiros 🌎 participantes do programa, permitindo a extração de **relatórios 📑 e insights 💡** por meio de filtros 🎯, gráficos 📈 e operações manuais 🛠️.

---

## 🖥️ 2. Estrutura Geral do Sistema

### 🔹 2.1 Módulos Principais

O sistema é dividido em quatro módulos principais, acessíveis por meio de uma **barra de tarefas** 📌:

- 🏠 **Home** – Página inicial com visão geral e navegação rápida.  
- 🔑 **Login** – Controle de acesso para usuários autorizados.  
- 📊 **Análise de Dados** – Módulo central para visualização e tratamento dos dados.  
- 👤 **Perfil** – Área para gerenciamento do perfil e exibição de dados pessoais.  
- 📝 **Cadastro de Alunos** – Registro de novos alunos, incluindo **nome, email e data de nascimento**.  
  - O sistema verifica automaticamente a **primeira célula vazia** no Excel e insere os novos dados.  

---

## 🔍 3. Funcionalidades e Navegação

### 🔑 3.1 Login
- Entrada de **usuário** 👨‍💻 com validação 🔍.  
- Decisão de acesso:  
  - ✅ **Sim** → Acesso à área interna.  
  - ❌ **Não** → Permanência na tela de login.  

### 🏠 3.2 Home
- Informações ℹ️ sobre o projeto.  
- Navegação para outros módulos 📂.  
- Botão **Sair** 🚪 para encerrar sessão.  

### 📊 3.3 Análise de Dados
- 📂 **Base de dados**: Importação e preparação dos dados.  
- ✍️ **Entrada manual**: Inclusão de registros específicos.  
- 📅 Seleção por **ano** ou 🔎 busca por **aluno**.  
- 🧹 **Dados tratados**: Dados limpos e organizados.  
- 📋 **Tabela de dados**: Visualização com filtros.  
- 🎯 **Filtro**: Aplicar critérios para análises específicas.  
- 🗑️ **Exclusão de alunos**: Busca por aluno e remoção direta do registro.  
- 📑 **Relatório**: Geração automática baseada nos filtros.  

### 👤 3.4 Perfil
- 🖼️ **Foto de perfil** e dados pessoais.  
- 📋 **Tabela de dados** associada ao usuário.  
- 🛠️ **Operações manuais**: Edição e atualização de informações.  

### 📝 3.5 Cadastro de Alunos
- Inclusão de **nome, email e data de nascimento**.  
- Validação automática para não sobrescrever registros existentes.  
- Registro salvo no arquivo:  

## 🔄 4. Fluxo de Navegação
A navegação segue um fluxo lógico 🔀 com opções de:

- ⬅️ Voltar à **Home**  
- 👤 Ir para **Perfil**  
- 🚪 **Sair** do sistema  
- 🎯 Aplicar **Filtros** e gerar 📑 **Relatórios**  
- 📝 **Adicionar ou remover alunos** diretamente da base de dados  

---

## ✅ 5. Conclusão
O sistema de **Análise de Dados PEC-G** foi desenvolvido para oferecer **usabilidade, controle e eficiência**.  
Sua arquitetura modular permite **monitoramento e gestão estratégica** das informações, fortalecendo a administração acadêmica e promovendo uma análise detalhada dos dados dos alunos estrangeiros.  

---

## ⚙️ 6. Requisitos
Para rodar o projeto, instale as dependências:

```bash
pip install -r requirements.txt
