// URL base de la API
const API_BASE_URL = "http://127.0.0.1:8000";

// Obtener y mostrar el mensaje de bienvenida
document.getElementById('fetch-welcome-btn').addEventListener('click', async () => {
  const response = await fetch(`${API_BASE_URL}/`);
  const data = await response.json();
  document.getElementById('welcome-message').textContent = data.message;
});

// Obtener una pregunta al azar y mostrarla
document.getElementById('get-question-btn').addEventListener('click', async () => {
  const response = await fetch(`${API_BASE_URL}/questions`);
  const question = await response.json();

  const questionContainer = document.getElementById('question-container');
  const questionTitle = document.getElementById('question-title');
  const optionsList = document.getElementById('options-list');
  const feedback = document.getElementById('feedback');

  // Mostrar el contenedor de la pregunta
  questionContainer.style.display = 'block';
  feedback.textContent = ''; // Resetear feedback

  // Configurar los datos de la pregunta
  questionTitle.textContent = question.question;
  optionsList.innerHTML = ''; // Limpiar opciones previas
  question.options.forEach((option, index) => {
    const li = document.createElement('li');
    li.textContent = option;
    li.dataset.optionIndex = index + 1; // Almacenar el índice de la opción
    optionsList.appendChild(li);
  });

  // Seleccionar una respuesta
  optionsList.addEventListener('click', (event) => {
    if (event.target.tagName === 'LI') {
      // Marcar la opción seleccionada
      [...optionsList.children].forEach(li => li.classList.remove('selected'));
      event.target.classList.add('selected');
    }
  });

  // Enviar la respuesta seleccionada
  document.getElementById('submit-answer-btn').addEventListener('click', async () => {
    const selectedOption = document.querySelector('li.selected');
    if (!selectedOption) {
      feedback.textContent = "⚠️ ¡Selecciona una respuesta antes de enviar!";
      return;
    }

    const answer = {
      question_id: question.id,
      selected_option: parseInt(selectedOption.dataset.optionIndex)
    };

    const answerResponse = await fetch(`${API_BASE_URL}/submit-answer`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(answer)
    });

    const result = await answerResponse.json();
    if (result.is_correct) {
      feedback.textContent = "🎉 ¡Respuesta correcta!";
    } else {
      feedback.textContent = `❌ Respuesta incorrecta. La respuesta correcta era la opción ${result.correct_option}.`;
    }
  });
});

// Obtener la documentación del backend (README.md)
document.getElementById('fetch-docs-btn').addEventListener('click', async () => {
  const response = await fetch(`${API_BASE_URL}/docs`);
  const docs = await response.text();
  document.getElementById('docs-content').textContent = docs;
});