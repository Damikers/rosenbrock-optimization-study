import numpy as np
import matplotlib.pyplot as plt


OBJECTIVE_EVALS = 0


def fmt_float(value, digits=7):
    return f"{float(value):.{digits}f}"


def rosenbrock_function(x):
    global OBJECTIVE_EVALS
    OBJECTIVE_EVALS += 1
    x1, x2 = np.array(x, dtype=float)
    return 100 * (x1 ** 2 - x2) ** 2 + (x1 - 1) ** 2


def circular_constraint(radius, center=(0.0, 0.0)):
    def g(x):
        return (x[0] - center[0]) ** 2 + (x[1] - center[1]) ** 2 - radius ** 2

    g.kind = "circle"
    g.radius = radius
    g.center = np.array(center, dtype=float)
    return g


def linear_constraint(a1, a2, b):
    def g(x):
        return a1 * x[0] + a2 * x[1] - b

    g.kind = "line"
    g.a1 = a1
    g.a2 = a2
    g.b = b
    return g


def nonconvex_constraint():
    def g(x):
        outer_circle = x[0] ** 2 + x[1] ** 2 - 4.0
        inner_hole = 0.10 - ((x[0] - 1.0) ** 2 + (x[1] - 1.0) ** 2)
        return max(outer_circle, inner_hole)

    g.kind = "nonconvex"
    return g


def is_feasible(x, constraints, tol=1e-12):
    point = np.array(x, dtype=float)
    return all(g(point) <= tol for g in constraints)


def project_to_feasible(x, constraints):
    x = np.array(x, dtype=float)
    for g in constraints:
        if getattr(g, "kind", "") == "circle":
            diff = x - g.center
            norm_diff = np.linalg.norm(diff)
            if norm_diff > g.radius:
                x = g.center + diff * (g.radius / max(norm_diff, 1e-12))
        elif getattr(g, "kind", "") == "line":
            normal = np.array([g.a1, g.a2], dtype=float)
            value = np.dot(normal, x) - g.b
            if value > 0:
                x = x - (value / max(np.dot(normal, normal), 1e-12)) * normal
        elif getattr(g, "kind", "") == "nonconvex":
            norm_x = np.linalg.norm(x)
            if norm_x > 2.0:
                x = x * (2.0 / max(norm_x, 1e-12))
            center = np.array([1.0, 1.0], dtype=float)
            hole_radius = np.sqrt(0.10)
            diff = x - center
            diff_norm = np.linalg.norm(diff)
            if diff_norm < hole_radius:
                if diff_norm < 1e-12:
                    diff = np.array([1.0, 0.0], dtype=float)
                    diff_norm = 1.0
                x = center + diff * (hole_radius / diff_norm)
    return x


def update_basis(step1, step2, s1, s2):
    a1 = np.array(step1, dtype=float) + np.array(step2, dtype=float)
    a2 = np.array(step2, dtype=float)
    a1_norm = np.linalg.norm(a1)
    if a1_norm < 1e-12:
        return np.array(s1, dtype=float), np.array(s2, dtype=float)

    new_s1 = a1 / a1_norm
    b2 = a2 - np.dot(a2, new_s1) * new_s1
    b2_norm = np.linalg.norm(b2)
    if b2_norm < 1e-12:
        new_s2 = np.array([-new_s1[1], new_s1[0]], dtype=float)
    else:
        new_s2 = b2 / b2_norm
    return new_s1, new_s2


def one_dimensional_function(func, x, direction):
    x = np.array(x, dtype=float)
    direction = np.array(direction, dtype=float)
    return lambda lam: func(x + lam * direction)


def sven_search(phi, x0=0.0, d=0.1, max_iter=60):
    y0 = phi(x0)
    x_left = x0 - d
    x_right = x0 + d
    y_left = phi(x_left)
    y_right = phi(x_right)

    if y_left >= y0 and y_right >= y0:
        return min(x_left, x_right), max(x_left, x_right)

    if y_left < y0:
        sign = -1.0
        points = [x0, x_left]
        values = [y0, y_left]
    else:
        sign = 1.0
        points = [x0, x_right]
        values = [y0, y_right]

    count = 1
    while count <= max_iter:
        step = d * 2 ** count
        x_new = points[-1] + sign * step
        y_new = phi(x_new)
        if y_new < values[-1]:
            points.append(x_new)
            values.append(y_new)
            count += 1
            continue

        x_prev = points[-1]
        x_mid = (x_prev + x_new) / 2.0
        return min(points[-2], x_new, x_mid), max(points[-2], x_new, x_mid)

    return min(points), max(points)


def golden_section(phi, a, b, eps=1e-6, max_iter=200):
    x1 = a + 0.382 * (b - a)
    x2 = a + 0.618 * (b - a)
    y1 = phi(x1)
    y2 = phi(x2)

    while (b - a) > eps and max_iter > 0:
        if y1 < y2:
            b = x2
            x2 = x1
            y2 = y1
            x1 = a + 0.382 * (b - a)
            y1 = phi(x1)
        else:
            a = x1
            x1 = x2
            y1 = y2
            x2 = a + 0.618 * (b - a)
            y2 = phi(x2)
        max_iter -= 1

    return (a + b) / 2.0


def dsk_powell(phi, a, b, eps=1e-6, max_iter=100):
    triple = [a, (a + b) / 2.0, b]
    values = [phi(triple[0]), phi(triple[1]), phi(triple[2])]

    for _ in range(max_iter):
        x1, x2, x3 = triple
        f1, f2, f3 = values

        denom_12 = x2 - x1
        denom_13 = x3 - x1
        denom_23 = x3 - x2
        if abs(denom_12) < 1e-12 or abs(denom_13) < 1e-12 or abs(denom_23) < 1e-12:
            return x2

        a1 = (f2 - f1) / denom_12
        a2 = ((f3 - f1) / denom_13 - (f2 - f1) / denom_12) / denom_23

        if abs(a2) < 1e-12:
            xs = (x1 + x3) / 2.0
        else:
            xs = (x1 + x2) / 2.0 - a1 / (2.0 * a2)
            if xs < x1 or xs > x3:
                xs = (x1 + x3) / 2.0

        ys = phi(xs)
        if abs(x2 - xs) <= eps and abs(f2 - ys) <= eps:
            return xs

        points = sorted([(x1, f1), (x2, f2), (x3, f3), (xs, ys)], key=lambda item: item[0])
        best_index = min(range(len(points)), key=lambda i: points[i][1])

        if best_index == 0:
            new_points = points[:3]
        elif best_index == len(points) - 1:
            new_points = points[-3:]
        else:
            new_points = points[best_index - 1:best_index + 2]

        triple = [item[0] for item in new_points]
        values = [item[1] for item in new_points]

    return triple[1]


def line_search_on_line(func, x, tangent, step0, method="golden", eps_1d=1e-6, sven_alpha=1.0):
    phi = one_dimensional_function(func, x, tangent)
    delta = max(abs(step0), 1e-3, sven_alpha)
    a, b = sven_search(phi, x0=0.0, d=delta)

    if method == "golden":
        lam = golden_section(phi, a, b, eps_1d)
    elif method == "dsk":
        lam = dsk_powell(phi, a, b, eps_1d)
    else:
        raise ValueError("method must be 'golden' or 'dsk'")

    return lam, np.array(x, dtype=float) + lam * np.array(tangent, dtype=float)


def constrained_value(func, point, constraints):
    point = np.array(point, dtype=float)
    if not is_feasible(point, constraints):
        return np.inf
    return func(point)


def rosenbrock_stage_kr(func, constraints,x,lmbd,a,b,n,n_rosen,f_comp,fail1,fail2,success1,success2,s1,s2,is_initial,rec_depth=0,max_rec_depth=500,):
    if rec_depth >= max_rec_depth:
        return np.array(x, dtype=float), np.array(lmbd, dtype=float), np.nan, n_rosen

    candidate1 = np.array(x, dtype=float) + lmbd[0] * s1
    f1 = constrained_value(func, candidate1, constraints)
    if f1 < f_comp:
        n += 1
        x = candidate1
        success1 = True
        f_comp = f1

        candidate2 = np.array(x, dtype=float) + lmbd[1] * s2
        f2 = constrained_value(func, candidate2, constraints)
        if f2 < f_comp:
            n += 1
            x = candidate2
            success2 = True
            f_comp = f2
            lmbd = np.array([lmbd[0] * a, lmbd[1] * a], dtype=float)
            return rosenbrock_stage_kr(
                func, constraints, x, lmbd, a, b, n, n_rosen, f_comp,
                fail1, fail2, success1, success2, s1, s2, is_initial,
                rec_depth + 1, max_rec_depth
            )

        n += 1
        if success2:
            fail2 = True
        lmbd = np.array([lmbd[0] * a, lmbd[1] * b], dtype=float)
        return rosenbrock_stage_kr(
            func, constraints, x, lmbd, a, b, n, n_rosen, f_comp,
            fail1, fail2, success1, success2, s1, s2, is_initial,
            rec_depth + 1, max_rec_depth
        )

    n += 1
    if success1:
        fail1 = True

    candidate2 = np.array(x, dtype=float) + lmbd[1] * s2
    f2 = constrained_value(func, candidate2, constraints)
    if f2 < f_comp:
        n += 1
        x = candidate2
        success2 = True
        f_comp = f2
        lmbd = np.array([lmbd[0] * b, lmbd[1] * a], dtype=float)
        return rosenbrock_stage_kr(
            func, constraints, x, lmbd, a, b, n, n_rosen, f_comp,
            fail1, fail2, success1, success2, s1, s2, is_initial,
            rec_depth + 1, max_rec_depth
        )

    n += 1
    if success2:
        fail2 = True
    lmbd = np.array([lmbd[0] * b, lmbd[1] * b], dtype=float)
    if fail1 and fail2:
        if not is_initial:
            lmbd = np.array([lmbd[0] / a * b, lmbd[1] / a * b], dtype=float)
        n_rosen += 1
        return np.array(x, dtype=float), lmbd, n, n_rosen

    return rosenbrock_stage_kr(
        func, constraints, x, lmbd, a, b, n, n_rosen, f_comp,
        fail1, fail2, success1, success2, s1, s2, is_initial,
        rec_depth + 1, max_rec_depth
    )


def params_kr_style(x, x_old, s1, s2):
    x = np.array(x, dtype=float)
    x_old = np.array(x_old, dtype=float)
    s1 = np.array(s1, dtype=float)
    s2 = np.array(s2, dtype=float)

    a1 = np.array([
        (x[0] - x_old[0]) * s1[0] + (x[1] - x_old[1]) * s2[0],
        (x[0] - x_old[0]) * s1[1] + (x[1] - x_old[1]) * s2[1],
    ], dtype=float)
    a2 = np.array([
        (x[1] - x_old[1]) * s2[0],
        (x[1] - x_old[1]) * s2[1],
    ], dtype=float)

    a1_norm = np.linalg.norm(a1)
    if a1_norm < 1e-12:
        return s1, s2

    new_s1 = a1 / a1_norm
    b2 = a2 - np.dot(a2, new_s1) * new_s1
    b2_norm = np.linalg.norm(b2)
    if b2_norm < 1e-12:
        new_s2 = np.array([-new_s1[1], new_s1[0]], dtype=float)
    else:
        new_s2 = b2 / b2_norm
    return new_s1, new_s2


def stop1_kr_style(x, x_old, func, eps):
    x = np.array(x, dtype=float)
    x_old = np.array(x_old, dtype=float)
    step_norm = np.linalg.norm(x - x_old)
    x_norm = np.linalg.norm(x)
    if x_norm < 1e-12:
        x_norm = 1.0
    if step_norm < 1e-12:
        return False
    return step_norm / x_norm < eps and abs(func(x) - func(x_old)) / abs(func(x_old)) < eps


def stalled_state_kr_style(x, x_old):
    return np.linalg.norm(np.array(x, dtype=float) - np.array(x_old, dtype=float)) < 1e-12


def rosenbrock_direct(func,constraints,x0,dx0,a=3.0,b=-0.5,eps=1e-4,max_stages=500,):
    x = project_to_feasible(x0, constraints)
    x_old = np.array(x, dtype=float).copy()
    lmbd = np.array(dx0, dtype=float)
    s1 = np.array([1.0, 0.0], dtype=float)
    s2 = np.array([0.0, 1.0], dtype=float)
    n = 0
    n_rosen = 0
    path = [x.copy()]

    for _ in range(max_stages):
        stage_start = np.array(x, dtype=float).copy()
        if n == 0:
            x, lmbd, n, n_rosen = rosenbrock_stage_kr(
                func, constraints, x, lmbd, a, b, n, n_rosen,
                constrained_value(func, x, constraints),
                False, False, False, False, s1, s2, True
            )
        else:
            x, lmbd, n, n_rosen = rosenbrock_stage_kr(
                func, constraints, x, lmbd, a, b, n, n_rosen,
                constrained_value(func, x, constraints),
                False, False, False, False, s1, s2, False
            )

        if isinstance(n, float) and np.isnan(n):
            return np.array(stage_start, dtype=float), lmbd, np.nan, path, True

        path.append(np.array(x, dtype=float).copy())
        prev_old = np.array(x_old, dtype=float).copy()
        x_old = np.array(stage_start, dtype=float).copy()
        s1, s2 = params_kr_style(x, x_old, s1, s2)

        if stop1_kr_style(x, x_old, func, eps):
            return np.array(x, dtype=float), lmbd, n, path, True

        if stalled_state_kr_style(x, x_old):
            return np.array(x, dtype=float), lmbd, n, path, True

        if np.allclose(prev_old, x_old) and np.allclose(x, stage_start):
            return np.array(x, dtype=float), lmbd, n, path, True

    return np.array(x, dtype=float), lmbd, n, path, False


def refine_on_linear_boundary(func,line_constraint_obj,x,dx,method="golden",eps_1d=1e-6,sven_alpha=0.1,):
    global OBJECTIVE_EVALS
    normal = np.array([line_constraint_obj.a1, line_constraint_obj.a2], dtype=float)
    tangent = np.array([-line_constraint_obj.a2, line_constraint_obj.a1], dtype=float)
    tangent /= max(np.linalg.norm(tangent), 1e-12)

    value = np.dot(normal, x) - line_constraint_obj.b
    x_on_line = np.array(x, dtype=float) - (value / max(np.dot(normal, normal), 1e-12)) * normal
    step0 = max(np.linalg.norm(dx), 1e-3)
    evals_before = OBJECTIVE_EVALS
    _, x_best = line_search_on_line(func, x_on_line, tangent, step0, method, eps_1d, sven_alpha)
    evals_used = OBJECTIVE_EVALS - evals_before
    return x_best, [x.copy(), x_on_line.copy(), x_best.copy()], evals_used


def coord_changes_from_paths(paths):
    count = 0
    for path in paths:
        for i in range(len(path) - 1):
            if not np.allclose(path[i], path[i + 1]):
                count += 1
    return count


def run_case(title,constraints,x0,dx0,a=3.0,b=-0.5,eps=1e-4,line_method=None,eps_1d=1e-6,sven_alpha=0.1,):
    global OBJECTIVE_EVALS
    OBJECTIVE_EVALS = 0

    x, dx, n_evals, path, terminated_by_stall = rosenbrock_direct(
        rosenbrock_function,constraints,x0,dx0,a=a,b=b,eps=eps,)

    paths = [path]
    line_used = False
    one_d_evals = 0
    linear_constraints = [g for g in constraints if getattr(g, "kind", "") == "line"]
    if line_method is not None and linear_constraints and terminated_by_stall:
        x, line_path, one_d_evals = refine_on_linear_boundary(rosenbrock_function,linear_constraints[0],x,dx,method=line_method,eps_1d=eps_1d,sven_alpha=sven_alpha)
        paths.append(line_path)
        line_used = True

    return {
        "title": title,
        "x": x,
        "f": rosenbrock_function(x),
        "f_evals_rosen": int(n_evals),
        "f_evals_1d": int(one_d_evals),
        "f_evals_total": int(n_evals + one_d_evals),
        "coord_changes": coord_changes_from_paths(paths),
        "n_rosen": int(n_evals),
        "paths": paths,
        "line_used": line_used,
        "line_method": line_method,
        "terminated_by_stall": terminated_by_stall,
    }


def print_case_table(header, results):
    print()
    print(header)
    has_1d = any(result["f_evals_1d"] > 0 for result in results)
    if has_1d:
        print("----+------------------------------+---------+---------+---------+---------+-------------+-------------+-------------")
        print(" №  | Сценарій                     | Nrosen  |  N1d    | Nsum    | Ncoord  |     x1      |     x2      |    f(x)     ")
        print("----+------------------------------+---------+---------+---------+---------+-------------+-------------+-------------")
    else:
        print("----+------------------------------+---------+---------+-------------+-------------+-------------")
        print(" №  | Сценарій                     | Nf(x)   | Ncoord  |     x1      |     x2      |    f(x)     ")
        print("----+------------------------------+---------+---------+-------------+-------------+-------------")
    for idx, result in enumerate(results, 1):
        x = result["x"]
        if has_1d:
            print(
                f"{idx:^4}| {result['title'][:28]:<28} | {result['f_evals_rosen']:^7} | {result['f_evals_1d']:^7} | "
                f"{result['f_evals_total']:^7} | {result['coord_changes']:^7} | {x[0]:^11.7f} | "
                f"{x[1]:^11.7f} | {fmt_float(result['f'], 7):^11}"
            )
        else:
            print(
                f"{idx:^4}| {result['title'][:28]:<28} | {result['f_evals_total']:^7} | {result['coord_changes']:^7} | "
                f"{x[0]:^11.7f} | {x[1]:^11.7f} | {fmt_float(result['f'], 7):^11}"
            )
    if has_1d:
        print("----+------------------------------+---------+---------+---------+---------+-------------+-------------+-------------")
    else:
        print("----+------------------------------+---------+---------+-------------+-------------+-------------")


def plot_bar_results(title, labels, values, ylabel):
    plt.figure(figsize=(10, 7))
    plt.bar(range(len(values)), values, color="steelblue")
    plt.xticks(range(len(values)), labels, ha="center")
    plt.ylabel(ylabel)
    plt.title(title)
    plt.tight_layout()
    plt.show()


def plot_line_results(title, x_values, y_values, x_label, y_label, x_scale=None, tick_labels=None):
    plt.figure(figsize=(10, 7))
    plt.plot(x_values, y_values, marker="o")
    if x_scale:
        plt.xscale(x_scale)
    if tick_labels is not None:
        plt.xticks(x_values, tick_labels)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.title(title)
    plt.grid(True, linestyle="--", alpha=0.5)
    plt.tight_layout()
    plt.show()


def draw_constraints(ax, constraints):
    for g in constraints:
        kind = getattr(g, "kind", "")
        if kind == "circle":
            t = np.linspace(0, 2 * np.pi, 400)
            ax.plot(
                g.center[0] + g.radius * np.cos(t),
                g.center[1] + g.radius * np.sin(t),
                linestyle="--",
                color="black",
                linewidth=2,
            )
        elif kind == "line":
            x_line = np.linspace(-3, 3, 300)
            y_line = (g.b - g.a1 * x_line) / g.a2
            ax.plot(x_line, y_line, linestyle="--", color="black", linewidth=2)
        elif kind == "nonconvex":
            t = np.linspace(0, 2 * np.pi, 400)
            ax.plot(2.0 * np.cos(t), 2.0 * np.sin(t), linestyle="--", color="black", linewidth=2)
            hole_r = np.sqrt(0.10)
            ax.plot(1.0 + hole_r * np.cos(t), 1.0 + hole_r * np.sin(t), linestyle="--", color="black", linewidth=2)


def plot_trajectory(title, paths, constraints):
    grid = np.linspace(-3, 3, 200)
    X, Y = np.meshgrid(grid, grid)
    Z = 100 * (X ** 2 - Y) ** 2 + (X - 1) ** 2

    fig, ax = plt.subplots(figsize=(7, 7))
    ax.contour(X, Y, Z, levels=20, cmap="viridis", alpha=0.6)
    ax.contour(X, Y, np.log10(Z + 1e-10), levels=2, cmap="viridis", alpha=0.4)
    draw_constraints(ax, constraints)
    colors = ["crimson", "darkorange", "seagreen"]
    labels = ["Розенброк", "1-D пошук", "Додатковий етап"]
    for idx, path in enumerate(paths):
        points = np.array(path, dtype=float)
        ax.plot(
            points[:, 0],
            points[:, 1],
            marker="o",
            color=colors[idx % len(colors)],
            linewidth=2,
            label=labels[idx] if idx < len(labels) else f"Етап {idx + 1}",
        )
    ax.plot(1.0, 1.0, marker="+", markersize=12, markeredgewidth=2, color="black")
    ax.set_xlabel("x1")
    ax.set_ylabel("x2")
    ax.set_title(title)
    ax.legend()
    fig.tight_layout()
    plt.show()


def convex_scenarios():
    return [
        ("Опукла область: мінімум всередині", [circular_constraint(2.0)]),
        ("Опукла область: мінімум на межі", [circular_constraint(1.0, center=(-0.5, 0.0))]),
    ]


def region_type_scenarios():
    return [
        ("Опукла область", [circular_constraint(1.0, center=(-0.5, 0.0))]),
        ("Лінійне обмеження x1+x2<=1.5", [linear_constraint(1.0, 1.0, 1.5)]),
        ("Неопукла область", [nonconvex_constraint()]),
    ]


if __name__ == "__main__":
    x0 = np.array([-1.2, 0.0], dtype=float)
    dx0 = np.array([1.95, 0.15], dtype=float)
    a = 4.5
    b = -0.25
    eps = 1e-3
    eps_1d = 1e-3
    sven_alpha = 0.1

    convex_results = [
        run_case(name, constraints, x0, dx0, a=a, b=b, eps=eps)
        for name, constraints in convex_scenarios()
    ]
    print_case_table("1. Основний метод Розенброка на опуклих областях", convex_results)
    plot_bar_results(
        "Опуклі області: кількість обчислень цільової функції",
        [result["title"] for result in convex_results],
        [result["f_evals_total"] for result in convex_results],
        "Nf(x)",
    )
    for result, (_, constraints) in zip(convex_results, convex_scenarios()):
        plot_trajectory(result["title"], result["paths"], constraints)

    region_results = [
        run_case(name, constraints, x0, dx0, a=a, b=b, eps=eps)
        for name, constraints in region_type_scenarios()
    ]
    print_case_table("2. Три види областей без допоміжних 1-D функцій", region_results)
    plot_bar_results(
        "Три види областей без допоміжних функцій",
        [result["title"] for result in region_results],
        [result["f_evals_total"] for result in region_results],
        "Nf(x)",
    )
    for result, (_, constraints) in zip(region_results, region_type_scenarios()):
        plot_trajectory(result["title"], result["paths"], constraints)

    line_constraints = [linear_constraint(1.0, 1.0, 1.5)]
    line_results = [
        run_case(f"Лінія + 1D пошук: {method}",line_constraints,x0,dx0,a=a,b=b,eps=eps,line_method=method,eps_1d=eps_1d,sven_alpha=sven_alpha,)
        for method in ["golden", "dsk"]
    ]
    print_case_table("3. Лінійне обмеження: Розенброк, потім рух уздовж межі", line_results)
    
    plot_bar_results(
        "Лінійне обмеження: обчислення лише 1-D пошуку",
        [result["line_method"] for result in line_results],
        [result["f_evals_1d"] for result in line_results],
        "N1d",
    )
    for result in line_results:
        plot_trajectory(result["title"], result["paths"], line_constraints)

    eps_1d_values = [1e-2, 1e-3, 1e-4, 1e-5, 1e-6, 1e-7, 1e-8, 1e-9, 1e-10]
    eps_results_golden = [
        run_case(f"eps_1d = {value:.0e}",line_constraints,x0,dx0,a=a,b=b,eps=eps,line_method="golden",eps_1d=value,sven_alpha=sven_alpha,)
        for value in eps_1d_values
    ]
    print_case_table("4а. Точність 1-D пошуку (золотий перетин)", eps_results_golden)
    
    plot_line_results(
        "Золотий перетин: вплив eps_1d на обчислення 1-D пошуку",
        list(range(len(eps_1d_values))),
        [result["f_evals_1d"] for result in eps_results_golden],
        "eps_1d",
        "N1d",
        tick_labels=[f"{value:.0e}" for value in eps_1d_values],
    )

    eps_results_dsk = [
        run_case(f"eps_1d = {value:.0e}",line_constraints,x0,dx0,a=a,b=b,eps=eps,line_method="dsk",eps_1d=value,sven_alpha=sven_alpha,)
        for value in eps_1d_values
    ]
    print_case_table("4б. Точність 1-D пошуку (ДСК-Пауелла)", eps_results_dsk)
    
    plot_line_results(
        "ДСК-Пауелла: вплив eps_1d на обчислення 1-D пошуку",
        list(range(len(eps_1d_values))),
        [result["f_evals_1d"] for result in eps_results_dsk],
        "eps_1d",
        "N1d",
        tick_labels=[f"{value:.0e}" for value in eps_1d_values],
    )

    sven_values = [0.001, 0.005, 0.01, 0.05, 0.1, 0.25, 0.5, 1.0]
    sven_results = [
        run_case(f"a_sven = {value}",line_constraints,x0,dx0,a=a,b=b,eps=eps,line_method="golden",eps_1d=eps_1d,sven_alpha=value,)
        for value in sven_values
    ]
    print_case_table("5. Вплив параметра a в алгоритмі Свена", sven_results)
    
    plot_line_results(
        "Вплив параметра a в алгоритмі Свена на обчислення 1-D пошуку",
        sven_values,
        [result["f_evals_1d"] for result in sven_results],
        "a_sven",
        "N1d",
        x_scale="log",
    )