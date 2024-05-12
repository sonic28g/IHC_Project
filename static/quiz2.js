// Função para carregar as perguntas do JSON
async function loadQuestions() {
    try {
      const response = await fetch("static/quiz2.json");
      const data = await response.json();
      return data.quiz;
    } catch (error) {
      console.error('Erro ao carregar as perguntas:', error);
    }
  }
  
  let quizQuestions = [];
  let currentQuestionIndex = 0;
  let score = 0;
  
  // Função para inicializar o quiz
  async function initializeQuiz() {
    quizQuestions = await loadQuestions();
    displayQuestion();
  }
  
  // Função para exibir a próxima pergunta
  function displayQuestion() {
    const currentQuestion = quizQuestions[currentQuestionIndex];
    const questionElement = document.getElementById("question");
    const optionsContainer = document.getElementById("options-container");
    const errorMessage = document.getElementById("error-message");
  
    // Adiciona o número da pergunta antes do texto da pergunta
    questionElement.textContent = `Question ${currentQuestionIndex + 1}/${quizQuestions.length}: ${currentQuestion.pergunta}`;
    optionsContainer.innerHTML = "";
    errorMessage.style.display = "none";
  
    Object.entries(currentQuestion.opcoes).forEach(([key, value]) => {
      const button = document.createElement("button");
      button.textContent = value;
      button.dataset.key = key; // Armazena a chave da opção no atributo 'data-key'
      button.classList.add("btn", "btn-secondary", "mb-2", "option-button"); // Adiciona classes de botão secundário e a classe 'option-button'
      button.onclick = () => selectOption(key);
      optionsContainer.appendChild(button);
    });
  }
  
  
  // Função para selecionar uma opção
  function selectOption(selectedAnswer) {
    // Remove a classe 'selected' de todos os botões e troca a cor das opções não selecionadas
    const buttons = document.querySelectorAll("#options-container button");
    buttons.forEach(button => {
      button.classList.remove("selected");
      button.classList.remove("btn-primary"); // Remove a classe de botão primário
      button.classList.add("btn-secondary"); // Adiciona a classe de botão secundário
    });
  
    // Adiciona a classe 'selected' e troca a cor do botão selecionado
    const selectedButton = document.querySelector(`#options-container button[data-key="${selectedAnswer}"]`);
    selectedButton.classList.add("selected");
    selectedButton.classList.remove("btn-secondary"); // Remove a classe de botão secundário
    selectedButton.classList.add("btn-primary"); // Adiciona a classe de botão primário
  }
  
  // Função para verificar se a resposta está correta e avançar para a próxima pergunta
  function nextQuestion() {
    const selectedButton = document.querySelector("#options-container button.selected");
    if (!selectedButton) {
      // Se nenhuma opção foi selecionada, exibe a mensagem de erro e retorna
      const errorMessage = document.getElementById("error-message");
      errorMessage.style.display = "block";
      return;
    }
  
    const selectedAnswer = selectedButton.dataset.key;
    const currentQuestion = quizQuestions[currentQuestionIndex];
    if (selectedAnswer === currentQuestion.resposta_correta) {
      score++;
    }
  
    currentQuestionIndex++;
    if (currentQuestionIndex < quizQuestions.length) {
      displayQuestion();
    } else {
      showScore();
    }
  }
  
  function showAlert(message, alertClass) {
    // Cria um elemento de div para o alerta
    var alertDiv = document.createElement('div');
    alertDiv.textContent = message;
    alertDiv.classList.add('alert', alertClass);
    alertDiv.setAttribute('role', 'alert');
  
    // Adiciona o alerta ao corpo do documento
    document.body.appendChild(alertDiv);
  }
  
  // Função para exibir a pontuação final
  function showScore() {
    const quizContainer = document.getElementById("quiz-container");
    const scoreContainer = document.getElementById("score-container");
    const scoreElement = document.getElementById("score");
    const messageElement = document.getElementById("message");
  
    quizContainer.style.display = "none";
    scoreContainer.style.display = "block";
  
    const totalQuestions = quizQuestions.length;
    const percentage = (score / totalQuestions) * 100;
    const finalScore = Math.round((percentage / 100) * 10);
  
    scoreElement.textContent = `${finalScore} out of 10`;
  
    if (finalScore < 10) {
      messageElement.textContent = "Better luck next time!";
    } else {
      if (finalScore === 10) {
       showAlert("Promotional Code: B45D-C7GH-M5EW", "alert-success");
  }
    }
  }
  
  // Inicialização do quiz
  initializeQuiz();
  