# TP 6: Sistema Multi-Agente Jerárquico con Patrón Supervisor en LangGraph

Este repositorio contiene la implementación de un **Sistema Multi-Agente Orquestado** bajo la topología de **Supervisor (Router)** utilizando **LangGraph**. El sistema cuenta con dos agentes especialistas (*Investigador* y *Analista*) y un nodo supervisor encargado de delegar tareas dinámicamente según el estado compartido.

---

## 🛠️ Arquitectura de la Topología Jerárquica

```mermaid
graph TD;
        __start__([start]):::first
        Supervisor(Supervisor)
        Investigador(Investigador)
        Analista(Analista)
        __end__([end]):::last
        Analista --> Supervisor;
        Investigador --> Supervisor;
        Supervisor -.-> Analista;
        Supervisor -.-> Investigador;
        Supervisor -. FINALIZAR .-> __end__;
        __start__ --> Supervisor;