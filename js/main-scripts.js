document.addEventListener('DOMContentLoaded', function() {
    const synthwave = document.getElementById('synthwave');
    const muteButton = document.getElementById('muteButton');
    const neonNerd = document.querySelector('#neonNerd img');
    const secretMessage = document.getElementById('secretMessage');
    const button = document.querySelector('.neon-button');
    const chatMessages = document.getElementById('chat-messages');
    const chatInput = document.getElementById('chat-input');
    const chatSend = document.getElementById('chat-send');
    const canvas = document.getElementById('gameCanvas');
    const ctx = canvas.getContext('2d');
    const gameMessage = document.getElementById('gameMessage');
    const levelDisplay = document.getElementById('level');
    const timerDisplay = document.getElementById('timer');
    const scoreDisplay = document.getElementById('score');
    const startButton = document.getElementById('startButton');

    let level = 1;
    let score = 0;
    let timeLeft = 60;
    let gameInterval;
    let timerInterval;

    const levels = [
        [
            [1, 1, 1, 1, 1],
            [1, 0, 0, 0, 1],
            [1, 0, 1, 0, 1],
            [1, 0, 0, 0, 1],
            [1, 1, 1, 1, 1]
        ]
    ];

    let player = { x: 1, y: 1 };
    let target = { x: levels[level - 1][0].length - 2, y: levels[level - 1].length - 2 };

    function drawGame() {
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        levels[level - 1].forEach((row, y) => {
            row.forEach((cell, x) => {
                if (cell === 1) {
                    ctx.fillStyle = 'purple';
                    ctx.fillRect(x * 80, y * 80, 80, 80);
                }
            });
        });

        ctx.fillStyle = 'green';
        ctx.beginPath();
        ctx.arc(target.x * 80 + 40, target.y * 80 + 40, 20, 0, Math.PI * 2);
        ctx.fill();

        ctx.fillStyle = 'blue';
        ctx.beginPath();
        ctx.arc(player.x * 80 + 40, player.y * 80 + 40, 20, 0, Math.PI * 2);
        ctx.fill();
    }

    function movePlayer(dx, dy) {
        const newX = player.x + dx;
        const newY = player.y + dy;

        if (newX >= 0 && newX < levels[level - 1][0].length && newY >= 0 && newY < levels[level - 1].length && levels[level - 1][newY][newX] === 0) {
            player.x = newX;
            player.y = newY;
        }

        if (player.x === target.x && player.y === target.y) {
            clearInterval(gameInterval);
            clearInterval(timerInterval);
            score += timeLeft * 10;
            gameMessage.textContent = `You Win! Final Score: ${score}`;
            return;
        }

        drawGame();
    }

    function startGame() {
        scoreDisplay.textContent = score;
        timeLeft = 60;
        timerDisplay.textContent = timeLeft;

        gameInterval = setInterval(drawGame, 100);
        timerInterval = setInterval(() => {
            timeLeft--;
            timerDisplay.textContent = timeLeft;
            if (timeLeft <= 0) {
                clearInterval(gameInterval);
                clearInterval(timerInterval);
                gameMessage.textContent = `Game Over! Score: ${score}`;
            }
        }, 1000);

        document.addEventListener('keydown', function(event) {
            switch(event.key) {
                case 'ArrowUp': movePlayer(0, -1); break;
                case 'ArrowDown': movePlayer(0, 1); break;
                case 'ArrowLeft': movePlayer(-1, 0); break;
                case 'ArrowRight': movePlayer(1, 0); break;
            }
        });
    }

    startButton.addEventListener('click', startGame);

    // Chatbot
    chatSend.addEventListener('click', function() {
        const message = chatInput.value.trim();
        if (message) {
            chatMessages.innerHTML += `<div>User: ${message}</div>`;
            chatMessages.scrollTop = chatMessages.scrollHeight;
            chatInput.value = '';

            setTimeout(() => {
                chatMessages.innerHTML += `<div>NeonNerd: Beep boop! I heard you say "${message}".</div>`;
                chatMessages.scrollTop = chatMessages.scrollHeight;
            }, 1000);
        }
    });

    // Feedback form
    document.getElementById('showFeedback').addEventListener('click', function() {
        document.getElementById('feedback-form').style.display = 'block';
    });

    document.getElementById('feedbackForm').addEventListener('submit', function(e) {
        e.preventDefault();
        const feedback = document.getElementById('feedback').value;

        // Send data to Firebase
        firebase.database().ref('feedbacks').push({
            feedback: feedback,
            timestamp: new Date().toISOString()
        });

        document.getElementById('feedbackMessage').textContent = 'Thank you for your feedback!';
        document.getElementById('feedback-form').style.display = 'none';
    });
});
