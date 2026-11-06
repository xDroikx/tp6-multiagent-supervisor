from langchain_core.messages import AIMessage
from langchain_core.tools import tool
from pydantic import BaseModel, Field

class CalcularMargenInput(BaseModel):
    ventas: float = Field(..., description="Monto total de ventas.")
    costos: float = Field(..., description="Monto total de costos operativos.")

@tool(args_schema=CalcularMargenInput)
def calcular_margen_ganancia(ventas: float, costos: float) -> str:
    """Calcula la ganancia neta y el porcentaje de margen operativo."""
    ganancia = ventas - costos
    margen = (ganancia / ventas) * 100 if ventas > 0 else 0.0
    return f"Ganancia neta: ${ganancia:,.2f} | Margen de ganancia: {margen:.2f}%"

def analyst_node(state):
    """Nodo especialista en Análisis."""
    resultado_calculo = calcular_margen_ganancia.invoke({"ventas": 150000.0, "costos": 45000.0})
    
    respuesta = AIMessage(
        content=f"📊 [Analista]: {resultado_calculo}. El margen operativo es de 70.00%, reflejando alta rentabilidad.",
        name="Analista"
    )
    return {"messages": [respuesta]}