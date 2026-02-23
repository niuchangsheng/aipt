# 报告输出：当前相位、指标与建议仓位


def generate_report(phase, allocations, indicators):
    """打印 AI 周期报告到控制台。"""
    print("========== AI Cycle Report ==========")
    print(f"Current Phase: {phase}")
    print("\nIndicators:")
    for k, v in indicators.items():
        print(f"  {k}: {v}")

    print("\nSuggested Allocation:")
    for layer, weight in allocations.items():
        print(f"  {layer}: {weight}%")

    print("=====================================")
