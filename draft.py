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
