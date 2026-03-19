// ==================== CONSTANTS ====================
const FEN_TO_FILEPATH = {
    'P': 'white_pawn.png', 'N': 'white_knight.png', 'B': 'white_bishop.png',
    'R': 'white_rook.png', 'Q': 'white_queen.png', 'K': 'white_king.png',
    'p': 'black_pawn.png', 'n': 'black_knight.png', 'b': 'black_bishop.png',
    'r': 'black_rook.png', 'q': 'black_queen.png', 'k': 'black_king.png',
};

const BOT_LIST = [
    { value: "random", label: "Random", icon: "./assets/icon/random.png" },
    { value: "alphabeta", label: "AlphaBeta", icon: "./assets/icon/alphabeta.png" },
    { value: "mcts", label: "MCTS", icon: "./assets/icon/mcts.png"}
];

const SIDE_LIST = [
    { value: "white", label: "White", icon: "./assets/chess_img/white_king.png" },
    { value: "random", label: "Random", icon: "./assets/icon/random.png" },
    { value: "black", label: "Black", icon: "./assets/chess_img/black_king.png" }
];

const STARTING_POSITION = {
    a1: 'R', b1: 'N', c1: 'B', d1: 'Q', e1: 'K', f1: 'B', g1: 'N', h1: 'R',
    a2: 'P', b2: 'P', c2: 'P', d2: 'P', e2: 'P', f2: 'P', g2: 'P', h2: 'P',
    a8: 'r', b8: 'n', c8: 'b', d8: 'q', e8: 'k', f8: 'b', g8: 'n', h8: 'r',
    a7: 'p', b7: 'p', c7: 'p', d7: 'p', e7: 'p', f7: 'p', g7: 'p', h7: 'p',
};

const STARTING_FEN = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1';


// ==================== BOARD RENDERING ====================
function getPlayerSide(selectedSide) {
    if (selectedSide === 'random') {
        return Math.random() < 0.5 ? 'white' : 'black';
    }
    return selectedSide;
}

function createBoard(flipped = false) {
    const board = document.getElementById('chessboard');
    board.innerHTML = '';

    for (let row = 0; row < 8; row++) {
        for (let col = 0; col < 8; col++) {
            const square = document.createElement('div');
            square.classList.add('square');
            square.classList.add((row + col) % 2 === 1 ? 'dark' : 'light');
            
            // Flip logic
            const actualRow = flipped ? 7 - row : row;
            const actualCol = flipped ? 7 - col : col;
            
            const file = String.fromCharCode('a'.charCodeAt(0) + actualCol);
            const rank = 8 - actualRow;
            square.dataset.square = file + rank;
            
            board.appendChild(square);
        }
    }
}

function createCoordinates(flipped = false) {
    const ranksDiv = document.getElementById('ranks');
    const filesDiv = document.getElementById('files');
    
    ranksDiv.innerHTML = '';
    filesDiv.innerHTML = '';

    // Ranks
    const ranks = flipped ? [1,2,3,4,5,6,7,8] : [8,7,6,5,4,3,2,1];
    ranks.forEach(r => {
        const div = document.createElement('div');
        div.classList.add('rank-label');
        div.textContent = r;
        ranksDiv.appendChild(div);
    });

    // Files
    const files = flipped ? ['h','g','f','e','d','c','b','a'] : ['a','b','c','d','e','f','g','h'];
    files.forEach(f => {
        const div = document.createElement('div');
        div.classList.add('file-label');
        div.textContent = f;
        filesDiv.appendChild(div);
    });
}

function pieceImagePath(code) {
    return `./assets/chess_img/${FEN_TO_FILEPATH[code]}`;
}

function renderPieces(position) {
    document.querySelectorAll('#chessboard .square').forEach(sq => {
        const img = sq.querySelector('img.piece');
        if (img) sq.removeChild(img);
    });

    Object.entries(position).forEach(([squareName, pieceCode]) => {
        const sq = document.querySelector(`#chessboard .square[data-square="${squareName}"]`);
        if (!sq) return;

        const img = document.createElement('img');
        img.classList.add('piece');
        img.src = pieceImagePath(pieceCode);
        img.alt = pieceCode;
        sq.appendChild(img);
    });
}


// ==================== FEN HANDLING ====================
function fenToPosition(fen) {
    const boardPart = fen.split(' ')[0];
    const rows = boardPart.split('/');
    const position = {};
    
    for (let row = 0; row < 8; row++) {
        let col = 0;
        for (const char of rows[row]) {
            if (char >= '1' && char <= '8') {
                col += parseInt(char);
            } else {
                const file = String.fromCharCode('a'.charCodeAt(0) + col);
                const rank = 8 - row;
                position[file + rank] = char;
                col++;
            }
        }
    }
    
    return position;
}

function renderBoard(fen) {
    const position = fenToPosition(fen);
    renderPieces(position);
}


// ==================== UI SELECTION COMPONENTS ====================
function renderChoices(targetId, list, name, onSelect) {
    const container = document.getElementById(targetId);
    container.innerHTML = '';
    
    list.forEach(item => {
        const block = document.createElement('label');
        block.classList.add('choice-block');

        const radio = document.createElement('input');
        radio.type = "radio";
        radio.name = name;
        radio.value = item.value;
        radio.style.display = "none";
        block.appendChild(radio);

        block.onclick = () => {
            Array.from(container.children).forEach(e => e.classList.remove('selected'));
            block.classList.add('selected');
            radio.checked = true;
            if (onSelect) onSelect(item.value);
        };

        const iconBox = document.createElement('div');
        iconBox.classList.add('icon-box');

        const img = document.createElement('img');
        img.src = item.icon;
        img.alt = item.label;
        img.classList.add(item.value === 'white' || item.value === 'black' ? 'king-img' : 'icon');
        iconBox.appendChild(img);
        block.appendChild(iconBox);

        const span = document.createElement('span');
        span.textContent = item.label;
        span.classList.add('choice-label');
        block.appendChild(span);

        container.appendChild(block);
    });
}

function renderBotChoices(targetId) {
    renderChoices(targetId, BOT_LIST, 'bot', (botValue) => {
        document.getElementById('depth-picker').style.display = botValue === 'alphabeta' ? '' : 'none';
        document.getElementById('side-picker').style.display = '';
        renderSideChoices('side-list');
        document.getElementById('start-btn').style.display = 'none';
    });
}

function renderSideChoices(targetId) {
    renderChoices(targetId, SIDE_LIST, 'side', () => {
        document.getElementById('start-btn').style.display = '';
    });
}


// ==================== GETTERS ====================
function getSelected(selector) {
    const selected = document.querySelector(selector);
    if (!selected) return null;
    const radio = selected.querySelector('input[type=radio]');
    return radio?.value || null;
}

function getSelectedBot() {
    return getSelected('#bot-list .selected');
}

function getSelectedSide() {
    return getSelected('#side-list .selected');
}

function getAlphaBetaDepth() {
    return parseInt(document.getElementById('depth-range').value);
}


// ==================== PLAYER MOVE HANDLING ====================
function clearHighlights() {
    document.querySelectorAll('.selected').forEach(el => el.classList.remove('selected'));
    document.querySelectorAll('.move-hint').forEach(dot => dot.remove());
}

function highlightMoves(fromSquare, targets) {
    clearHighlights();
    
    document.querySelector(`#chessboard .square[data-square="${fromSquare}"]`)
        .classList.add('selected');

    targets.forEach(targetSquare => {
        const sq = document.querySelector(`#chessboard .square[data-square="${targetSquare}"]`);
        const dot = document.createElement('div');
        dot.classList.add('move-hint');
        sq.appendChild(dot);
    });
}

function disablePlayerUI() {
    document.querySelectorAll('#chessboard .square').forEach(sq => {
        sq.onclick = null;
    });
}

function getPlayerMove(legalMoves) {
    return new Promise((resolve) => {
        let fromSquare = null;

        document.querySelectorAll("#chessboard .square").forEach(sq => {
            sq.onclick = function() {
                const clickedSquare = this.dataset.square;

                if (fromSquare === null) {
                    if (legalMoves[clickedSquare]) {
                        fromSquare = clickedSquare;
                        highlightMoves(fromSquare, legalMoves[fromSquare]);
                    }
                } else {
                    const targets = legalMoves[fromSquare];
                    
                    if (targets?.includes(clickedSquare)) {
                        clearHighlights();
                        disablePlayerUI();
                        resolve({ from: fromSquare, to: clickedSquare });
                    } else {
                        clearHighlights();
                        fromSquare = null;
                    }
                }
            };
        });
    });
}


// ==================== RESULT POPUP ====================
function showResultPopup(result, playerSide) {
    const overlay = document.getElementById('result-overlay');
    const title = document.getElementById('result-title');
    const message = document.getElementById('result-message');
    
    if (result === 'draw') {
        title.textContent = 'Draw!';
        message.textContent = 'The game ended in a draw.';
    } else if (result === playerSide) {
        title.textContent = 'Victory!';
        message.textContent = 'Congratulations, you won!';
    } else {
        title.textContent = 'Defeat';
        message.textContent = 'Better luck next time!';
    }
    
    overlay.style.display = 'flex';
}

function hideResultPopup() {
    document.getElementById('result-overlay').style.display = 'none';
}


// ==================== RESET & NAVIGATION ====================
function resetSelections() {
    ['#bot-list', '#side-list'].forEach(selector => {
        document.querySelectorAll(`${selector} .selected`).forEach(el => {
            el.classList.remove('selected');
            const radio = el.querySelector('input[type=radio]');
            if (radio) radio.checked = false;
        });
    });
    
    const depthRange = document.getElementById('depth-range');
    const depthValue = document.getElementById('depth-value');
    depthRange.value = 1;
    depthValue.textContent = '1';
}

function hideAllSidebars() {
    document.getElementById('sidebar-game').style.display = 'none';
    document.getElementById('sidebar-offline').style.display = 'none';
    document.getElementById('side-picker').style.display = 'none';
    document.getElementById('start-btn').style.display = 'none';
    document.getElementById('depth-picker').style.display = 'none';
}

function returnToMainMenu() {
    hideResultPopup();
    hideAllSidebars();
    resetSelections();
    createBoard(false);
    createCoordinates(false);
    renderPieces(STARTING_POSITION);
    
    document.getElementById('sidebar-menu').style.display = '';

    if (socket && socket.connected) {
        socket.disconnect();
        socket = null;
    }
    
    currentRoomId = null;
    myColor = null;
    onlineCurrentFen = null;
    isMyTurn = false;
}


// ==================== MOVE HISTORY ====================
function renderMoveHistory(moveHistory) {
    const moveList = document.getElementById('move-list');
    moveList.innerHTML = '';

    for (let i = 0; i < moveHistory.length; i += 2) {
        const moveNumber = Math.floor(i / 2) + 1;
        const whiteMove = moveHistory[i];
        const blackMove = moveHistory[i + 1];
        
        const pair = document.createElement('div');
        pair.classList.add('move-pair');
        
        const numSpan = document.createElement('span');
        numSpan.classList.add('move-number');
        numSpan.textContent = `${moveNumber}.`;
        pair.appendChild(numSpan);
        
        const whiteSpan = document.createElement('span');
        whiteSpan.classList.add('white-move');
        whiteSpan.textContent = whiteMove;
        pair.appendChild(whiteSpan);
        
        if (blackMove) {
            const blackSpan = document.createElement('span');
            blackSpan.classList.add('black-move');
            blackSpan.textContent = blackMove;
            pair.appendChild(blackSpan);
        }
        
        moveList.appendChild(pair);
    }
    
    moveList.scrollTop = moveList.scrollHeight;
}


// ==================== GAME CONTROL ====================
function createResignController() {
    let resignResolve = null;
    
    const promise = new Promise((resolve) => {
        resignResolve = resolve;
    });
    
    return {
        promise: promise,
        trigger: () => resignResolve('resigned')
    };
}

async function conductGame(selectedSide, botType, depth) {
    // Determine actual player side (handle random)
    const playerSide = getPlayerSide(selectedSide);
    const flipped = playerSide === 'black';
    
    // Recreate board with flip if needed
    createBoard(flipped);
    createCoordinates(flipped);
    
    let currentFen = STARTING_FEN;
    let turn = (playerSide === "white") ? "player" : "bot";
    let moveHistory = [];
    
    // Render starting position
    renderBoard(currentFen);
    
    document.getElementById('sidebar-game').style.display = 'flex';
    renderMoveHistory(moveHistory);

    const resignController = createResignController();
    const resignBtn = document.getElementById('resign-btn');
    resignBtn.onclick = () => resignController.trigger();

    while (true) {
        const gameStatus = await eel.get_game_status(currentFen)();
        if (gameStatus.game_over) {
            resignBtn.onclick = null;
            return gameStatus.result;
        }

        let move = null;

        if (turn === 'player') {
            const legalMoves = await eel.get_legal_moves(currentFen)();
            
            const result = await Promise.race([
                getPlayerMove(legalMoves).then(m => ({ type: 'move', move: m })),
                resignController.promise.then(() => ({ type: 'resign' }))
            ]);
            
            if (result.type === 'resign') {
                resignBtn.onclick = null;
                return playerSide === 'white' ? 'black' : 'white';
            }
            
            move = result.move;
            currentFen = await eel.apply_move(currentFen, move.from, move.to)();
            turn = 'bot';
        } else {
            const result = await Promise.race([
                (async () => {
                    await new Promise(resolve => setTimeout(resolve, 1000));
                    const botMove = await eel.get_bot_move(currentFen, botType, depth)();
                    return { type: 'move', move: botMove };
                })(),
                resignController.promise.then(() => ({ type: 'resign' }))
            ]);
            
            if (result.type === 'resign') {
                resignBtn.onclick = null;
                return playerSide === 'white' ? 'black' : 'white';
            }
            
            move = result.move;
            currentFen = await eel.apply_move(currentFen, move.from, move.to, move.promotion)();
            turn = 'player';
        }

        moveHistory.push(move.from + move.to);
        renderMoveHistory(moveHistory);
        renderBoard(currentFen);
    }
}

let socket = null;
let currentRoomId = null;
let myColor = null;
let onlineCurrentFen = null;  
let isMyTurn = false;         


// ===== ONLINE FUNCTIONS =====
function initSocketConnection(hostIp) {
    socket = io(`http://${hostIp}:5000`);
    
    socket.on('game_created', (data) => {
        currentRoomId = data.room_id;
        myColor = data.color;
        document.getElementById('room-code').textContent = currentRoomId;
        document.getElementById('online-host').style.display = 'block';
    });
    
    socket.on('opponent_joined', () => {
        startOnlineGame();
    });
    
    socket.on('game_started', (data) => {
        myColor = data.color;
        onlineCurrentFen = data.fen; 
        startOnlineGame();
    });
    
    socket.on('move_made', (data) => {
        // Update FEN
        onlineCurrentFen = data.fen;
        
        // Render board
        renderBoard(data.fen);
        renderMoveHistory(data.move_history);
        
        // Determine whose turn
        const board = data.fen.split(' ')[1];
        const turnColor = board === 'w' ? 'white' : 'black';
        isMyTurn = (turnColor === myColor);
        
        // Re-enable clicks if my turn
        if (isMyTurn) {
            enableOnlineClicks();
        }
    });
    
    socket.on('game_over', (data) => {
        disablePlayerUI();
        showResultPopup(data.result, myColor);
    });
    
    socket.on('opponent_left', () => {
        disablePlayerUI();
        showResultPopup(myColor, myColor);
    });
    
    socket.on('error', (data) => {
        alert(data.message);
    });
}


async function startOnlineGame() {
    document.getElementById('sidebar-online').style.display = 'none';
    document.getElementById('sidebar-game').style.display = 'flex';
    
    const flipped = myColor === 'black';
    createBoard(flipped);
    createCoordinates(flipped);
    
    // Initialize FEN
    onlineCurrentFen = STARTING_FEN;
    renderBoard(onlineCurrentFen);
    
    // Clear move history
    document.getElementById('move-list').innerHTML = '';
    
    // Set initial turn
    isMyTurn = (myColor === 'white');
    
    // Enable clicks if it's my turn
    if (isMyTurn) {
        enableOnlineClicks();
    }
    
    // Setup resign
    document.getElementById('resign-btn').onclick = () => {
        if (confirm('Are you sure you want to resign?')) {
            socket.emit('resign', {
                room_id: currentRoomId
            });
        }
    };
}

function enableOnlineClicks() {
    let fromSquare = null;
    
    document.querySelectorAll("#chessboard .square").forEach(sq => {
        sq.onclick = null;
    });
    
    document.querySelectorAll("#chessboard .square").forEach(sq => {
        sq.onclick = async function() {
            // Kiểm tra lượt
            if (!isMyTurn) {
                return;
            }
            
            const clickedSquare = this.dataset.square;
            const legalMoves = await eel.get_legal_moves(onlineCurrentFen)();
            
            if (fromSquare === null) {
                if (legalMoves[clickedSquare]) {
                    const position = fenToPosition(onlineCurrentFen);
                    const piece = position[clickedSquare];
                    
                    if (piece) {
                        const isWhitePiece = piece === piece.toUpperCase();
                        const pieceColor = isWhitePiece ? 'white' : 'black';
                        
                        if (pieceColor === myColor) {
                            fromSquare = clickedSquare;
                            highlightMoves(fromSquare, legalMoves[fromSquare]);
                        }
                    }
                }
            } else {
                const targets = legalMoves[fromSquare];
                
                if (targets?.includes(clickedSquare)) {
                    clearHighlights();
                    isMyTurn = false;
                    disablePlayerUI();
                    
                    socket.emit('make_move', {
                        room_id: currentRoomId,
                        from: fromSquare,
                        to: clickedSquare
                    });
                    
                    fromSquare = null;
                } else {
                    clearHighlights();
                    fromSquare = null;
                }
            }
        };
    });
}


// ==================== EVENT HANDLERS & INITIALIZATION ====================
window.addEventListener('DOMContentLoaded', () => {
    // Offline mode
    document.getElementById('btn-offline').onclick = () => {
        document.getElementById('sidebar-menu').style.display = 'none';
        document.getElementById('sidebar-offline').style.display = 'flex';
        renderBotChoices('bot-list');
    };

    // Start game
    document.getElementById('start-btn').onclick = () => {
        const bot = getSelectedBot();
        const selectedSide = getSelectedSide();  // Giữ nguyên 'random'
        const depth = bot === "alphabeta" ? getAlphaBetaDepth() : null;

        document.getElementById('sidebar-offline').style.display = 'none';
        conductGame(selectedSide, bot, depth).then((result) => {
            const actualSide = getPlayerSide(selectedSide); // Get actual side for popup
            showResultPopup(result, actualSide);
        });
    };

    // Back button
    document.getElementById('btn-back').onclick = () => {
        document.getElementById('sidebar-offline').style.display = 'none';
        document.getElementById('sidebar-menu').style.display = '';
        hideAllSidebars();
    };

    // Result popup buttons
    document.getElementById('close-popup').onclick = hideResultPopup;
    document.getElementById('main-menu-btn').onclick = returnToMainMenu;

    // Depth slider
    const depthRange = document.getElementById('depth-range');
    const depthValue = document.getElementById('depth-value');
    depthRange.addEventListener('input', () => {
        depthValue.textContent = depthRange.value;
    });

    // Initialize board
    createBoard();
    createCoordinates();
    renderPieces(STARTING_POSITION);

    // Online button
    document.getElementById('btn-online').onclick = () => {
        document.getElementById('sidebar-menu').style.display = 'none';
        document.getElementById('sidebar-online').style.display = 'flex';
    };

    // Back button online
    document.getElementById('btn-back-online').onclick = () => {
        document.getElementById('sidebar-online').style.display = 'none';
        document.getElementById('sidebar-menu').style.display = '';
        
        // Reset online screens
        document.getElementById('online-menu').style.display = '';
        document.getElementById('online-host').style.display = 'none';
        document.getElementById('online-join').style.display = 'none';
    };

    // Create game
    document.getElementById('btn-create-game').onclick = async () => {
        const hostIp = await eel.get_local_ip()();
        document.getElementById('host-ip').textContent = hostIp;
        
        initSocketConnection(hostIp); 
        socket.emit('create_game');
        
        document.getElementById('online-menu').style.display = 'none';
        document.getElementById('online-host').style.display = 'block';
    };

    // Join game
    document.getElementById('btn-join-game').onclick = () => {
        document.getElementById('online-menu').style.display = 'none';
        document.getElementById('online-join').style.display = 'block';
    };

    document.getElementById('btn-connect').onclick = () => {
        const hostIp = document.getElementById('input-host-ip').value;
        const roomCode = document.getElementById('input-room-code').value;
        
        if (!hostIp || !roomCode) {
            alert('Please enter both Host IP and Room Code');
            return;
        }
        
        currentRoomId = roomCode.toUpperCase();
        
        initSocketConnection(hostIp);
        socket.emit('join_game', {room_id: currentRoomId});
    };
});
