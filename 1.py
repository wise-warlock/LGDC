import sys

def solve():
    # Read all inputs from standard input
    input_data = sys.stdin.read().split()
    if not input_data: return
    
    out = []
    # Skip the first element (T) and process each testcase (4 strings per test case)
    for i in range(1, len(input_data), 4):
        S = input_data[i]
        grid = input_data[i+1] + input_data[i+2] + input_data[i+3]
        
        # Map each character to its (row, column) coordinates
        c2p = {ch: (j // 3, j % 3) for j, ch in enumerate(grid)}
        
        # Function to calculate the score string for a given sequence
        def get_scores(seq):
            r, c, d1, d2 = [0] * 3, [0] * 3, 0, 0
            res = []
            for ch in seq:
                x, y = c2p[ch]
                r[x] += 1; c[y] += 1
                d1 += (x == y); d2 += (x + y == 2)
                
                # Check bingo conditions for the current cell
                score = (r[x] == 3) + (c[y] == 3) + (x == y and d1 == 3) + (x + y == 2 and d2 == 3)
                res.append(score)
            return res
        
        tgt_scores = get_scores(S)
        chars = sorted(S)
        ans = []
        
        # Backtracking states
        r, c, d1, d2 = [0] * 3, [0] * 3, 0, 0
        
        def dfs(depth, used_mask):
            if depth == 9:
                return True
                
            for j, ch in enumerate(chars):
                # If character is not used yet
                if not (used_mask & (1 << j)):
                    x, y = c2p[ch]
                    
                    # Apply move
                    nonlocal d1, d2
                    r[x] += 1; c[y] += 1
                    d1 += (x == y); d2 += (x + y == 2)
                    
                    score = (r[x] == 3) + (c[y] == 3) + (x == y and d1 == 3) + (x + y == 2 and d2 == 3)
                    
                    # Prune: continue only if the score matches the target score at the current depth
                    if score == tgt_scores[depth]:
                        ans.append(ch)
                        if dfs(depth + 1, used_mask | (1 << j)):
                            return True
                        ans.pop()
                        
                    # Backtrack (undo move)
                    r[x] -= 1; c[y] -= 1
                    d1 -= (x == y); d2 -= (x + y == 2)
                    
            return False
        
        # Start backtracking
        dfs(0, 0)
        
        # Format the output string
        target_str = "".join(map(str, tgt_scores))
        ans_str = "".join(ans)
        out.append(f"{target_str} {ans_str}")
        
    # Print all results separated by a newline
    print('\n'.join(out))

if __name__ == '__main__':
    solve()
