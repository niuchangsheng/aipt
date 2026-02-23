# AI 周期相位雷达系统 - 入口
# 规则可解释 + 模块化 + 易于替换数据源，便于升级 v2/v3

from indicators import (
    compute_cpi,
    compute_rdi,
    compute_mqi,
    compute_lpi,
)
from phase_classifier import classify_phase
from allocation_mapper import allocation_by_phase
from report import generate_report


def main():
    # 此处为手动测试值（后续可替换为 data_fetch + 财报解析）
    capex_growth = 40
    revenue_growth = 20
    cloud_growth = 28
    dc_growth = 35
    margin_change = -2
    fcf_growth = 5
    rate_change = 0.3
    credit_spread_change = 0.1
    pci_value = 0

    cpi = compute_cpi(capex_growth, revenue_growth)
    rdi = compute_rdi(cloud_growth, dc_growth)
    mqi = compute_mqi(margin_change, fcf_growth)
    lpi = compute_lpi(rate_change, credit_spread_change)

    phase = classify_phase(cpi, rdi, mqi, lpi, pci_value)
    allocations = allocation_by_phase(phase)

    indicators = {
        "CPI": cpi,
        "RDI": rdi,
        "MQI": mqi,
        "LPI": lpi,
        "PCI": pci_value,
    }

    generate_report(phase, allocations, indicators)


if __name__ == "__main__":
    main()
