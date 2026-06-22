# 🤖 Omnix: Análisis de datos económicos impulsados por IA y RAG

![Python](https://img.shields.io/badge/Python-3.11-yellow?style=for-the-badge&logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-API%20Backend-green?style=for-the-badge&logo=fastapi)
![RAG](https://img.shields.io/badge/RAG-Retrieval%20Augmented%20Generation-blue?style=for-the-badge)
![LLM](https://img.shields.io/badge/LLM-Generative%20AI-purple?style=for-the-badge)
![Vector DB](https://img.shields.io/badge/Vector%20Database-FAISS-orange?style=for-the-badge)
![Estado](https://img.shields.io/badge/Estado-MVP%20Funcional-brightgreen?style=for-the-badge)

---

## 📌 Situación (Problema de negocio)

La información económica y financiera se encuentra dispersa en múltiples fuentes, documentos técnicos, informes de mercado y publicaciones especializadas.

Para analistas, inversores y usuarios interesados en economía, encontrar información relevante suele implicar:

- Revisar grandes volúmenes de documentación
- Contrastar múltiples fuentes manualmente
- Interpretar conceptos financieros complejos
- Invertir tiempo significativo en investigación

Además, los modelos de lenguaje tradicionales presentan limitaciones al responder preguntas especializadas, ya que pueden generar respuestas incorrectas o desactualizadas cuando no cuentan con acceso a fuentes verificables.

---

## 🎯 Tarea (Objetivo del proyecto)

Diseñar y desarrollar un asistente inteligente capaz de:

- Responder consultas económicas y financieras en lenguaje natural
- Recuperar información relevante desde una base documental especializada
- Reducir las alucinaciones típicas de los LLMs mediante RAG
- Proporcionar respuestas contextualizadas y fundamentadas en evidencia
- Construir una arquitectura escalable preparada para evolucionar hacia un entorno de producción

---

## ⚙️ Acción (Solución implementada)

Se desarrolló un MVP funcional basado en una arquitectura moderna de IA generativa compuesta por:

### 🔹 Modelos de Lenguaje (LLMs)

- Interpretación de preguntas complejas
- Generación de respuestas contextuales
- Explicación de conceptos financieros y económicos

### 🔹 Arquitectura RAG (Retrieval-Augmented Generation)

- Recuperación dinámica de información relevante
- Enriquecimiento del contexto antes de generar respuestas
- Reducción de respuestas incorrectas o inventadas

### 🔹 Embeddings y búsqueda semántica

- Transformación de documentos en representaciones vectoriales
- Búsqueda basada en significado y no únicamente en palabras clave
- Recuperación eficiente de contenido relacionado

### 🔹 Base de datos vectorial

- Indexación de conocimiento financiero
- Almacenamiento optimizado para consultas semánticas
- Recuperación de contexto en tiempo real mediante FAISS

### 🔹 Backend y API

- Desarrollo de API REST utilizando FastAPI
- Arquitectura modular y escalable
- Integración sencilla con aplicaciones web o futuras interfaces conversacionales

### 🔹 Pipeline completo

- Ingesta documental
- Procesamiento y vectorización
- Recuperación contextual
- Generación de respuestas
- Exposición mediante API

---

## 📊 Resultado

Se logró construir un MVP funcional capaz de:

- Responder preguntas económicas utilizando información contextualizada
- Recuperar conocimiento relevante desde una base documental indexada
- Mejorar significativamente la calidad de las respuestas respecto a un LLM sin contexto externo
- Proporcionar una arquitectura preparada para futuras ampliaciones y despliegue en producción

---

## 🏗️ Arquitectura de la solución

Usuario
↓
Consulta financiera
↓
FastAPI
↓
Pipeline RAG
↓
Embeddings
↓
Base Vectorial (FAISS)
↓
Recuperación de contexto
↓
LLM
↓
Respuesta fundamentada

---

## 🛠️ Tecnologías utilizadas

- Python 3.11
- FastAPI
- LangChain
- OpenAI API / LLMs
- FAISS
- Embeddings
- Retrieval-Augmented Generation (RAG)
- Uvicorn
- Pydantic

---

## 🚀 Uso del repositorio

1. Clonar el repositorio
2. Instalar dependencias del proyecto
3. Configurar variables de entorno necesarias
4. Ejecutar el backend mediante Uvicorn
5. Ingestar documentación económica en la base vectorial
6. Realizar consultas a través de la API
7. Obtener respuestas contextualizadas generadas por el sistema

---

## 🔮 Próximas mejoras

- Interfaz web conversacional
- Soporte para múltiples fuentes económicas
- Evaluación automática de respuestas
- Integración con modelos open-source
- Despliegue cloud escalable
- Sistema de citación de fuentes
