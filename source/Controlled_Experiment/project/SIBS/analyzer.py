import re
from collections import defaultdict, deque
from typing import Dict, List, Set

# Conditions that trigger a rebuild
TRIGGER_PATTERNS = [
    re.compile(r"-march=[^\s]+"),                  # Instruction set architecture
    re.compile(
        r"-f(no-)?("
        r"pic|pie|omit-frame-pointer|"
        r"stack-protector(-(all|strong))?|"
        r"visibility=(hidden|default|internal|protected)|"
        r"common|ident|wrapv|trapv|"
        r"(function|data)-sections|"
        r"align-(functions|jumps|labels)=\d+|"
        r"rtti|exceptions|inline(-functions)?|"
        r"unroll(-all-loops)?|"
        r"caller-saves|cprop-registers|"
        r"builtin|profile-arcs|test-coverage|"
        r"strict-aliasing|fast-math|no-math-errno|reciprocal-math|"
        r"short-enums|short-wchar"
        r")\b"
    ),
    re.compile(r"-l\S+"),  # Link library
]

# Matches warning flags such as -Wall, -Wextra
WARNING_PATTERN = re.compile(r"-W[^\s]+")

# Compilation-time factors corresponding to optimization levels
COMPILATION_TIME_FACTORS = {
    "-O0": 1.0,
    "-O1": 1.15,
    "-O": 1.15,
    "-O2": 1.3,
    "-O3": 1.5,
    "-Os": 1.3,
    "-Og": 1.1,
}

# =========================
# Utility functions
# =========================

def is_trigger(token: str, trigger_cache: Dict[str, bool]) -> bool:
    """Determine whether a token triggers a rebuild (with caching)."""
    if token in trigger_cache:
        return trigger_cache[token]
    result = any(pattern.match(token) for pattern in TRIGGER_PATTERNS)
    trigger_cache[token] = result
    return result

def is_warning(token: str, warning_cache: Dict[str, bool]) -> bool:
    """Determine whether a token is a warning flag (with caching)."""
    if token in warning_cache:
        return warning_cache[token]
    result = bool(WARNING_PATTERN.match(token))
    warning_cache[token] = result
    return result

# =========================
# Main logic
# =========================

def compute_config_distance(
    config1: Dict[str, List[str]],
    config2: Dict[str, List[str]],
    verbose: bool = False
) -> float:
    """
    Compute the difference distance between two build configurations.
    """

    # --- Internal helper functions ---

    def build_reverse_dependency_graph(
        config: Dict[str, List[str]]
    ) -> Dict[str, Set[str]]:
        graph = defaultdict(set)
        for target, dependencies in config.items():
            for dep in dependencies:
                if dep in config:
                    graph[dep].add(target)
        return graph

    def get_optimization_factor(
        dependencies: List[str], optimization_cache: Dict[str, float]
    ) -> float:
        factor = 1.0
        for dep in dependencies:
            if dep in COMPILATION_TIME_FACTORS:
                factor = COMPILATION_TIME_FACTORS[dep]
                break
        optimization_cache[tuple(dependencies)] = factor
        return factor

    def bfs_rebuild(start_target: str):
        queue = deque([start_target])
        visited = set()
        while queue:
            current = queue.popleft()
            if current not in visited:
                visited.add(current)
                targets_to_rebuild.add(current)
                queue.extend(reverse_graph1.get(current, set()))
                queue.extend(reverse_graph2.get(current, set()))

    # --- Initialize caches ---

    trigger_cache = {}
    warning_cache = {}
    optimization_cache = {}

    # --- Build reverse dependency graphs ---

    reverse_graph1 = build_reverse_dependency_graph(config1)
    reverse_graph2 = build_reverse_dependency_graph(config2)

    all_targets = set(config1.keys()) | set(config2.keys())
    targets_to_rebuild = set()

    symmetric_diff_map = defaultdict(lambda: {"config1": set(), "config2": set()})

    # --- Compute per-target differences ---

    for target in all_targets:
        deps1 = set(config1.get(target, []))
        deps2 = set(config2.get(target, []))

        symmetric_diff = deps1.symmetric_difference(deps2)
        for dep in symmetric_diff:
            if dep in deps1:
                symmetric_diff_map[target]["config1"].add(dep)
            if dep in deps2:
                symmetric_diff_map[target]["config2"].add(dep)

    # --- Determine targets that need rebuilding ---

    for target in all_targets:
        if target not in targets_to_rebuild:
            changed_deps = (
                symmetric_diff_map[target]["config1"]
                | symmetric_diff_map[target]["config2"]
            )
            if any(is_trigger(dep, trigger_cache) for dep in changed_deps):
                bfs_rebuild(target)

    # --- Calculate total difference ---

    total_difference = 0.0

    for target in all_targets:
        deps1 = set(config1.get(target, []))
        deps2 = set(config2.get(target, []))

        if not deps1 or not deps2:
            # Target exists only in one configuration
            deps = deps1 if deps1 else deps2
            factor = get_optimization_factor(list(deps), optimization_cache)
            num_deps = len(deps)
            total_difference += num_deps * factor
            if verbose:
                print(
                    f"[ONLY IN CONFIG] {target} → +{num_deps} (Factor: {factor})"
                )

        if target in targets_to_rebuild:
            # Re-build required
            all_deps = deps1.union(deps2)
            factor = get_optimization_factor(list(all_deps), optimization_cache)
            num_deps = len(all_deps)
            total_difference += num_deps * factor
            if verbose:
                print(
                    f"[REBUILD REQUIRED] {target} → +{num_deps} (Factor: {factor})"
                )

        if target not in targets_to_rebuild and deps1 and deps2:
            # Penalty for non-trigger differences, excluding warnings
            non_trigger_differences = [
                d
                for d in (
                    symmetric_diff_map[target]["config1"]
                    | symmetric_diff_map[target]["config2"]
                )
                if not is_trigger(d, trigger_cache)
                and not is_warning(d, warning_cache)
            ]
            if non_trigger_differences:
                num_non_trigger = len(non_trigger_differences)
                total_difference += num_non_trigger
                if verbose:
                    print(
                        f"[NON-TRIGGER DIFFERENCE] {target} → +{num_non_trigger}"
                    )

    return round(total_difference, 3)