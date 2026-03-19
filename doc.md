# Tài liệu Thuật toán Cờ vua (Chess AI Algorithms)

Dự án này triển khai hai thuật toán AI cờ vua phổ biến: **Alpha-Beta Pruning** và **Monte Carlo Tree Search (MCTS)**.

---

## 1. Thuật toán Alpha-Beta Pruning (4/10)

### Tổng quan
Alpha-Beta Pruning là một phiên bản cải tiến của thuật toán **Minimax**, giúp giảm đáng kể số lượng các nút cần đánh giá trong cây trò chơi bằng cách loại bỏ các nhánh không ảnh hưởng đến kết quả cuối cùng.

### Cơ chế hoạt động
Thuật toán duy trì hai giá trị:
*   **Alpha**: Giá trị tối đa mà người chơi Max có thể đảm bảo.
*   **Beta**: Giá trị tối thiểu mà người chơi Min có thể đảm bảo.

Khi duyệt cây, nếu tại một nút nào đó mà `Beta <= Alpha`, chúng ta có thể dừng duyệt nhánh đó (cắt tỉa) vì kết quả của nó chắc chắn không thay đổi được quyết định ở các nút cha.

### Hàm đánh giá (Heuristic)
Do không thể duyệt đến tận cùng của ván cờ, AI sử dụng hàm đánh giá để ước tính "điểm" của một thế trận tại một độ sâu nhất định:
*   **Material Score**: Tổng giá trị các quân cờ (Tốt=100, Mã=320, ...).
*   **Position Score (PST)**: Điểm cộng/trừ dựa trên vị trí của quân cờ trên bàn (ví dụ: Mã ở trung tâm mạnh hơn ở góc).

---

## 2. Monte Carlo Tree Search - MCTS (4/10)

### Tổng quan
Khác với Alpha-Beta dựa trên tìm kiếm vét cạn, MCTS là một thuật toán dựa trên xác suất. Nó xây dựng cây trò chơi bằng cách mô phỏng hàng ngàn ván đấu ngẫu nhiên (rollouts).

### 4 Giai đoạn cốt lõi
1.  **Selection (Chọn lọc)**: Từ nút gốc, chọn nút con tốt nhất dựa trên công thức **UCB1** (Upper Confidence Bound) để cân bằng giữa việc *khai thác* các nước đi tốt đã biết và *khám phá* các nước đi mới.
2.  **Expansion (Mở rộng)**: Thêm một nước đi hợp lệ mới vào cây nếu nút hiện tại chưa được khám phá hết.
3.  **Simulation (Mô phỏng)**: Từ nút mới, AI chơi ngẫu nhiên cho đến khi ván đấu kết thúc để xem kết quả (Thắng/Thua/Hòa).
4.  **Backpropagation (Truyền ngược)**: Cập nhật kết quả của ván đấu mô phỏng ngược lên các nút cha để cập nhật tỷ lệ thắng và số lần truy cập.

---

## 3. So sánh Alpha-Beta và MCTS (1/10)

| Tiêu chí | Alpha-Beta Pruning | MCTS |
| :--- | :--- | :--- |
| **Bản chất** | Duyệt cây tìm kiếm có hệ thống (Vét cạn). | Mô phỏng xác suất và thống kê. |
| **Kiến thức** | Cần hàm đánh giá (Heuristic) phức tạp. | Không cần nhiều kiến thức chuyên môn về cờ (chỉ cần luật chơi). |
| **Độ sâu** | Rất mạnh ở độ sâu thấp nhưng tăng độ phức tạp cực nhanh. | Có thể đưa ra nước đi tốt ngay cả với ít thời gian mô phỏng. |
| **Điểm mạnh** | Tìm được nước đi tối ưu tuyệt đối trong phạm vi độ sâu. | Thích hợp cho các trò chơi có không gian trạng thái khổng lồ. |
| **Điểm yếu** | "Bị mù" nếu nước đi tốt nằm ngoài độ sâu tìm kiếm. | Có thể bỏ lỡ các nước đi "sát cục" nếu không mô phỏng đủ nhiều. |

---
*Tài liệu được biên soạn cho dự án Chess AI - 2026.*
