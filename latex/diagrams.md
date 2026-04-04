# Biểu đồ thuật toán Alpha-Beta Pruning (Negamax & Quiescence Search)

## 1. Sơ đồ luồng điều khiển tích hợp Quiescence Search
Sơ đồ này mô tả cấu trúc của Negamax kết hợp với Quiescence Search để giải quyết "hiệu ứng đường chân trời".

```mermaid
graph TD
    Start([Bắt đầu Negamax]) --> CheckCache{Có trong<br/>Transposition Table?}
    CheckCache -- Có --> ReturnCache[Trả về giá trị từ bộ nhớ đệm]
    CheckCache -- Không --> CheckDepth{Độ sâu = 0?}
    
    CheckDepth -- Đúng --> CallQ[Gọi Quiescence Search]
    CheckDepth -- Không --> LoopMoves[Sắp xếp & Duyệt từng nước đi]
    
    subgraph Quiescence_Search [Tìm kiếm tĩnh - Chỉ xét ăn quân]
        CallQ --> StandPat[Đánh giá tĩnh - Stand Pat]
        StandPat --> QAlpha{score >= beta?}
        QAlpha -- Đúng --> ReturnBetaQ[Trả về beta]
        QAlpha -- Không --> LoopCaptures[Duyệt các nước đi ăn quân]
        LoopCaptures --> RecurQ[Gọi đệ quy Quiescence]
        RecurQ --> UpdateQAlpha[Cập nhật score & alpha]
        UpdateQAlpha --> QBeta{alpha >= beta?}
        QBeta -- Đúng --> ReturnBetaQ
        QBeta -- Không --> MoreCaptures{Còn nước ăn quân?}
        MoreCaptures -- Còn --> LoopCaptures
        MoreCaptures -- Hết --> ReturnAlphaQ[Trả về alpha]
    end
    
    LoopMoves --> RecurNegamax[Gọi đệ quy -Negamax<br/>alpha = -beta, beta = -alpha]
    RecurNegamax --> UpdateBest[best_value = max best_value, -score]
    UpdateBest --> UpdateAlpha[alpha = max alpha, best_value]
    UpdateAlpha --> Prune{alpha >= beta?}
    Prune -- Đúng --> StoreTT[Lưu vào Transposition Table]
    Prune -- Không --> MoreMoves{Còn nước đi?}
    MoreMoves -- Còn --> LoopMoves
    MoreMoves -- Hết --> StoreTT
    
    StoreTT --> ReturnBest[Trả về best_value]
    ReturnCache --> End([Kết thúc])
    ReturnBest --> End
    ReturnAlphaQ --> End
    ReturnBetaQ --> End
```

## 2. Luồng Logic Đánh giá (Evaluation Flow)
Sơ đồ mô tả cách hàm `evaluate` tính toán điểm số thế trận.

```mermaid
flowchart TD
    Eval[Bắt đầu Evaluate] --> Base{Kiểm tra trạng thái đặc biệt}
    Base -- Chiếu bí --> ScoreMate[+/- 99999]
    Base -- Hòa/Hết quân --> ScoreZero[0]
    Base -- Bình thường --> DetectEndgame[Nhận diện giai đoạn: Endgame?]
    
    DetectEndgame --> LoopSquares[Duyệt qua 64 ô trên bàn cờ]
    LoopSquares --> GetPiece{Ô có quân cờ?}
    GetPiece -- Có --> CalcValue[Lấy Material Value]
    CalcValue --> GetPST[Lấy điểm Position Square Table]
    
    subgraph PST_Logic [Logic Bảng điểm vị trí]
        GetPST --> IsKing{Quân Vua?}
        IsKing -- Đúng --> KingStage{Endgame?}
        KingStage -- Sai --> PST_Mid[Sử dụng KING_MID]
        KingStage -- Đúng --> PST_End[Sử dụng KING_END]
        IsKing -- Không --> PST_Standard[Sử dụng bảng theo loại quân]
    end
    
    PST_Logic --> SumScore[score += material + position]
    SumScore --> MoreSquares{Hết 64 ô?}
    MoreSquares -- Chưa --> LoopSquares
    MoreSquares -- Rồi --> FinalScore[Trả về score theo lượt đi]
```

## 3. Biểu đồ logic flow thuật toán MCTS
Sơ đồ dưới đây bám theo luồng chính trong `model/mcts.py`: lặp `select -> expand -> simulate -> backpropagate`, có dừng sớm khi trạng thái được chứng minh (proven value), rồi chọn nước đi cuối cùng theo độ ưu tiên.

```mermaid
flowchart TD
    A([Bắt đầu mcts board iterations rollout_depth]) --> B[Tạo root Node]
    B --> C{Lặp i từ 0 đến iterations-1}

    C --> D{root.proven_value khác None?}
    D -- Có --> E[Dừng sớm early exit]
    D -- Không --> F[select root]

    subgraph S1 [Select]
        F --> F1{node có children?}
        F1 -- Không --> F8[Trả node hiện tại]
        F1 -- Có --> F2[Lọc children không proven loss]
        F2 --> F3{available rỗng?}
        F3 -- Có --> F8
        F3 -- Không --> F4{Có child chưa visit?}
        F4 -- Có --> F5[Chọn ngẫu nhiên 1 child chưa visit]
        F4 -- Không --> F6[Chọn child max UCT]
        F6 --> F1
        F5 --> F8
    end

    F8 --> G[expand node]

    subgraph S2 [Expand]
        G --> G1{node đã có children?}
        G1 -- Có --> G5[Giữ nguyên node]
        G1 -- Không --> G2[Lấy legal moves]
        G2 --> G3{Có nước đi hợp lệ?}
        G3 -- Không --> G5
        G3 -- Có --> G4[Tạo child cho từng move]
        G4 --> G6[Chọn ngẫu nhiên 1 child để rollout]
    end

    G5 --> H[simulate node.board.copy]
    G6 --> H

    subgraph S3 [Simulate]
        H --> H1[Thiết lập is_endgame, effective_depth, epsilon]
        H1 --> H2{Game over hoặc đạt depth?}
        H2 -- Chưa --> H3[greedy_move epsilon-greedy]
        H3 --> H4{move None?}
        H4 -- Có --> H6[Tính evaluate board]
        H4 -- Không --> H5[push move, depth+1]
        H5 --> H2
        H2 -- Rồi --> H6
        H6 --> H7[Chuẩn hóa dấu theo phía người chơi ban đầu]
    end

    H7 --> I[backpropagate node result]

    subgraph S4 [Backpropagate]
        I --> I1{node tồn tại?}
        I1 -- Không --> I9[Kết thúc lan truyền]
        I1 -- Có --> I2[visits += 1, value += result]
        I2 --> I3[min_result = min min_result result]
        I3 --> I4{node.board game_over?}
        I4 -- Có --> I5[Gán proven_value draw hoặc loss]
        I4 -- Không --> I6[_update_proven_value từ children]
        I5 --> I6
        I6 --> I7[result = -result]
        I7 --> I8[node = parent]
        I8 --> I1
    end

    I9 --> C
    E --> J{root có children?}
    C --> J

    J -- Không --> K[Trả None]
    J -- Có --> L[Sắp xếp children theo visits giảm dần]
    L --> M{Có child proven win?}
    M -- Có --> N[Trả move proven win]
    M -- Không --> O[Lọc candidates không proven loss]
    O --> P{candidates rỗng?}
    P -- Có --> Q[Dùng toàn bộ root.children]
    P -- Không --> R[Giữ candidates]
    Q --> S[Chọn child visits lớn nhất]
    R --> S
    S --> T[Trả best move]

    K --> U([Kết thúc])
    N --> U
    T --> U
```

## 4. Mã giả 4 giai đoạn của MCTS
Phần này tách riêng từng giai đoạn cốt lõi để dễ trình bày trong báo cáo.

### 4.1 Selection
```text
FUNCTION SELECT(node):
    WHILE node has children:
        available <- children with proven_value != -INF
        IF available is empty:
            RETURN node

        unvisited <- children in available with visits = 0
        IF unvisited is not empty:
            RETURN RANDOM_CHOICE(unvisited)

        node <- ARGMAX(available, UCT)

    RETURN node
```

### 4.2 Expansion
```text
FUNCTION EXPAND(node):
    IF node already has children:
        RETURN node

    moves <- LEGAL_MOVES(node.board)
    IF moves is empty:
        RETURN node

    FOR each move in moves:
        b <- COPY(node.board)
        PUSH(b, move)
        ADD_CHILD(node, NEW_NODE(b, parent=node))

    RETURN RANDOM_CHOICE(node.children)
```

### 4.3 Simulation (Rollout)
```text
FUNCTION SIMULATE(board, rollout_depth):
    mover <- OPPOSITE(board.turn)
    depth <- 0

    total_pieces <- COUNT_PIECES(board)
    is_endgame <- (total_pieces <= 16)

    IF is_endgame:
        effective_depth <- MAX(rollout_depth, 20)
        epsilon <- 0.15
        top_k <- 3
    ELSE:
        effective_depth <- rollout_depth
        epsilon <- 0.35
        top_k <- 5

    WHILE NOT GAME_OVER(board) AND depth < effective_depth:
        move <- GREEDY_MOVE(board, top_k, epsilon)
        IF move is NONE:
            BREAK
        PUSH(board, move)
        depth <- depth + 1

    result <- EVALUATE(board)

    IF ABS(result) > 0.9:
        speed <- (effective_depth - depth + 1) / (effective_depth + 1)
        result <- result * (0.95 + 0.05 * speed)

    IF mover == WHITE:
        RETURN result
    ELSE:
        RETURN -result
```

### 4.4 Backpropagation
```text
FUNCTION BACKPROPAGATE(node, result):
    WHILE node is not NULL:
        node.visits <- node.visits + 1
        node.value <- node.value + result
        node.min_result <- MIN(node.min_result, result)

        IF GAME_OVER(node.board):
            outcome <- OUTCOME(node.board)
            IF outcome.winner is NULL:
                node.proven_value <- 0.0
            ELSE:
                node.proven_value <- -INF

        UPDATE_PROVEN_VALUE_FROM_CHILDREN(node)

        result <- -result
        node <- node.parent
```

### 4.5 Khung vòng lặp MCTS đầy đủ
```text
FUNCTION MCTS(board, iterations, rollout_depth):
    root <- NEW_NODE(board)

    FOR i from 0 to iterations - 1:
        IF root.proven_value is not NULL:
            BREAK

        node <- SELECT(root)
        node <- EXPAND(node)
        result <- SIMULATE(COPY(node.board), rollout_depth)
        BACKPROPAGATE(node, result)

    IF root has no children:
        RETURN NONE

    proven_wins <- children of root with proven_value = +INF
    IF proven_wins is not empty:
        RETURN MOVE_OF(proven_wins[0])

    candidates <- children of root with proven_value != -INF
    IF candidates is empty:
        candidates <- root.children

    best <- ARGMAX(candidates, visits)
    RETURN MOVE_OF(best)
```
