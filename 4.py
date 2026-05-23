import sys

def solve():
    # Read all tokens from standard input
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    T_cases = int(input_data[0])
    idx = 1
    
    out = []
    
    for _ in range(T_cases):
        n = int(input_data[idx])
        idx += 1
        
        H = []
        for _ in range(n):
            H.append(int(input_data[idx]))
            idx += 1
            
        R = []
        for _ in range(n):
            R.append(int(input_data[idx]))
            idx += 1
            
        # Group properties and sort descending by height
        toys = [(H[i], R[i], i + 1) for i in range(n)]
        toys.sort(key=lambda x: x[0], reverse=True)
        
        TH = [x[0] for x in toys]
        TR = [x[1] for x in toys]
        T_orig = [x[2] for x in toys]
        
        n_states = n << 4
        
        def run_dp(case_num):
            parents = [[-1] * n_states for _ in range(n)]
            active_states = [0]
            
            for i in range(1, n):
                new_active = []
                th_i = TH[i]
                tr_i = TR[i]
                pi = parents[i]
                
                for state_code in active_states:
                    other_idx = state_code >> 4
                    is_right = (state_code >> 3) & 1
                    mod_L = (state_code >> 2) & 1
                    
                    if is_right:
                        left_idx = other_idx
                        right_idx = i - 1
                    else:
                        left_idx = i - 1
                        right_idx = other_idx
                        
                    # Evaluate placing the toy on the Left boundary
                    if th_i < TH[left_idx]:
                        if case_num == 1:
                            valid_L = (tr_i < TR[left_idx]) if mod_L == 0 else (tr_i > TR[left_idx])
                        else:
                            valid_L = (tr_i > TR[left_idx]) if mod_L == 0 else (tr_i < TR[left_idx])
                            
                        if valid_L:
                            nxt_code = (right_idx << 4) | ((1 - mod_L) << 2) | 2 | (state_code & 1)
                            if pi[nxt_code] == -1:
                                pi[nxt_code] = state_code  # Record parent mapping path (0 assigned implies 'L')
                                new_active.append(nxt_code)
                                
                    # Evaluate placing the toy on the Right boundary
                    if th_i < TH[right_idx]:
                        mod_R = (i - 1 - mod_L) & 1
                        if case_num == 1:
                            valid_R = (tr_i < TR[right_idx]) if mod_R == 0 else (tr_i > TR[right_idx])
                        else:
                            valid_R = (tr_i > TR[right_idx]) if mod_R == 0 else (tr_i < TR[right_idx])
                            
                        if valid_R:
                            nxt_code = (left_idx << 4) | 8 | (state_code & 4) | (state_code & 2) | 1
                            if pi[nxt_code] == -1:
                                pi[nxt_code] = state_code | 16384  # Combine parent trace pointer with 'R' choice flag utilizing upper bit (1 << 14)
                                new_active.append(nxt_code)
                                
                active_states = new_active
                if not active_states:
                    return None  # Short-circuit evaluating further if a branch completely breaks
                    
            # At culmination, confirm path exists with both left sequence and right sequence formed
            for state_code in active_states:
                if (state_code & 3) == 3:
                    path = []
                    curr = state_code
                    for i in range(n - 1, 0, -1):
                        val = parents[i][curr]
                        choice = val >> 14
                        curr = val & 16383
                        path.append(choice)
                    path.reverse()
                    return path
            return None
            
        path = run_dp(1)
        if not path:
            path = run_dp(2)
            
        if path:
            left_part = []
            right_part = []
            for i in range(n - 1):
                if path[i] == 0:
                    left_part.append(T_orig[i + 1])
                else:
                    right_part.append(T_orig[i + 1])
            
            # Left prefix pushes iteratively backwards, reversing it aligns left-to-right correctly      
            left_part.reverse()
            ans = left_part + [T_orig[0]] + right_part
            out.append(" ".join(map(str, ans)))
        else:
            out.append("-1")
            
    print("\n".join(out))

if __name__ == '__main__':
    solve()
