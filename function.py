def avg(first, *rest):
    return (first + sum(rest)) / (1 + len(rest))

print(avg(10, 20, 30))
print(avg(10, 20, 30, 40, 50))
