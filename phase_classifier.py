# 相位分类：根据五维指标判断当前周期阶段


def classify_phase(cpi, rdi, mqi, lpi, pci):
    """
    根据 CPI, RDI, MQI, LPI, PCI 判断当前处于哪个相位。
    返回: "Phase 1 - Expansion" | "Phase 2 - Efficiency Divergence" | ...
    """
    if cpi > 20 and rdi > 30 and mqi >= 0 and pci < 50:
        return "Phase 1 - Expansion"

    if cpi > 20 and rdi < 30:
        return "Phase 2 - Efficiency Divergence"

    if 0 <= cpi <= 10 and mqi > 0:
        return "Phase 3 - Monetization"

    if cpi < 0 and rdi < 20 and lpi > 0:
        return "Phase 4 - Contraction"

    return "Transitional"
