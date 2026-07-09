from langchain.agents import create_agent
from langchain_google_genai import data  # Importação possivelmente não utilizada (pode ser resquício)
from langchain_ollama import ChatOllama
from datetime import datetime
import gradio as gr
from langgraph.checkpoint.sqlite import SqliteSaver
import sqlite3
import uuid
from langchain_tavily import TavilySearch
from dotenv import load_dotenv
import pprint

# Carrega variáveis de ambiente do arquivo .env (chaves de API, etc.)
load_dotenv()

# ================== CONFIGURAÇÕES DO MODELO ==================
model = "gemma4:12b"  #model = "qwen3.5:9b"
temperature = 0.7

def get_date():
    """Obtem a data atual"""
    return datetime.now().strftime("%Y-%m-%d")


# ================== FERRAMENTAS (Tools) ==================
# Ferramenta de busca na web (Tavily)
search_tool = TavilySearch()

# ================== MEMÓRIA PERSISTENTE ==================
# Conecta ao banco SQLite para salvar o histórico das conversas
conn = sqlite3.connect('chatbot_memory.db', check_same_thread=False)
# SqliteSaver é o checkpointer do LangGraph que permite persistir o estado
checkpointer = SqliteSaver(conn)

# ================== LLM (Large Language Model) ==================
# Inicializa o modelo local via Ollama
llm = ChatOllama(model=model, temperature=temperature)

# ================== PROMPT DO SISTEMA ==================
system_prompt = """
Você é um assistente útil e amigável. 
Você pode responder perguntas e realizar tarefas usando as ferramentas disponíveis. 
Use a ferramenta get_date se o usuário perguntar sobre a data de hoje.
Use a ferramenta search_tool para responder perguntas que exigem pesquisa na web.
Seja claro e conciso em suas respostas.
"""

# ================== CRIAÇÃO DO AGENTE ==================
# Cria o agente usando a função create_agent do LangChain
# Ele combina o LLM + ferramentas + prompt do sistema + memória persistente
agent = create_agent(
    model=llm, 
    tools=[get_date, search_tool], 
    system_prompt=system_prompt, 
    checkpointer=checkpointer)

# ================== FUNÇÃO DE CHAT (Callback do Gradio) ==================
def chat(message, history, thread_id):
    """
    Função chamada a cada mensagem enviada pelo usuário.
    
    Parâmetros:
        message: texto enviado pelo usuário
        history: histórico da conversa (gerenciado pelo Gradio)
        thread_id: identificador único da conversa (para memória)
    """
    # Configuração necessária para o LangGraph identificar a thread/conversa
    config = {"configurable": {"thread_id": thread_id}}
    
    # Invoca o agente com a mensagem do usuário
    response = agent.invoke({"messages": [{"role": "user", "content": message}]}, config)
    
    # Imprime a resposta completa no terminal (debug e compreensão do fluxo)
    pprint.pprint(response)
    
    # Extrai apenas o conteúdo da última mensagem do agente
    last_response = response['messages'][-1].content
    return last_response   


# ================== INTERFACE GRADIO ==================
with gr.Blocks(title="Chatbot com Ollama", fill_height=True) as demo:
    
    # Gera um ID único para cada nova sessão de chat
    UniqueID =  lambda: str(uuid.uuid4())
    uid = UniqueID()
    print("Novo chat iniciado: ", uid)
    
    # Armazena o thread_id no estado do Gradio
    thread_id = gr.State(value = str(uid))

    # Cabeçalho da aplicação
    gr.Markdown("# RecrutaTalks - Julho de 2026 - Chatbot com LangChain + Ollama")
    gr.Markdown(f"**ID da conversa:** {uid}")

    # Interface de chat do Gradio
    gr.ChatInterface(
        fn=chat,                    # Função que será chamada a cada mensagem
        additional_inputs=[thread_id],  # Passa o thread_id para a função chat
        fill_height=True, 
        title="Assistente de Inteligencia Artificial",
        description="Modelo: " + model,
        cache_examples=False
    )


# ================== INICIALIZAÇÃO DO SERVIDOR ==================
demo.launch(
    # server_name="0.0.0.0",    # Descomente para acessar de outros dispositivos na rede
    server_name="localhost",
    server_port=7860,
    height=1000
)

# ================== CÓDIGO COMENTADO (VERSÃO ANTIGA) ==================
# O bloco abaixo está comentado e representa uma versão anterior/simplificada
# do código (mantido para referência):

# with gr.Blocks() as demo:
#    UniqueID =  lambda: str(uuid.uuid4())
#    uid = UniqueID()
#    print("Novo chat iniciado: ", uid)
#    thread_id = gr.State(value = str(uid))
#    gr.Markdown("## Chatbot com LangChain e Ollama <h6>"+ uid+"</h6>")
#    gr.ChatInterface(fn=chat, additional_inputs=[thread_id])

# def chat(message, history, thread_id):
#    config = {"configurable": {"thread_id": thread_id}}
#    response = agent.invoke({"messages": [{"role": "user", "content": message}]}, config)
#    print(response)
#    last_response = response['messages'][-1].content
#    return last_response   