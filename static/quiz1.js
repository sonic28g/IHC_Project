// Função para carregar as perguntas do JSON
async function loadQuestions() {
    try {
      const response = await fetch("static/quiz1.json");
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
  
    questionElement.textContent = currentQuestion.pergunta;
    optionsContainer.innerHTML = "";
  
    Object.entries(currentQuestion.opcoes).forEach(([key, value]) => {
      const button = document.createElement("button");
      button.textContent = value;
      button.onclick = () => checkAnswer(key);
      optionsContainer.appendChild(button);
    });
  }
  
  // Função para verificar se a resposta está correta
  function checkAnswer(selectedAnswer) {
    const currentQuestion = quizQuestions[currentQuestionIndex];
    if (selectedAnswer === currentQuestion.resposta_correta) {
      score++;
    }
  }
  
  // Função para exibir a próxima pergunta ou a pontuação final
  function nextQuestion() {
    currentQuestionIndex++;
    if (currentQuestionIndex < quizQuestions.length) {
      displayQuestion();
    } else {
      showScore();
    }
  }
  
  // Função para exibir a pontuação final
  function showScore() {
    const quizContainer = document.getElementById("quiz-container");
    const scoreContainer = document.getElementById("score-container");
    const scoreElement = document.getElementById("score");
  
    quizContainer.style.display = "none";
    scoreContainer.style.display = "block";
  
    const totalQuestions = quizQuestions.length;
    const percentage = (score / totalQuestions) * 100;
    const finalScore = Math.round((percentage / 100) * 10);
  
    scoreElement.textContent = `Você marcou ${finalScore} de 10.`;
  }
  
  // Inicialização do quiz
  initializeQuiz();
  