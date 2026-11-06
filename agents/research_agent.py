from langchain_core.messages import AIMessage
from langchain_core.tools import tool
from pydantic import BaseModel, Field

# 1. Esquema de entrada
class BusquedaConocimientoInput(BaseModel):
    tema: str = Field(..., description="Tema o palabra clave a buscar en la base de conocimiento.")

# 2. Herramienta de búsqueda
@tool(args_schema=BusquedaConocimientoInput)
def buscar_informacion(tema: str) -> str:
    """Busca datos y métricas financieras o de ventas sobre un tema específico."""
    return (
        "Resultados de búsqueda:\n"
        "- Ventas: Las ventas netas alcanzaron $150,000 en el Q1.\n"
        "- Costos: Los costos operativos totales ascendieron a $45,000."
    )

# 3. Nodo del Investigador
def research_node(state):
    """Nodo especialista en Investigación."""
    mensajes = state["messages"]
    primer_mensaje = mensajes[0].content if mensajes else ""
    
    hallazgo = buscar_informacion.invoke({"tema": primer_mensaje})
    
    respuesta = AIMessage(
        content=f"🔍 [Investigador]: {hallazgo}",
        name="Investigador"
    )
    return {"messages": [respuesta]}