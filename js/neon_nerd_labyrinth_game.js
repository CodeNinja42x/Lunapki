    // Labirent Oyunu
    const canvas = document.getElementById('gameCanvas');
    const ctx = canvas.getContext('2d');
    const tileSize = 40; // Her kutunun boyutu
    const player = { x: 0, y: 0 }; // Oyuncunun başlangıç pozisyonu
    const goal = { x: 9, y: 9 }; // Hedefin pozisyonu
    const maze = [
        [0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 1, 1, 1, 1, 1, 1, 1, 1, 0],
        [0, 1, 0, 0, 0, 0, 0, 0, 1, 0],
        [0, 1, 0, 1, 1, 1, 1, 0, 1, 0],
        [0, 1, 0, 1, 0, 0, 1, 0, 1, 0],
        [0, 1, 1, 1, 1, 1, 1, 0, 1, 0],
        [0, 0, 0, 0, 0, 0, 1, 0, 1, 0],
        [0, 1, 1, 1, 1, 1, 1, 0, 1, 0],
        [0, 1, 0, 0, 0, 0, 0, 0, 1, 0],
        [0, 1, 1, 1, 1, 1, 1, 1, 1, 0]
    ];

    function drawMaze() {
        for (let row = 0; row < maze.length; row++) {
            for (let col = 0; col < maze[row].length; col++) {
                if (maze[row][col] === 1) {
                    ctx.fillStyle = '#00ffff'; // Neon turkuaz
                } else {
                    ctx.fillStyle = '#111'; // Siyah
                }
                ctx.fillRect(col * tileSize, row * tileSize, tileSize, tileSize);
            }
        }

        // Oyuncu çizimi
        ctx.fillStyle = '#ff00ff'; // Neon pembe
        ctx.fillRect(player.x * tileSize, player.y * tileSize, tileSize, tileSize);

        // Hedef çizimi
        ctx.fillStyle = '#ffeb3b'; // Neon sarı
        ctx.fillRect(goal.x * tileSize, goal.y * tileSize, tileSize, tileSize);
    }

    function movePlayer(event) {
        const key = event.key;
        let newX = player.x;
        let newY = player.y;

        if (key === 'ArrowUp') newY--;
        if (key === 'ArrowDown') newY++;
        if (key === 'ArrowLeft') newX--;
        if (key === 'ArrowRight') newX++;

        // Hareket geçerli mi kontrol et (labirent dışına çıkma ve duvar kontrolü)
        if (newX >= 0 && newY >= 0 && newX < maze[0].length && newY < maze.length && maze[newY][newX] === 1) {
            player.x = newX;
            player.y = newY;
        }

        // Oyuncuyu yeniden çiz ve hedefe ulaşıp ulaşmadığını kontrol et
        drawMaze();
        checkWin();
    }

    function checkWin() {
        if (player.x === goal.x && player.y === goal.y) {
            document.getElementById('gameMessage').textContent = 'Congrats! You’ve helped NeonNerd escape!';
        }
    }

    // Labirenti çiz ve klavye olaylarını dinle
    drawMaze();
    window.addEventListener('keydown', movePlayer);
});
