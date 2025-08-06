import time
import random

FLAG = "Blitz{SUD0_M4K3_B07***}"
MOD = 10**9 + 7
M = [
    [1, 2, 3],
    [3, 1, 2],
    [2, 3, 1],
]

def matrix_multiply(a, b):
    c = [[0] * len(b) for _ in range(len(a))]
    for i in range(len(a)):
        for j in range(len(b[0])):
            for k in range(len(b)):
                c[i][j] = (c[i][j] + a[i][k] * b[k][j]) % MOD
    return c

def matrix_power(m, p):
    result = [[int(i == j) for j in range(len(m))] for i in range(len(m))]  # Identity matrix
    while p > 0:
        if p % 2 == 1:
            result = matrix_multiply(result, m)
        m = matrix_multiply(m, m)
        p //= 2
    return result

def compute_bot(b0, y0, r0, n):
    bot = [
        [b0, y0, r0],
    ]

    if n == 0:
        return bot[0]

    m = matrix_power(M, n)

    return matrix_multiply(bot, m)[0]

def main():
    test_cases = [
        [1, 2, 3, 0],
        [1, 2, 3, 1],
        [1, 2, 3, 2],
        [1, 2, 3, 3],
        [random.randint(1, 10), random.randint(1, 10), random.randint(1, 10), 10],
        [random.randint(10, 100), random.randint(10, 100), random.randint(10, 100), 100],
        [random.randint(100, 1000), random.randint(100, 1000), random.randint(100, 1000), 1000],
        [random.randint(1000, 1000000), random.randint(1000, 1000000), random.randint(1000, 1000000), 1000000],
        [random.randint(1000000, 1000000000000), random.randint(1000000, 1000000000000), random.randint(1000000, 1000000000000), 1000000000000],
        [random.randint(1000000000000, 10**18), random.randint(1000000000000, 10**18), random.randint(1000000000000, 10**18), 10**18],
    ]

    expected_results = []
    for t in test_cases:
        expected_results.append(compute_bot(*t))

    start = time.time()
    for i in range(len(test_cases)):
        print(*test_cases[i], flush=True)
        try:
            answer = list(map(int, input().strip().split()))
            if answer != expected_results[i]:
                print("Wrong Answer", flush=True)
                return
        except ValueError:
            print("Wrong Answer", flush=True)
            return

    end = time.time()
    duration = end - start
    if duration > 3:
        print("Time Limit Exceeded", flush=True)
        return

    print(FLAG, flush=True)

if __name__ == "__main__":
    main()