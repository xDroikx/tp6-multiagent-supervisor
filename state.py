from typing import Annotated, Literal, TypedDict
from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages

# Definimos las opciones de ruteo del Supervisor
AgentOptions = Literal["Investigador", "Analista", "FINALIZAR"]

class AgentState(TypedDict):
    """
    Estado compartido del sistema multi-agente.
    - messages: Historial acumulativo de la conversación (usando add_messages reducer).
    - next: El próximo agente al que el Supervisor delega la tarea ("Investigador", "Analista" o "FINALIZAR").
    """
    messages: Annotated[list[BaseMessage], add_messages]
    next: AgentOptions