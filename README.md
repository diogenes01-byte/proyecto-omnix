# Proyecto Omnix: Análisis de datos económicos impulsado por IA y RAG

![Python](https://img.shields.io/badge/Python-3.11-yellow?style=for-the-badge&logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-API%20Backend-green?style=for-the-badge&logo=fastapi)
![RAG](https://img.shields.io/badge/RAG-Retrieval%20Augmented%20Generation-blue?style=for-the-badge)
![LLM](https://img.shields.io/badge/LLM-Contextual%20AI-purple?style=for-the-badge)
![Estado](https://img.shields.io/badge/Estado-Completado-brightgreen?style=for-the-badge)

Este repositorio presenta el desarrollo de un **sistema de preguntas y respuestas económicas basado en modelos de lenguaje (LLM) y Retrieval-Augmented Generation (RAG)**.

El objetivo es construir una arquitectura capaz de **responder preguntas complejas de economía de forma contextualizada, verificable y fundamentada en fuentes de información externas**, reduciendo significativamente las alucinaciones del modelo.

---

## Contenido

- **Arquitectura LLM + RAG:** Integración de modelos de lenguaje con recuperación de información externa.  
- **Ingesta y recuperación de datos:** Indexación de documentos y búsqueda semántica para enriquecer el contexto de las respuestas.  
- **Pipeline de preguntas y respuestas:** Flujo completo desde la consulta del usuario hasta la generación de la respuesta final.  
- **Backend con FastAPI:** Exposición del sistema como API REST para consumo externo o interfaces web.  
- **Gestión de contexto:** Estrategias para mejorar la coherencia, precisión y relevancia de las respuestas.  
- **Evaluación del sistema:** Análisis cualitativo del rendimiento del modelo y calidad de las respuestas generadas.

---

## Propósitos del proyecto

- Diseñar un sistema capaz de **responder preguntas económicas con soporte en fuentes externas fiables**.  
- Implementar una arquitectura moderna basada en **RAG para reducir alucinaciones en LLMs**.  
- Integrar un flujo completo de **recuperación, procesamiento y generación de información contextualizada**.  
- Exponer el sistema mediante una **API escalable y modular con FastAPI**.  
- Explorar el uso práctico de LLMs en **casos reales de análisis económico y toma de decisiones basada en datos**.

---

## Tecnologías y herramientas

- **Python:** Lenguaje principal del sistema.  
- **FastAPI:** Desarrollo del backend y API REST.  
- **LangChain / frameworks RAG:** Orquestación del pipeline de recuperación y generación.  
- **Embeddings (OpenAI u otros modelos):** Representación semántica de texto.  
- **Vector databases (FAISS u otros):** Almacenamiento y búsqueda eficiente de información.  
- **LLM (GPT u otros modelos):** Generación de respuestas finales.  
- **Docker:** Contenerización del sistema para despliegue reproducible.

---

## Uso del repositorio

1. Clonar el repositorio.  
2. Instalar las dependencias del proyecto.  
3. Configurar variables de entorno necesarias (API keys, rutas, etc.).  
4. Levantar el backend con FastAPI usando Uvicorn.  
5. Ingestar documentos en el sistema RAG.  
6. Realizar consultas a través de la API o interfaz conectada.
