# ==========================================
# 7. ADVANCED DATA STRUCTURES (CẤU TRÚC DỮ LIỆU NÂNG CAO)
# ==========================================

"""
A. SEGMENT TREE (Cây Phân Đoạn)
KHI NÀO DÙNG:
- Cần truy vấn (Tìm Max/Min, Tính Tổng, v.v.) trên một đoạn [L, R] của mảng.
- Có thao tác CẬP NHẬT từng phần tử (Point Update) đan xen với truy vấn.
- Rất phổ biến ở BOJ Gold/Platinum (Mạnh hơn Fenwick/BIT vì BIT chỉ tính được tổng).
"""
def build_seg(node, start, end, arr, tree):
    if start == end:
        tree[node] = arr[start]
        return
    mid = (start + end) // 2
    build_seg(2 * node, start, mid, arr, tree)
    build_seg(2 * node + 1, mid + 1, end, arr, tree)
    # Thay đổi hàm ở đây tùy bài toán (max, min, sum...)
    tree[node] = max(tree[2 * node], tree[2 * node + 1])

def update_seg(node, start, end, idx, val, tree):
    if start == end:
        tree[node] = val
        return
    mid = (start + end) // 2
    if start <= idx <= mid:
        update_seg(2 * node, start, mid, idx, val, tree)
    else:
        update_seg(2 * node + 1, mid + 1, end, idx, val, tree)
    tree[node] = max(tree[2 * node], tree[2 * node + 1])

def query_seg(node, start, end, l, r, tree):
    if r < start or end < l:
        return -float('inf') # Trả về giá trị vô hại (0 với sum, inf với min)
    if l <= start and end <= r:
        return tree[node]
    mid = (start + end) // 2
    p1 = query_seg(2 * node, start, mid, l, r, tree)
    p2 = query_seg(2 * node + 1, mid + 1, end, l, r, tree)
    return max(p1, p2)


"""
B. TRIE (Cây Tiền Tố)
KHI NÀO DÙNG:
- Tìm kiếm chuỗi, kiểm tra xem một từ có phải tiền tố của từ khác không.
- Bài toán liên quan đến Tự điển (Dictionary) hoặc Auto-complete.
"""
class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end = False

class Trie:
    def __init__(self):
        self.root = TrieNode()
        
    def insert(self, word):
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end = True
        
    def search(self, word):
        node = self.root
        for char in word:
            if char not in node.children:
                return False
            node = node.children[char]
        return node.is_end

# ==========================================
# 8. ADVANCED GRAPH ALGORITHMS (ĐỒ THỊ NÂNG CAO)
# ==========================================

"""
A. TOPOLOGICAL SORT (Sắp xếp Topo)
KHI NÀO DÙNG:
- Bài toán có điều kiện tiên quyết (Ví dụ: Việc A phải làm trước việc B).
- Chỉ áp dụng trên Đồ thị có hướng không có chu trình (DAG).
- Thường kết hợp với DP để tìm thời gian hoàn thành ngắn nhất.
"""
def topo_sort(n, adj, in_degree):
    queue = deque()
    for i in range(1, n + 1):
        if in_degree[i] == 0:
            queue.append(i)
            
    result = []
    while queue:
        u = queue.popleft()
        result.append(u)
        for v in adj[u]:
            in_degree[v] -= 1
            if in_degree[v] == 0:
                queue.append(v)
    # Nếu len(result) < n -> Đồ thị có chu trình!
    return result


"""
B. FLOYD-WARSHALL
KHI NÀO DÙNG:
- Tìm đường đi ngắn nhất giữa TẤT CẢ CÁC CẶP ĐỈNH.
- Đồ thị nhỏ (N <= 500) vì độ phức tạp là O(N^3).
- Chấp nhận cạnh âm (nhưng không được có chu trình âm).
"""
def floyd_warshall(n, graph_matrix):
    # graph_matrix[i][j] khởi tạo là khoảng cách ban đầu, chéo chính = 0, vô cực nếu không nối
    for k in range(1, n + 1):
        for i in range(1, n + 1):
            for j in range(1, n + 1):
                if graph_matrix[i][k] + graph_matrix[k][j] < graph_matrix[i][j]:
                    graph_matrix[i][j] = graph_matrix[i][k] + graph_matrix[k][j]


"""
C. LOWEST COMMON ANCESTOR - LCA (Tổ Tiên Chung Gần Nhất) - Dùng Binary Lifting
KHI NÀO DÙNG:
- Cho một cây, truy vấn nhiều lần: Tìm nút cha chung gần nhất của đỉnh U và đỉnh V.
- Độ phức tạp tiền xử lý O(N log N), mỗi truy vấn O(log N).
"""
# depth[u] lưu độ sâu, up[u][j] lưu tổ tiên thứ 2^j của đỉnh u
def lca(u, v, depth, up, LOG):
    if depth[u] < depth[v]:
        u, v = v, u
    # Nâng u lên cùng độ sâu với v
    for i in range(LOG - 1, -1, -1):
        if depth[u] - (1 << i) >= depth[v]:
            u = up[u][i]
    if u == v:
        return u
    # Nâng cả u và v lên gần sát LCA
    for i in range(LOG - 1, -1, -1):
        if up[u][i] != up[v][i]:
            u = up[u][i]
            v = up[v][i]
    return up[u][0]

# ==========================================
# 9. ADVANCED DYNAMIC PROGRAMMING (DP NÂNG CAO)
# ==========================================

"""
A. BITMASK DP - TSP (Bài toán người chào hàng)
KHI NÀO DÙNG:
- Có tập N đỉnh nhỏ (N <= 20).
- Trạng thái dp có dạng: dp(mask, last_node) = Chi phí nhỏ nhất khi đã thăm tập các đỉnh (mask) và đang đứng ở last_node.
"""
def tsp(n, W):
    # Khởi tạo bảng DP với vô cực
    # mask chạy từ 0 đến 2^N - 1
    dp = [[float('inf')] * n for _ in range(1 << n)]
    dp[1][0] = 0 # Bắt đầu ở đỉnh 0, mask = 1 (tức là 0001)
    
    for mask in range(1 << n):
        for u in range(n):
            if not (mask & (1 << u)): continue # Nếu đỉnh u chưa thăm thì bỏ qua
            for v in range(n):
                if mask & (1 << v): continue # Nếu đỉnh v ĐÃ thăm thì bỏ qua
                if W[u][v] == 0: continue # Không có đường đi
                
                next_mask = mask | (1 << v)
                dp[next_mask][v] = min(dp[next_mask][v], dp[mask][u] + W[u][v])
                
    # Trở về điểm xuất phát
    ans = float('inf')
    for i in range(1, n):
        if W[i][0] != 0:
            ans = min(ans, dp[(1 << n) - 1][i] + W[i][0])
    return ans


"""
B. LONGEST COMMON SUBSEQUENCE (Dãy con chung dài nhất)
KHI NÀO DÙNG:
- Tìm chuỗi/dãy con giống nhau dài nhất giữa 2 chuỗi A và B (không cần liên tiếp).
"""
def lcs(s1, s2):
    n, m = len(s1), len(s2)
    dp = [[0] * (m + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            if s1[i-1] == s2[j-1]:
                dp[i][j] = dp[i-1][j-1] + 1
            else:
                dp[i][j] = max(dp[i-1][j], dp[i][j-1])
    return dp[n][m]

# ==========================================
# 10. GEOMETRY & MATH NÂNG CAO (HÌNH HỌC & TOÁN)
# ==========================================

"""
A. CCW (Counter-Clockwise - Định hướng góc)
KHI NÀO DÙNG:
- Trái tim của mọi bài hình học.
- Xác định 3 điểm A, B, C tạo thành góc rẽ Trái, rẽ Phải hay Thẳng Hàng.
- Kiểm tra 2 đoạn thẳng có cắt nhau không (Intersection).
"""
def ccw(x1, y1, x2, y2, x3, y3):
    # Trả về: > 0 (Ngược chiều kim đồng hồ / Rẽ trái)
    #         < 0 (Cùng chiều kim đồng hồ / Rẽ phải)
    #         = 0 (Thẳng hàng)
    return (x2 - x1) * (y3 - y1) - (y2 - y1) * (x3 - x1)


"""
B. MODULAR COMBINATORICS (Tính nCr % MOD) dùng Fermat nhỏ
KHI NÀO DÙNG:
- Tính Tổ Hợp Chọn R phần tử từ N phần tử (N lớn tới 10^5, 10^6).
- Công thức: nCr = N! * (R! * (N-R)!)^-1 % MOD
"""
def nCr_mod(n, r, mod, fact, inv_fact):
    if r < 0 or r > n: return 0
    # Cần tiền xử lý fact[i] (i!) và inv_fact[i] (nghịch đảo modulo của i!)
    return fact[n] * inv_fact[r] % mod * inv_fact[n - r] % mod

# ==========================================
# 11. STRING PROCESSING (XỬ LÝ CHUỖI)
# ==========================================

"""
A. KMP (Knuth-Morris-Pratt)
KHI NÀO DÙNG:
- Đếm số lần xuất hiện của chuỗi Pattern trong chuỗi Text.
- Tìm vị trí bắt đầu của Pattern trong Text với O(N + M).
"""
def build_pi(pattern):
    m = len(pattern)
    pi = [0] * m
    j = 0
    for i in range(1, m):
        while j > 0 and pattern[i] != pattern[j]:
            j = pi[j - 1]
        if pattern[i] == pattern[j]:
            j += 1
            pi[i] = j
    return pi

def kmp_search(text, pattern):
    n, m = len(text), len(pattern)
    pi = build_pi(pattern)
    j = 0
    res = [] # Lưu các vị trí match
    for i in range(n):
        while j > 0 and text[i] != pattern[j]:
            j = pi[j - 1]
        if text[i] == pattern[j]:
            if j == m - 1:
                res.append(i - m + 1)
                j = pi[j]
            else:
                j += 1
    return res
