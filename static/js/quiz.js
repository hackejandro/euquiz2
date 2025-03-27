document.addEventListener('DOMContentLoaded', function() {
    // DOM elements
    const loadingSpinner = document.getElementById('loading-spinner');
    const quizContent = document.getElementById('quiz-content');
    const resultsContainer = document.getElementById('results-container');
    const acronymElement = document.getElementById('acronym');
    const optionsContainer = document.getElementById('options-container');
    const feedbackContainer = document.getElementById('feedback-container');
    const nextButton = document.getElementById('next-button');
    const currentQuestionElement = document.getElementById('current-question');
    const totalQuestionsElement = document.getElementById('total-questions');
    const progressBar = document.getElementById('progress-bar');
    const finalScoreElement = document.getElementById('final-score');
    const finalTotalElement = document.getElementById('final-total');
    const scoreMessageElement = document.getElementById('score-message');
    const retryButton = document.getElementById('retry-button');

    // State
    let currentQuestion = null;
    let selectedAnswer = null;
    let totalQuestions = 0;
    
    // Fetch the first question
    fetchQuestion();
    
    // Event listeners
    nextButton.addEventListener('click', function() {
        nextButton.classList.add('d-none');
        feedbackContainer.classList.add('d-none');
        
        // Enable all option buttons for the next question
        const optionButtons = document.querySelectorAll('.option-btn');
        optionButtons.forEach(btn => {
            btn.disabled = false;
            btn.classList.remove('btn-success', 'btn-danger', 'btn-secondary');
            btn.classList.add('btn-outline-primary');
        });
        
        fetchQuestion();
    });
    
    retryButton.addEventListener('click', function() {
        // Reset the quiz with the same data
        fetch('/reset', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                // Reload the page to start a new quiz
                window.location.reload();
            }
        })
        .catch(error => {
            console.error('Error resetting quiz:', error);
        });
    });

    // Functions
    function fetchQuestion() {
        // Show loading spinner, hide content
        loadingSpinner.classList.remove('d-none');
        quizContent.classList.add('d-none');
        resultsContainer.classList.add('d-none');
        
        fetch('/get_question')
            .then(response => response.json())
            .then(data => {
                // Hide loading spinner
                loadingSpinner.classList.add('d-none');
                
                if (data.completed) {
                    // Quiz completed, show results
                    showResults(data.score, data.total);
                } else {
                    // Show the question
                    quizContent.classList.remove('d-none');
                    displayQuestion(data);
                }
            })
            .catch(error => {
                console.error('Error fetching question:', error);
                loadingSpinner.classList.add('d-none');
                alert('An error occurred while loading the question. Please try again.');
            });
    }
    
    function displayQuestion(questionData) {
        currentQuestion = questionData;
        totalQuestions = questionData.total_questions;
        
        // Update the question number and progress bar
        currentQuestionElement.textContent = questionData.question_number;
        totalQuestionsElement.textContent = totalQuestions;
        const progressPercentage = ((questionData.question_number - 1) / totalQuestions) * 100;
        progressBar.style.width = `${progressPercentage}%`;
        progressBar.setAttribute('aria-valuenow', progressPercentage);
        
        // Display the acronym
        acronymElement.textContent = questionData.acronym;
        
        // Create option buttons
        optionsContainer.innerHTML = '';
        questionData.options.forEach((option, index) => {
            const button = document.createElement('button');
            button.type = 'button';
            button.className = 'btn btn-outline-primary btn-lg w-100 mb-3 option-btn text-start p-3';
            button.textContent = option;
            button.dataset.option = option;
            button.addEventListener('click', () => selectOption(option));
            optionsContainer.appendChild(button);
        });
    }
    
    function selectOption(option) {
        selectedAnswer = option;
        
        // Disable all option buttons
        const optionButtons = document.querySelectorAll('.option-btn');
        optionButtons.forEach(btn => {
            btn.disabled = true;
            if (btn.dataset.option === option) {
                btn.classList.remove('btn-outline-primary');
                btn.classList.add('btn-primary');
            } else {
                btn.classList.remove('btn-outline-primary');
                btn.classList.add('btn-secondary');
            }
        });
        
        // Submit the answer
        submitAnswer(option);
    }
    
    function submitAnswer(answer) {
        fetch('/submit_answer', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ answer: answer })
        })
        .then(response => response.json())
        .then(data => {
            // Show feedback
            displayFeedback(data);
            
            // Highlight the correct/incorrect answers
            highlightAnswers(answer, data.correct_answer);
            
            // Show next button if there's a next question
            if (data.next_question) {
                nextButton.classList.remove('d-none');
            } else {
                // Quiz completed, fetch the final results
                setTimeout(() => {
                    fetchQuestion();
                }, 2000);
            }
        })
        .catch(error => {
            console.error('Error submitting answer:', error);
            alert('An error occurred while submitting your answer. Please try again.');
        });
    }
    
    function displayFeedback(data) {
        feedbackContainer.innerHTML = '';
        feedbackContainer.classList.remove('d-none', 'alert-success', 'alert-danger');
        
        if (data.correct) {
            feedbackContainer.classList.add('alert-success');
            feedbackContainer.innerHTML = '<i class="bi bi-check-circle-fill me-2"></i><strong>Correct!</strong> Great job!';
        } else {
            feedbackContainer.classList.add('alert-danger');
            feedbackContainer.innerHTML = `<i class="bi bi-x-circle-fill me-2"></i><strong>Incorrect!</strong> The correct answer is: <strong>${data.correct_answer}</strong>`;
        }
    }
    
    function highlightAnswers(selectedAnswer, correctAnswer) {
        const optionButtons = document.querySelectorAll('.option-btn');
        optionButtons.forEach(btn => {
            btn.classList.remove('btn-outline-primary', 'btn-primary', 'btn-secondary');
            
            if (btn.dataset.option === correctAnswer) {
                btn.classList.add('btn-success');
            } else if (btn.dataset.option === selectedAnswer && selectedAnswer !== correctAnswer) {
                btn.classList.add('btn-danger');
            } else {
                btn.classList.add('btn-secondary');
            }
        });
    }
    
    function showResults(score, total) {
        // Hide quiz content and show results
        quizContent.classList.add('d-none');
        resultsContainer.classList.remove('d-none');
        
        // Update the score
        finalScoreElement.textContent = score;
        finalTotalElement.textContent = total;
        
        // Set score message based on performance
        const percentage = (score / total) * 100;
        let message = '';
        
        if (percentage >= 90) {
            message = "Outstanding! You're an EU organization expert!";
        } else if (percentage >= 75) {
            message = "Great job! You really know your EU organizations!";
        } else if (percentage >= 60) {
            message = "Good work! You have solid knowledge of EU organizations.";
        } else if (percentage >= 40) {
            message = "Nice effort! You're on your way to becoming an EU organization expert.";
        } else {
            message = "Keep learning! With practice, you'll become familiar with EU organizations.";
        }
        
        scoreMessageElement.textContent = message;
    }
});
