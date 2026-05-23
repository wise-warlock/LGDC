# ==========================================
# 12. PRO MAX DATA STRUCTURES (CẤU TRÚC DỮ LIỆU BẬC CAO)
# ==========================================

"""
A. SEGMENT TREE WITH LAZY PROPAGATION (Cây phân đoạn + Cập nhật lười)
KHI NÀO DÙNG:
- Yêu cầu CẬP NHẬT MỘT ĐOẠN [L, R] (ví dụ: cộng thêm V vào tất cả phần tử từ L đến R).
- VÀ TRUY VẤN trên một đoạn [L, R] (Tìm Max/Min/Sum).
- Segment Tree thường (Point Update) sẽ bị TLE (chạy quá thời gian) nếu phải cập nhật từng phần tử một.
"""
def push_down(node, start, end, tree, lazy):
    if lazy[node] != 0:
        # Cập nhật giá trị hiện tại của node (Ví dụ: tính Tổng)
        tree[node] += lazy[node] * (end - start + 1)
        # Nếu chưa phải lá, đẩy giá trị lazy xuống 2 con
        if start != end:
            lazy[2 * node] += lazy[node]
            lazy[2 * node + 1] += lazy[node]
        # Xóa lazy của node hiện tại
        lazy[node] = 0

def update_lazy(node, start, end, l, r, val, tree, lazy):
    push_down(node, start, end, tree, lazy)
    if r < start or end < l:
        return
    if l <= start and end <= r:
        lazy[node] += val
        push_down(node, start, end, tree, lazy)
        return
    mid = (start + end) // 2
    update_lazy(2 * node, start, mid, l, r, val, tree, lazy)
    update_lazy(2 * node + 1, mid + 1, end, l, r, val, tree, lazy)
    tree[node] = tree[2 * node] + tree[2 * node + 1]

def query_lazy(node, start, end, l, r, tree, lazy):
    push_down(node, start, end, tree, lazy)
    if r < start or end < l:
        return 0 # Giá trị vô hại (0 cho Sum, inf cho Min)
    if l <= start and end <= r:
        return tree[node]
    mid = (start + end) // 2
    p1 = query_lazy(2 * node, start, mid, l, r, tree, lazy)
    p2 = query_lazy(2 * node + 1, mid + 1, end, l, r, tree, lazy)
    return p1 + p2


"""
B. SPARSE TABLE (Bảng thưa - Truy vấn RMQ O(1))
KHI NÀO DÙNG:
- Cần truy vấn Min/Max trên một đoạn [L, R] RẤT NHIỀU LẦN (vd: 10^6 lần).
- ĐẶC BIỆT: Mảng không bao giờ bị thay đổi (No Updates).
- Khởi tạo O(N log N), Truy vấn O(1) -> Nhanh hơn Segment Tree rất nhiều!
"""
def build_sparse_table(arr, n):
    LOG = 20
    st = [[0] * LOG for _ in range(n)]
    for i in range(n):
        st[i][0] = arr[i]
        
    for j in range(1, LOG):
        for i in range(n - (1 << j) + 1):
            st[i][j] = min(st[i][j - 1], st[i + (1 << (j - 1))][j - 1])
    return st

def query_sparse_table(st, l, r):
    # l, r là 0-based index
    length = r - l + 1
    j = length.bit_length() - 1 # Tìm k lớn nhất sao cho 2^k <= length
    return min(st[l][j], st[r - (1 << j) + 1][j])


# ==========================================
# 13. GRAPH MASTERY (ĐỈNH CAO ĐỒ THỊ)
# ==========================================

"""
A. STRONGLY CONNECTED COMPONENTS (Thành phần liên thông mạnh - Thuật toán Tarjan)
KHI NÀO DÙNG:
- Tìm các cụm đỉnh trong đồ thị CÓ HƯỚNG mà từ bất kỳ đỉnh nào trong cụm cũng đi đến được mọi đỉnh khác trong cụm.
- Dùng để giải bài toán 2-SAT (Thỏa mãn logic boolean).
"""
def tarjan_scc(n, adj):
    ids = [-1] * (n + 1)
    low = [-1] * (n + 1)
    on_stack = [False] * (n + 1)
    stack = []
    scc_list = []
    id_counter = [0]
    
    def dfs(u):
        ids[u] = low[u] = id_counter[0]
        id_counter[0] += 1
        stack.append(u)
        on_stack[u] = True
        
        for v in adj[u]:
            if ids[v] == -1:
                dfs(v)
                low[u] = min(low[u], low[v])
            elif on_stack[v]:
                low[u] = min(low[u], ids[v])
                
        if low[u] == ids[u]:
            scc = []
            while True:
                node = stack.pop()
                on_stack[node] = False
                scc.append(node)
                if node == u:
                    break
            scc_list.append(scc)
            
    for i in range(1, n + 1):
        if ids[i] == -1:
            dfs(i)
    return scc_list


"""
B. BIPARTITE MATCHING (Cặp ghép cực đại trên đồ thị 2 phía)
KHI NÀO DÙNG:
- Phân công công việc: Có N người và M công việc, mỗi người làm được vài việc. Tìm cách phân công sao cho số công việc hoàn thành là nhiều nhất.
- Đồ thị chia làm 2 tập độc lập (A và B), chỉ có đường đi nối từ A sang B.
"""
def bipartite_match(u, adj, match, visited):
    for v in adj[u]:
        if visited[v]:
            continue
        visited[v] = True
        # Nếu đỉnh v bên tập B chưa ghép với ai, HOẶC người đang ghép với v có thể chuyển sang ghép với đỉnh khác
        if match[v] == -1 or bipartite_match(match[v], adj, match, visited):
            match[v] = u
            return True
    return False

# Sử dụng:
# match = [-1] * (M + 1)
# matches_count = 0
# for i in range(1, N + 1):
#     visited = [False] * (M + 1)
#     if bipartite_match(i, adj, match, visited): matches_count += 1


# ==========================================
# 14. MATRIX & MODULAR ALGEBRA (ĐẠI SỐ & MA TRẬN)
# ==========================================

"""
A. MATRIX EXPONENTIATION (Lũy thừa ma trận O(K^3 log N))
KHI NÀO DÙNG:
- Tìm số Fibonacci thứ N (với N lên tới 10^18).
- Đếm số đường đi độ dài N trên đồ thị (N cực lớn).
- Giải các công thức truy hồi tuyến tính siêu lớn.
"""
def multiply_matrix(A, B, mod):
    rows_A = len(A)
    cols_A = len(A[0])
    cols_B = len(B[0])
    C = [[0] * cols_B for _ in range(rows_A)]
    for i in range(rows_A):
        for j in range(cols_B):
            for k in range(cols_A):
                C[i][j] = (C[i][j] + A[i][k] * B[k][j]) % mod
    return C

def power_matrix(A, p, mod):
    n = len(A)
    # Ma trận đơn vị (Identity Matrix)
    res = [[1 if i == j else 0 for j in range(n)] for i in range(n)]
    base = A
    while p > 0:
        if p % 2 == 1:
            res = multiply_matrix(res, base, mod)
        base = multiply_matrix(base, base, mod)
        p //= 2
    return res


"""
B. EXTENDED EUCLIDEAN ALGORITHM (Euclid mở rộng)
KHI NÀO DÙNG:
- Giải phương trình Diophantine: A*x + B*y = UCLN(A, B).
- Tìm nghịch đảo modulo: (A * x) % M = 1 -> Tìm x (Rất cần thiết trong tính tổ hợp).
"""
def ext_gcd(a, b):
    # Trả về: (g, x, y) sao cho a*x + b*y = g = gcd(a, b)
    if b == 0:
        return a, 1, 0
    g, x1, y1 = ext_gcd(b, a % b)
    x = y1
    y = x1 - y1 * (a // b)
    return g, x, y

def mod_inverse(A, M):
    g, x, y = ext_gcd(A, M)
    if g != 1:
        return -1 # Không tồn tại nghịch đảo modulo
    return (x % M + M) % M # Đảm bảo x luôn dương

# ==========================================
# 15. PYTHON MAGIC & TRICKS (BÍ KÍP PYTHON TÍCH HỢP)
# ==========================================

"""
A. THƯ VIỆN COLLECTIONS
KHI NÀO DÙNG: Cần đếm tần số, dùng Hàng đợi, hoặc tránh lỗi KeyError khi tạo Đồ thị.
"""
from collections import Counter, defaultdict, deque

# 1. Counter: Đếm tần số xuất hiện của các phần tử trong O(N)
# arr = [1, 2, 2, 3, 3, 3]
# count = Counter(arr)  -> count[3] sẽ trả về 3. Rất tiện để kiểm tra số lần xuất hiện.

# 2. defaultdict: Dictionary tự động khởi tạo giá trị mặc định. Rất tốt cho Đồ thị.
# adj = defaultdict(list)
# adj[1].append(2) -> Không bao giờ bị lỗi KeyError kể cả khi key '1' chưa tồn tại.

"""
B. THƯ VIỆN ITERTOOLS (Sinh Tổ hợp, Chỉnh hợp, Hoán vị)
KHI NÀO DÙNG: Các bài toán yêu cầu Vét cạn (Brute-force) với N nhỏ (N <= 10).
"""
from itertools import permutations, combinations, accumulate

# 1. Sinh Hoán vị (Có phân biệt thứ tự)
# perms = list(permutations([1, 2, 3], 2)) -> [(1, 2), (1, 3), (2, 1), (2, 3), (3, 1), (3, 2)]

# 2. Sinh Tổ hợp (Không phân biệt thứ tự)
# combs = list(combinations([1, 2, 3], 2)) -> [(1, 2), (1, 3), (2, 3)]

# 3. Tính mảng cộng dồn cực nhanh (Prefix Sum 1D)
# arr = [1, 2, 3, 4]
# pref = list(accumulate(arr)) -> [1, 3, 6, 10]

"""
C. BISECT (Chặt nhị phân tích hợp sẵn)
KHI NÀO DÙNG: Tìm vị trí chèn phần tử vào mảng đã sắp xếp trong O(log N). Thay vì phải tự viết Binary Search.
"""
import bisect
# arr = [1, 3, 3, 5, 7]
# bisect.bisect_left(arr, 3)  -> Trả về 1 (Vị trí ĐẦU TIÊN của số 3)
# bisect.bisect_right(arr, 3) -> Trả về 3 (Vị trí NGAY SAU số 3 cuối cùng)
# Mẹo: Số lượng phần tử 'x' trong mảng = bisect_right(arr, x) - bisect_left(arr, x)

"""
D. CUSTOM SORTING (Sắp xếp tùy chỉnh siêu tốc bằng Lambda)
KHI NÀO DÙNG: Sắp xếp mảng nhiều chiều theo nhiều tiêu chí phức tạp.
"""
# arr = [(1, 5), (2, 3), (1, 4)]
# Yêu cầu: Sắp xếp ưu tiên phần tử đầu TĂNG DẦN, nếu bằng nhau thì phần tử sau GIẢM DẦN.
# arr.sort(key=lambda x: (x[0], -x[1])) -> Kết quả: [(1, 5), (1, 4), (2, 3)]


# ==========================================
# 16. FUNDAMENTAL TECHNIQUES (KỸ THUẬT CƠ BẢN HIỆU QUẢ)
# ==========================================

"""
A. TWO POINTERS (Hai con trỏ)
KHI NÀO DÙNG: 
- Thường dùng trên MẢNG ĐÃ SẮP XẾP.
- Giúp giảm độ phức tạp từ O(N^2) xuống O(N).
- Ví dụ: Tìm 2 số có tổng bằng K, Đếm số cặp có hiệu bằng K.
"""
def two_pointers_sum(arr, target):
    arr.sort() # Bắt buộc phải sắp xếp
    left, right = 0, len(arr) - 1
    
    while left < right:
        curr = arr[left] + arr[right]
        if curr == target:
            return True, left, right # Tìm thấy
        elif curr < target:
            left += 1  # Cần tổng lớn hơn, nhích con trỏ trái
        else:
            right -= 1 # Cần tổng nhỏ hơn, nhích con trỏ phải
            
    return False, -1, -1


"""
B. SLIDING WINDOW (Cửa sổ trượt)
KHI NÀO DÙNG: 
- Tìm mảng con / đoạn con LIÊN TIẾP có độ dài K hoặc thỏa mãn điều kiện X.
- O(N) truy duyệt.
"""
def sliding_window_max_sum(arr, k):
    # Tìm đoạn con liên tiếp độ dài K có tổng lớn nhất
    n = len(arr)
    if n < k: return -1
    
    # Tính tổng cửa sổ đầu tiên
    window_sum = sum(arr[:k])
    max_sum = window_sum
    
    # Trượt cửa sổ đi từng ô
    for i in range(1, n - k + 1):
        # Tổng mới = Tổng cũ - phần tử bị loại ra + phần tử mới vào
        window_sum = window_sum - arr[i - 1] + arr[i + k - 1]
        max_sum = max(max_sum, window_sum)
        
    return max_sum


"""
C. MATRIX ROTATION (Xoay Ma Trận bằng Python 1 dòng)
KHI NÀO DÙNG: 
- Rất hay gặp trong các bài toán Mô phỏng (Simulation).
"""
def rotate_90_clockwise(matrix):
    # Xoay ma trận NxM thành MxN theo chiều kim đồng hồ
    # Hàm zip(*...) unpacking ma trận, [::-1] để đảo ngược các hàng
    return [list(elem) for elem in zip(*matrix[::-1])]

def rotate_90_counter_clockwise(matrix):
    # Xoay ngược chiều kim đồng hồ
    return [list(elem) for elem in zip(*matrix)][::-1]


# ==========================================
# 17. MATH BASICS (TOÁN CƠ BẢN NHANH)
# ==========================================

import math

# Ước chung lớn nhất (GCD)
# math.gcd(a, b)

# Bội chung nhỏ nhất (LCM) - Từ Python 3.9 trở đi
# math.lcm(a, b)

# Khai căn nguyên (Lấy phần nguyên của căn bậc 2)
# math.isqrt(n)

# ==========================================
# 18. MASTERCLASS ALGORITHMS (THUẬT TOÁN ĐỈNH CAO)
# ==========================================

"""
A. MO'S ALGORITHM (Thuật toán Mo - Square Root Decomposition)
KHI NÀO DÙNG:
- Trả lời hàng vạn truy vấn trên đoạn [L, R] nhưng KHÔNG CÓ THAO TÁC CẬP NHẬT (Offline Queries).
- Đặc biệt dùng khi bài toán KHÔNG THỂ giải bằng Segment Tree (ví dụ: Đếm số lượng phần tử phân biệt trong đoạn [L, R], hoặc đếm số lần xuất hiện chẵn/lẻ).
- Mẹo: Việc sắp xếp các truy vấn theo block (căn bậc 2 của N) giúp tổng thời gian trượt con trỏ chỉ là O(N * sqrt(N)).
"""
def mos_algorithm(arr, queries):
    # queries: danh sách các tuple (L, R, index_ban_đầu)
    n = len(arr)
    block_size = int(n ** 0.5) + 1
    
    # Sắp xếp truy vấn theo Block của L, sau đó theo R.
    # Trick tối ưu: Block chẵn thì R tăng dần, Block lẻ thì R giảm dần (giảm thời gian trượt)
    queries.sort(key=lambda x: (x[0] // block_size, x[1] if (x[0] // block_size) % 2 == 0 else -x[1]))
    
    answers = [0] * len(queries)
    curr_L, curr_R = 0, -1
    curr_result = 0 # Lưu kết quả hiện tại của cửa sổ (ví dụ: số phần tử phân biệt)
    count = [0] * 1000005 # Mảng đếm tần số (tùy bài)
    
    def add(idx):
        nonlocal curr_result
        # Logic khi thêm arr[idx] vào cửa sổ (ví dụ minh họa đếm số phân biệt)
        if count[arr[idx]] == 0:
            curr_result += 1
        count[arr[idx]] += 1

    def remove(idx):
        nonlocal curr_result
        # Logic khi bỏ arr[idx] khỏi cửa sổ
        count[arr[idx]] -= 1
        if count[arr[idx]] == 0:
            curr_result -= 1

    for L, R, q_idx in queries:
        # Mở rộng hoặc thu hẹp cửa sổ để khớp với truy vấn hiện tại
        while curr_L > L:
            curr_L -= 1; add(curr_L)
        while curr_R < R:
            curr_R += 1; add(curr_R)
        while curr_L < L:
            remove(curr_L); curr_L += 1
        while curr_R > R:
            remove(curr_R); curr_R -= 1
            
        answers[q_idx] = curr_result
        
    return answers


"""
B. CONVEX HULL - MONOTONE CHAIN (Bao Lồi Hình Học)
KHI NÀO DÙNG:
- Tìm một đa giác lồi nhỏ nhất bao trọn toàn bộ N điểm trên mặt phẳng.
- Tưởng tượng bạn đóng đinh vào N điểm trên bảng gỗ, sau đó lấy 1 sợi dây thun buộc vòng quanh tất cả các đinh. Sợi dây thun đó chính là Bao Lồi.
- Độ phức tạp: O(N log N) do thao tác sắp xếp.
"""
def convex_hull(points):
    # points = [(x, y), (x, y), ...]
    points = sorted(set(points)) # Sắp xếp theo X, nếu X bằng nhau sắp xếp theo Y
    if len(points) <= 1:
        return points

    # Hàm CCW nội bộ: Rẽ trái > 0, Cùng chiều < 0, Thẳng hàng = 0
    def cross(o, a, b):
        return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])

    # Xây dựng nửa dưới bao lồi
    lower = []
    for p in points:
        while len(lower) >= 2 and cross(lower[-2], lower[-1], p) <= 0:
            lower.pop()
        lower.append(p)

    # Xây dựng nửa trên bao lồi
    upper = []
    for p in reversed(points):
        while len(upper) >= 2 and cross(upper[-2], upper[-1], p) <= 0:
            upper.pop()
        upper.append(p)

    # Nối lại (bỏ đỉnh cuối của mỗi nửa vì bị trùng lặp)
    return lower[:-1] + upper[:-1]


"""
C. TERNARY SEARCH (Tìm kiếm tam phân)
KHI NÀO DÙNG:
- Bạn cần tìm Max hoặc Min của một hàm số Lồi/Lõm (Unimodal Function - hàm có dạng hình Parabol chữ U hoặc chữ U ngược).
- Không dùng được Chặt Nhị Phân (Binary Search) vì hàm không đơn điệu (không tăng mãi hoặc giảm mãi).
"""
def ternary_search(low, high):
    # low, high là kiểu số thực (float)
    # Tìm cực tiểu của hàm số f(x)
    for _ in range(100): # Lặp 100 lần với số thực là đủ độ chính xác (sai số cực nhỏ)
        mid1 = low + (high - low) / 3
        mid2 = high - (high - low) / 3
        
        # Hàm f(x) do bạn tự định nghĩa
        if f(mid1) < f(mid2):
            high = mid2 # Cực tiểu nằm lệch về bên trái mid2
        else:
            low = mid1  # Cực tiểu nằm lệch về bên phải mid1
            
    return f(low) # Trả về giá trị cực tiểu

def f(x):
    # Dummy function: y = (x - 2)^2 + 5 (Cực tiểu tại x = 2, y = 5)
    return (x - 2)**2 + 5


"""
D. ROLLING HASH / STRING HASHING (Băm Chuỗi Siêu Tốc)
KHI NÀO DÙNG:
- So sánh xem 2 chuỗi con có giống nhau không trong thời gian O(1) sau khi đã tiền xử lý.
- Có thể dùng thay thế cho thuật toán KMP trong nhiều bài toán tìm chuỗi phức tạp.
"""
def build_string_hash(s):
    n = len(s)
    MOD = 10**9 + 7
    BASE = 313 # Số nguyên tố cơ sở
    
    pref_hash = [0] * (n + 1)
    power = [1] * (n + 1)
    
    for i in range(n):
        # Tính lũy thừa của BASE
        power[i + 1] = (power[i] * BASE) % MOD
        # Hash cộng dồn
        pref_hash[i + 1] = (pref_hash[i] * BASE + ord(s[i])) % MOD
        
    return pref_hash, power

def get_substring_hash(pref_hash, power, L, R, MOD=10**9+7):
    # L, R là 1-based index (vị trí từ 1 đến N). Lấy hash của chuỗi s[L-1 : R]
    res = (pref_hash[R] - pref_hash[L - 1] * power[R - L + 1]) % MOD
    return (res + MOD) % MOD # Đảm bảo hash luôn dương

# ==========================================
# 19. PYTHON MICRO-OPTIMIZATIONS (TỐI ƯU HÓA VI MÔ)
# ==========================================

"""
A. QUY TẮC SỐ 1: LUÔN VIẾT CODE TRONG HÀM (LOCAL VARIABLES)
Tại sao? Trong CPython, truy xuất biến cục bộ (local variables) bên trong một hàm (ví dụ: def solve():)
nhanh hơn đáng kể (khoảng 15-20%) so với truy xuất biến toàn cục (global variables).
Bởi vì Python dùng mảng tĩnh (STORE_FAST) cho biến cục bộ, còn biến toàn cục phải tra cứu Dictionary (STORE_NAME).
"""
# TỐT:
def main():
    n = 1000000
    arr = [0] * n
    # Xử lý logic ở đây...
# main()

# XẤU (Nên tránh khi làm giải thuật):
# n = 1000000
# arr = [0] * n
# for i in range(n): ...


"""
B. LIST & ARRAY TRICKS (Kỹ thuật mảng cực nhanh)
KHI NÀO DÙNG: Cần xử lý mảng dữ liệu khổng lồ (N > 10^5).
"""
# 1. Khởi tạo mảng (Pre-allocation) NHANH HƠN list.append()
# Nếu biết trước kích thước, KHÔNG dùng append.
n = 100000
arr_fast = [0] * n        # Nhanh gấp đôi!
arr_slow = []
# for i in range(n): arr_slow.append(0) # Bỏ cách này đi

# 2. List Comprehension (Nhanh hơn vòng lặp for thường)
# Viết gộp vòng lặp vào trong mảng được tối ưu hóa ở tầng C của Python.
old_arr = [1, 2, 3, 4, 5]
new_arr = [x * 2 for x in old_arr if x % 2 != 0]

# 3. Flatten (Làm phẳng) Mảng 2D siêu tốc
matrix = [[1, 2], [3, 4], [5, 6]]
flat_list = [item for sublist in matrix for item in sublist] # Kết quả: [1, 2, 3, 4, 5, 6]


"""
C. SET & DICT (Vũ khí tra cứu O(1))
KHI NÀO DÙNG: Yêu cầu kiểm tra phần tử CÓ TỒN TẠI KHÔNG (toán tử 'in').
"""
# Nếu kiểm tra 'if x in arr' với List -> Mất O(N) thời gian (Rất dễ TLE).
# Nếu biến arr thành Set -> Mất O(1) thời gian (Chớp mắt).
arr = [1, 5, 9, 100, 2500]
lookup_set = set(arr)
# if 100 in lookup_set:  # Nhanh hơn hàng ngàn lần so với List nếu mảng lớn

# Gộp 2 Dictionary nhanh nhất (Python 3.9+)
dict1 = {'a': 1, 'b': 2}
dict2 = {'b': 3, 'c': 4}
merged_dict = dict1 | dict2 # Kết quả: {'a': 1, 'b': 3, 'c': 4}


"""
D. VÒNG LẶP FOR / WHILE BIẾN TẤU (Loop Hacks)
"""
# 1. Hàm ENUMERATE: Vừa lấy giá trị, vừa lấy vị trí (Nhanh và chuẩn Pythonic)
# Thay vì: for i in range(len(arr)): print(i, arr[i])
# Hãy dùng:
# for idx, val in enumerate(arr):
#     pass

# 2. Hàm ZIP: Duyệt nhiều mảng cùng lúc không lo lệch index
arr_A = [1, 2, 3]
arr_B = ['A', 'B', 'C']
# for a, b in zip(arr_A, arr_B):
#     print(a, b) # In ra: 1 A, 2 B, 3 C

# 3. Cú pháp FOR...ELSE (Cực kỳ xịn trong Competitive Programming)
# KHI NÀO DÙNG: Cần tìm kiếm thứ gì đó trong mảng. Thay vì phải dùng biến cờ (flag = True/False),
# khối 'else' sẽ ĐƯỢC CHẠY nếu vòng lặp kết thúc bình thường (KHÔNG bị ngắt bởi 'break').
target = 5
for x in arr_A:
    if x == target:
        print("Tìm thấy!")
        break
else:
    # Đoạn này CHỈ chạy nếu không có lệnh break nào xảy ra ở trên
    print("Tìm hết mảng rồi nhưng không thấy!")


"""
E. ADVANCED SORTING (Sắp xếp bằng itemgetter - Nhanh hơn Lambda)
KHI NÀO DÙNG: Khi bạn cần sắp xếp mảng tuple/list mà bị TLE khi dùng lambda.
"""
from operator import itemgetter

data = [(1, 'apple', 50), (2, 'banana', 20), (3, 'cherry', 50)]

# Sắp xếp theo phần tử thứ 3 (index 2) tăng dần, nếu bằng thì xếp theo index 0 giảm dần.
# Mẹo: Lambda linh hoạt hơn, nhưng itemgetter CHẠY NHANH HƠN ở tầng C của Python.
# Nếu chỉ đơn thuần là lấy index, hãy dùng itemgetter.
data.sort(key=itemgetter(2, 0))


"""
F. MẸO ĐỌC DỮ LIỆU ĐỈNH CAO (Cắt từng chữ - Iterator mapping)
KHI NÀO DÙNG: Khi file Input khổng lồ và có hàng triệu con số rải rác ở nhiều dòng.
"""
import sys
def ultra_fast_read():
    # Đọc TOÀN BỘ file đầu vào dưới dạng 1 chuỗi dài, sau đó cắt theo khoảng trắng
    # Iterator map giúp không phải nạp toàn bộ mảng vào RAM cùng lúc.
    token_iterator = map(int, sys.stdin.read().split())
    
    # Hàm next() sẽ nhổ từng số ra một cách cực kỳ mượt mà
    try:
        N = next(token_iterator)
        M = next(token_iterator)
        # arr = [next(token_iterator) for _ in range(N)]
    except StopIteration:
        pass
