# Chatbot Quiz Bot API

Esta es una API REST desarrollada con **FastAPI**, que proporciona un chatbot para preguntas y respuestas de opción múltiple sobre programación en Python. Esta API está diseñada para ser integrada en un frontend interactivo.

## Requisitos

- Python 3.11.9
- FastAPI
- Uvicorn (para ejecutar el servidor)

Instalar las dependencias necesarias:

```bash
pip install fastapi uvicorn
```

## Ejecutar el Servidor

Ejecuta el servidor local con el siguiente comando:

```bash
uvicorn main:app --reload
```

Por defecto, el servidor estará disponible en `http://127.0.0.1:8000`.

## Endpoints Disponibles

### GET `/questions`

Devuelve una pregunta al azar con sus opciones de respuesta.

- **Método**: `GET`
- **Respuesta Exitosa** (Ejemplo):

```json
{
    "id": 1,
    "question": "¿Cuál de las siguientes opciones es un comentario válido en Python?",
    "options": ["/* Esto es un comentario */", "// Esto es un comentario", "# Esto es un comentario", "<!-- Esto es un comentario -->"]
}
```

---

### POST `/submit-answer`

Valida si la respuesta enviada por el usuario es correcta para una pregunta específica.

- **Método**: `POST`
- **Cuerpo de la Petición**:

```json
{
    "question_id": 1,
    "selected_option": 3
}
```

- **Respuesta Exitosa**:

Si la respuesta es correcta:

```json
{
    "question_id": 1,
    "is_correct": true,
    "correct_option": 3
}
```

Si la respuesta es incorrecta:

```json
{
    "question_id": 1,
    "is_correct": false,
    "correct_option": 3
}
```

Si la pregunta no es encontrada:

```json
{
    "message": "Pregunta no encontrada."
}
```

---

### POST `/exit`

Endpoint para finalizar el chat de preguntas.

- **Método**: `POST`
- **Respuesta**:

```json
{
    "message": "¡Gracias por participar! ¡Hasta pronto!"
}
```

---

## Integración con el Frontend

Esta API puede ser consumida desde cualquier frontend utilizando peticiones HTTP estándar. Por ejemplo, puedes usar `fetch` en JavaScript para conectarte con el backend y procesar las respuestas en tiempo real.

## Contribuciones

Las contribuciones son bienvenidas. Por favor, crea un fork y envía un pull request para analizarlos.

---

## Licencia

Este proyecto está bajo la licencia Creative Commons Attribution 4.0.