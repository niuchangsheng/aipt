"""
AIPT 回测数据模块
包含 README 中 2023 Q4 - 2025 Q4 的季度指标数据，作为回测信号源。
"""

from dataclasses import dataclass
from typing import List


@dataclass
class QuarterData:
    """单季度数据记录"""
    quarter: str           # 如 "2025Q1"
    effective_date: str    # 该季度信号生效日期（季度首个交易日）
    # 原始输入
    capex_growth: float
    revenue_growth: float
    cloud_growth: float
    dc_growth: float
    margin_change: float
    fcf_growth: float
    rate_10y: float
    rate_change: float
    nvda_vs_200ma: str     # "Above" / "Near" / "Below"
    # 计算得到的五维指标
    cpi: float
    rdi: float
    mqi: float
    lpi: float
    pci: int
    # 相位判定
    phase: str
    phase_label: str


# ── 从 README 提取的季度数据 ──────────────────────────────────────────────
# 回测区间: 2024-04-01 → 2026-02-27
# 使用 2023 Q4 数据作为初始仓位建立依据

QUARTERLY_DATA: List[QuarterData] = [
    # 2023 Q4 — Phase 1 巅峰（作为回测起始仓位依据）
    QuarterData(
        quarter="2023Q4",
        effective_date="2024-04-01",   # 回测起始日
        capex_growth=22, revenue_growth=13,
        cloud_growth=28, dc_growth=206,
        margin_change=3, fcf_growth=15,
        rate_10y=3.9, rate_change=-0.7,
        nvda_vs_200ma="Above",
        cpi=9, rdi=117, mqi=18, lpi=-0.7, pci=50,
        phase="Phase 1",
        phase_label="🟢 Phase 1 巅峰"
    ),
    # 2024 Q1 — Phase 1 持续
    QuarterData(
        quarter="2024Q1",
        effective_date="2024-07-01",
        capex_growth=30, revenue_growth=14,
        cloud_growth=30, dc_growth=262,
        margin_change=2, fcf_growth=20,
        rate_10y=4.3, rate_change=0.4,
        nvda_vs_200ma="Above",
        cpi=16, rdi=146, mqi=22, lpi=0.4, pci=50,
        phase="Phase 1",
        phase_label="🟢 Phase 1 军备竞赛"
    ),
    # 2024 Q2 — Phase 1 军备竞赛高潮
    QuarterData(
        quarter="2024Q2",
        effective_date="2024-10-01",
        capex_growth=42, revenue_growth=15,
        cloud_growth=29, dc_growth=122,
        margin_change=3, fcf_growth=25,
        rate_10y=4.3, rate_change=0.0,
        nvda_vs_200ma="Above",
        cpi=27, rdi=76, mqi=28, lpi=0.0, pci=50,
        phase="Phase 1",
        phase_label="🟢 Phase 1 军备竞赛高潮"
    ),
    # 2024 Q3 — Phase 1 末期
    QuarterData(
        quarter="2024Q3",
        effective_date="2025-01-02",
        capex_growth=55, revenue_growth=14,
        cloud_growth=33, dc_growth=94,
        margin_change=1, fcf_growth=15,
        rate_10y=4.2, rate_change=-0.1,
        nvda_vs_200ma="Above",
        cpi=41, rdi=64, mqi=16, lpi=-0.1, pci=50,
        phase="Phase 1",
        phase_label="🟢 Phase 1 末期"
    ),
    # 2024 Q4 — Phase 1→2 过渡
    QuarterData(
        quarter="2024Q4",
        effective_date="2025-04-01",
        capex_growth=63, revenue_growth=14,
        cloud_growth=31, dc_growth=78,
        margin_change=1, fcf_growth=10,
        rate_10y=4.6, rate_change=0.4,
        nvda_vs_200ma="Above",
        cpi=49, rdi=55, mqi=11, lpi=0.4, pci=50,
        phase="Phase 1→2",
        phase_label="🟡 怀疑期（Phase 1→2 过渡）"
    ),
    # 2025 Q1 — 继续过渡，MQI 首次转负
    QuarterData(
        quarter="2025Q1",
        effective_date="2025-07-01",
        capex_growth=63, revenue_growth=13,
        cloud_growth=32, dc_growth=69,
        margin_change=0, fcf_growth=-5,
        rate_10y=4.2, rate_change=-0.4,
        nvda_vs_200ma="Near",
        cpi=50, rdi=51, mqi=-5, lpi=-0.4, pci=50,
        phase="Phase 1→2",
        phase_label="🟡 MQI 转负，怀疑加深"
    ),
    # 2025 Q2 — 正式进入 Phase 2
    QuarterData(
        quarter="2025Q2",
        effective_date="2025-10-01",
        capex_growth=72, revenue_growth=14,
        cloud_growth=33, dc_growth=52,
        margin_change=-1, fcf_growth=-20,
        rate_10y=4.3, rate_change=0.1,
        nvda_vs_200ma="Above",
        cpi=58, rdi=43, mqi=-21, lpi=0.1, pci=50,
        phase="Phase 2",
        phase_label="🟠 Phase 2 初期 — 效率审判开启"
    ),
    # 2025 Q3 — Phase 2 持续
    QuarterData(
        quarter="2025Q3",
        effective_date="2026-01-02",
        capex_growth=78, revenue_growth=14,
        cloud_growth=35, dc_growth=44,
        margin_change=-1, fcf_growth=-10,
        rate_10y=4.5, rate_change=0.2,
        nvda_vs_200ma="Above",
        cpi=64, rdi=40, mqi=-11, lpi=0.2, pci=50,
        phase="Phase 2",
        phase_label="🟠 Phase 2 — 分化持续"
    ),
    # 2025 Q4 — Phase 2 深化（数据尚未完全披露，基于指引预估）
    QuarterData(
        quarter="2025Q4",
        effective_date="2026-04-01",  # 超出回测结束日，不会触发
        capex_growth=100, revenue_growth=16,
        cloud_growth=38, dc_growth=55,
        margin_change=-2, fcf_growth=-15,
        rate_10y=4.0, rate_change=-0.5,
        nvda_vs_200ma="Above",
        cpi=84, rdi=47, mqi=-17, lpi=-0.5, pci=50,
        phase="Phase 2",
        phase_label="🟠 Phase 2 深化 — CPI/MQI 剪刀差极限"
    ),
]


def get_phase_allocation(phase: str) -> dict:
    """
    根据相位判定返回 L1-L5 仓位配比。
    在过渡期使用介于两个相位之间的配比。
    """
    allocations = {
        # 标准相位
        "Phase 1":  {"L1": 0.35, "L2": 0.30, "L3": 0.15, "L4": 0.10, "L5": 0.10},
        "Phase 2":  {"L1": 0.30, "L2": 0.15, "L3": 0.20, "L4": 0.20, "L5": 0.15},
        "Phase 3":  {"L1": 0.40, "L2": 0.10, "L3": 0.15, "L4": 0.20, "L5": 0.15},
        "Phase 4":  {"L1": 0.20, "L2": 0.05, "L3": 0.20, "L4": 0.30, "L5": 0.25},
        # 过渡期：渐进退出第一阶段（L2 -5%, L5 +5%）
        "Phase 1→2": {"L1": 0.35, "L2": 0.25, "L3": 0.15, "L4": 0.10, "L5": 0.15},
    }
    return allocations.get(phase, allocations["Phase 2"])


# ── 各层代表标的 ──────────────────────────────────────────────────────────

LAYER_TICKERS = {
    "L1": ["MSFT", "AMZN", "GOOGL"],   # 等权
    "L2": ["NVDA"],
    "L3": ["CEG", "NEE"],               # 等权
    "L4": ["XLP"],                       # 必需消费 ETF
    "L5": ["SHV"],                       # 短债 ETF（近似现金）
}

BENCHMARK_TICKER = "SPY"

# 回测时间范围
BACKTEST_START = "2024-04-01"
BACKTEST_END = "2026-02-27"
DATA_FETCH_START = "2023-06-01"  # 提前拉取以计算 200MA 等
