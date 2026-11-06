import json
from langchain_core.messages import HumanMessage
from graph import app


def main():
    print("============================================================")
    print("🤖 PRE-ENTREGA 6: SISTEMA MULTI-AGENTE CON PATRÓN SUPERVISOR")
    print("============================================================\n")

    # Identificador de sesión para persistencia en SQLite
    thread_config = {"configurable": {"thread_id": "sesion_orquestador_01"}}

    consulta_usuario = "Necesito averiguar los datos de ventas y costos operativos de la empresa y calcular el margen de ganancia."
    print(f"👤 Usuario: {consulta_usuario}\n")
    print("-------------------- FLUJO DE DELEGACIÓN --------------------\n")

    input_data = {
        "messages": [HumanMessage(content=consulta_usuario)]
    }

    # Stream de eventos para observar la interacción entre Supervisor y Especialistas
    nodos_ejecutados = []
    for event in app.stream(input_data, config={**thread_config, "recursion_limit": 15}):
        for nodo_nombre, estado_actual in event.items():
            nodos_ejecutados.append(nodo_nombre)
            print(f"🔄 [Nodo Ejecutado]: {nodo_nombre}")
            
            if "next" in estado_actual:
                print(f"👉 [Decisión Supervisor]: Próximo agente -> '{estado_actual['next']}'")
            
            if "messages" in estado_actual and estado_actual["messages"]:
                ultimo_msg = estado_actual["messages"][-1]
                print(f"💬 {ultimo_msg.content}\n")

    # ----------------------------------------------------
    # OBTENER ESTADO FINAL Y EXPORTAR TRAZA
    # ----------------------------------------------------
    estado_final = app.get_state(thread_config)
    mensajes_finales = estado_final.values.get("messages", [])

    print("---------------------- RESPUESTA FINAL ----------------------")
    if mensajes_finales:
        print(f"🤖 Sistema Multi-Agente:\n{mensajes_finales[-1].content}\n")

    # Exportar traza de la conversación completa
    traza = []
    for msg in mensajes_finales:
        item = {
            "tipo": msg.type,
            "autor": getattr(msg, "name", msg.type),
            "contenido": msg.content
        }
        traza.append(item)

    with open("trace_example.json", "w", encoding="utf-8") as f:
        json.dump(traza, f, indent=2, ensure_ascii=False)

    print("✅ Traza exportada en 'trace_example.json'.")

    # ----------------------------------------------------
    # GENERAR DIAGRAMA MERMAID
    # ----------------------------------------------------
    print("\n------------------- DIAGRAMA MERMAID DEL GRAFO -------------------")
    mermaid_code = app.get_graph().draw_mermaid()
    print(mermaid_code)
    print("------------------------------------------------------------------")


if __name__ == "__main__":
    main()