numbers = [1.5, 2.3, 0.7, -0.001, 4.4]
total = 0
for num in numbers:
    assert num > 0.0, 'List contains negative input'
    total += num


