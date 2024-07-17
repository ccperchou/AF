// Exemple pour ajouter une question
let questionCounter = 1;

function addQuestion() {
    questionCounter++;
    const container = document.getElementById('questions-container');

    const questionDiv = document.createElement('div');
    questionDiv.classList.add('form-group');
    questionDiv.id = `question${questionCounter}`;
    questionDiv.innerHTML = `
        <label>Question</label>
        <div class="d-flex align-items-center">
            <input type="text" class="form-control" name="question${questionCounter}" required>
            <button type="button" class="btn btn-sm btn-danger ml-2" onclick="deleteQuestion(${questionCounter})">Supprimer</button>
        </div>
        <div id="answers-container-${questionCounter}" class="mt-2"></div>
        <button type="button" class="btn btn-sm btn-primary mt-2" onclick="addAnswerField(${questionCounter})">Ajouter une réponse</button>
    `;

    container.appendChild(questionDiv);
}

// Appel de la fonction directement pour tester
// addQuestion(); // Décommentez cette ligne pour tester directement depuis la console

// Exemple pour ajouter une réponse
function addAnswerField(questionNumber) {
    const answersContainer = document.getElementById(`answers-container-${questionNumber}`);

    const answerCount = answersContainer.querySelectorAll('.form-group').length + 1;

    const answerDiv = document.createElement('div');
    answerDiv.classList.add('form-group', 'd-flex', 'align-items-center');
    answerDiv.innerHTML = `
        <label>Réponse</label>
        <input type="text" class="form-control ml-2" name="answer${questionNumber}_${answerCount}" required>
        <select class="form-control ml-2" name="correct${questionNumber}_${answerCount}">
            <option value="false">Réponse Fausse</option>
            <option value="true">Réponse Correcte</option>
        </select>
        <button type="button" class="btn btn-sm btn-danger ml-2" onclick="deleteAnswer(${questionNumber}, ${answerCount})">Supprimer</button>
    `;

    answersContainer.appendChild(answerDiv);
}
// Exemple pour supprimer une question
function deleteQuestion(questionNumber) {
    const questionDiv = document.getElementById(`question${questionNumber}`);
    questionDiv.remove(); // Utilisation de .remove() pour supprimer l'élément du DOM

    // Vous devrez peut-être appeler une fonction pour mettre à jour d'autres éléments après la suppression
    refreshQuestionNumbers(); // Assurez-vous d'appeler la fonction pour actualiser les numéros de question après la suppression
}

// Exemple pour supprimer une réponse
function deleteAnswer(questionNumber, answerCount) {
    const answersContainer = document.getElementById(`answers-container-${questionNumber}`);
    const answerDiv = document.getElementById(`answer${questionNumber}_${answerCount}`);
    answerDiv.remove(); // Utilisation de .remove() pour supprimer l'élément du DOM

    // Actualisez les numéros de réponse après la suppression
    refreshAnswerNumbers(answersContainer, questionNumber);
}

// Exemple de fonction pour actualiser les numéros de réponse après la suppression
function refreshAnswerNumbers(container, questionNumber) {
    const answerDivs = container.querySelectorAll('.form-group');
    answerDivs.forEach((div, index) => {
        const label = div.querySelector('label');
        label.textContent = `Réponse ${index + 1}:`; // Actualisez le texte de label si nécessaire
    });
}
// Function to delete an answer input field
function deleteAnswer(questionNumber, answerCount) {
    const answersContainer = document.getElementById(`answers-container-${questionNumber}`);
    const answerDiv = answersContainer.querySelector(`[name="answer${questionNumber}_${answerCount}"]`).closest('.form-group');
    if (answerDiv) {
        answersContainer.removeChild(answerDiv);
        refreshAnswerNumbers(answersContainer, questionNumber);
    }
}

// Function to refresh answer numbers after deletion
function refreshAnswerNumbers(container, questionNumber) {
    const answerDivs = container.querySelectorAll('.form-group');
    answerDivs.forEach((div, index) => {
        const label = div.querySelector('label');
        label.textContent = `Réponse ${index + 1}`;
        const inputs = div.querySelectorAll('input, select');
        inputs.forEach(input => {
            if (input.name.startsWith(`answer${questionNumber}_`)) {
                const newName = `answer${questionNumber}_${index + 1}`;
                input.name = newName;
            } else if (input.name.startsWith(`correct${questionNumber}_`)) {
                const newName = `correct${questionNumber}_${index + 1}`;
                input.name = newName;
            }
        });
        const button = div.querySelector('button');
        button.setAttribute('onclick', `deleteAnswer(${questionNumber}, ${index + 1})`);
    });
}

// Function to handle form submission
document.getElementById('question-form').addEventListener('submit', function(event) {
    event.preventDefault();
    // Gather form data
    const formData = new FormData(this);
    let formDataObject = {};
    for (const [key, value] of formData.entries()) {
        formDataObject[key] = value;
    }
    displayRecap(formDataObject);
});
// Fonction pour afficher le récapitulatif et la modal de confirmation
function displayRecapAndConfirm() {
    const formData = new FormData(document.getElementById('question-form'));
    let formDataObject = {};
    for (const [key, value] of formData.entries()) {
        formDataObject[key] = value;
    }
    displayRecap(formDataObject); // Afficher le récapitulatif dans la modal
}

// Fonction pour afficher le récapitulatif dans une popup
function displayRecap(formDataObject) {
    const recapContent = document.getElementById('recapContent');
    recapContent.innerHTML = '';

    Object.keys(formDataObject).forEach((key, index) => {
        const value = formDataObject[key];
        if (key.startsWith('question')) {
            const questionNumber = key.match(/\d+/)[0];
            recapContent.innerHTML += `<h5>Question ${questionNumber}: ${value}</h5>`;
            const answers = Object.keys(formDataObject).filter(answerKey => answerKey.startsWith(`answer${questionNumber}_`));
            answers.forEach(answerKey => {
                const answerNumber = answerKey.match(/\d+_\d+/)[0].split('_')[1];
                const isCorrect = formDataObject[`correct${questionNumber}_${answerNumber}`] === 'true';
                const answerClass = isCorrect ? 'correct-answer' : 'incorrect-answer';
                recapContent.innerHTML += `<p class="${answerClass}">Réponse ${answerNumber}: ${formDataObject[answerKey]}</p>`;
            });
        }
    });

    $('#recapModal').modal('show'); // Affiche la modal de récapitulatif
}

// Fonction pour gérer la confirmation d'envoi par email
function confirmForm() {
    // Récupérer toutes les questions et réponses du formulaire
    const formData = {
        questions: []
    };

    const questions = document.querySelectorAll('[id^="question"]');
    questions.forEach((questionElement, index) => {
        const questionText = questionElement.querySelector('input[name^="question"]').value;
        const answers = [];
        const answerElements = questionElement.querySelectorAll('input[name^="answer"]');
        answerElements.forEach(answerElement => {
            answers.push(answerElement.value);
        });
        formData.questions.push({
            question: questionText,
            answers: answers
        });
    });

    // Récupérer les adresses e-mail du champ d'entrée
    const emailInput = document.getElementById('email');
    const emailAddresses = emailInput.value.split(',').map(email => email.trim());

    // Envoyer les données du formulaire à votre backend avec fetch()
    fetch('/send-email', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ formData: formData, emails: emailAddresses }),
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert('Un e-mail de validation a été envoyé à votre adresse. Veuillez vérifier pour activer votre compte.');
        } else {
            alert('Erreur lors de l\'envoi de l\'e-mail de validation. Veuillez réessayer. ' + data.error);
        }
    })
    .catch((error) => {
        console.error('Error:', error);
    });

    // Après confirmation, vous pouvez cacher la modal si nécessaire
    $('#recapModal').modal('hide');
}
// Appel de la fonction directement pour tester
// addAnswerField(1); // Décommentez cette ligne pour tester directement depuis la console
