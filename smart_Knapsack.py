class Package:
    def __init__(self, id, weight, volume, priority, customer_demand, delivery_deadline):
        self.id = id
        self.weight = weight
        self.volume = volume
        self.priority = priority
        self.customer_demand = customer_demand
        self.delivery_deadline = delivery_deadline

    def __repr__(self):
        return (f"Package(id='{self.id}', weight={self.weight}, volume={self.volume}, "
                f"priority={self.priority}, customer_demand={self.customer_demand}, delivery_deadline={self.delivery_deadline})")

# ------------------- Greedy Algorithm ------------------- #

def greedy_algorithm(packages, max_weight):
    """
    Greedy Algorithm for selecting packages based on priority-to-weight ratio.
    """
    packages.sort(key=lambda pkg: pkg.priority / pkg.weight, reverse=True)
    selected_packages = []
    total_weight = 0
    total_priority = 0

    for pkg in packages:
        if total_weight + pkg.weight <= max_weight:
            selected_packages.append(pkg)
            total_weight += pkg.weight
            total_priority += pkg.priority

    return selected_packages, total_weight, total_priority

# ------------------- Dynamic Programming ------------------- #

def dynamic_programming(packages, max_weight):
    """
    Dynamic Programming approach for solving the knapsack problem.
    """
    n = len(packages)
    dp = [[0 for _ in range(max_weight + 1)] for _ in range(n + 1)]

    for i in range(1, n + 1):
        for w in range(max_weight + 1):
            if packages[i - 1].weight <= w:
                dp[i][w] = max(dp[i - 1][w], 
                               dp[i - 1][int(w - packages[i - 1].weight)] + packages[i - 1].priority)
            else:
                dp[i][w] = dp[i - 1][w]

    # Trace back to find selected packages
    w = max_weight
    selected_packages = []
    for i in range(n, 0, -1):
        if dp[i][w] != dp[i - 1][w]:
            selected_packages.append(packages[i - 1])
            w -= int(packages[i - 1].weight)

    total_priority = dp[n][max_weight]
    total_weight = sum(pkg.weight for pkg in selected_packages)

    return selected_packages, total_weight, total_priority

# ------------------- Branch and Bound ------------------- #

class Node:
    def __init__(self, level, weight, priority, bound, selected):
        self.level = level
        self.weight = weight
        self.priority = priority
        self.bound = bound
        self.selected = selected

def bound(node, n, max_weight, packages):
    if node.weight >= max_weight:
        return 0

    profit_bound = node.priority
    j = node.level + 1
    total_weight = node.weight

    while j < n and total_weight + packages[j].weight <= max_weight:
        total_weight += packages[j].weight
        profit_bound += packages[j].priority
        j += 1

    if j < n:
        profit_bound += (max_weight - total_weight) * (packages[j].priority / packages[j].weight)

    return profit_bound

def branch_and_bound(packages, max_weight):
    packages.sort(key=lambda pkg: pkg.priority / pkg.weight, reverse=True)
    n = len(packages)
    queue = []
    v = Node(-1, 0, 0, 0.0, [])
    queue.append(v)

    max_priority = 0
    best_selection = []

    while queue:
        v = queue.pop(0)

        if v.level == -1:
            u_level = 0
        else:
            u_level = v.level + 1

        if u_level < n:
            u = Node(u_level, v.weight + packages[u_level].weight,
                     v.priority + packages[u_level].priority, 0.0, v.selected + [packages[u_level]])

            if u.weight <= max_weight and u.priority > max_priority:
                max_priority = u.priority
                best_selection = u.selected

            u.bound = bound(u, n, max_weight, packages)

            if u.bound > max_priority:
                queue.append(u)

            u = Node(u_level, v.weight, v.priority, 0.0, v.selected)
            u.bound = bound(u, n, max_weight, packages)

            if u.bound > max_priority:
                queue.append(u)

    total_weight = sum(pkg.weight for pkg in best_selection)

    return best_selection, total_weight, max_priority

# ------------------- Main Program ------------------- #

if __name__ == "__main__":
    packages = [
        Package('PKG-1', 5.55, 4.55, 8.54, 0.65, 16.95),
        Package('PKG-2', 2.25, 1.55, 5.14, 0.45, 12.12),
        Package('PKG-3', 7.81, 0.36, 8.38, 0.24, 5.36),
        Package('PKG-4', 1.56, 2.02, 3.3, 0.38, 26.61),
        # Add more packages as needed...
    ]

    max_weight = 50  # Maximum weight constraint

    print("\n--- Greedy Algorithm ---")
    greedy_selected, greedy_weight, greedy_priority = greedy_algorithm(packages, max_weight)
    print(f"Selected Packages: {greedy_selected}")
    print(f"Total Weight: {greedy_weight:.2f}")
    print(f"Total Priority: {greedy_priority:.2f}")

    print("\n--- Dynamic Programming ---")
    dp_selected, dp_weight, dp_priority = dynamic_programming(packages, max_weight)
    print(f"Selected Packages: {dp_selected}")
    print(f"Total Weight: {dp_weight:.2f}")
    print(f"Total Priority: {dp_priority:.2f}")

    print("\n--- Branch and Bound ---")
    bb_selected, bb_weight, bb_priority = branch_and_bound(packages, max_weight)
    print(f"Selected Packages: {bb_selected}")
    print(f"Total Weight: {bb_weight:.2f}")
    print(f"Total Priority: {bb_priority:.2f}")
