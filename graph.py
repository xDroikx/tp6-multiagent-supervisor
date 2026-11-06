import sqlite3
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.sqlite import SqliteSaver

from state import AgentState
from agents.supervisor_agent import supervisor_node
from agents.research_agent import research_node
from agents.analyst_agent import analyst_node

# 1. Instanciar el StateGraph con el Estado Compartido
workflow = StateGraph(AgentState)

# 2. Agregar los nodos del sistema
workflow.add_node("Supervisor", supervisor_node)
workflow.add_node("Investigador", research_node)
workflow.add_node("Analista", analyst_node)

# 3. Conectar los agentes especialistas de regreso al Supervisor (Topología Jerárquica)
workflow.add_edge("Investigador", "Supervisor")
workflow.add_edge("Analista", "Supervisor")

# 4. Conectar la entrada del usuario al Supervisor
workflow.add_edge(START, "Supervisor")

# 5. Arista condicional: el Supervisor decide el siguiente paso
def route_next(state):
    return state["next"]

workflow.add_conditional_edges(
    "Supervisor",
    route_next,
    {
        "Investigador": "Investigador",
        "Analista": "Analista",
        "FINALIZAR": END
    }
)

# 6. Compilar el grafo con persistencia SQLite
conn = sqlite3.connect("checkpoints.sqlite", check_same_thread=False)
memory = SqliteSaver(conn)

app = workflow.compile(checkpointer=memory)