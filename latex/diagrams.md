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
