from sympy import symbols, Eq, solve

x = symbols('x')

Re = 2000
Rb2 = 30000
Rb1 = 70000
Vbe = 0.7
Vcc = 10

# Define the equation
equation = Eq((x * Re + Vbe) / Rb2 + x, (Vcc - Vbe - x * Re) / Rb1)

# Solve the equation
solution = solve(equation, x)

print(solution)