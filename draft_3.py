# ==========================================
# 20. ADVANCED PATHFINDING (TÌM ĐƯỜNG NÂNG CAO)
# ==========================================

"""
A. 0-1 BFS (Thuật toán BFS 0-1)
KHI NÀO DÙNG:
- Tìm đường đi ngắn nhất trên đồ thị/bảng mà chi phí (trọng số) của các bước chỉ là 0 hoặc 1.
- Ví dụ: Đi trên đường bình thường mất chi phí 0, phá tường mất chi phí 1.
- Thay vì dùng Dijkstra mất O(E log V), 0-1 BFS dùng Deque chỉ mất O(V + E) (Cực kỳ nhanh).
"""
def bfs_01(start, n, adj):
    # adj[u] = [(v, weight), ...] với weight chỉ là 0 hoặc 1
    distances = [float('inf')] * (n + 1)
    distances[start] = 0
    q = deque([start])
    
    while q:
        u = q.popleft()
        for v, weight in adj[u]:
            if distances[u] + weight < distances[v]:
                distances[v] = distances[u] + weight
                # KỸ THUẬT CỐT LÕI: Trọng số 0 đẩy lên ĐẦU hàng đợi, 1 đẩy xuống CUỐI
                if weight == 0:
                    q.appendleft(v)
                else:
                    q.append(v)
    return distances


"""
B. BELLMAN-FORD (Phát hiện chu trình âm)
KHI NÀO DÙNG:
- Tìm đường đi ngắn nhất khi đồ thị CÓ TRỌNG SỐ ÂM (Dijkstra sẽ bị sai).
- Bài toán hỏi: "Có thể du hành thời gian vô tận không?" -> Chính là tìm Chu trình âm (Negative Cycle).
"""
def bellman_ford(start, n, edges):
    # edges là mảng chứa các tuple (u, v, weight)
    dist = [float('inf')] * (n + 1)
    dist[start] = 0
    
    # Bước 1: Lặp n-1 lần để nới lỏng (relax) tất cả các cạnh
    for _ in range(n - 1):
        for u, v, w in edges:
            if dist[u] != float('inf') and dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                
    # Bước 2: Kiểm tra chu trình âm bằng cách lặp thêm 1 lần
    has_negative_cycle = False
    for u, v, w in edges:
        if dist[u] != float('inf') and dist[u] + w < dist[v]:
            has_negative_cycle = True
            break
            
    return dist, has_negative_cycle


# ==========================================
# 21. ARRAY & SEQUENCE MASTERY (ĐIỀU KHIỂN DÃY SỐ)
# ==========================================

"""
A. COORDINATE COMPRESSION (Nén tọa độ)
KHI NÀO DÙNG:
- Bạn có mảng $N$ phần tử ($N \le 10^5$), nhưng giá trị của chúng lên tới $10^9$ (hoặc cả tỷ).
- Cần đếm phân phối hoặc dùng mảng đánh dấu nhưng RAM không đủ chứa $10^9$ phần tử.
- Thuật toán thu nhỏ các giá trị về phạm vi từ 0 đến N-1 mà vẫn giữ nguyên thứ tự Lớn/Nhỏ.
"""
def compress_coordinates(arr):
    # Lấy các giá trị duy nhất và sắp xếp
    sorted_unique = sorted(list(set(arr)))
    # Tạo từ điển ánh xạ Giá trị gốc -> Thứ hạng (Rank)
    rank_map = {val: idx for idx, val in enumerate(sorted_unique)}
    # Trả về mảng đã nén
    return [rank_map[x] for x in arr], rank_map


"""
B. INVERSION COUNTING (Đếm số nghịch thế bằng Merge Sort)
KHI NÀO DÙNG:
- Cần đếm xem mảng đang bị "lộn xộn" đến mức nào. (Bao nhiêu cặp i < j mà arr[i] > arr[j]).
- Bài toán: Tìm số lần hoán đổi (swap) ít nhất để sắp xếp mảng bằng Bubble Sort.
"""
def count_inversions(arr):
    if len(arr) <= 1:
        return arr, 0
    
    mid = len(arr) // 2
    left, inv_left = count_inversions(arr[:mid])
    right, inv_right = count_inversions(arr[mid:])
    
    merged = []
    inv_count = inv_left + inv_right
    i = j = 0
    
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            merged.append(left[i])
            i += 1
        else:
            merged.append(right[j])
            j += 1
            # Nếu phần tử bên phải nhỏ hơn, nó tạo nghịch thế với TẤT CẢ phần tử còn lại bên trái
            inv_count += (len(left) - i)
            
    merged.extend(left[i:])
    merged.extend(right[j:])
    return merged, inv_count


# ==========================================
# 22. MATRIX & TABLE ALGORITHMS (THUẬT TOÁN BẢNG CHỮ NHẬT)
# ==========================================

"""
A. LARGEST RECTANGLE IN HISTOGRAM (Monotonic Stack)
KHI NÀO DÙNG:
- Tìm hình chữ nhật có diện tích lớn nhất được tạo bởi các cột biểu đồ.
- Nền tảng để giải bài toán: "Tìm ma trận hình chữ nhật toàn số 1 lớn nhất trong lưới 2D".
- Độ phức tạp thần thánh O(N) nhờ ngăn xếp đơn điệu.
"""
def largest_rectangle_area(heights):
    stack = [] # Lưu index
    max_area = 0
    heights = heights + [0] # Thêm cột 0 vào cuối để ép stack đẩy hết ra
    
    for i, h in enumerate(heights):
        start = i
        # Nếu cột hiện tại thấp hơn cột trên đỉnh stack -> Không thể mở rộng hình chữ nhật
        while stack and stack[-1][1] > h:
            idx, height = stack.pop()
            max_area = max(max_area, height * (i - idx))
            start = idx # Kéo lùi mốc xuất phát của hình chữ nhật hiện tại về bên trái
        stack.append((start, h))
        
    return max_area


"""
B. MAXIMAL RECTANGLE IN 2D GRID
KHI NÀO DÙNG:
- Tìm vùng hình chữ nhật lớn nhất toàn số 1 trong một ma trận nhị phân NxM.
- Chuyển từng hàng của ma trận thành một biểu đồ (Histogram) rồi gọi hàm ở trên.
"""
def maximal_rectangle_2d(matrix):
    if not matrix: return 0
    n, m = len(matrix), len(matrix[0])
    heights = [0] * m
    max_area = 0
    
    for i in range(n):
        for j in range(m):
            # Nếu ô là 1 thì cộng dồn chiều cao cột, nếu là 0 thì reset cột về 0
            heights[j] = heights[j] + 1 if matrix[i][j] == 1 else 0
        max_area = max(max_area, largest_rectangle_area(heights))
        
    return max_area


# ==========================================
# 23. PRO MAX DYNAMIC PROGRAMMING (QUY HOẠCH ĐỘNG BẬC THẦY)
# ==========================================

"""
A. TREE DP (Quy hoạch động trên Cây)
KHI NÀO DÙNG:
- Cấu trúc dữ liệu là Đồ thị vô hướng không có chu trình (Cây).
- Ví dụ: Đếm kích thước cây con, Tìm đường kính của cây, Tính chi phí max/min dọc theo cành cây.
- Kỹ thuật: Tính toán từ Lá (bottom) lên Gốc (up).
"""
def tree_dp(n, adj):
    # Khởi tạo dp mảng. Ví dụ: dp[u] lưu kích thước cây con có gốc là u
    subtree_size = [1] * (n + 1)
    visited = [False] * (n + 1)
    
    def dfs_dp(u):
        visited[u] = True
        for v in adj[u]:
            if not visited[v]:
                dfs_dp(v)
                # Kéo dữ liệu từ cây con (v) lên nút cha (u)
                subtree_size[u] += subtree_size[v]
                
    dfs_dp(1) # Chạy từ đỉnh tùy ý coi như gốc
    return subtree_size


"""
B. DIGIT DP (Quy hoạch động Chữ Số)
KHI NÀO DÙNG:
- Bài toán yêu cầu: "Đếm số lượng các số nguyên trong khoảng [A, B] thỏa mãn một tính chất X". (Với A, B cực lớn lên tới 10^18).
- Cách giải: Đếm số thỏa mãn từ [0, B] trừ đi số thỏa mãn từ [0, A-1].
- Xây dựng từng chữ số một từ trái qua phải.
"""
def solve_digit_dp(limit_str):
    # limit_str là số dạng chuỗi, vd: "987654321"
    n = len(limit_str)
    
    # dp_memo: lưu trữ kết quả để tránh tính lại. (Cấu trúc: tuple trạng thái -> giá trị)
    memo = {}
    
    def dp(idx, is_tight, is_leading_zero, current_sum):
        """
        idx: Vị trí chữ số đang xét (0 đến n-1)
        is_tight: Cờ kiểm tra xem các chữ số trước đó đã sát mốc giới hạn (limit) chưa
        is_leading_zero: Cờ xem số này đang là số 0 vô nghĩa ở đầu không
        current_sum: Trạng thái bài toán (Ví dụ: tổng các chữ số)
        """
        if idx == n:
            return 1 if current_sum == TARGET else 0 # Điều kiện thành công
            
        state = (idx, is_tight, is_leading_zero, current_sum)
        if state in memo:
            return memo[state]
            
        # Xác định giới hạn trên của chữ số tại vị trí hiện tại
        upper_bound = int(limit_str[idx]) if is_tight else 9
        
        ans = 0
        for digit in range(upper_bound + 1):
            next_tight = is_tight and (digit == upper_bound)
            next_leading_zero = is_leading_zero and (digit == 0)
            
            # Cập nhật trạng thái logic tùy vào bài toán (ví dụ: tính tổng chữ số)
            next_sum = current_sum + digit if not next_leading_zero else 0
            
            ans += dp(idx + 1, next_tight, next_leading_zero, next_sum)
            
        memo[state] = ans
        return ans

    return dp(0, True, True, 0)

# ==========================================
# 24. NETWORK FLOW (LUỒNG MẠNG - DINIC'S ALGORITHM)
# ==========================================

"""
A. DINIC'S ALGORITHM (Thuật toán Dinic - Tìm luồng cực đại O(V^2 * E))
KHI NÀO DÙNG:
- Bài toán: Cho hệ thống ống nước, tìm lượng nước lớn nhất có thể bơm từ Nguồn (Source) đến Đích (Sink).
- Bipartite Matching (Cặp ghép nhị phân) cũng có thể giải bằng Network Flow.
- BOJ Platinum rất hay ra dạng "Min-Cut Max-Flow" (Lát cắt nhỏ nhất = Luồng cực đại).
"""
def dinic_max_flow(n, source, sink, capacity):
    # capacity[u][v] = Sức chứa của cạnh từ u đến v
    graph = [[] for _ in range(n + 1)]
    for u in range(n + 1):
        for v in range(n + 1):
            if capacity[u][v] > 0 or capacity[v][u] > 0:
                graph[u].append(v)
                
    def bfs():
        level = [-1] * (n + 1)
        level[source] = 0
        q = deque([source])
        while q:
            u = q.popleft()
            for v in graph[u]:
                if level[v] == -1 and capacity[u][v] > 0:
                    level[v] = level[u] + 1
                    q.append(v)
        return level

    def dfs(u, flow, level, ptr):
        if u == sink or flow == 0:
            return flow
        for i in range(ptr[u], len(graph[u])):
            ptr[u] = i # Tối ưu hóa: Tránh duyệt lại các cạnh đã bị "chặn"
            v = graph[u][i]
            if level[v] == level[u] + 1 and capacity[u][v] > 0:
                pushed = dfs(v, min(flow, capacity[u][v]), level, ptr)
                if pushed > 0:
                    capacity[u][v] -= pushed
                    capacity[v][u] += pushed # Cạnh ngược (Residual edge)
                    return pushed
        return 0

    max_flow = 0
    while True:
        level = bfs()
        if level[sink] == -1: # Không còn đường đi từ Source đến Sink
            break
        ptr = [0] * (n + 1)
        while True:
            pushed = dfs(source, float('inf'), level, ptr)
            if not pushed:
                break
            max_flow += pushed
            
    return max_flow


# ==========================================
# 25. 2-SAT (THỎA MÃN LOGIC BOOLEAN)
# ==========================================

"""
A. 2-SAT (2-Satisfiability)
KHI NÀO DÙNG:
- Bạn có N biến boolean (True/False) và các điều kiện dạng: (A OR B) AND (NOT A OR C) AND ...
- Câu hỏi: Có tồn tại cách gán True/False cho N biến để biểu thức đúng không?
- Cốt lõi: Đưa về đồ thị có hướng: (A OR B) tương đương với (NOT A -> B) và (NOT B -> A). Dùng SCC Tarjan để giải.
"""
# Ghi chú: Định dạng đỉnh: x là biến x, -x là phủ định của x.
# Thường map sang index dương: x -> 2*x, -x -> 2*x + 1
def solve_2sat(n, clauses):
    adj = [[] for _ in range(2 * n + 2)]
    
    def get_node(x):
        return 2 * x if x > 0 else 2 * (-x) + 1
        
    def get_neg(node):
        return node + 1 if node % 2 == 0 else node - 1

    for u, v in clauses:
        nu, nv = get_node(u), get_node(v)
        adj[get_neg(nu)].append(nv) # ~u -> v
        adj[get_neg(nv)].append(nu) # ~v -> u
        
    # Gọi thuật toán SCC Tarjan (đã định nghĩa ở khối trên)
    scc_list, scc_id = tarjan_scc_for_2sat(2 * n + 1, adj)
    
    assignment = [-1] * (n + 1)
    for i in range(1, n + 1):
        pos_node = 2 * i
        neg_node = 2 * i + 1
        if scc_id[pos_node] == scc_id[neg_node]:
            return False, [] # Mâu thuẫn: x và ~x cùng thuộc 1 thành phần liên thông
            
        # SCC id tạo ra nghịch đảo Topological sort. Đỉnh nào có SCC ID nhỏ hơn thì đứng sau trong đồ thị Topo.
        # Ta gán True cho đỉnh đứng sau (ID nhỏ hơn)
        assignment[i] = 1 if scc_id[pos_node] < scc_id[neg_node] else 0
        
    return True, assignment


# ==========================================
# 26. SWEEPING ALGORITHM (ĐƯỜNG QUÉT)
# ==========================================

"""
A. LINE SWEEPING (Gộp các đoạn thẳng / Diện tích phủ)
KHI NÀO DÙNG:
- Có hàng triệu tia/đoạn thẳng chồng chéo nhau. Hỏi tổng chiều dài thực tế được bao phủ.
- Quét từ trái sang phải, mở ngoặc khi bắt đầu 1 đoạn và đóng ngoặc khi kết thúc.
"""
def sweeping_intervals(intervals):
    # intervals = [(start1, end1), (start2, end2), ...]
    if not intervals: return 0
    
    intervals.sort(key=lambda x: x[0])
    total_length = 0
    current_start, current_end = intervals[0]
    
    for start, end in intervals[1:]:
        if start <= current_end:
            # Giao nhau hoặc nằm trong nhau -> Kéo dài current_end
            current_end = max(current_end, end)
        else:
            # Tách rời nhau -> Cộng dồn vào tổng và bắt đầu đoạn mới
            total_length += (current_end - current_start)
            current_start, current_end = start, end
            
    total_length += (current_end - current_start)
    return total_length


# ==========================================
# 27. EULERIAN PATH (ĐƯỜNG ĐI EULER)
# ==========================================

"""
A. HIERHOLZER'S ALGORITHM (Tìm Đường Đi Euler)
KHI NÀO DÙNG:
- Trò chơi "Vẽ hình không nhấc bút". Đi qua tất cả các CẠNH của đồ thị, mỗi cạnh đúng 1 lần.
- Đồ thị vô hướng: Tất cả đỉnh chẵn bậc (Chu trình), hoặc đúng 2 đỉnh lẻ bậc (Đường đi).
- Đồ thị có hướng: in_degree == out_degree, hoặc đúng 1 đỉnh (out - in = 1) và 1 đỉnh (in - out = 1).
"""
def get_euler_path(start_node, adj):
    # Lưu ý: Cần xóa cạnh sau khi đi qua nên dùng pop() trên adj
    stack = [start_node]
    path = []
    
    while stack:
        u = stack[-1]
        if adj[u]:
            v = adj[u].pop() # Xóa cạnh vừa đi
            stack.append(v)
        else:
            path.append(stack.pop())
            
    # Kết quả của Hierholzer là đường đi ngược, cần đảo lại
    return path[::-1]


# ==========================================
# 28. GAME THEORY (LÝ THUYẾT TRÒ CHƠI)
# ==========================================

"""
A. SPRAGUE-GRUNDY THEOREM (Trò chơi Nim)
KHI NÀO DÙNG:
- Bài toán 2 người chơi luân phiên (Alice và Bob). Ai không thể đi tiếp là thua.
- Tổng XOR (Nim-sum) của các trạng thái. Nếu XOR-sum != 0 -> Người đi trước thắng.
- Hàm MEX (Minimum Excluded): Số nguyên không âm nhỏ nhất KHÔNG nằm trong tập hợp.
"""
def calculate_grundy(n, max_stones, valid_moves):
    grundy = [0] * (max_stones + 1)
    
    for stones in range(1, max_stones + 1):
        seen_grundy = set()
        for move in valid_moves:
            if stones >= move:
                seen_grundy.add(grundy[stones - move])
                
        # Tìm MEX
        mex = 0
        while mex in seen_grundy:
            mex += 1
        grundy[stones] = mex
        
    return grundy
    
# Phán đoán: 
# xor_sum = grundy[pile1] ^ grundy[pile2] ^ ...
# Nếu xor_sum > 0: "First player wins", ngược lại "Second player wins"


# ==========================================
# 29. FFT (FAST FOURIER TRANSFORM)
# ==========================================

"""
A. FFT (Biến đổi Fourier Nhanh)
KHI NÀO DÙNG:
- Boss cuối của thuật toán BOJ (Đỉnh cao của Diamond).
- Cần nhân hai đa thức (hoặc nhân hai số khổng lồ có độ dài 10^5 chữ số) trong thời gian O(N log N) thay vì O(N^2).
- Thường áp dụng kết hợp với Combinatorics (Tổ hợp) để đếm số cặp có tổng bằng K.
"""
import cmath

def fft(a, invert):
    n = len(a)
    if n == 1:
        return
    
    # Chia chẵn lẻ
    a0 = a[0::2]
    a1 = a[1::2]
    fft(a0, invert)
    fft(a1, invert)
    
    # Góc quay
    ang = 2 * cmath.pi / n * (-1 if invert else 1)
    w = 1
    wn = cmath.exp(complex(0, ang))
    
    for i in range(n // 2):
        a[i] = a0[i] + w * a1[i]
        a[i + n // 2] = a0[i] - w * a1[i]
        if invert:
            a[i] /= 2
            a[i + n // 2] /= 2
        w *= wn

def multiply_polynomials(p1, p2):
    # p1, p2 là mảng hệ số đa thức. Ví dụ: 1 + 2x + 3x^2 -> [1, 2, 3]
    n = 1
    # Bậc của đa thức kết quả có thể lên tới len(p1) + len(p2). Tìm lũy thừa của 2 gần nhất.
    while n < len(p1) + len(p2):
        n <<= 1
        
    # Padding bằng 0 để đạt kích thước 2^k
    a = [complex(x, 0) for x in p1] + [0] * (n - len(p1))
    b = [complex(x, 0) for x in p2] + [0] * (n - len(p2))
    
    fft(a, False)
    fft(b, False)
    
    for i in range(n):
        a[i] *= b[i]
        
    fft(a, True)
    
    # Làm tròn để khử sai số số thực
    result = [round(x.real) for x in a]
    
    # Cắt bỏ các số 0 thừa ở đuôi
    while len(result) > 1 and result[-1] == 0:
        result.pop()
        
    return result

# ==========================================
# 30. BACKTRACKING & COMBINATORICS (QUAY LUI & DUYỆT TỔ HỢP)
# ==========================================

"""
A. BACKTRACKING TEMPLATE (Quay lui có cắt tỉa - Pruning)
KHI NÀO DÙNG:
- Giải các bài toán N-Queens, Sudoku, hoặc sinh cấu hình mà itertools KHÔNG THỂ giải được vì cần cắt tỉa (dừng sớm nếu thấy sai).
- "Cắt tỉa" (Pruning) là linh hồn của Backtracking để tránh TLE.
"""
def solve_n_queens(n):
    res = []
    # Các mảng đánh dấu cột và 2 đường chéo
    cols = [False] * n
    diag1 = [False] * (2 * n) # Đường chéo chính (r - c)
    diag2 = [False] * (2 * n) # Đường chéo phụ (r + c)
    
    def backtrack(row, current_board):
        if row == n:
            res.append(current_board[:])
            return
            
        for col in range(n):
            # CẮT TỈA: Nếu vị trí này bị khống chế thì bỏ qua ngay lập tức
            if cols[col] or diag1[row - col + n] or diag2[row + col]:
                continue
                
            # Đánh dấu đã đặt Queen
            cols[col] = diag1[row - col + n] = diag2[row + col] = True
            current_board.append(col)
            
            backtrack(row + 1, current_board)
            
            # Trả lại trạng thái (Backtrack)
            current_board.pop()
            cols[col] = diag1[row - col + n] = diag2[row + col] = False
            
    backtrack(0, [])
    return res


# ==========================================
# 31. SPANNING TREES (CÂY KHUNG NHỎ NHẤT)
# ==========================================

"""
A. KRUSKAL'S ALGORITHM (Thuật toán Kruskal)
KHI NÀO DÙNG:
- Tìm mạng lưới kết nối tất cả các đỉnh với tổng chi phí nhỏ nhất (Minimum Spanning Tree - MST).
- Phải kết hợp với Disjoint Set (Union-Find) đã khai báo ở phần trước.
"""
def kruskal_mst(n, edges):
    # edges là danh sách các tuple (trọng_số, u, v)
    # Rất quan trọng: Phải sắp xếp các cạnh theo trọng số tăng dần
    edges.sort()
    
    parent = [i for i in range(n + 1)]
    rank = [0] * (n + 1)
    
    mst_weight = 0
    mst_edges = 0
    
    for weight, u, v in edges:
        # Nếu u và v chưa được kết nối (không tạo thành chu trình)
        if find(parent, u) != find(parent, v):
            union(parent, rank, u, v)
            mst_weight += weight
            mst_edges += 1
            if mst_edges == n - 1: # Đã đủ số cạnh cho cây khung
                break
                
    # Trả về tổng trọng số và kiểm tra xem đồ thị có liên thông hoàn toàn không
    return mst_weight if mst_edges == n - 1 else -1


# ==========================================
# 32. BICONNECTED COMPONENTS (KHỚP & CẦU ĐỒ THỊ)
# ==========================================

"""
A. ARTICULATION POINTS & BRIDGES (Đỉnh Khớp & Cạnh Cầu)
KHI NÀO DÙNG:
- Tìm điểm yếu của hệ thống mạng: "Nếu máy chủ X hỏng, hoặc đường truyền Y đứt, mạng có bị chia cắt không?"
- Sử dụng thuật toán Tarjan sửa đổi.
"""
def find_articulation_points_and_bridges(n, adj):
    disc = [-1] * (n + 1) # Thời gian thăm (Discovery time)
    low = [-1] * (n + 1)  # Thời gian thăm nhỏ nhất có thể lùi về
    parent = [-1] * (n + 1)
    articulation_points = set()
    bridges = []
    time = [0]
    
    def dfs(u):
        children = 0
        disc[u] = low[u] = time[0]
        time[0] += 1
        
        for v in adj[u]:
            if disc[v] == -1: # Nếu v chưa thăm
                parent[v] = u
                children += 1
                dfs(v)
                
                low[u] = min(low[u], low[v])
                
                # Điều kiện CẦU (Bridge): Không có đường nào từ v quay ngược lại trên u
                if low[v] > disc[u]:
                    bridges.append((min(u, v), max(u, v)))
                    
                # Điều kiện KHỚP (Articulation Point): 
                # Nếu u không phải gốc và cây con v không thể quay lại trên u
                if parent[u] != -1 and low[v] >= disc[u]:
                    articulation_points.add(u)
                    
            elif v != parent[u]: # Cạnh ngược (Back edge)
                low[u] = min(low[u], disc[v])
                
        # Điều kiện KHỚP cho đỉnh gốc (Root): Có nhiều hơn 1 nhánh cây con độc lập
        if parent[u] == -1 and children > 1:
            articulation_points.add(u)
            
    for i in range(1, n + 1):
        if disc[i] == -1:
            dfs(i)
            
    return list(articulation_points), bridges


# ==========================================
# 33. MERGE SORT TREE (CÂY PHÂN ĐOẠN TRỘN)
# ==========================================

"""
A. MERGE SORT TREE
KHI NÀO DÙNG:
- Khi cần trả lời nhanh truy vấn: "Trong khoảng [L, R] của mảng, có bao nhiêu phần tử LỚN HƠN (hoặc nhỏ hơn) K?".
- Không có thao tác cập nhật (Offline queries friendly).
- Là sự kết hợp giữa Segment Tree và Merge Sort. Mỗi Node của cây lưu một mảng ĐÃ SẮP XẾP.
"""
import bisect

def build_merge_sort_tree(node, start, end, arr, tree):
    if start == end:
        tree[node] = [arr[start]]
        return
    mid = (start + end) // 2
    build_merge_sort_tree(2 * node, start, mid, arr, tree)
    build_merge_sort_tree(2 * node + 1, mid + 1, end, arr, tree)
    
    # Trộn 2 mảng con đã sắp xếp (Merge phase của Merge Sort)
    left_arr = tree[2 * node]
    right_arr = tree[2 * node + 1]
    
    # Kỹ thuật trộn nhanh bằng Python
    merged = []
    i = j = 0
    while i < len(left_arr) and j < len(right_arr):
        if left_arr[i] < right_arr[j]:
            merged.append(left_arr[i])
            i += 1
        else:
            merged.append(right_arr[j])
            j += 1
    merged.extend(left_arr[i:])
    merged.extend(right_arr[j:])
    tree[node] = merged

def query_merge_sort_tree(node, start, end, l, r, k, tree):
    # Đếm số lượng phần tử > K trong đoạn [l, r]
    if r < start or end < l:
        return 0
    if l <= start and end <= r:
        # Dùng Binary Search trên node hiện tại
        idx = bisect.bisect_right(tree[node], k)
        return len(tree[node]) - idx
        
    mid = (start + end) // 2
    p1 = query_merge_sort_tree(2 * node, start, mid, l, r, k, tree)
    p2 = query_merge_sort_tree(2 * node + 1, mid + 1, end, l, r, k, tree)
    return p1 + p2


# ==========================================
# 34. DP WITH QUEUE (TỐI ƯU DP BẰNG DEQUE)
# ==========================================

"""
A. MONOTONE QUEUE DP OPTIMIZATION (Tối ưu DP bằng hàng đợi đơn điệu)
KHI NÀO DÙNG:
- Công thức DP có dạng: dp[i] = max(dp[j]) + cost[i], với (i - K <= j <= i - 1).
- Nếu dùng vòng lặp for lồng nhau sẽ mất O(N*K) -> Bị TLE.
- Dùng Deque đơn điệu giúp giảm xuống O(N).
- Ứng dụng: Chơi game nhảy lò cò (nhảy xa tối đa K bước), Cửa sổ trượt.
"""
from collections import deque

def dp_with_monotone_queue(arr, k):
    n = len(arr)
    dp = [0] * n
    dp[0] = arr[0]
    
    # Deque lưu trữ các chỉ số (index), sao cho giá trị dp tương ứng LUÔN GIẢM DẦN
    # (Đỉnh của deque chứa index có giá trị dp LỚN NHẤT)
    q = deque([0])
    
    for i in range(1, n):
        # 1. Loại bỏ các phần tử đã "hết hạn" (nằm ngoài cửa sổ nhảy K bước)
        while q and q[0] < i - k:
            q.popleft()
            
        # 2. Tính dp[i] dựa trên giá trị lớn nhất còn hiệu lực trong deque
        dp[i] = dp[q[0]] + arr[i]
        
        # 3. Duy trì tính đơn điệu: Loại bỏ các phần tử có giá trị DP <= dp[i] ở đuôi deque
        # Vì dp[i] mới vừa tính ra lớn hơn chúng, và dp[i] lại có hạn sử dụng lâu hơn
        while q and dp[q[-1]] <= dp[i]:
            q.pop()
            
        q.append(i)
        
    return max(dp)
