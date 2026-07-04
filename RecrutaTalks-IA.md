# Palestra sobre forças e fraquezas da IA: criação de ferramentas e agentes e ataques adversariais. RecrutaTalks Julho de 2026.
---
# Código: Chatbot Inteligente com LangChain + Ollama + Gradio

Um chatbot conversacional poderoso construído com **LangChain**, **Ollama** (modelos locais) e interface amigável com **Gradio**. Possui memória persistente, ferramentas (tools) e suporte a múltiplas conversas.

---

## ✨ Funcionalidades

- **Modelos locais** via Ollama (totalmente offline e privado)
- **Memória persistente** de conversas usando SQLite
- **Ferramentas integradas**:
  - `get_date` → Retorna a data atual
  - `Tavily Search` → Pesquisa na internet em tempo real
- Interface web moderna com **Gradio**
- Suporte a múltiplas sessões (thread_id)
- Histórico completo de mensagens (ReAct / Tool Calling)

---

## 🛠 Tecnologias Utilizadas

- **Python**
- **LangChain** / **LangGraph**
- **Ollama** (modelos locais)
- **Gradio** (interface)
- **SQLite** (memória persistente)
- **Tavily** (busca na web)
- **dotenv** (variáveis de ambiente)

---

## 📋 Pré-requisitos

- Python 3.10+
- [Ollama](https://ollama.com/) instalado e rodando
- Uma chave API do [Tavily](https://tavily.com) (opcional, mas recomendado)

---

## 🚀 Instalação

```bash
# 1. Clone o repositório
git clone https://github.com/gazstao/RecrutaTalks-IA
cd RecrutaTalks-IA

# 2. Crie o ambiente virtual
python -m venv .venv

# 3. Ative o ambiente
# Windows:
.\.venv\Scripts\activate
# Linux/Mac:
# source .venv/bin/activate

# 4. Instale as dependências
pip install --upgrade langchain langchain-core langgraph langchain-ollama langchain-community gradio python-dotenv tavily-python
```

---

## ⚙️ Configuração

1. Crie um arquivo `.env` na raiz do projeto:

```env
TAVILY_API_KEY=sua_chave_aqui
```

2. Baixe o modelo no Ollama:

```bash
ollama pull gemma3:12b     # ou qwen3.5:9b, llama3.2, etc.
```

---

## ▶️ Como Executar

```bash
python app.py
```

Acesse o link que aparecer no terminal (geralmente `http://127.0.0.1:7860`).

---

## 📁 Estrutura do Projeto

```
/
├── app.py                 # Arquivo principal
├── chatbot_memory.db      # Banco de memória (gerado automaticamente)
├── .env                   # Variáveis de ambiente
├── requirements.txt
└── README.md
```

---

## 📝 Exemplo de Uso

O assistente pode:
- Responder perguntas gerais
- Dizer a data atual
- Realizar pesquisas na internet quando necessário

**Exemplo de interação:**
- "Que dia é hoje?"
- "Qual a situação atual do mercado de criptomoedas?"
- "Me explique como funciona o LangGraph"

---

## 🔧 Personalização

- Para mudar o modelo: altere a variável `model` no arquivo `app.py`
- Para adicionar novas ferramentas: crie funções com o decorator `@tool` e adicione na lista de tools
- Para ajustar o comportamento: modifique o `system_prompt`

---

## 📌 Observações

- O projeto utiliza `create_agent` do LangChain (padrão ReAct/Tool Calling)
- A memória é salva localmente no arquivo `chatbot_memory.db`
- Cada nova sessão gera um `thread_id` único

---

## 📄 Licença

Este projeto está sob a licença MIT. Sinta-se à vontade para usar e modificar.

---

## 🤝 Contribuindo

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues e pull requests.

---

**Made with ❤️ by Gazstao 2026 - Based on [Ardit Sulce Python Udemy Course](https://www.udemy.com/course/the-python-mega-course)**

```

---

### Como usar:

1. Copie todo o conteúdo acima
2. Crie um arquivo `README.md` na raiz do seu projeto
3. Cole o conteúdo
4. Substitua:
   - `SEU_USUARIO`
   - `nome-do-repo`

Quer que eu também gere um `requirements.txt` e ajuste o código atual (ele tem alguns pequenos problemas, como a ferramenta `get_date` sem decorator)?
