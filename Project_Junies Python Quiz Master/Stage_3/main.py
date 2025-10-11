from fastapi import FastAPI
from fastapi.responses import PlainTextResponse, FileResponse
import os
from pydantic import BaseModel
import random

# Configurar la aplicación FastAPI
app = FastAPI()

# Predefinir preguntas y respuestas
questions = [
    {
        "id": 1,
        "question": "¿Cuál de las siguientes opciones es un comentario válido en Python?",
        "options": ["/* Esto es un comentario */", "// Esto es un comentario", "# Esto es un comentario",
                    "<!-- Esto es un comentario -->"],
        "correct_option": 3
    },
    {
        "id": 2,
        "question": "¿Cuál es el resultado de la expresión: 3 + 2 * 2?",
        "options": ["10", "7", "5", "9"],
        "correct_option": 2
    },
    {
        "id": 3,
        "question": "¿Qué función estándar se utiliza para obtener la entrada del usuario en Python?",
        "options": ["input()", "user_input()", "scanf()", "cin()"],
        "correct_option": 1
    },
    {
        "id": 4,
        "question": "¿Qué palabra clave se utiliza para definir una función en Python?",
        "options": ["func", "define", "def", "function"],
        "correct_option": 3
    },
    {
        "id": 5,
        "question": "¿Cuál de las siguientes es una estructura de datos mutable en Python?",
        "options": ["Tupla", "Lista", "Cadena (String)", "Conjunto (Set)"],
        "correct_option": 2
    }
]


# Modelo para enviar respuesta como JSON
class AnswerRequest(BaseModel):
    question_id: int
    selected_option: int

# Ruta principal ("/")
@app.get("/", tags=["Root"])
def read_root():
    """
    Devuelve un mensaje de bienvenida personalizado en la raíz.
    """
    return {"message": "Welcome to the Python Quiz API ver. V.Sh."}

@app.get("/questions", tags=["Quiz"])
def get_question():
    """
    Devuelve una pregunta al azar y sus opciones de respuesta.
    """
    question = random.choice(questions)
    return {
        "id": question["id"],
        "question": question["question"],
        "options": question["options"]
    }


@app.post("/submit-answer", tags=["Quiz"])
def submit_answer(answer: AnswerRequest):
    """
    Verifica si la respuesta seleccionada por el usuario es correcta.
    """
    # Filtrar para encontrar la pregunta por ID
    question = next((q for q in questions if q["id"] == answer.question_id), None)

    if not question:
        return {"message": "Pregunta no encontrada."}

    is_correct = answer.selected_option == question["correct_option"]
    return {
        "question_id": question["id"],
        "is_correct": is_correct,
        "correct_option": question["correct_option"]
    }


# Ruta para acceder al contenido de README.md como texto
@app.get("/docs", tags=["Documentation"])
def get_readme():
    """
    Devuelve el contenido del archivo README.md.
    """
    readme_path = "README.md"
    if os.path.exists(readme_path):
        # Devuelve el contenido del archivo README.md
        return FileResponse(readme_path, media_type="text/markdown", filename="README.md")
    else:
        # Si no se encuentra el archivo, dispara un error
        raise HTTPException(status_code=404, detail="README.md no encontrado en el directorio del proyecto.")

@app.post("/exit", tags=["Quiz"])
def exit_chat():
    """
    Endpoint para finalizar el chat.
    """
    return {"message": "¡Gracias por participar! ¡Hasta pronto!"}
