import sys

def solve():
    # Fast I/O
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    T = int(input_data[0])
    idx = 1
    
    MOD = 10**9 + 7
    out = []
    
    for _ in range(T):
        R = int(input_data[idx])
        C = int(input_data[idx+1])
        N = int(input_data[idx+2])
        idx += 3
        
        U = input_data[idx : idx+R]
        idx += R
        
        F = input_data[idx]
        idx += 1
        
        # 1. Precompute 2D Prefix Sums to quickly check for favorite fruits
        fruit_map = {'S': 0, 'B': 1, 'R': 2}
        pref = [[[0] * (C + 1) for _ in range(R + 1)] for _ in range(3)]
        
        for i in range(R):
            row = U[i]
            for j in range(C):
                char = row[j]
                for f in range(3):
                    pref[f][i+1][j+1] = pref[f][i][j+1] + pref[f][i+1][j] - pref[f][i][j]
                if char in fruit_map:
                    pref[fruit_map[char]][i+1][j+1] += 1
                    
        req = [fruit_map[ch] for ch in F]
        
        # 2. DP Tables
        # next_DP stores ways for the (k+1)-th step
        # next_SumR and next_SumC are suffix sums of next_DP to optimize interval summing
        next_DP = [[0] * C for _ in range(R)]
        next_SumR = [[0] * C for _ in range(R)]
        next_SumC = [[0] * C for _ in range(R)]
        
        # Base Case: evaluating for the last friend (k = N - 1)
        f_last = req[-1]
        for r in range(R - 1, -1, -1):
            for c in range(C - 1, -1, -1):
                # O(1) Check if the bounding piece has the specific fruit
                val = pref[f_last][R][C] - pref[f_last][r][C] - pref[f_last][R][c] + pref[f_last][r][c]
                if val > 0:
                    next_DP[r][c] = 1
                
                # Precompute suffix sums locally
                sr = next_DP[r][c]
                if r + 1 < R: sr = (sr + next_SumR[r+1][c]) % MOD
                next_SumR[r][c] = sr
                
                sc = next_DP[r][c]
                if c + 1 < C: sc = (sc + next_SumC[r][c+1]) % MOD
                next_SumC[r][c] = sc
                
        # DP transitions for the other friends
        for k in range(N - 2, -1, -1):
            curr_DP = [[0] * C for _ in range(R)]
            curr_SumR = [[0] * C for _ in range(R)]
            curr_SumC = [[0] * C for _ in range(R)]
            f_k = req[k]
            
            for r in range(R - 1, -1, -1):
                for c in range(C - 1, -1, -1):
                    ans = 0
                    
                    # - Horizontal Cuts: Binary search the smallest valid top cut
                    low, high = r + 1, R - 1
                    ans_nr = R
                    while low <= high:
                        mid = (low + high) // 2
                        val = pref[f_k][mid][C] - pref[f_k][r][C] - pref[f_k][mid][c] + pref[f_k][r][c]
                        if val > 0:
                            ans_nr = mid
                            high = mid - 1
                        else:
                            low = mid + 1
                    
                    if ans_nr < R:  # Using suffix sum to add all valid permutations simultaneously 
                        ans = (ans + next_SumR[ans_nr][c]) % MOD
                        
                    # - Vertical Cuts: Binary search the smallest valid left cut
                    low, high = c + 1, C - 1
                    ans_nc = C
                    while low <= high:
                        mid = (low + high) // 2
                        val = pref[f_k][R][mid] - pref[f_k][r][mid] - pref[f_k][R][c] + pref[f_k][r][c]
                        if val > 0:
                            ans_nc = mid
                            high = mid - 1
                        else:
                            low = mid + 1
                            
                    if ans_nc < C:  # Using suffix sum to add all valid permutations simultaneously
                        ans = (ans + next_SumC[r][ans_nc]) % MOD
                        
                    curr_DP[r][c] = ans
                    
                    # Update active suffixes for upper DP layer
                    sr = ans
                    if r + 1 < R: sr = (sr + curr_SumR[r+1][c]) % MOD
                    curr_SumR[r][c] = sr
                    
                    sc = ans
                    if c + 1 < C: sc = (sc + curr_SumC[r][c+1]) % MOD
                    curr_SumC[r][c] = sc
                    
            next_DP, next_SumR, next_SumC = curr_DP, curr_SumR, curr_SumC
            
        out.append(str(next_DP[0][0]))
        
    print('\n'.join(out))

if __name__ == '__main__':
    solve()
