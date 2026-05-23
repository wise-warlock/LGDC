import sys
from collections import deque
import heapq
import math

# ==========================================
# 1. SETUP & FAST I/O (NHẬP XUẤT NHANH)
# ==========================================
"""
KHI NÀO DÙNG: 
Luôn luôn dùng trong mọi bài toán trên Baekjoon (BOJ) để tránh lỗi Time Limit Exceeded (TLE).
"""
sys.setrecursionlimit(200005) # Bắt buộc cho các bài dùng DFS
input = sys.stdin.readline    # Đọc từng dòng cực nhanh

def read_ints():
    return list(map(int, input().split()))

# ==========================================
# 2. GRAPH ALGORITHMS (THUẬT TOÁN ĐỒ THỊ)
# ==========================================

"""
A. DFS (Depth-First Search) & BFS (Breadth-First Search) trên Ma trận 2D
KHI NÀO DÙNG:
- Tìm đường đi ngắn nhất trên bảng/lưới không có trọng số (chỉ dùng BFS).
- Đếm số vùng không gian / Đếm số thành phần liên thông (Flood Fill).
- Bài toán mê cung, loang màu.
"""
# 4 hướng di chuyển: Lên, Xuống, Trái, Phải
dx = [-1, 1, 0, 0]
dy = [0, 0, -1, 1]

def bfs_2d(start_x, start_y, grid, N, M):
    queue = deque([(start_x, start_y)])
    visited = [[False] * M for _ in range(N)]
    visited[start_x][start_y] = True
    
    while queue:
        x, y = queue.popleft()
        for i in range(4):
            nx, ny = x + dx[i], y + dy[i]
            if 0 <= nx < N and 0 <= ny < M and not visited[nx][ny]:
                if grid[nx][ny] == 1:  # Điều kiện đi tiếp (ví dụ: 1 là đường đi)
                    visited[nx][ny] = True
                    queue.append((nx, ny))


"""
B. DIJKSTRA (Đường đi ngắn nhất có trọng số)
KHI NÀO DÙNG:
- Tìm đường đi ngắn nhất từ 1 đỉnh đến các đỉnh còn lại.
- Bắt buộc đồ thị KHÔNG có trọng số âm.
- Ví dụ: Tìm chi phí nhỏ nhất để đi từ thành phố A đến B.
"""
def dijkstra(start, n, graph):
    # graph[u] = [(v, weight), ...]
    distances = [float('inf')] * (n + 1)
    distances[start] = 0
    pq = [(0, start)] # (khoảng_cách, đỉnh)
    
    while pq:
        current_dist, u = heapq.heappop(pq)
        
        # Bỏ qua nếu tìm được đường dài hơn đường đã lưu
        if distances[u] < current_dist:
            continue
            
        for v, weight in graph[u]:
            dist = current_dist + weight
            if dist < distances[v]:
                distances[v] = dist
                heapq.heappush(pq, (dist, v))
    return distances


"""
C. DISJOINT SET UNION (Cấu trúc dữ liệu Disjoint Set / Union-Find)
KHI NÀO DÙNG:
- Cần gom nhóm các phần tử rời rạc lại với nhau.
- Kiểm tra xem 2 đỉnh có thuộc cùng một đồ thị liên thông không.
- Phát hiện chu trình trong đồ thị vô hướng.
- Tìm Cây Khung Nhỏ Nhất (Kruskal's Algorithm).
"""
def find(parent, i):
    if parent[i] == i:
        return i
    parent[i] = find(parent, parent[i]) # Path compression (Nén đường)
    return parent[i]

def union(parent, rank, i, j):
    root_i = find(parent, i)
    root_j = find(parent, j)
    if root_i != root_j:
        if rank[root_i] < rank[root_j]:
            parent[root_i] = root_j
        elif rank[root_i] > rank[root_j]:
            parent[root_j] = root_i
        else:
            parent[root_j] = root_i
            rank[root_i] += 1

# ==========================================
# 3. BINARY SEARCH / PARAMETRIC SEARCH
# ==========================================
"""
KHI NÀO DÙNG:
- Tìm kiếm một phần tử trong mảng ĐÃ SẮP XẾP.
- Parametric Search (Chặt nhị phân kết quả): Khi bài toán yêu cầu tìm "Giá trị lớn nhất có thể" hoặc "Giá trị nhỏ nhất có thể" thỏa mãn một điều kiện nào đó.
"""
def parametric_search(low, high):
    ans = -1
    while low <= high:
        mid = (low + high) // 2
        # condition(mid) là hàm tự viết kiểm tra xem mid có hợp lệ không
        if condition(mid): 
            ans = mid
            # Nếu cần tìm giá trị LỚN NHẤT, ta tăng low (low = mid + 1)
            # Nếu cần tìm giá trị NHỎ NHẤT, ta giảm high (high = mid - 1)
            low = mid + 1 
        else:
            high = mid - 1
    return ans

def condition(mid):
    # Dummy condition function
    return True

# ==========================================
# 4. DATA STRUCTURES & ARRAYS
# ==========================================

"""
A. PREFIX SUM 1D & 2D (Mảng cộng dồn)
KHI NÀO DÙNG:
- Cần tính tổng của một đoạn (1D) hoặc một hình chữ nhật (2D) rất nhiều lần (truy vấn liên tục).
- Giúp giảm thời gian tính tổng từ O(N) xuống O(1).
"""
def build_prefix_sum_2d(matrix, N, M):
    pref = [[0] * (M + 1) for _ in range(N + 1)]
    for i in range(1, N + 1):
        for j in range(1, M + 1):
            pref[i][j] = matrix[i-1][j-1] + pref[i-1][j] + pref[i][j-1] - pref[i-1][j-1]
    return pref

def get_sum_2d(pref, r1, c1, r2, c2):
    # Trả về tổng hcn từ (r1, c1) đến (r2, c2) - 1-based index
    return pref[r2][c2] - pref[r1-1][c2] - pref[r2][c1-1] + pref[r1-1][c1-1]


"""
B. FENWICK TREE / BINARY INDEXED TREE (Cây BIT)
KHI NÀO DÙNG:
- Giống mảng cộng dồn, nhưng mảng BAN ĐẦU LIÊN TỤC BỊ CẬP NHẬT/THAY ĐỔI.
- Tính tổng mảng / cập nhật điểm trong O(log N).
"""
def update_bit(tree, i, delta, n):
    while i <= n:
        tree[i] += delta
        i += i & (-i)

def query_bit(tree, i):
    total = 0
    while i > 0:
        total += tree[i]
        i -= i & (-i)
    return total


# ==========================================
# 5. DYNAMIC PROGRAMMING (QUY HOẠCH ĐỘNG)
# ==========================================

"""
A. 0/1 KNAPSACK (Cái túi)
KHI NÀO DÙNG:
- Có một bộ các vật phẩm với Trọng lượng (Weight) và Giá trị (Value).
- Cần chọn đồ vật sao cho Tổng Giá Trị lớn nhất nhưng không vượt quá Tổng Trọng Lượng cho phép.
- Mỗi đồ vật chỉ được chọn 1 lần.
"""
def knapsack(weights, values, capacity, n):
    # dp[w] lưu giá trị lớn nhất đạt được với trọng lượng w
    dp = [0] * (capacity + 1)
    for i in range(n):
        # Duyệt ngược để không chọn 1 đồ vật nhiều lần
        for w in range(capacity, weights[i] - 1, -1):
            dp[w] = max(dp[w], dp[w - weights[i]] + values[i])
    return max(dp)


"""
B. LONGEST INCREASING SUBSEQUENCE - LIS (Dãy con tăng dài nhất) - O(N log N)
KHI NÀO DÙNG:
- Cần tìm một dãy con có thứ tự tăng dần dài nhất.
- Ứng dụng nhiều trong bài toán xếp đồ, xây cầu không cắt nhau.
"""
import bisect
def lis_n_log_n(arr):
    tails = []
    for num in arr:
        idx = bisect.bisect_left(tails, num)
        if idx == len(tails):
            tails.append(num)
        else:
            tails[idx] = num
    return len(tails)


# ==========================================
# 6. MATH & NUMBER THEORY (TOÁN HỌC)
# ==========================================

"""
A. SIEVE OF ERATOSTHENES (Sàng Nguyên Tố)
KHI NÀO DÙNG:
- Cần kiểm tra rất nhiều số xem có phải số nguyên tố không.
- Tìm tất cả số nguyên tố từ 1 đến N (N thường lên tới 10^6 hoặc 10^7).
"""
def sieve(n):
    is_prime = [True] * (n + 1)
    is_prime[0] = is_prime[1] = False
    for i in range(2, int(math.sqrt(n)) + 1):
        if is_prime[i]:
            for j in range(i * i, n + 1, i):
                is_prime[j] = False
    return [i for i in range(2, n + 1) if is_prime[i]]


"""
B. FAST MODULAR EXPONENTIATION (Lũy thừa ma trận / Tính (A^B) % M nhanh)
KHI NÀO DÙNG:
- Tính số mũ cực lớn mà không bị tràn bộ nhớ hoặc chạy quá chậm.
- Ví dụ: Tính 2^1000000000 % 1000000007.
"""
def mod_pow(base, exp, mod):
    res = 1
    base = base % mod
    while exp > 0:
        if exp % 2 == 1:
            res = (res * base) % mod
        exp = exp >> 1
        base = (base * base) % mod
    return res

if __name__ == "__main__":
    # Nơi chạy thử code của bạn
    pass

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

# ==========================================
# 35. GREEDY ALGORITHM (THUẬT TOÁN THAM LAM)
# ==========================================

"""
A. INTERVAL SCHEDULING (Lập lịch hoạt động / Chọn đoạn thẳng)
KHI NÀO DÙNG:
- Cần chọn ra SỐ LƯỢNG LỚN NHẤT các sự kiện/cuộc họp không bị trùng lặp thời gian.
- BOJ cực kỳ hay ra dạng bài: Cho N cuộc họp với thời gian [Start, End], tìm cách xếp lịch được nhiều cuộc họp nhất.
- Bí quyết Tham lam: LUÔN ƯU TIÊN CUỘC HỌP KẾT THÚC SỚM NHẤT! (Sắp xếp theo End Time).
"""
def max_non_overlapping_intervals(intervals):
    # intervals là mảng các tuple (start, end)
    if not intervals: return 0
    
    # Bước 1: Sắp xếp theo thời gian KẾT THÚC (end) tăng dần. 
    # Nếu kết thúc cùng lúc, sắp xếp theo start tăng dần.
    intervals.sort(key=lambda x: (x[1], x[0]))
    
    count = 0
    last_end_time = -float('inf')
    
    for start, end in intervals:
        # Nếu cuộc họp này bắt đầu sau khi cuộc họp trước kết thúc -> Chọn!
        if start >= last_end_time:
            count += 1
            last_end_time = end
            
    return count


# ==========================================
# 36. DIVIDE AND CONQUER (CHIA ĐỂ TRỊ)
# ==========================================

"""
A. CLOSEST PAIR OF POINTS (Cặp điểm gần nhất 2D)
KHI NÀO DÙNG:
- Cho N điểm trên mặt phẳng tọa độ (N = 10^5). Tìm khoảng cách ngắn nhất giữa 2 điểm bất kỳ.
- Không thể dùng O(N^2) duyệt mọi cặp điểm. Dùng Chia để trị giảm xuống O(N log N) hoặc O(N log^2 N).
- Kỹ thuật: Chia đôi mặt phẳng theo trục X, tìm min 2 bên, rồi xét dải ranh giới (Strip) nằm giữa.
"""
import math

def distance(p1, p2):
    return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

def closest_pair(points):
    # points = [(x1, y1), (x2, y2), ...]
    points.sort(key=lambda x: x[0]) # Sắp xếp theo tọa độ X
    
    def solve(l, r):
        # Nếu chỉ có <= 3 điểm, vét cạn (Base case)
        if r - l <= 3:
            min_d = float('inf')
            for i in range(l, r):
                for j in range(i + 1, r + 1):
                    min_d = min(min_d, distance(points[i], points[j]))
            return min_d
            
        # Chia đôi mặt phẳng
        mid = (l + r) // 2
        mid_x = points[mid][0]
        
        # Trị từng nửa
        d1 = solve(l, mid)
        d2 = solve(mid + 1, r)
        d = min(d1, d2)
        
        # Xét dải ranh giới (Strip) ở giữa có chiều rộng 2*d
        strip = []
        for i in range(l, r + 1):
            if abs(points[i][0] - mid_x) < d:
                strip.append(points[i])
                
        # Sắp xếp các điểm trong strip theo tọa độ Y
        strip.sort(key=lambda p: p[1])
        
        # Kiểm tra các điểm trong strip (Chỉ cần xét tối đa 6-7 điểm lân cận nhờ tính chất hình học)
        for i in range(len(strip)):
            for j in range(i + 1, len(strip)):
                if strip[j][1] - strip[i][1] >= d:
                    break # Điểm y đã lệch quá d thì bỏ qua ngay
                d = min(d, distance(strip[i], strip[j]))
                
        return d
        
    return solve(0, len(points) - 1)


# ==========================================
# 37. MINIMUM VERTEX COVER (BAO PHỦ ĐỈNH NHỎ NHẤT)
# ==========================================

"""
A. MINIMUM VERTEX COVER ON TREE (DP trên cây)
KHI NÀO DÙNG:
- Bài toán: Chọn ít đỉnh nhất sao cho MỌI CẠNH trong cây đều có ít nhất 1 đầu mút được chọn.
- Áp dụng Tree DP. Trạng thái: dp[u][0] = Không chọn u, dp[u][1] = Có chọn u.
"""
import sys
sys.setrecursionlimit(200005)

def tree_vertex_cover(n, adj):
    # dp[u][0]: Số đỉnh tối thiểu cần chọn trong cây con gốc u NẾU KHÔNG CHỌN đỉnh u
    # dp[u][1]: Số đỉnh tối thiểu cần chọn trong cây con gốc u NẾU CHỌN đỉnh u
    dp = [[0, 1] for _ in range(n + 1)]
    visited = [False] * (n + 1)
    
    def dfs(u):
        visited[u] = True
        for v in adj[u]:
            if not visited[v]:
                dfs(v)
                # Nếu KHÔNG chọn u -> BẮT BUỘC phải chọn tất cả các đỉnh con v (để phủ cạnh u-v)
                dp[u][0] += dp[v][1]
                
                # Nếu CÓ chọn u -> Đỉnh con v có thể được chọn HOẶC không chọn (lấy phương án tối ưu hơn)
                dp[u][1] += min(dp[v][0], dp[v][1])
                
    # Giả sử cây liên thông, bắt đầu từ đỉnh 1
    dfs(1)
    return min(dp[1][0], dp[1][1])


# ==========================================
# 38. OFFLINE QUERIES (TRUY VẤN NGOẠI TUYẾN)
# ==========================================

"""
A. DSU WITH SORTING QUERIES (Union-Find kết hợp nén truy vấn)
KHI NÀO DÙNG:
- Đề bài cho đồ thị N đỉnh, M cạnh có trọng số. Sau đó hỏi Q truy vấn dạng: 
  "Nếu chỉ dùng các cạnh có trọng số <= W, đỉnh U và V có đi tới được nhau không?".
- Thay vì trả lời từng truy vấn (Online) bị TLE, ta lưu hết truy vấn lại, SẮP XẾP theo W tăng dần. 
- Vừa duyệt truy vấn, vừa nối các cạnh (Union-Find) tương ứng -> O(M log M + Q log Q).
"""
def offline_queries_dsu(n, edges, queries):
    # edges: list các tuple (weight, u, v)
    # queries: list các tuple (W, u, v, index_gốc_của_truy_vấn)
    
    # Sắp xếp cạnh và truy vấn theo giới hạn trọng số tăng dần
    edges.sort(key=lambda x: x[0])
    queries.sort(key=lambda x: x[0])
    
    parent = list(range(n + 1))
    def find(i):
        if parent[i] == i: return i
        parent[i] = find(parent[i])
        return parent[i]
        
    def union(i, j):
        root_i, root_j = find(i), find(j)
        if root_i != root_j:
            parent[root_i] = root_j
            
    ans = [False] * len(queries)
    edge_idx = 0
    
    for w, u, v, q_idx in queries:
        # Thêm tất cả các cạnh có trọng số <= W của truy vấn hiện tại vào hệ thống DSU
        while edge_idx < len(edges) and edges[edge_idx][0] <= w:
            union(edges[edge_idx][1], edges[edge_idx][2])
            edge_idx += 1
            
        # Trả lời truy vấn: Kiểm tra xem u và v có cùng thành phần liên thông không
        ans[q_idx] = (find(u) == find(v))
        
    return ans
