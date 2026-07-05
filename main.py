from langchain.agents import create_agent
from langchain_ollama import ChatOllama
from datetime import datetime
import gradio as gr
from langgraph.checkpoint.sqlite import SqliteSaver
import sqlite3
import uuid
from langchain_community.tools.tavily_search import TavilySearchResults
from dotenv import load_dotenv

load_dotenv()

model = "gemma4:12b"  #model = "qwen3.5:9b"
temperature = 0.7

def get_date():
    """Obtem a data atual"""
    return datetime.now().strftime("%Y-%m-%d")

search_tool = TavilySearchResults()

conn = sqlite3.connect('chatbot_memory.db', check_same_thread=False)
checkpointer = SqliteSaver(conn)

llm = ChatOllama(model=model, temperature=temperature)

system_prompt = """
Você é um assistente útil e amigável. 
Você pode responder perguntas e realizar tarefas usando as ferramentas disponíveis. 
Use a ferramenta get_date se o usuário perguntar sobre a data de hoje.
Use a ferramenta search_tool para responder perguntas que exigem pesquisa na web.
Seja claro e conciso em suas respostas.
"""

agent = create_agent(
    model=llm, 
    tools=[get_date, search_tool], 
    system_prompt=system_prompt, 
    checkpointer=checkpointer)

def chat(message, history, thread_id):
    config = {"configurable": {"thread_id": thread_id}}
    response = agent.invoke({"messages": [{"role": "user", "content": message}]}, config)
    print("Respomse: ", response)
    last_response = response['messages'][-1].content
    return last_response   

with gr.Blocks(title="Chatbot com Ollama", fill_height=True) as demo:
    
    UniqueID =  lambda: str(uuid.uuid4())
    uid = UniqueID()
    print("Novo chat iniciado: ", uid)
    thread_id = gr.State(value = str(uid))

    gr.Markdown("# RecrutaTalks - Julho de 2026 - Chatbot com LangChain + Ollama")
    gr.Markdown(f"**ID da conversa:** {uid}")

    gr.ChatInterface(
        fn=chat,
        additional_inputs=[thread_id],
        fill_height=True, 
        title="Assistente de Inteligencia Artificial",
        description="Modelo: " + model,
        cache_examples=False
    )

demo.launch(
    # server_name="0.0.0.0",    para acessar de outros dispositivos na rede
    server_name="localhost",
    server_port=7860,
    height=1000
)

# with gr.Blocks() as demo:
#    UniqueID =  lambda: str(uuid.uuid4())
#    uid = UniqueID()
#    print("Novo chat iniciado: ", uid)
#    thread_id = gr.State(value = str(uid))
#    gr.Markdown("## Chatbot com LangChain e Ollama <h6>"+ uid+"</h6>")
#    gr.ChatInterface(fn=chat, additional_inputs=[thread_id])
