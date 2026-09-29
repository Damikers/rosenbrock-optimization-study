import matplotlib.pyplot as plt
import numpy as np

print("-----Завдання 1-----")

x_0 = 30
d = 5

def f(x):
    return (100 - x) ** 2

y_0 = f(x_0)

print(f"x_0 = {x_0}, f(x_0) = {y_0}")

points = [x_0]
funcs = [y_0]

count = 0
sign = 0

while True:

    if count == 0:

        x_left = round(x_0 - d, 3)
        x_right = round(x_0 + d, 3)

        y_left = round(f(x_left), 3)
        y_right = round(f(x_right), 3)

        print(f"x_л = {x_left}, f(x_л) = {y_left}")
        print(f"x_п = {x_right}, f(x_п) = {y_right}")

        # Check direction of decrease
        if y_left >= y_0 and y_right >= y_0:
            break

        elif y_left < y_0:
            sign = -1
            points.append(x_left)
            funcs.append(y_left)

        else:
            sign = 1
            points.append(x_right)
            funcs.append(y_right)

        count += 1

    else:

        x_prev = points[-1]
        y_prev = funcs[-1]

        step = d * 2 ** count
        x_new = round(x_prev + sign * step, 3)
        y_new = round(f(x_new), 3)

        print(f"x_{count+1} = {x_new}, f(x_{count+1}) = {y_new}")

        # Continue moving if decreasing
        if y_new < y_prev:
            points.append(x_new)
            funcs.append(y_new)
            count += 1

        # Otherwise bracket found
        else:
            x_mid = round((x_prev + x_new) / 2, 3)
            y_mid = round(f(x_mid), 3)

            print(f"x_сер = {x_mid}, f(x_сер) = {y_mid}")
            points.append(x_mid)
            funcs.append(y_mid)
            points.append(x_new)
            funcs.append(y_new)

            break

interval = []

for i in range(len(points) - 1):
    if funcs[i - 1] > funcs[i] and funcs[i] < funcs[i + 1]:
        if points[i - 1] > points[i + 1]:
            print(f"Відповідь: [{points[i + 1]}, {points[i - 1]}]")
            interval.append(points[i + 1])
            interval.append(points[i - 1])
        else:
            print(f"Відповідь: [{points[i - 1]}, {points[i + 1]}]")
            interval.append(points[i - 1])
            interval.append(points[i + 1])

#-----Завдання 2a-----
print("\n-----Завдання 2.1-----")
e = 0.2

interval_d = interval.copy()
print(interval_d)

while True:
    x_m = (interval_d[0] + interval_d[1]) / 2
    y_m = f(x_m)

    x_1 = (interval_d[0] + x_m) / 2
    y_1 = f(x_1)

    x_2 = (x_m + interval_d[1]) / 2
    y_2 = f(x_2)

    y_a = f(interval_d[0])
    y_b = f(interval_d[1])

    if interval_d[1] - interval_d[0] <= e:
        break
    else:
        print(f"y_сер = {round(y_m, 4)}, y_1 = {round(y_1, 4)}, y_2 = {round(y_2, 4)}, y_a = {round(y_a, 4)}, y_b = {round(y_b, 4)}")
        if round(y_1, 4) >= round(y_m, 4) and round(y_2, 4) >= round(y_m, 4):
            interval_d[0] = x_1
            interval_d[1] = x_2
        elif round(y_a, 4) >= round(y_1, 4) and round(y_1, 4) <= round(y_m, 4):
            interval_d[1] = x_m
        elif y_m >= y_2 and y_2 <= y_b:
            interval_d[0] = x_m
    print(f"[{interval_d[0]}, {interval_d[1]}]")

print(f"Відповідь: [{interval_d[0]}, {interval_d[1]}]")


# #-----Завдання 2b-----
print("\n-----Завдання 2.2-----")
e = 0.2

interval_c = interval.copy()
x_1 = interval_c[0] + 0.382 * (interval_c[1] - interval_c[0])
x_2 = interval_c[0] + 0.618 * (interval_c[1] - interval_c[0])
y_1 = f(x_1)
y_2 = f(x_2)

print(interval_c)

while True:
    y_a = f(interval_c[0])
    y_b = f(interval_c[1])
    print(f"y_a = {round(y_a, 4)}, y_1 = {round(y_1, 4)}, y_2 = {round(y_2, 4)}, y_b = {round(y_b, 4)}")
    if interval_c[1] - interval_c[0] <= e:
        break
    else:
        if y_1 < y_2:
            interval_c[1] = x_2
            x_2 = x_1
            y_2 = y_1
            x_1 = interval_c[0] + 0.382 * (interval_c[1] - interval_c[0])
            y_1 = f(x_1)
        else:
            interval_c[0] = x_1
            x_1 = x_2
            y_1 = y_2
            x_2 = interval_c[0] + 0.618 * (interval_c[1] - interval_c[0])
            y_2 = f(x_2)
    print(f"[{interval_c[0]:.4f}, {interval_c[1]:.4f}]")

print(f"Відповідь: [{interval_c[0]:.4f}, {interval_c[1]:.4f}]")

# #-----Завдання 2c-----
print("\n-----Завдання 2.3-----")
e = 10 ** (-2)

def f(x):
    return 3 * (9.668) ** 2 - 9.668 * (x - 2) + 4 * (x - 2) ** 2

interval = [0.987252221906238, 4.9362611095311895]
middle = round((interval[0] + interval[1]) / 2, 4)
interval_p = [round(interval[0], 4), middle, round(interval[1], 4)]


funcs = [round(f(interval_p[0]), 4), round(f(interval_p[1]), 4), round(f(interval_p[2]), 4)]

while True:

    a_1 = (funcs[1] - funcs[0]) / (interval_p[1] - interval_p[0])
    a_2 = 1 / (interval_p[2] - interval_p[1]) * (
        (funcs[2] - funcs[0]) / (interval_p[2] - interval_p[0])
        - (funcs[1] - funcs[0]) / (interval_p[1] - interval_p[0])
    )

    x = round((interval_p[0] + interval_p[1]) / 2 - a_1 / (2 * a_2), 4)
    y = round(f(x), 4)

    print("\nПоточні x:", interval_p)
    print("Поточні f(x):", funcs)
    print("Новий x:", x, "f(x):", y)
    
    interval_p[1] = round(interval_p[1], 4)
    funcs[1] = round(funcs[1], 4)
    i_diff = round(interval_p[1] - x, 4)
    f_diff = round(funcs[1] - y, 4)
    
    print(f"\n|{interval_p[1]} - {x}| <= {e}: {abs(i_diff) <= e}")
    print(f"|{funcs[1]} - {y}| <= {e}: {abs(f_diff) <= e}")
    if abs(interval_p[1] - x) <= e and abs(funcs[1] - y) <= e:
        print("x =", x)
        break

    inserted = False
    for i in range(0, 2):
        if interval_p[i] <= x <= interval_p[i + 1]:
            interval_p.insert(i + 1, x)
            funcs.insert(i + 1, y)
            inserted = True
            break

    if not inserted:
        if x < interval_p[0]:
            interval_p.insert(0, x)
            funcs.insert(0, y)
        else:
            interval_p.append(x)
            funcs.append(y)

    print("Після вставки x:", interval_p)
    print("Після вставки f(x):", funcs)

    y_min = min(funcs)
    min_index = funcs.index(y_min)

    if min_index == 0:
        interval_p.pop(-1)
        funcs.pop(-1)

    elif min_index == len(funcs) - 1:
        interval_p.pop(0)
        funcs.pop(0)

    else:
        left_dist = abs(interval_p[min_index] - interval_p[0])
        right_dist = abs(interval_p[-1] - interval_p[min_index])

        if left_dist > right_dist:
            interval_p.pop(0)
            funcs.pop(0)
        else:
            interval_p.pop(-1)
            funcs.pop(-1)

    print("Після видалення x:", interval_p)
    print("Після видалення f(x):",funcs)

print(f"x_1 = {interval[0]}, x_2 = {middle}, x_3 = {interval[1]}, x* = {x}")

# #-----Завдання 3a-----
print("\n-----Завдання 3.1-----")
store = []
def f(x):
    return x ** 2 + 9 / x

def f1(x):
    return 2 * x - 9 / x ** 2

def f2(x):
    return 2 + 18 / x ** 3

n = 3
x_0 = 0.1

for i in range(0, n):
    f_0 = f(x_0)
    f1_0 = f1(x_0)
    f2_0 = f2(x_0)
    print(f"i = {i + 1} | x_{i} = {x_0:^5.3} | f'(x) = {f1(x_0):^9.6} | f''(x) = {f2(x_0):^9.6} | x_{i + 1} = {x_0 - f1_0 / f2_0:.3}")
    x_0 = x_0 - f1_0 / f2_0
    store.append(x_0)

print("\nВідповідь:")
for i in range(0, len(store)):
    print(f"x_{i + 1} = {store[i]:.3} ,  f'(x) = {f1(store[i]):.3f}")

# #-----Завдання 3b-----
print("\n-----Завдання 3.2-----")
n = 3

interval = [0.1, 2]
x_mid = []

for i in range(0, n):
    f_0 = f(interval[0])
    f1_0 = f1(interval[0])
    x = (interval[0] + interval[1]) / 2
    x_mid.append(x)
    f1_x = f1(x)
    int_text = []

    if f1_x > 0:
        int_text.append(x)
        int_text.append(interval[1])
    else:
        int_text.append(interval[0])
        int_text.append(x)

    print(f"i = {i + 1} | x1 = {interval[0]:^5.3f} | x2 = {interval[1]:^5.3f} | f'(x1) = {f1(interval[0]):^9.3f} | f'(x2) = {f1(interval[1]):^9.3f} | x* = {x:^5.3f} | f'(x*) = {f1_x:^9.3f} | Виключається: {int_text}")
    
    int_text = []

    if f1_x < 0:
        interval[0] = x
    else:
        interval[1] = x
print("\nВідповідь:")
for i in range(0, len(x_mid)):
    print(f"x_{i + 1} = {x_mid[i]:.3f} ,  f'(x) = {f1(x_mid[i]):.3f}")

# #-----Завдання 3c-----
print("\n-----Завдання 3.3-----")
n = 3

interval = [0.1, 2]
x_mid = []


for i in range(0, n):
    f1_1 = f1(interval[0])
    f1_2 = f1(interval[1])
    x = round(interval[1] - (f1_2 * (interval[1] - interval[0])) / (f1_2 - f1_1), 3)
    x_mid.append(x)
    int_text = []
    
    f1_x = round(f1(x), 3)
    if f1_x > 0:
        int_text.append(x)
        int_text.append(round(interval[1], 3))
    else:
        int_text.append(round(interval[0], 3))
        int_text.append(x)
        
    print(f"i = {i + 1} | x1 = {interval[0]:^5.3f} | x2 = {interval[1]:^5.3f} | f'(x1) = {f1(interval[0]):^7.3f} | f'(x2) = {f1(interval[1]):^7.3f} | x* = {x:^5.3f} | f'(x*) = {f1_x:^7.3f} | Виключається: {int_text}")

    int_text = []
    if f1_x < 0:
        interval[0] = x
    else:
        interval[1] = x

print("\nВідповідь:")
for i in range(0, len(x_mid)):
    print(f"x_{i + 1} = {x_mid[i]:.3f} ,  f'(x) = {f1(x_mid[i]):.3f}")