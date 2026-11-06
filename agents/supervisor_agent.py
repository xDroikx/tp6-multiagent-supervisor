import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from pydantic import BaseModel, Field

from state import AgentOptions

load_dotenv()

class Router(BaseModel):
    next: AgentOptions = Field(
        ...,
        description="Selecciona 'Investigador' para buscar datos, 'Analista' para calcular métricas, o 'FINALIZAR' si la tarea concluyó."
    )

system_prompt = (
    "Eres el Supervisor de un equipo multi-agente ('Investigador' y 'Analista').\n"
    "REGLAS DE DELEGACIÓN:\n"
    "1. Si la conversación NO contiene aún los datos de ventas y costos, responde 'Investigador'.\n"
    "2. Si el Investigador YA aportó las ventas y costos, pero NO se ha calculado el margen de ganancia, responde 'Analista'.\n"
    "3. Si el Analista YA calculó el margen de ganancia, responde 'FINALIZAR'.\n"
    "No repitas a un agente si su tarea ya fue realizada."
)

prompt = ChatPromptTemplate.from_messages([
    ("system", system_prompt),
    MessagesPlaceholder(variable_name="messages"),
    (
        "system",
        "Basado en el historial, ¿quién debe intervenir ahora? Elige estrictamente entre: ['Investigador', 'Analista', 'FINALIZAR']"
    )
])

api_key = os.getenv("OPENAI_API_KEY")
model_name = os.getenv("DEFAULT_MODEL", "llama-3.3-70b-versatile")
base_url = os.getenv("OPENAI_BASE_URL", "https://api.groq.com/openai/v1")

llm = ChatOpenAI(
    model=model_name,
    api_key=api_key,
    base_url=base_url,
    temperature=0.0
)

supervisor_chain = prompt | llm.with_structured_output(Router)

def supervisor_node(state):
    resultado = supervisor_chain.invoke(state)
    return {"next": resultado.next}