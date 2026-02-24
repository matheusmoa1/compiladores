
from compiler import compile_ec1

tests = [
    "42",
    "(7 + 11)",
    "(7 + (3 + 8))",
    "((10 * 2) - (9 / 3))"
]

for t in tests:
    print("Programa:", t)
    print(compile_ec1(t))
