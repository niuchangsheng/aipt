# 仓位映射：根据相位自动给出五层仓位建议


def allocation_by_phase(phase):
    """
    根据当前相位返回 L1~L5 建议仓位（百分比）。
    """
    allocations = {
        "Phase 1 - Expansion": {"L1": 35, "L2": 30, "L3": 15, "L4": 10, "L5": 10},
        "Phase 2 - Efficiency Divergence": {"L1": 30, "L2": 15, "L3": 20, "L4": 20, "L5": 15},
        "Phase 3 - Monetization": {"L1": 40, "L2": 10, "L3": 15, "L4": 20, "L5": 15},
        "Phase 4 - Contraction": {"L1": 20, "L2": 5, "L3": 20, "L4": 30, "L5": 25},
    }
    return allocations.get(phase, {})
