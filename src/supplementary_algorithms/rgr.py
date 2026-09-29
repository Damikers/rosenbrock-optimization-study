# import numpy as np
# import matplotlib.pyplot as plt

# n = 10
# epsilon = 0.01

# def f_2d(x):
#     return 3 * (x[0] - 10)**2 - x[0] * x[1] + 4 * (x[1]**2)

# x0 = np.array([-1.2 * n - 4, -1.2 * n - 4])
# s1 = np.array([1, 0])
# s2 = np.array([0, 1])


# def get_f_1d(x_start, direction):
#     """Reduces 2D function to 1D along a given direction from x_start."""
#     def f_1d(lam):
#         point_2d = x_start + lam * direction
#         return f_2d(point_2d)
#     return f_1d

# lam0 = 0
# def sven_algorithm(f_1d, x_vec, s_vec):
#     d = 0.1 * (np.linalg.norm(x_vec) / np.linalg.norm(s_vec))

#     y0 = f_1d(lam0)

#     x_left = lam0 - d
#     x_right = lam0 + d
#     y_left = f_1d(x_left)
#     y_right = f_1d(x_right)

#     if y_left >= y0 and y_right >= y0:
#         return [x_left, x_right]
#     elif y_left < y0:
#         sign = -1
#         points = [lam0, x_left]
#         funcs = [y0, y_left]
#     else:
#         sign = 1
#         points = [lam0, x_right]
#         funcs = [y0, y_right]

#     count = 1
#     while True:
#         step = d * 2 ** count
#         x_new = points[-1] + sign * step
#         y_new = f_1d(x_new)

#         if y_new < funcs[-1]:
#             points.append(x_new)
#             funcs.append(y_new)
#             count += 1
#         else:
#             x_mid = (points[-1] + x_new) / 2
#             points.append(x_mid)
#             funcs.append(f_1d(x_mid))
            
            
#             break

#     a, b = sorted([points[-3], points[-1]])
#     print(points)
#     print(funcs)
#     return [a, b]

# def golden_ratio(f_1d, interval, eps):
#     a, b = interval[0], interval[1]

#     x1 = a + 0.382 * (b - a)
#     x2 = a + 0.618 * (b - a)
#     y1 = f_1d(x1)
#     y2 = f_1d(x2)

#     while b - a > eps:
#         if y1 < y2:
#             b = x2
#             x2 = x1
#             y2 = y1
#             x1 = a + 0.382 * (b - a)
#             y1 = f_1d(x1)
#         else:
#             a = x1
#             x1 = x2
#             y1 = y2
#             x2 = a + 0.618 * (b - a)
#             y2 = f_1d(x2)

#     print(a, b)
#     return (a + b) / 2

# def dsk_powell(f_1d, interval, eps):
#     x_mid = (interval[0] + interval[1]) / 2
#     interval_p = [interval[0], x_mid, interval[1]]
#     funcs = [f_1d(p) for p in interval_p]

#     while True:
#         a1 = (funcs[1] - funcs[0]) / (interval_p[1] - interval_p[0])
#         a2 = (1 / (interval_p[2] - interval_p[1])) * (
#             (funcs[2] - funcs[0]) / (interval_p[2] - interval_p[0])
#             - (funcs[1] - funcs[0]) / (interval_p[1] - interval_p[0])
#         )

#         if a2 == 0:
#             return interval_p[1]

#         x_star = (interval_p[0] + interval_p[1]) / 2 - a1 / (2 * a2)
#         y_star = f_1d(x_star)

#         if abs(interval_p[1] - x_star) <= eps and abs(funcs[1] - y_star) <= eps:
#             return x_star

#         inserted = False
#         for i in range(len(interval_p) - 1):
#             if interval_p[i] <= x_star <= interval_p[i + 1]:
#                 interval_p.insert(i + 1, x_star)
#                 funcs.insert(i + 1, y_star)
#                 inserted = True
#                 print(interval_p, funcs)
#                 break

#         if not inserted:
#             if x_star < interval_p[0]:
#                 interval_p.insert(0, x_star)
#                 funcs.insert(0, y_star)
#             else:
#                 interval_p.append(x_star)
#                 funcs.append(y_star)

#         y_min = min(funcs)
#         min_index = funcs.index(y_min)

#         if min_index == 0:
#             interval_p.pop(-1)
#             funcs.pop(-1)
#         elif min_index == len(funcs) - 1:
#             interval_p.pop(0)
#             funcs.pop(0)
#         else:
#             left_dist = abs(interval_p[min_index] - interval_p[0])
#             right_dist = abs(interval_p[-1] - interval_p[min_index])
#             if left_dist > right_dist:
#                 interval_p.pop(0)
#                 funcs.pop(0)
#             else:
#                 interval_p.pop(-1)
#                 funcs.pop(-1)

# history = [x0]

# f_1d = get_f_1d(history[-1], s2)
# interval = sven_algorithm(f_1d, history[-1], s2)
# lam_star = golden_ratio(f_1d, interval, epsilon)
# x1 = history[-1] + lam_star * s2
# history.append(x1)
# print(f"Iter 1: x1 = {x1}, lam = {lam_star:.4f}")

# f_1d = get_f_1d(history[-1], s1)
# interval = sven_algorithm(f_1d, history[-1], s1)
# lam_star = golden_ratio(f_1d, interval, epsilon)
# x2 = history[-1] + lam_star * s1
# history.append(x2)
# print(f"Iter 2: x2 = {x2}, lam = {lam_star:.4f}")

# f_1d = get_f_1d(history[-1], s2)
# interval = sven_algorithm(f_1d, history[-1], s2)
# lam_star = dsk_powell(f_1d, interval, epsilon)
# x3 = history[-1] + lam_star * s2
# history.append(x3)
# print(f"Iter 3: x3 = {x3}, lam = {lam_star:.4f}")

# s_accel = history[3] - history[1]
# f_1d = get_f_1d(history[-1], s_accel)
# interval = sven_algorithm(f_1d, history[-1], s_accel)
# lam_star = dsk_powell(f_1d, interval, epsilon)
# x4 = history[-1] + lam_star * s_accel
# history.append(x4)
# print(f"Iter 4: x4 = {x4}, lam = {lam_star:.4f}")

# print("\nFinal Result:", x4)
# print(f"f(x4) = {f_2d(x4):.6f}")

# x_coords = [point[0] for point in history]
# y_coords = [point[1] for point in history]

# plt.plot(x_coords, y_coords, color='black', marker='o')
# plt.vlines(0, min(y_coords) - 0.2 * max(y_coords), max(y_coords) + 0.2 * max(y_coords), color='black', linewidth=1)
# plt.hlines(0, min(x_coords) - 0.2 * max(x_coords), max(x_coords) + 0.2 * max(x_coords), color='black', linewidth=1)
# plt.grid(True, linestyle='--', color='gray', linewidth=0.5)
# plt.show()

import numpy as np

# 1. Визначення констант та функцій
n = 10
e = 0.01  # Точність (epsilon) [cite: 8, 53]

def f_2d(x):
    # Цільова функція f(x) [cite: 2, 55]
    return 3 * (x[0] - 10)**2 - x[0] * x[1] + 4 * (x[1]**2)

# Дані для 4-ї ітерації (згідно з вашим PDF)
x1_2d = np.array([-16, -1.999])  # Результат 1-ї ітерації [cite: 13]
x3_2d = np.array([9.668, 1.2085]) # Результат 3-ї ітерації [cite: 27]
s_accel = x3_2d - x1_2d          # Напрямок (x3 - x1) [cite: 30]

def f_1d_iter4(lam):
    """
    Одномірна функція f(lam) вздовж напрямку прискорення.
    lam — це крок пошуку (аналог x у вашому прикладі).
    """
    point_2d = x3_2d + lam * s_accel
    return f_2d(point_2d)

# 2. Параметри для методу ДСК-Пауелла (отримані після Свена)
# Для 4-ї ітерації інтервал після Свена [0, 0.0753] [cite: 31]
interval = [0, 0.0753]
middle = (interval[0] + interval[1]) / 2
interval_p = [interval[0], middle, interval[1]]

# Початкові значення функції в точках
funcs = [f_1d_iter4(p) for p in interval_p]

print(f"--- Початок ДСК-Пауелла для 4-ї ітерації ---")
print(f"Напрямок s_accel: {s_accel}")

# 3. Основний цикл алгоритму
iteration = 1
while True:
    # Розрахунок коефіцієнтів параболічної апроксимації
    # a1 = (f2 - f1) / (x2 - x1)
    a1 = (funcs[1] - funcs[0]) / (interval_p[1] - interval_p[0])
    
    # a2 = [ (f3 - f1)/(x3 - x1) - (f2 - f1)/(x2 - x1) ] / (x3 - x2)
    a2 = (1 / (interval_p[2] - interval_p[1])) * (
        (funcs[2] - funcs[0]) / (interval_p[2] - interval_p[0]) - a1
    )

    if a2 == 0:
        x_star = interval_p[1]
        print("Попередження: a2 = 0, парабола виродилася.")
    else:
        # Вершина параболи (точка x*)
        x_star = (interval_p[0] + interval_p[1]) / 2 - a1 / (2 * a2)
    
    y_star = f_1d_iter4(x_star)

    # Вивід поточного стану (як у вашому прикладі з round)
    print(f"\nІтерація Пауелла #{iteration}")
    print(f"Поточні кроки lambda: {[round(p, 5) for p in interval_p]}")
    print(f"Новий крок lambda*: {round(x_star, 5)}, f(lambda*): {round(y_star, 5)}")
    
    # Перевірка критеріїв зупинки 
    i_diff = abs(interval_p[1] - x_star)
    f_diff = abs(funcs[1] - y_star)
    
    print(f"|x2 - x*| <= {e}: {i_diff <= e} (різниця: {round(i_diff, 6)})")
    print(f"|f2 - f*| <= {e}: {f_diff <= e} (різниця: {round(f_diff, 6)})")
    
    if i_diff <= e and f_diff <= e:
        print(f"\nКритерій виконано! Фінальний lambda = {round(x_star, 5)}")
        final_x2d = x3_2d + x_star * s_accel
        print(f"Фінальна точка x4: {final_x2d}")
        break

    # Оновлення точок (вставка x_star у список)
    inserted = False
    for i in range(len(interval_p) - 1):
        if interval_p[i] <= x_star <= interval_p[i + 1]:
            interval_p.insert(i + 1, x_star)
            funcs.insert(i + 1, y_star)
            inserted = True
            break
    
    if not inserted:
        if x_star < interval_p[0]:
            interval_p.insert(0, x_star)
            funcs.insert(0, y_star)
        else:
            interval_p.append(x_star)
            funcs.append(y_star)

    # Вибір трійки точок для наступного кроку (скорочення інтервалу)
    y_min = min(funcs)
    min_index = funcs.index(y_min)

    # Логіка видалення точок, щоб залишити x_min та сусідів [cite: 163-180]
    if min_index == 0:
        interval_p = interval_p[:3]
        funcs = funcs[:3]
    elif min_index == len(funcs) - 1:
        interval_p = interval_p[-3:]
        funcs = funcs[-3:]
    else:
        # Залишаємо мінімум та дві точки по боках
        # Якщо точок більше 3, видаляємо ту, що далі від мінімуму
        while len(interval_p) > 3:
            left_dist = abs(interval_p[min_index] - interval_p[0])
            right_dist = abs(interval_p[-1] - interval_p[min_index])
            if left_dist > right_dist:
                interval_p.pop(0)
                funcs.pop(0)
                min_index -= 1
            else:
                interval_p.pop(-1)
                funcs.pop(-1)
    
    iteration += 1
    if iteration > 10: # Захист від вічного циклу
        break