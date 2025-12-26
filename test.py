a=3
b=2
answer = 0
def calculate(a, b):
    answer = a + b
    return answer

def test():
    assert calculate(3, 2) == 5
    assert calculate(-1, 1) == 0
    assert calculate(0, 0) == 0
    return "All tests passed."

print(calculate(a, b))
print(test())