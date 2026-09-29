import math
import numpy as np

print("-----Завдання 1-----")

def f(x1, x2):
    return 3 * (x1 - 10) ** 2 - x1 * x2 + 4 * x2 ** 2

def df1(x1, x2):
    return 6 * (x1 - 10) - x2

def df2(x1, x2):
    return - x1 + 8 * x2

x1 = -16
x2 = -16

df1_0 = 0
df2_0 = 0

s1 = 0
s2 = 0

n = 0
while True:

    if n == 0:
        df1_0 = df1(x1, x2)
        df2_0 = df2(x1, x2)
        s1 = - df1_0
        s2 = - df2_0

    else:
        df1_1 = df1(x1, x2)
        df2_1 = df2(x1, x2)
        dff1 = math.sqrt(df1_1 ** 2 + df2_1 ** 2)
        dff0 = math.sqrt(df1_0 ** 2 + df2_0 ** 2)
        s1 = - df1_1 + dff1 ** 2 * s1 / dff0 ** 2
        s2 = - df2_1 + dff1 ** 2 * s2 / dff0 ** 2
        df1_0 = df1_1
        df2_0 = df2_1

    l = (-(df1_0 * s1 + df2_0 * s2)) / (6 * s1**2 - 2 * s1 * s2 + 8 * s2**2)

    print(f"\nІтерація {n}")
    print(f"Градієнт: [{df1_0:.3f}, {df2_0:.3f}]")
    print(f"Напрямок s: [{s1:.3f}, {s2:.3f}]")
    print(f"Крок l: {l:.3f}\n")

    x1 += l * s1
    x2 += l * s2
    df1_1 = df1(x1, x2)
    df2_1 = df2(x1, x2)
    n += 1

    print(f"l_{n - 1} = {l:.3f}, x_{n} = [{x1:.3f}, {x2:.3f}] , ||f(x_{n})|| = {math.sqrt(df1(x1, x2) ** 2 + df2(x1, x2) ** 2):.3f}")
    if n == 2:
        break


print("\n-----Завдання 2-----")

def f(x1, x2):
    return 3 * (x1 - 10) ** 2 - x1 * x2 + 4 * x2 ** 2

def df1(x1, x2):
    return 6 * (x1 - 10) - x2

def df2(x1, x2):
    return - x1 + 8 * x2

x1 = -16
x2 = -16

a = np.array([[1.0, 0.0], [0.0, 1.0]])
n = 0

while n < 2:
    df1_0 = df1(x1, x2)
    df2_0 = df2(x1, x2)
    
    if n == 0:
        s1 = - a[0][0] * df1_0 - a[0][1] * df2_0
        s2 = - a[1][0] * df1_0 - a[1][1] * df2_0
    else:
        dx1, dx2 = x1 - x1_p, x2 - x2_p
        dg1, dg2 = df1_0 - df1_p, df2_0 - df2_p

        num1 = np.outer([dx1, dx2], [dx1, dx2])
        den1 = dx1 * dg1 + dx2 * dg2
        m1 = num1 / den1

        Adg = np.matmul(a, [dg1, dg2])
        num2 = np.outer(Adg, Adg)
        den2 = np.dot([dg1, dg2], Adg)
        m2 = num2 / den2

        a = a + m1 - m2
        
        s = -np.matmul(a, [df1_0, df2_0])
        s1, s2 = s[0], s[1]

    l = (-(df1_0 * s1 + df2_0 * s2)) / (6 * s1**2 - 2 * s1 * s2 + 8 * s2**2)

    print(f"\nІтерація {n}")
    print(f"Напрямок s: [{s1:.3f}, {s2:.3f}]")
    print(f"Крок l: {l:.3f}\n")

    x1_p, x2_p = x1, x2
    df1_p, df2_p = df1_0, df2_0

    x1 += l * s1
    x2 += l * s2
    n += 1

    print(f"l_{n - 1} = {l:.3f}, x_{n} = [{x1:.3f}, {x2:.3f}] , ||f(x_{n})|| = {math.sqrt(df1(x1, x2) ** 2 + df2(x1, x2) ** 2):.3f}")


dx1, dx2 = x1 - x1_p, x2 - x2_p
dg1, dg2 = df1(x1, x2) - df1_p, df2(x1, x2) - df2_p
num1 = np.outer([dx1, dx2], [dx1, dx2])
m1 = num1 / (dx1 * dg1 + dx2 * dg2)
Adg = np.matmul(a, [dg1, dg2])
m2 = np.outer(Adg, Adg) / np.dot([dg1, dg2], Adg)
a = a + m1 - m2

print("\n-----Аналіз матриць-----")
print("Матриця A_2 (наближення DFP):")
print(a)

H_inv = np.linalg.inv(np.array([[6, -1], [-1, 8]]))
print("\nОбернена матриця Гессе H^-1 (аналітична):")
print(H_inv)