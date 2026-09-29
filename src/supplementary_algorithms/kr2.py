import math
import matplotlib.pyplot as plt

print("-----Завдання 1-----")

def f(x1, x2):
    return (x1 - 4) ** 2 + x2 ** 2 * 2

e = 0.4

def stop1(dx1, dx2):
    return math.sqrt(dx1 ** 2 + dx2 ** 2)

def stop2(x1, x2):
    print(round(math.sqrt((x1[0] - x2[0]) ** 2 + (x1[1] - x2[1]) ** 2) / math.sqrt(x2[0] ** 2 + x2[1] ** 2), 3))
    print(round(abs((f(x1[0], x1[1]) - f(x2[0], x2[1])) / abs(f(x2[0], x2[1]))), 3))
    

# Початкова точка
x1b = 8
x2b = 6

graphx = [x1b]
graphy = [x2b]

x1_old = x1b
x2_old = x2b

x1p = 0
x2p = 0

dx1 = 0.6
dx2 = 0.8

f_current = f(x1b, x2b)

n = 1

while True:
    if n == 4:
        print("\n---------")
        print(f"Критерій закінчення 1:\n {stop1(dx1, dx2)}")
        print(f"Критерій закінчення 2:")
        stop2((x1b, x2b), (x1_old, x2_old))
        break

    if n == 1:

        print("\n---------")
        print(f"n = {n}")
        print(f"БТ: [{x1b}, {x2b}] - x_{n - 1}")
        fb = round(f(x1b, x2b), 5)
        print(f"f = {fb}")

        if f(x1b + dx1, x2b) < f_current:
            x1b = round(x1b + dx1, 5)
            print(f"f({x1b},{x2b}) = {round(f(x1b, x2b), 5)} < {round(f_current, 5)}")
            f_current = round(f(x1b, x2b), 5)
        else:
            x1b = round(x1b - dx1, 5)
            print(f"f({x1b},{x2b}) = {round(f(x1b, x2b), 5)} < {round(f_current, 5)}")
            f_current = round(f(x1b, x2b), 5)
    
        if f(x1b, x2b + dx2) < f_current:
            x2b = round(x2b + dx2, 5)
            print(f"f({x1b},{x2b}) = {round(f(x1b, x2b), 5)} < {round(f_current, 5)}")
            f_current = round(f(x1b, x2b), 5)
        else:
            x2b = round(x2b - dx2, 5)
            print(f"f({x1b},{x2b}) = {round(f(x1b, x2b), 5)} < {round(f_current, 5)}")
            f_current = round(f(x1b, x2b), 5)

        print(f"ПБТ: [{x1b}, {x2b}] - x_{n}")

        x1p = 2 * x1b - x1_old
        x2p = 2 * x2b - x2_old
        f_current = f(x1p, x2p)

        n += 1

    else:

        print("\n---------")
        print(f"n = {n}")
        print(f"ПБТ: [{x1b}, {x2b}] - x_{n - 1}")
        m1 = x1b
        m2 = x2b
        fp = round(f(x1p, x2p), 5)
        print(f"f = {fp}")
        
        if f(x1p + dx1, x2p) < f_current:
            x1p = round(x1p + dx1, 5)
            print(f"f({x1p},{x2p}) = {round(f(x1p, x2p), 5)} < {round(f_current, 5)}")
            f_current = f(x1p, x2p)
        else:
            x1p = round(x1p - dx1, 5)
            print(f"f({x1p},{x2p}) = {round(f(x1p, x2p), 5)} < {round(f_current, 5)}")
            f_current = f(x1p, x2p)
    
        if f(x1p, x2p + dx2) < f_current:
            x2p = round(x2p + dx2, 5)
            print(f"f({x1p},{x2p}) = {round(f(x1p, x2p), 5)} < {round(f_current, 5)}")
            f_current = f(x1p, x2p)
        else:
            x2p = round(x2p - dx2, 5)
            print(f"f({x1p},{x2p}) = {round(f(x1p, x2p), 5)} < {round(f_current, 5)}")
            f_current = f(x1p, x2p)
        
        if f_current < f(m1, m2):
            print(f"f({x1p},{x2p}) = {round(f(x1p, x2p), 5)} < {round(f(m1, m2), 5)}")
            
            x1_old = m1
            x2_old = m2

            x1b = x1p
            x2b = x2p

            x1p = round(2 * x1b - x1_old, 5)
            x2p = round(2 * x2b - x2_old, 5)

            print(f"БТ: [{x1_old}, {x2_old}] - x_{n - 1}")
            print(f"ПБТ: [{x1b}, {x2b}] - x_{n}")
            

            f_current = f(x1p, x2p)

            n += 1

        else:
            print(f"f({x1p},{x2p}) = {round(f(x1p, x2p), 5)} > {round(f(m1, m2), 5)}")

            dx1 /= 2
            dx2 /= 2

            x1b = x1_old
            x2b = x2_old

            x1p = x1b
            x2p = x2b

            x1_old = m1
            x2_old = m2

            print(f"БТ: [{x1b}, {x2b}] - x_{n - 1}")
            print(f"ПБТ: [{x1p}, {x2p}] - x_{n}")

            f_current = f(x1p, x2p)
            n += 1
    graphx.append(x1b)
    graphy.append(x2b)


print("\nМінімум приблизно в точці:")
print(f"[{round(x1b,5)}, {round(x2b,5)}]")
print(f"f = {round(f(x1b,x2b),5)}")


plt.plot(graphx, graphy, marker="o", markersize=3, color="black", linestyle="-")
plt.grid(True)
plt.show()

print("\n-----Завдання 2-----")

def f(x1, x2):
    return 2 * (x1 - 3) ** 2 + (x2 - 4) ** 2

dub_count = 0

graph1 = []
graph2 = []
graph3 = []

x11 = 6
x12 = 5

x21 = 8
x22 = 7

x31 = 6
x32 = 7

x41 = 0
x42 = 0

xl1 = 0
xl2 = 0

xh1 = 0
xh2 = 0

xg1 = 0
xg2 = 0

a = 1
b = 0.5
y = 2
m = 3

counter = 0
memory = []

def count(counter):
    for i in memory[-(3 * m):]:
        for j in memory:
            if j == i:
                counter += 1
        if counter == m:
            counter = 0
            memory.clear()
            return i
        counter = 0
    return False

n = 1

while True:
    print("\n----------")
    print(f"n = {n}")
    print("----------\n")
    
    if n == 1:
        f1 = f(x11, x12)
        f2 = f(x21, x22)
        f3 = f(x31, x32)

        if f1 < f2 and f1 < f3:
            if f2 < f3:
                xl1 = x11
                xl2 = x12
                xh1 = x31
                xh2 = x32
                xg1 = x21
                xg2 = x22
            else:
                xl1 = x11
                xl2 = x12
                xh1 = x21
                xh2 = x22
                xg1 = x31
                xg2 = x32

        elif f2 < f1 and f2 < f3:
            if f1 < f3:
                xl1 = x21
                xl2 = x22
                xh1 = x31
                xh2 = x32
                xg1 = x11
                xg2 = x12
            else:
                xl1 = x21
                xl2 = x22
                xh1 = x11
                xh2 = x12
                xg1 = x31
                xg2 = x32
            
        elif f3 < f1 and f3 < f2:
            if f1 < f2:
                xl1 = x31
                xl2 = x32
                xh1 = x21
                xh2 = x22
                xg1 = x11
                xg2 = x12
            else:
                xl1 = x31
                xl2 = x32
                xh1 = x11
                xh2 = x12
                xg1 = x21
                xg2 = x22

        print(f"xl = [{xl1}, {xl2}]")
        print(f"xh = [{xh1}, {xh2}]")
        print(f"xg = [{xg1}, {xg2}]")

        graph1.append([xl1, xl2])
        graph2.append([xh1, xh2])
        graph3.append([xg1, xg2])

        x1_new = xh1 + (1 + a) * ((xl1 + xg1) / 2 - xh1)
        x2_new = xh2 + (1 + a) * ((xl2 + xg2) / 2 - xh2)

        f_new = f(x1_new, x2_new)

        print(f"x_new = [{x1_new}, {x2_new}]")
        print(f"f(xn) = {f_new}")

        if f_new < f(xl1, xl2):
            x41 = xh1 + (1 + y) * ((xl1 + xg1) / 2 - xh1)
            x42 = xh2 + (1 + y) * ((xl2 + xg2) / 2 - xh2)
            f41 = f(x41, x42)
            print(f"x41 = [{x41}, {x42}]")
            print(f"f(x41) = {f41}")

            fl = f(xl1, xl2)
            fh = f(xh1, xh2)
            fg = f(xg1, xg2)
            print(f"f(xl) = {fl}, f(xh) = {fh}, f(xg) = {fg}")
            
            points = [
                (fl, xl1, xl2),
                (fg, xg1, xg2),
                (fh, xh1, xh2),
                (f41, x41, x42)
            ]

            points.sort(key=lambda p: p[0])

            memory.append(points[0])
            memory.append(points[1])
            memory.append(points[2])

            fl, xl1, xl2 = points[0]
            fg, xg1, xg2 = points[1]
            fh, xh1, xh2 = points[2]
            
        n += 1

    else:
        print(f"xl = [{xl1}, {xl2}]")
        print(f"xh = [{xh1}, {xh2}]")
        print(f"xg = [{xg1}, {xg2}]")

        memory.append(points[0])
        memory.append(points[1])
        memory.append(points[2])

        graph1.append([xl1, xl2])
        graph2.append([xh1, xh2])
        graph3.append([xg1, xg2])

        ex = 0

        dup = count(counter)
        if dup:
            ex = 1
            print(f"Точка повторюється {m} разів: " + str(dup))
            dub_count += 1
            
            # 1. Рахуємо нові координати (середини сторін відносно найкращої points[0])
            x1a = (points[0][1] + points[1][1]) / 2
            x2a = (points[0][2] + points[1][2]) / 2

            x1b = (points[0][1] + points[2][1]) / 2
            x2b = (points[0][2] + points[2][2]) / 2

            print(f"Симплекс до редукції: {points}")

            # 2. ПОВНІСТЮ ОНОВЛЮЄМО СПИСОК (замість трьох pop та append)
            # Ми беремо стару найкращу точку і додаємо дві нові розраховані
            points = [
                points[0],               # Найкраща лишається на місці
                (f(x1a, x2a), x1a, x2a), # Нова точка "а"
                (f(x1b, x2b), x1b, x2b)  # Нова точка "b"
            ]

            # 3. Сортуємо, щоб fl, fg, fh знову стали на свої місця
            points.sort(key=lambda p: p[0])

            fl, xl1, xl2 = points[0]
            fg, xg1, xg2 = points[1]
            fh, xh1, xh2 = points[2]
            
            # Не забудь обнулити counter після редукції, щоб вона не йшла циклом
            counter = 0


        if ex != 1:

            x1_new = xh1 + (1 + a) * ((xl1 + xg1) / 2 - xh1)
            x2_new = xh2 + (1 + a) * ((xl2 + xg2) / 2 - xh2)

            f_new = f(x1_new, x2_new)

            print(f"x_new = [{x1_new}, {x2_new}]")
            print(f"f(xn) = {f_new}")

        if f_new < f(xl1, xl2) and ex != 1:
            print(f"xl = {fl} > x_new = {f_new}")
            
            x41 = xh1 + (1 + y) * ((xl1 + xg1) / 2 - xh1)
            x42 = xh2 + (1 + y) * ((xl2 + xg2) / 2 - xh2)
            f41 = f(x41, x42)

            fl = f(xl1, xl2)
            fh = f(xh1, xh2)
            fg = f(xg1, xg2)
            

            points = [
                (fl, xl1, xl2),
                (fg, xg1, xg2),
                (fh, xh1, xh2),
                (f41, x41, x42)
            ]

            points.sort(key=lambda p: p[0])

            fl, xl1, xl2 = points[0]
            fg, xg1, xg2 = points[1]
            fh, xh1, xh2 = points[2]

            print(f"f(xl) = {fl}, f(xh) = {fh}, f(xg) = {fg}")

        elif fl <= f_new < fh:
            print("Відображення: точка середня, але краща за найгіршу. Замінюємо.")
            points[2] = (f_new, x1_new, x2_new) # Замінюємо найгіршу на відображену
            points.sort(key=lambda p: p[0])

            # Оновлюємо робочі змінні
            fl, xl1, xl2 = points[0]
            fg, xg1, xg2 = points[1]
            fh, xh1, xh2 = points[2]

            # ОБОВ'ЯЗКОВО: скидаємо лічильник повторів, бо симплекс змінився!
            counter = 0
            

        elif f_new > f(xh1, xh2) and ex != 1:
            print(f"xh = {fh} < x_new = {f_new}")
            
            x41 = xh1 + (1 - b) * ((xl1 + xg1) / 2 - xh1)
            x42 = xh2 + (1 - b) * ((xl2 + xg2) / 2 - xh2)
            f41 = f(x41, x42)
            

            fl = f(xl1, xl2)
            fh = f(xh1, xh2)
            fg = f(xg1, xg2)


            points = [
                (fl, xl1, xl2),
                (fg, xg1, xg2),
                (fh, xh1, xh2),
                (f41, x41, x42)
            ]

            points.sort(key=lambda p: p[0])

            fl, xl1, xl2 = points[0]
            fg, xg1, xg2 = points[1]
            fh, xh1, xh2 = points[2]

            print(f"f(xl) = {fl}, f(xh) = {fh}, f(xg) = {fg}")


        n += 1

    if dub_count == 2:
        print("\n---------")
        print(f"xl = [{xl1}, {xl2}]")
        print(f"xh = [{xh1}, {xh2}]")
        print(f"xg = [{xg1}, {xg2}]")

        graph1.append((xl1, xl2))
        graph2.append((xh1, xh2))
        graph3.append((xg1, xg2))

        xc1 = (xl1 + xh1 + xg1) / 3
        xc2 = (xl2 + xh2 + xg2) / 3
        fc = f(xc1, xc2)

        end = (((fl - fc) ** 2 + (fh - fc) ** 2 + (fg - fc) ** 2) / 3) ** 0.5
        
        print("\n---------")
        print(f"Критерій закінчення = {round(end, 3)}")
        print("---------")

        print(graph1)
        print(graph2)
        print(graph3)
        break

for i in range(len(graph1)):
    # 1. Collect the 3 vertices for the current triangle
    p1 = graph1[i]
    p2 = graph2[i]
    p3 = graph3[i]
    
    # 2. Extract X and Y coordinates
    # We add p1 at the end to close the triangle: [p1, p2, p3, p1]
    x = [p1[0], p2[0], p3[0], p1[0]]
    y = [p1[1], p2[1], p3[1], p1[1]]
    
    # 3. Plot the triangle
    plt.plot(x, y, label=f'Triangle {i}', color='black', marker='o')

plt.grid(True)
plt.show()