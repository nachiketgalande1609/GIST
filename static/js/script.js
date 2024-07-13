// /////////////////////////////////////////////////////////////////////////
// --------------------------------BASE PAGE--------------------------------
// /////////////////////////////////////////////////////////////////////////


// Mark active page in the sidebar
document.addEventListener("DOMContentLoaded", function () {
    var links = document.querySelectorAll(".sidebar-link");
    var currentUrl = window.location.pathname;

    links.forEach(function (link) {
        if (link.getAttribute("href") === currentUrl) {
            link.classList.add("active");
        }
    });
});

// Confetti on Grammar and Stories Page

function openConfetti() {
    var myCanvas = document.createElement('canvas');
    myCanvas.style.position = 'absolute';
    myCanvas.style.top = '0';
    myCanvas.style.left = '0';
    myCanvas.style.zIndex = '10000';
    document.body.appendChild(myCanvas);
    myCanvas.style.width = '100%';
    var myConfetti = confetti.create(myCanvas, {
        resize: true,
        useWorker: true
    });
    myConfetti({
        particleCount: 500,
        spread: 1600
    });

    setTimeout(function() {
        myCanvas.parentNode.removeChild(myCanvas);
    }, 2000);
}


if (window.location.pathname == '/signup') {
    document.addEventListener("DOMContentLoaded", function() {
        const checkbox = document.getElementById("therapist_checkbox");
        const emailInputDiv = document.getElementById("therapist_email_input_div");

        checkbox.addEventListener("change", function() {
            if (checkbox.checked) {
                emailInputDiv.style.display = "none";
                console.log('Hidden');
            } else {
                emailInputDiv.style.display = "block";
            }
        });
    });
}

// ///////////////////////////////////////////////////////////////////////////////
// --------------------------------TALK TO ME PAGE--------------------------------
// ///////////////////////////////////////////////////////////////////////////////

// On the talk_to_me page, on page reload, speak "Hello!, Can you start by saying Whats your name"
if (window.location.pathname == '/talk_to_me') {
    window.onload = function () {
        // Welcome message
        fetch("/speak", {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ text: 'Hello!, Whats your name' })
        })
    };
}

// On talk_to_me page, on click of mic button start speech recognition and send message to OpenAI and create message block
function startSpeechRecognition(module) {
    var mic = document.getElementById('mic');
    var mic_btn = document.getElementById('mic-btn');
    mic.style.color = '#fff';
    mic.classList.remove('bi-mic');
    mic.classList.add('bi-mic-fill');
    mic_btn.classList.add('grow-shrink'); // Add animation class when starting speech recognition
    console.log('Speech recognition started.');
    const recognition = new webkitSpeechRecognition() || new SpeechRecognition();
    recognition.lang = 'en-US'; // Change to your desired language
    recognition.interimResults = true;

    let recognizedText = '';

    recognition.onresult = function (event) {
        let interimTranscript = '';
        for (let i = event.resultIndex; i < event.results.length; i++) {
            if (event.results[i].isFinal) {
                recognizedText += event.results[i][0].transcript;
            } else {
                interimTranscript += event.results[i][0].transcript;
            }
        }
    };

    recognition.onerror = function (event) {
        console.error('Speech recognition error:', event.error);
    };

    recognition.onend = function () {
        console.log('Speech recognition ended.');
        mic.style.color = '#fff';
        mic.classList.remove('bi-mic-fill');
        mic.classList.add('bi-mic');
        mic_btn.classList.remove('grow-shrink'); // Remove animation class when ending speech recognition
        createMessageBlock(recognizedText, 'self')
        fetch('/text_to_speech', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ text: recognizedText, module: module })
        })
            .then(response => response.json())
            .then(data => {
                if (window.location.pathname == '/talk_to_me') {
                    createMessageBlock(data.message, 'other')
                }
                console.log("Talking Over");
            })
            .catch(error => {
                console.error('Error in fetch:', error);
            });
        return recognizedText;
    };

    recognition.start();
}


// Talking animation(start) on talk_to_me page
function blinkTalkingIconStart() {
    var talking = document.getElementById('talking');
    var color = 'red';
    setInterval(function () {
        color = (color === 'red') ? 'black' : 'red';
        talking.style.transition = 'color 0.2s ease'; // Smooth transition for color change
        talking.style.color = color;
    }, 500); // Blink every 1000 milliseconds (1 second)
}

// Talking animation(stop) on talk_to_me page
function blinkTalkingIconStop() {
    var talking = document.getElementById('talking');
    talking.style.visibility = 'hidden'
}

// Function to create message block on talk_to_me page
function createMessageBlock(message, username) {
    const messagesDiv = document.getElementById('messages');
    const messageBlock = document.createElement('div');
    const messageCard = document.createElement('div');
    const messageCardBody = document.createElement('div');

    messageCardBody.classList.add('card-body');
    messageCardBody.innerHTML = message;

    messageCard.appendChild(messageCardBody);
    messageBlock.appendChild(messageCard);
    messagesDiv.appendChild(messageBlock);

    if (username === "self") {
        messageBlock.classList.add('d-flex', 'justify-content-end', 'message-block', 'mb-3');
        messageCard.classList.add('card', 'message-card-self', 'text-white');
    } else {
        typeText(messageCardBody, message, 50);
        messageBlock.classList.add('d-flex', 'message-block', 'mb-3');
        messageCard.classList.add('card', 'message-card', 'bg-light');
    }
    document.getElementById('messages').scrollTo(0, document.getElementById('messages').scrollHeight);
    return messageBlock;
};

// Typing effect on talk_to_me page
function typeText(element, text, speed) {
    let i = 0;
    element.innerHTML = ''; // Clear existing text
    const typingInterval = setInterval(() => {
        element.innerHTML += text.charAt(i);
        i++;
        if (i === text.length) {
            clearInterval(typingInterval);
        }
    }, speed);
}


// ////////////////////////////////////////////////////////////////////////////
// --------------------------------STORIES PAGE--------------------------------
// ////////////////////////////////////////////////////////////////////////////

// Update stories score
function update_stories_score(value) {
    fetch("/update_stories_score", {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ score: value })
    })
}

// On stories page, on click of submit button, show the answer modal and call update_stories_score() method
if (window.location.pathname == '/stories') {
    document.getElementById('submitBtn').addEventListener('click', function () {
        var questionGroups = document.querySelectorAll('input[type="radio"]:checked');

        questionGroups.forEach(function (radioButton) {
            var selectedAnswer = radioButton.value;
            var correctOption = document.querySelector('.correct');
            var correctAnswer = correctOption.value; // Get the value of the correct option

            var answerStatusMessage;
            var modalBackgroundColor;
            var showRetryButton = true; // Default value for showing the retry button
            if (selectedAnswer === correctAnswer) {
                openConfetti()
                answerStatusMessage = "Correct answer!";
                modalBackgroundColor = "#28a745";
                update_stories_score(1);
                showRetryButton = false; // Hide the retry button if the answer is correct
            } else {
                answerStatusMessage = "Incorrect answer! Please try again.";
                modalBackgroundColor = "#dc3545";
                update_stories_score(0);
            }

            document.getElementById('answerStatusMessage').innerText = answerStatusMessage;
            document.getElementById('modalContent').style.backgroundColor = modalBackgroundColor;

            // Show or hide the retry button based on the condition
            if (showRetryButton) {
                document.getElementById('retryButton').style.display = 'block';
            } else {
                document.getElementById('retryButton').style.display = 'none';
            }

            // Show the modal
            $('#answerStatusModal').modal('show');

            // Retry button functionality
            document.getElementById('retryButton').addEventListener('click', function () {
                $('#answerStatusModal').modal('hide');
            });
        });
    });
}

// ////////////////////////////////////////////////////////////////////////////
// --------------------------------GRAMMAR PAGE--------------------------------
// ////////////////////////////////////////////////////////////////////////////

// Update grammar score
function update_grammar_score(value) {
    fetch("/update_grammar_score", {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ score: value })
    })
}

// On grammar page, on click of submit button, show the answer modal and call update_grammar_score() method
if (window.location.pathname == '/grammar/quiz') {
    document.getElementById('submitBtn').addEventListener('click', function () {
        var questionGroups = document.querySelectorAll('input[type="radio"]:checked');

        questionGroups.forEach(function (radioButton) {
            var selectedAnswer = radioButton.value;
            var correctOption = document.querySelector('.correct');
            var correctAnswer = correctOption.value; // Get the value of the correct option

            var answerStatusMessage;
            var modalBackgroundColor;
            var showRetryButton = true;
            if (selectedAnswer === correctAnswer) {
                openConfetti()
                answerStatusMessage = "Correct answer!";
                modalBackgroundColor = "#28a745";
                update_grammar_score(1);
                showRetryButton = false;
            } else {
                answerStatusMessage = "Incorrect answer! Please try again.";
                modalBackgroundColor = "#dc3545";
                update_grammar_score(0);
            }

            document.getElementById('answerStatusMessage').innerText = answerStatusMessage;
            document.getElementById('modalContent').style.backgroundColor = modalBackgroundColor;

            if (showRetryButton) {
                document.getElementById('retryButton').style.display = 'block';
            } else {
                document.getElementById('retryButton').style.display = 'none';
            }

            // Show the modal
            $('#answerStatusModal').modal('show');

            document.getElementById('retryButton').addEventListener('click', function () {
                $('#answerStatusModal').modal('hide');
            });

        });
    });
}

// //////////////////////////////////////////////////////////////////////////
// --------------------------------VOCAB PAGE--------------------------------
// //////////////////////////////////////////////////////////////////////////

// On vocab page, on click of mic button, record the audio and save it on local directory
let isRecording = false;
let mediaRecorder;

function toggleRecord() {
    if (isRecording) {
        stopRecording();
    }
    else {
        isRecording = true;
        let chunks = [];
        const constraints = { audio: true };

        navigator.mediaDevices.getUserMedia(constraints)
            .then(function (stream) {
                mediaRecorder = new MediaRecorder(stream);

                mediaRecorder.ondataavailable = function (e) {
                    chunks.push(e.data);
                };

                mediaRecorder.onstop = function () {
                    const blob = new Blob(chunks, { 'type': 'audio/ogg; codecs=opus' });
                    chunks = [];
                    const formData = new FormData();
                    formData.append('audio', blob);
                    saveAudio(formData);
                };

                mediaRecorder.start();
                console.log('Recording started');
                document.getElementById('mic-icon').className = 'bi bi-stop';
                document.getElementById('vocab-mic-btn').classList.add('grow-shrink'); // Add animation class
            })
            .catch(function (error) {
                console.error('Error accessing microphone:', error);
            });
    }
}

function stopRecording() {
    mediaRecorder.stop();
    isRecording = false;
    console.log('Recording stopped');
    document.getElementById('mic-icon').className = 'bi bi-mic';
    document.getElementById('vocab-mic-btn').classList.remove('grow-shrink'); // Remove animation class
}

function saveAudio(formData) {
    fetch('/save-audio', {
        method: 'POST',
        body: formData
    })
        .then(function (response) {
            if (response.ok) {
                console.log('Audio recorded and saved successfully');
                setTimeout(() => {
                    document.getElementById('user-plot').style.visibility = 'visible';
                    document.getElementById('comparison-msg').style.visibility = 'visible';
                }, 500)
                return response.json(); // Parse response as JSON
            } else {
                console.error('Failed to save audio');
                throw new Error('Failed to save audio');
            }
        })
        .then(function (data) {
            // Extract filename from response
            const filename = data.filename;

            // Construct URL with filename
            const url = `/generate-waveform-plot?audio_file=${encodeURIComponent(filename)}`;

            // Make an AJAX request to generate waveform plot
            return fetch(url);
        })
        .then(function (response) {
            return response.json();
        })
        .then(function (data) {
            if (data.plot_url) {
                // Update the HTML to display the second image
                document.getElementById('your-voice-img').src = data.plot_url;
            }
        })
        .catch(function (error) {
            console.error('Error saving audio:', error);
        });
}





// Speak vocab words on click of speak button
function speakWord(word) {
    fetch("/speak", {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ text: word })
    })
        .then(response => response.json())
        .then(data => {
        })
        .catch(error => {
            console.error('There was a problem with the fetch operation:', error);
        });
}

// //////////////////////////////////////////////////////////////////////////////////
// --------------------------------PRONUNCIATION PAGE--------------------------------
// //////////////////////////////////////////////////////////////////////////////////

// On pronunciation page, function to highlight the clicked sound card
var selectedLetter = '';

function highlightLetterCard(card) {
    var allCards = document.querySelectorAll('.letter-card');
    allCards.forEach(function (card) {
        card.classList.remove('highlight');
    });

    card.classList.add('highlight');
    var letter = card.querySelector('h2').textContent.trim();

    // Store the selected letter in the variable
    selectedLetter = letter;
}

// On pronunciation page, on click of activity card, highlight the card and load the page in iframe
if (window.location.pathname == '/pronunciation') {
    var pww_btn = document.getElementById('prac-with-words-button');
    var tt_btn = document.getElementById('tongue-twisters-button');
    var ps_btn = document.getElementById('pronunciation-stories-button');
    var iframe = document.getElementById('pronunciation-iframe');
    var loadingIcon = document.getElementById('pronunciation-loading-icon');

    function showLoadingIcon() {
        loadingIcon.style.display = 'block';
    }

    function hideLoadingIcon() {
        loadingIcon.style.display = 'none';
    }

    function loadURL(url) {
        showLoadingIcon();
        iframe.src = url;
    }

    iframe.addEventListener('load', function () {
        hideLoadingIcon();
    });

    pww_btn.addEventListener('click', function () {
        tt_btn.classList.remove('active-btn');
        ps_btn.classList.remove('active-btn');
        this.classList.add('active-btn');
        var url = '/prac_with_words/p';
        loadURL(url);
    });

    tt_btn.addEventListener('click', function () {
        pww_btn.classList.remove('active-btn');
        ps_btn.classList.remove('active-btn');
        this.classList.add('active-btn');
        var url = '/tongue_twisters/p';
        loadURL(url);
    });

    ps_btn.addEventListener('click', function () {
        pww_btn.classList.remove('active-btn');
        tt_btn.classList.remove('active-btn');
        this.classList.add('active-btn');
        var url = '/stories/p';
        loadURL(url);
    });
}

// ////////////////////////////////////////////////////////////////////////////
// --------------------------------PROFILE PAGE--------------------------------
// ////////////////////////////////////////////////////////////////////////////

function submitProfileUpdateForm(event) {
    event.preventDefault();

    // Get form data
    var formData = new FormData(document.getElementById('updateProfileForm'));
    // Send fetch request
    fetch('/update_profile', {
        method: 'POST',
        body: formData
    })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            window.location.href = '/profile';
        })
        .catch(error => {
            alert('An error occurred while updating profile');
            console.error('Error:', error);
        });
}

function expandProfile(button) {
    var hiddenProfileItems = document.querySelectorAll('.profile-hidden');
    if (hiddenProfileItems.length > 0) {
        hiddenProfileItems.forEach(function (item) {
            if (item.style.display === 'none' || item.style.display === '') {
                item.style.display = 'block';
                button.innerHTML = 'View Less<i class="bi bi-chevron-up ms-2"></i>';
            } else {
                item.style.display = 'none';
                button.innerHTML = 'View More<i class="bi bi-chevron-down ms-2"></i>';
            }
        });
    } else {
        console.error("No elements with class '.profile-hidden' found.");
    }
}

function expandProgress(element) {
    var progressHidden = document.getElementById("progress-hidden");

    var grammarScoreElement = document.getElementById('grammar-perc');
    var grammar_score_perc = parseInt(grammarScoreElement.getAttribute('data-percent'));
    var storiesScoreElement = document.getElementById('stories-perc');
    var stories_score_perc = parseInt(storiesScoreElement.getAttribute('data-percent'));

    // Find the child <i> element within the parent element
    var childIcon = element.querySelector('#progress-expand-collapse-btn');

    if (progressHidden.style.display === "none") {
        animateScore(grammarScoreElement, grammar_score_perc);
        animateScore(storiesScoreElement, stories_score_perc);
        progressHidden.style.display = "block";

        // Remove class 'bi-chevron-down' from the child <i> element
        childIcon.classList.remove("bi-chevron-down");
        childIcon.classList.add("bi-chevron-up");
    } else {
        progressHidden.style.display = "none";

        // Add class 'bi-chevron-down' to the child <i> element
        childIcon.classList.remove("bi-chevron-up");
        childIcon.classList.add("bi-chevron-down");
    }
}
// Animate grammar and stories score percentage

function animateScore(element, target) {
    var duration = 1500; // Animation duration in milliseconds
    var interval = 15; // Interval between each update in milliseconds
    var frame = duration / interval;
    var increment = target / frame;
    var current = 0;

    var updateInterval = setInterval(function () {
        if (current < target) {
            element.textContent = Math.round(current) + '%';
            current += increment;
        } else {
            element.textContent = target + '%';
            clearInterval(updateInterval);
        }
    }, interval);
}

// /////////////////////////////////////////////////////////////////////
// --------------------------------OTHER--------------------------------

setTimeout(function () {
    var flashMessages = document.getElementsByClassName('flash-message');
    for (var i = 0; i < flashMessages.length; i++) {
        flashMessages[i].style.display = 'none';
    }
}, 3000);

