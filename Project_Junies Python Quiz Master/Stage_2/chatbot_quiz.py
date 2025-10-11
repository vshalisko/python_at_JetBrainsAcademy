import random

# Lista de preguntas
questions = [
    {
        "question": "¿Cuál de las siguientes opciones es un comentario válido en Python?",
        "options": ["1. /* Esto es un comentario */",
                    "2. // Esto es un comentario",
                    "3. # Esto es un comentario",
                    "4. <!-- Esto es un comentario -->"],
        "answer": 3
    },
    {
        "question": "¿Cuál es el resultado de la expresión: 3 + 2 * 2?",
        "options": ["1. 10", "2. 7", "3. 5", "4. 9"],
        "answer": 2
    },
    {
        "question": "¿Qué función estándar se utiliza para obtener la entrada del usuario en Python?",
        "options": ["1. input()", "2. user_input()", "3. scanf()", "4. cin()"],
        "answer": 1
    },
    {
        "question": "¿Qué palabra clave se utiliza para definir una función en Python?",
        "options": ["1. func", "2. define", "3. def", "4. function"],
        "answer": 3
    },
    {
        "question": "¿Cuál de las siguientes es una estructura de datos mutable en Python?",
        "options": ["1. Tupla", "2. Lista", "3. Cadena (String)", "4. Conjunto (Set)"],
        "answer": 2
    }
]


def chatbot():
    print("Hola, soy tu chatbot de Python. Puedes salir del chat escribiendo 'salir'. ¡Vamos a aprender y divertirnos!")
    while True:
        # Selecciona una pregunta aleatoriamente
        question = random.choice(questions)

        # Muestra la pregunta y las opciones
        print("\n" + question["question"])
        for option in question["options"]:
            print(option)

        # Obtiene la respuesta del usuario
        user_input = input("\nEscribe el número de tu respuesta (o escribe 'salir' para terminar): ")

        if user_input.lower() == 'salir':
            print("¡Gracias por participar! ¡Hasta pronto!")
            break

        # Valida que la entrada sea un número válido
        if not user_input.isdigit():
            print("Entrada inválida. Por favor, elige una opción válida (1, 2, 3 o 4).")
            continue

        user_answer = int(user_input)

        # Verifica si la respuesta es correcta
        if user_answer == question["answer"]:
            print("👍 ¡Correcto!")
        else:
            print(f"❌ Incorrecto. La respuesta correcta era la opción {question['answer']}.")


# Ejecutar el chatbot
if __name__ == "__main__":
    chatbot()# Chatbot Quiz Bot API
