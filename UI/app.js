const FEN_TO_FILEPATH = {
    'P': 'white_pawn.png', 'N': 'white_knight.png', 'B': 'white_bishop.png',
    'R': 'white_rook.png', 'Q': 'white_queen.png', 'K': 'white_king.png',
    'p': 'black_pawn.png', 'n': 'black_knight.png', 'b': 'black_bishop.png',
    'r': 'black_rook.png', 'q': 'black_queen.png', 'k': 'black_king.png',
};

const BOT_LIST = [
    { value: "random", label: "Random Move", icon: "./assets/icon/random.png" },
    { value: "alphabeta", label: "Alpha-Beta Pruning", icon: "./assets/icon/alphabeta.png" },
    { value: "mcts", label: "Monte Carlo Tree Search", icon: "./assets/icon/mcts.png"}
];

const SIDE_LIST = [
    { value: "white", label: "White Pieces", icon: `./assets/chess_img/${FEN_TO_FILEPATH['K']}` },
    { value: "random", label: "Random Side", icon: "./assets/icon/random.png" },
    { value: "black", label: "Black Pieces", icon: `./assets/chess_img/${FEN_TO_FILEPATH['k']}` }
];

const STARTING_FEN = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1';

function playSound(type) {
    const audio = document.getElementById(`snd-${type}`);
    if (audio) { audio.currentTime = 0; audio.play().catch(e => console.warn(e)); }
}

function requestNotificationPermission() {
    if ("Notification" in window) Notification.requestPermission();
}

function notifyAIMove(moveStr) {
    if ("Notification" in window && Notification.permission === "granted") {
        new Notification("Chess AI Intro", { body: `AI has made a move: ${moveStr}` });
    }
}

function getPlayerSide(selectedSide) {
    if (selectedSide === 'random') return Math.random() < 0.5 ? 'white' : 'black';
    return selectedSide;
}

function createBoard(flipped = false) {
    const board = document.getElementById('chessboard'); board.innerHTML = '';
    for (let row = 0; row < 8; row++) {
        for (let col = 0; col < 8; col++) {
            const square = document.createElement('div');
            square.classList.add('square'); square.classList.add((row + col) % 2 === 1 ? 'dark' : 'light');
            const actualRow = flipped ? 7 - row : row, actualCol = flipped ? 7 - col : col;
            square.dataset.square = String.fromCharCode('a'.charCodeAt(0) + actualCol) + (8 - actualRow);
            board.appendChild(square);
        }
    }
}

function createCoordinates(flipped = false) {
    const ranksDiv = document.getElementById('ranks'), filesDiv = document.getElementById('files');
    ranksDiv.innerHTML = ''; filesDiv.innerHTML = '';
    const ranks = flipped ? [1,2,3,4,5,6,7,8] : [8,7,6,5,4,3,2,1];
    ranks.forEach(r => { const div = document.createElement('div'); div.classList.add('rank-label'); div.textContent = r; ranksDiv.appendChild(div); });
    const files = flipped ? ['h','g','f','e','d','c','b','a'] : ['a','b','c','d','e','f','g','h'];
    files.forEach(f => { const div = document.createElement('div'); div.classList.add('file-label'); div.textContent = f; filesDiv.appendChild(div); });
}

function renderBoard(fen) {
    if (!fen) return;
    const rows = fen.split(' ')[0].split('/');
    document.querySelectorAll('#chessboard .square').forEach(sq => { const img = sq.querySelector('img.piece'); if (img) sq.removeChild(img); });
    for (let row = 0; row < 8; row++) {
        let col = 0;
        for (const char of rows[row]) {
            if (char >= '1' && char <= '8') col += parseInt(char);
            else {
                const sq = document.querySelector(`#chessboard .square[data-square="${String.fromCharCode('a'.charCodeAt(0) + col)}${8 - row}"]`);
                if (sq) {
                    const img = document.createElement('img');
                    img.classList.add('piece');
                    img.src = `./assets/chess_img/${FEN_TO_FILEPATH[char]}`;
                    sq.appendChild(img);
                }
                col++;
            }
        }
    }
}

function getPlayerMove(legalMoves) {
    return new Promise((resolve) => {
        let fromSquare = null;
        const squares = document.querySelectorAll("#chessboard .square");
        const resignBtn = document.getElementById('resign-btn');
        
        const cleanup = () => {
            squares.forEach(s => s.onclick = null);
            resignBtn.removeEventListener('click', onResign);
        };

        const onResign = () => {
            cleanup();
            resolve(null);
        };

        resignBtn.addEventListener('click', onResign);

        squares.forEach(sq => {
            sq.onclick = function() {
                const clicked = this.dataset.square;
                if (fromSquare === null && legalMoves[clicked]) { fromSquare = clicked; highlight(fromSquare, legalMoves[fromSquare]); }
                else if (fromSquare && legalMoves[fromSquare]?.includes(clicked)) { 
                    clearHi(); 
                    cleanup();
                    resolve({ from: fromSquare, to: clicked }); 
                }
                else { clearHi(); fromSquare = null; }
            };
        });
    });
}

function highlight(from, targets) {
    clearHi(); 
    const startSq = document.querySelector(`#chessboard .square[data-square="${from}"]`);
    if (startSq) startSq.classList.add('selected');
    targets.forEach(t => {
        const sq = document.querySelector(`#chessboard .square[data-square="${t}"]`);
        if (sq) {
            const dot = document.createElement('div'); dot.classList.add('move-hint');
            if (sq.querySelector('.piece')) { dot.style.width = '80%'; dot.style.height = '80%'; dot.style.background = 'transparent'; dot.style.border = '6px solid rgba(0,0,0,0.1)'; }
            sq.appendChild(dot);
        }
    });
}

function clearHi() { document.querySelectorAll('.selected').forEach(e => e.classList.remove('selected')); document.querySelectorAll('.move-hint').forEach(d => d.remove()); }
function clearLastMove() { document.querySelectorAll('.last-move').forEach(e => e.classList.remove('last-move')); }
function highlightLastMove(from, to) {
    clearLastMove();
    document.querySelector(`#chessboard .square[data-square="${from}"]`)?.classList.add('last-move');
    document.querySelector(`#chessboard .square[data-square="${to}"]`)?.classList.add('last-move');
}

async function conductGame(side, botType, params) {
    const flipped = side === 'black';
    createBoard(flipped); createCoordinates(flipped);
    let currentFen = STARTING_FEN, turn = (side === "white") ? "player" : "bot", history = [];
    renderBoard(currentFen); document.getElementById('sidebar-game').style.display = 'flex';
    clearLastMove();
    
    document.getElementById('resign-btn').style.display = 'block';
    document.getElementById('game-back-btn').style.display = 'none';

    let isResigned = false;
    document.getElementById('resign-btn').onclick = () => isResigned = true;

    while (true) {
        if (isResigned) {
            document.getElementById('resign-btn').style.display = 'none';
            document.getElementById('game-back-btn').style.display = 'block';
            return { result: side === 'white' ? 'black' : 'white' };
        }
        try {
            const status = await eel.get_game_status(currentFen)();
            if (status.game_over) { 
                playSound('game-over'); 
                document.getElementById('resign-btn').style.display = 'none';
                document.getElementById('game-back-btn').style.display = 'block';
                return { result: status.result }; 
            }

            let move = null, result = null;
            if (turn === 'player') {
                move = await getPlayerMove(await eel.get_legal_moves(currentFen)());
                if (!move) continue; // Might be resigned
                result = await eel.apply_move(currentFen, move.from, move.to)();
                turn = 'bot';
            } else {
                await new Promise(r => setTimeout(r, 600));
                move = await eel.get_bot_move(currentFen, botType, params)();
                if (!move) break;
                result = await eel.apply_move(currentFen, move.from, move.to, move.promotion)();
                turn = 'player';
                notifyAIMove(result.san);
            }

            if (result.san.includes('+')) playSound('check');
            else if (result.san.includes('x')) playSound('capture');
            else playSound('move');

            currentFen = result.fen;
            highlightLastMove(move.from, move.to);
            history.push(result.san);
            renderHistory(history); renderBoard(currentFen);
        } catch (e) { console.error(e); return { result: 'error' }; }
    }
    return { result: 'error' };
}

function renderHistory(history) {
    const list = document.getElementById('move-list'); list.innerHTML = '';
    for (let i = 0; i < history.length; i += 2) {
        const div = document.createElement('div'); div.classList.add('move-pair');
        div.innerHTML = `<span class="move-number">${Math.floor(i/2)+1}.</span><span>${history[i]}</span><span>${history[i+1] || ''}</span>`;
        list.appendChild(div);
    }
    list.scrollTop = list.scrollHeight;
}

function showPopup(res, side) {
    if (res === 'error') return;
    document.getElementById('result-overlay').style.display = 'flex';
    document.getElementById('result-title').textContent = res === 'draw' ? 'Draw!' : (res === side ? 'Victory!' : 'Defeated');
    document.getElementById('result-message').textContent = res === 'draw' ? 'No moves left.' : (res === side ? 'Checkmate! Well played.' : 'AI is too strong.');
}

function renderChoices(targetId, list, name, onSelect) {
    const container = document.getElementById(targetId); container.innerHTML = '';
    list.forEach(item => {
        const block = document.createElement('label'); block.classList.add('choice-block');
        block.innerHTML = `<input type="radio" name="${name}" value="${item.value}" style="display:none"><div class="icon-box"><img src="${item.icon}"></div><span>${item.label}</span>`;
        block.onclick = () => { Array.from(container.children).forEach(e => e.classList.remove('selected')); block.classList.add('selected'); block.querySelector('input').checked = true; if (onSelect) onSelect(item.value); };
        container.appendChild(block);
    });
}

window.addEventListener('DOMContentLoaded', () => {
    requestNotificationPermission();
    
    document.getElementById('btn-offline').onclick = () => { 
        document.getElementById('sidebar-menu').style.display = 'none'; 
        document.getElementById('sidebar-offline').style.display = 'flex'; 
        
        // Reset settings visibility for new session
        document.getElementById('alphabeta-settings').style.display = 'none'; 
        document.getElementById('mcts-settings').style.display = 'none'; 
        document.getElementById('side-picker').style.display = 'none'; 
        document.getElementById('start-btn').style.display = 'none';

        renderChoices('bot-list', BOT_LIST, 'bot', (v) => { 
            document.getElementById('alphabeta-settings').style.display = v === 'alphabeta' ? '' : 'none'; 
            document.getElementById('mcts-settings').style.display = v === 'mcts' ? '' : 'none'; 
            document.getElementById('side-picker').style.display = ''; 
            renderChoices('side-list', SIDE_LIST, 'side', () => document.getElementById('start-btn').style.display = ''); 
        }); 
    };

    document.getElementById('start-btn').onclick = () => { 
        const bot = document.querySelector('#bot-list .selected input')?.value;
        const selectedSide = document.querySelector('#side-list .selected input')?.value;
        if (!bot || !selectedSide) return;

        const actualSide = getPlayerSide(selectedSide);
        
        const params = {
            bot: bot,
            depth: parseInt(document.getElementById('depth-range').value),
            q_depth: parseInt(document.getElementById('q-depth-range').value),
            iterations: parseInt(document.getElementById('iter-range').value),
            rollout_depth: parseInt(document.getElementById('rollout-range').value)
        };

        document.getElementById('sidebar-offline').style.display = 'none';
        conductGame(actualSide, bot, params).then(data => showPopup(data.result, actualSide));
    };

    document.getElementById('btn-back').onclick = () => { document.getElementById('sidebar-offline').style.display = 'none'; document.getElementById('sidebar-menu').style.display = 'flex'; };
    const toMenu = () => { 
        document.getElementById('result-overlay').style.display = 'none'; 
        document.getElementById('sidebar-game').style.display = 'none'; 
        document.getElementById('sidebar-offline').style.display = 'none'; 
        document.getElementById('sidebar-menu').style.display = 'flex'; 
        createBoard(); renderBoard(STARTING_FEN); 
    };

    document.getElementById('main-menu-btn').onclick = toMenu;
    document.getElementById('game-back-btn').onclick = toMenu;
    document.getElementById('close-popup').onclick = () => document.getElementById('result-overlay').style.display = 'none';
    
    // Update Slider Labels
    const sliders = [
        { id: 'depth-range', val: 'depth-value' },
        { id: 'q-depth-range', val: 'q-depth-value' },
        { id: 'iter-range', val: 'iter-value' },
        { id: 'rollout-range', val: 'rollout-value' }
    ];
    sliders.forEach(s => {
        const el = document.getElementById(s.id);
        if (el) el.oninput = function() { document.getElementById(s.val).textContent = this.value; };
    });

    createBoard(); renderBoard(STARTING_FEN);
});
