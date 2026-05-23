import sys

def solve():
    # Use a generator to lazily process inputs, saving memory & execution time
    def get_ints():
        for token in sys.stdin.read().split():
            yield int(token)
            
    tokens = get_ints()
    try:
        T = next(tokens)
    except StopIteration:
        return
        
    MOD = 10**9 + 7
    MAX_N = 50005
    
    # Precompute factorials up to the maximum possible N
    fact = [1] * MAX_N
    for i in range(1, MAX_N):
        fact[i] = (fact[i-1] * i) % MOD
        
    out = []
    for _ in range(T):
        n = next(tokens)
        m = next(tokens)
        
        A = [next(tokens) for _ in range(n)]
        
        # Difference array to calculate frequency of each index efficiently
        diff = [0] * (n + 2)
        for _ in range(m):
            diff[next(tokens)] += 1
            diff[next(tokens) + 1] -= 1
            
        freq = [0] * n
        curr = 0
        for i in range(1, n + 1):
            curr += diff[i]
            freq[i-1] = curr
            
        # Sort both array A and frequency tracker in descending order
        freq.sort(reverse=True)
        A.sort(reverse=True)
        
        # Calculating the Maximum Value Output
        max_sum = sum(f * a for f, a in zip(freq, A))
        
        # Count the number of ways to arrange the sequence (permutations on tied frequencies)
        ways = 1
        count = 1
        for i in range(1, n):
            if freq[i] == freq[i-1]:
                count += 1
            else:
                ways = (ways * fact[count]) % MOD
                count = 1
                
        # Don't forget to multiply the factorial combination of the last grouped frequencies
        ways = (ways * fact[count]) % MOD
        
        out.append(f"{max_sum} {ways}")
        
    # Fast standard I/O format
    print('\n'.join(out))

if __name__ == '__main__':
    solve()
