def fast_function():
    return sum([i for i in range(100)])

def slow_function():
    total = 0
    for i in range(100):
        for j in range(100):
            total += i * j
    return total
