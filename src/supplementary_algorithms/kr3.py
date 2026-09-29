import math
import matplotlib.pyplot as plt

print("-----Завдання 1-----")

def f(x1, x2):
    return 3 * (x1 - 10) ** 2 - x1 * x2 + 4 * x2 ** 2

def df1(x1, x2):
    return 6 * (x1 - 10) - x2

def df2(x1, x2):
    return - x1 + 8 * x2

l = 1
x1 = -16
x2 = -16
x1plot = [x1]
x2plot = [x2]
f0 = f(x1, x2)
n = 0

while True:
    df1_0 = df1(x1, x2)
    df2_0 = df2(x1, x2)
    ddf = math.sqrt(df1_0 ** 2 + df2_0 ** 2)
    s1 = - df1_0 / ddf
    s2 = - df2_0 / ddf

    if f(x1 + l * s1, x2 + l * s2) < f0:
        x1 += l * s1
        x2 += l * s2
        f0 = f(x1, x2)
        x1plot.append(x1)
        x2plot.append(x2)
        n += 1
        print(f"x_{n} = [{x1:.4f}, {x2:.4f}] , ||f(x_{n})|| = {math.sqrt(df1(x1, x2) ** 2 + df2(x1, x2) ** 2):.4f}")
    else:
        l /= 2

    if n == 3:
        break
        


plt.plot(x1plot, x2plot, color='black', marker='o')
plt.vlines(0, -17,3, color='black', linewidth=2)
plt.hlines(0,-17,3, color='black', linewidth=2)
plt.grid(True, linestyle='--', color='gray', linewidth=0.5)
plt.show()


print("\n-----Завдання 2-----")

def f(x1, x2):
    return 3 * (x1 - 10) ** 2 - x1 * x2 + 4 * x2 ** 2

def df1(x1, x2):
    return 6 * (x1 - 10) - x2

def df2(x1, x2):
    return - x1 + 8 * x2

x1 = -16
x2 = -16
x1plot = [x1]
x2plot = [x2]
f0 = f(x1, x2)
n = 0
l = 0


while True:
    df1_0 = df1(x1, x2)
    df2_0 = df2(x1, x2)
    s1 = - df1_0
    s2 = - df2_0

    l = (-(df1_0 * s1 + df2_0 * s2)) / (6*s1**2 - 2*s1*s2 + 8*s2**2)

    x1 += l * s1
    x2 += l * s2
    x1plot.append(x1)
    x2plot.append(x2)
    f0 = f(x1, x2)
    n += 1

    print(f"x_{n} = [{x1:.4f}, {x2:.4f}] , ||f(x_{n})|| = {math.sqrt(df1(x1, x2) ** 2 + df2(x1, x2) ** 2):.4f}")

    if n == 3:
        break


plt.plot(x1plot, x2plot, color='black', marker='o')
plt.vlines(0, min(x2plot) - 0.2 * max(x2plot), max(x2plot) + 0.2 * max(x2plot), color='black', linewidth=2)
plt.hlines(0, min(x1plot) - 0.2 * max(x1plot), max(x1plot) + 0.2 * max(x1plot), color='black', linewidth=2)
plt.grid(True, linestyle='--', color='gray', linewidth=0.5)
plt.show()

print("\n-----Завдання 3-----")

def f(x1, x2):
    return 3 * (x1 - 10) ** 2 - x1 * x2 + 4 * x2 ** 2

def df1(x1, x2):
    return 6 * (x1 - 10) - x2

def df2(x1, x2):
    return - x1 + 8 * x2

x1 = -16
x2 = -16
x1plot = [x1]
x2plot = [x2]
f0 = f(x1, x2)
n = 0
l = 0

while True:
    df1_0 = df1(x1, x2)
    df2_0 = df2(x1, x2)

    if n > 1 and (n + 1) % 3 == 0:
        pr1 = x1plot[n - 2]
        pr2 = x2plot[n - 2]
        s1 = x1 - pr1
        s2 = x2 - pr2
    else:
        s1 = - df1_0
        s2 = - df2_0

    l = (-(df1_0 * s1 + df2_0 * s2)) / (6*s1**2 - 2*s1*s2 + 8*s2**2)

    x1 += l * s1
    x2 += l * s2
    x1plot.append(x1)
    x2plot.append(x2)
    f0 = f(x1, x2)
    n += 1

    print(f"x_{n} = [{x1:.4f}, {x2:.4f}] , ||f(x_{n})|| = {math.sqrt(df1(x1, x2) ** 2 + df2(x1, x2) ** 2):.4f}")

    if n == 3:
        break


plt.plot(x1plot, x2plot, color='black', marker='o')
plt.vlines(0, min(x2plot) - 0.2 * max(x2plot), max(x2plot) + 0.2 * max(x2plot), color='black', linewidth=2)
plt.hlines(0, min(x1plot) - 0.2 * max(x1plot), max(x1plot) + 0.2 * max(x1plot), color='black', linewidth=2)
x1plot.pop(1)
x2plot.pop(1)
plt.plot(x1plot, x2plot, color='black', linestyle='--', linewidth=0.5)
plt.grid(True, linestyle='--', color='gray', linewidth=0.5)
plt.show()

print("\n-----Завдання 4-----")


def df1(x1, x2, h11, h12):
    return h11 * (x1 - 10) + h12 * x2

def df2(x1, x2, h21, h22):
    return h21 * x1 + h22 * x2


x1, x2 = -16, -16
h = [[6, -1], [-1, 8]]

n = 0

while True:
    df1_0 = df1(x1, x2, h[0][0], h[0][1])
    df2_0 = df2(x1, x2, h[1][0], h[1][1])
    
    det = h[0][0] * h[1][1] - h[0][1] * h[1][0]
    
    h_inv = [
        [h[1][1] / det, -h[0][1] / det],
        [-h[1][0] / det, h[0][0] / det]
    ]
    
    x1 = x1 - (h_inv[0][0] * df1_0 + h_inv[0][1] * df2_0)
    x2 = x2 - (h_inv[1][0] * df1_0 + h_inv[1][1] * df2_0)
    
    n += 1
    print(f"x_{n} = [{x1:.4f}, {x2:.4f}] , ||f(x_{n})|| = {math.sqrt(df1(x1, x2, h[0][0], h[0][1]) ** 2 + df2(x1, x2, h[1][0], h[1][1]) ** 2):.4f}")
    
    if n == 1:
        break