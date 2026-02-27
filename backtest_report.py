"""
AIPT 回测可视化报告
生成 3 张关键图表 + 统计摘要，保存到 backtest_output/ 目录。
"""

import os
import matplotlib
matplotlib.use("Agg")  # 无头模式
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.patches as mpatches
import numpy as np
import pandas as pd

# 中文字体设置（优先尝试系统中文字体，不行就用默认）
plt.rcParams["font.family"] = ["DejaVu Sans", "SimHei", "WenQuanYi Micro Hei", "sans-serif"]
plt.rcParams["axes.unicode_minus"] = False

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "backtest_output")

# 配色方案
COLORS = {
    "portfolio": "#2196F3",   # 蓝
    "benchmark": "#9E9E9E",   # 灰
    "L1": "#1565C0",          # 深蓝
    "L2": "#E53935",          # 红
    "L3": "#43A047",          # 绿
    "L4": "#FB8C00",          # 橙
    "L5": "#8E24AA",          # 紫
    "cpi": "#2196F3",
    "rdi": "#4CAF50",
    "mqi": "#FF9800",
}

PHASE_COLORS = {
    "Phase 1":   "#C8E6C9",   # 浅绿
    "Phase 1→2": "#FFF9C4",   # 浅黄
    "Phase 2":   "#FFE0B2",   # 浅橙
    "Phase 3":   "#BBDEFB",   # 浅蓝
    "Phase 4":   "#FFCDD2",   # 浅红
}


def generate_backtest_report(results: dict):
    """生成完整的回测报告图表"""
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    print("\n🎨 正在生成可视化报告...")

    _plot_nav_curve(results)
    _plot_allocation_area(results)
    _plot_indicator_evolution(results)

    print(f"\n✅ 所有图表已保存到 {OUTPUT_DIR}/")


def _plot_nav_curve(results: dict):
    """图1: 净值曲线 + 相位背景 + 关键事件标注"""
    fig, ax = plt.subplots(figsize=(16, 8))

    portfolio_nav = results["portfolio_nav"]
    benchmark_nav = results["benchmark_nav"]
    phase_changes = results["phase_changes"]
    stats = results["stats"]

    # 归一化为基准 1.0
    port_norm = portfolio_nav / portfolio_nav.iloc[0]
    bench_norm = benchmark_nav / benchmark_nav.iloc[0]

    # 绘制相位背景色块
    _draw_phase_backgrounds(ax, phase_changes, portfolio_nav.index)

    # 净值曲线
    ax.plot(port_norm.index, port_norm.values, color=COLORS["portfolio"],
            linewidth=2.5, label=f'AIPT Portfolio ({stats["portfolio_total_return"]:+.1%})',
            zorder=5)
    ax.plot(bench_norm.index, bench_norm.values, color=COLORS["benchmark"],
            linewidth=2, linestyle="--",
            label=f'SPY Benchmark ({stats["benchmark_total_return"]:+.1%})',
            zorder=4)

    # 标注相位切换点
    for pc in phase_changes:
        if pc["date"] in port_norm.index:
            idx = port_norm.index.get_loc(pc["date"])
            y_val = port_norm.iloc[idx]
            ax.annotate(
                f'{pc["quarter"]}\n{pc["phase"]}',
                xy=(pc["date"], y_val),
                xytext=(0, 30), textcoords="offset points",
                fontsize=8, ha="center",
                arrowprops=dict(arrowstyle="->", color="#666"),
                bbox=dict(boxstyle="round,pad=0.3", facecolor="white",
                          edgecolor="#ccc", alpha=0.9),
                zorder=10,
            )

    # 标注关键事件
    key_events = [
        ("2025-01-27", "DeepSeek\nNVDA -17%", -60),
        ("2025-08-15", "MIT ROI\nReport", -40),
        ("2026-02-10", "Cloud CapEx\nSell-off", -50),
    ]
    for date_str, label, y_offset in key_events:
        evt_date = pd.Timestamp(date_str)
        if evt_date in port_norm.index:
            idx = port_norm.index.get_loc(evt_date)
        else:
            # 找最接近的交易日
            close_dates = port_norm.index[port_norm.index >= evt_date]
            if len(close_dates) == 0:
                continue
            evt_date = close_dates[0]
            idx = port_norm.index.get_loc(evt_date)
        y_val = port_norm.iloc[idx]
        ax.annotate(
            label,
            xy=(evt_date, y_val),
            xytext=(0, y_offset), textcoords="offset points",
            fontsize=7, ha="center", color="#D32F2F",
            arrowprops=dict(arrowstyle="->", color="#D32F2F", lw=0.8),
            zorder=10,
        )

    ax.set_title("AIPT Model Backtest: Portfolio NAV vs SPY Benchmark\n"
                 "2025-01 to 2026-02 | Quarterly Rebalancing by Phase Signal",
                 fontsize=14, fontweight="bold", pad=15)
    ax.set_ylabel("Normalized NAV (Start = 1.0)", fontsize=11)
    ax.legend(loc="upper left", fontsize=10, framealpha=0.9)
    ax.grid(True, alpha=0.3, linestyle="--")
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m"))
    ax.xaxis.set_major_locator(mdates.MonthLocator(interval=2))
    fig.autofmt_xdate()

    # 统计摘要文本框
    stats_text = (
        f"AIPT Annual Return: {stats['portfolio_annual_return']:+.1%}\n"
        f"SPY Annual Return:  {stats['benchmark_annual_return']:+.1%}\n"
        f"Excess Return:      {stats['excess_return']:+.1%}\n"
        f"AIPT Max Drawdown:  {stats['portfolio_max_drawdown']:.1%}\n"
        f"AIPT Sharpe Ratio:  {stats['portfolio_sharpe']:.2f}"
    )
    ax.text(0.98, 0.02, stats_text, transform=ax.transAxes,
            fontsize=9, verticalalignment="bottom", horizontalalignment="right",
            bbox=dict(boxstyle="round,pad=0.5", facecolor="white",
                      edgecolor="#ccc", alpha=0.95),
            fontfamily="monospace",
            zorder=10)

    fig.tight_layout()
    path = os.path.join(OUTPUT_DIR, "01_nav_curve.png")
    fig.savefig(path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"   📊 净值曲线图 → {path}")


def _plot_allocation_area(results: dict):
    """图2: 仓位配比堆叠面积图"""
    fig, ax = plt.subplots(figsize=(16, 6))

    alloc_hist = results["allocations_history"]
    phase_changes = results["phase_changes"]

    layers = ["L5", "L4", "L3", "L2", "L1"]  # 从下到上
    layer_labels = {
        "L1": "L1 Core Platform (MSFT/AMZN/GOOGL)",
        "L2": "L2 AI Engine (NVDA)",
        "L3": "L3 Power/Infra (CEG/NEE)",
        "L4": "L4 Defensive (XLP)",
        "L5": "L5 Cash (SHV)",
    }

    # 堆叠面积图
    ax.stackplot(
        alloc_hist.index,
        *[alloc_hist[layer].values for layer in layers],
        labels=[layer_labels[l] for l in layers],
        colors=[COLORS[l] for l in layers],
        alpha=0.85,
        zorder=3,
    )

    # 标注相位切换垂直线
    for pc in phase_changes:
        ax.axvline(x=pc["date"], color="#333", linewidth=1, linestyle=":",
                   alpha=0.6, zorder=4)
        ax.text(pc["date"], 102, f'{pc["quarter"]}\n{pc["phase"]}',
                fontsize=7, ha="center", va="bottom",
                bbox=dict(boxstyle="round,pad=0.2", facecolor="white",
                          edgecolor="#999", alpha=0.8),
                zorder=5)

    ax.set_title("AIPT Allocation History by Layer\n"
                 "Phase-Driven Quarterly Rebalancing",
                 fontsize=14, fontweight="bold", pad=15)
    ax.set_ylabel("Allocation (%)", fontsize=11)
    ax.set_ylim(0, 115)
    ax.legend(loc="upper center", ncol=3, fontsize=8, framealpha=0.9,
              bbox_to_anchor=(0.5, -0.08))
    ax.grid(True, alpha=0.2, axis="y")
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m"))
    ax.xaxis.set_major_locator(mdates.MonthLocator(interval=2))
    fig.autofmt_xdate()

    fig.tight_layout()
    path = os.path.join(OUTPUT_DIR, "02_allocation_history.png")
    fig.savefig(path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"   📊 仓位配比图 → {path}")


def _plot_indicator_evolution(results: dict):
    """图3: 核心指标演变 + 相位时间线"""
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(16, 10),
                                    gridspec_kw={"height_ratios": [3, 1]},
                                    sharex=True)

    quarterly_data = results["quarterly_data"]

    quarters = [qd.quarter for qd in quarterly_data]
    dates = [pd.Timestamp(qd.effective_date) for qd in quarterly_data]
    cpis = [qd.cpi for qd in quarterly_data]
    rdis = [qd.rdi for qd in quarterly_data]
    mqis = [qd.mqi for qd in quarterly_data]

    # 上图: CPI / RDI / MQI 折线
    ax1.plot(dates, cpis, "o-", color=COLORS["cpi"], linewidth=2.5,
             markersize=8, label="CPI (CapEx Momentum)", zorder=5)
    ax1.plot(dates, rdis, "s-", color=COLORS["rdi"], linewidth=2.5,
             markersize=8, label="RDI (Demand Validation)", zorder=5)
    ax1.plot(dates, mqis, "D-", color=COLORS["mqi"], linewidth=2.5,
             markersize=8, label="MQI (Profit Quality)", zorder=5)

    # 标注数值
    for i, (d, c, r, m) in enumerate(zip(dates, cpis, rdis, mqis)):
        ax1.annotate(f"{c}", (d, c), textcoords="offset points",
                     xytext=(0, 12), ha="center", fontsize=8,
                     color=COLORS["cpi"], fontweight="bold")
        ax1.annotate(f"{r}", (d, r), textcoords="offset points",
                     xytext=(0, 12), ha="center", fontsize=8,
                     color=COLORS["rdi"], fontweight="bold")
        ax1.annotate(f"{m}", (d, m), textcoords="offset points",
                     xytext=(0, -16), ha="center", fontsize=8,
                     color=COLORS["mqi"], fontweight="bold")

    ax1.axhline(y=0, color="#999", linewidth=0.8, linestyle="-", alpha=0.5)
    ax1.axhline(y=20, color=COLORS["cpi"], linewidth=0.6, linestyle=":",
                alpha=0.4, label="CPI Warning (20)")
    ax1.axhline(y=40, color=COLORS["rdi"], linewidth=0.6, linestyle=":",
                alpha=0.4, label="RDI Support (40)")

    # CPI-MQI 剪刀差填充
    ax1.fill_between(dates, mqis, cpis, alpha=0.08, color="#FF5722",
                     label="CPI-MQI Scissors Gap")

    ax1.set_title("AIPT Core Indicators Evolution\n"
                  "CPI / RDI / MQI Quarterly Tracking (2024Q4 - 2025Q4)",
                  fontsize=14, fontweight="bold", pad=15)
    ax1.set_ylabel("Indicator Score", fontsize=11)
    ax1.legend(loc="upper left", fontsize=8, framealpha=0.9, ncol=2)
    ax1.grid(True, alpha=0.3, linestyle="--")

    # 下图: 相位时间线
    phase_colors_list = [PHASE_COLORS.get(qd.phase, "#EEEEEE") for qd in quarterly_data]
    phase_labels = [qd.phase for qd in quarterly_data]

    for i, (d, pc, pl) in enumerate(zip(dates, phase_colors_list, phase_labels)):
        width = 80  # 大约季度宽度（天数）
        ax2.barh(0, width, left=d, height=0.6, color=pc,
                 edgecolor="#999", linewidth=0.5)
        ax2.text(d + pd.Timedelta(days=width/2), 0,
                 f"{quarters[i]}\n{pl}", ha="center", va="center",
                 fontsize=8, fontweight="bold")

    ax2.set_ylim(-0.5, 0.5)
    ax2.set_yticks([])
    ax2.set_title("Phase Timeline", fontsize=11, fontweight="bold")
    ax2.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m"))

    fig.tight_layout()
    path = os.path.join(OUTPUT_DIR, "03_indicator_evolution.png")
    fig.savefig(path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"   📊 指标演变图 → {path}")


def _draw_phase_backgrounds(ax, phase_changes, date_index):
    """在图表上绘制相位背景色块"""
    for i, pc in enumerate(phase_changes):
        start = pc["date"]
        if i + 1 < len(phase_changes):
            end = phase_changes[i + 1]["date"]
        else:
            end = date_index[-1]
        color = PHASE_COLORS.get(pc["phase"], "#F5F5F5")
        ax.axvspan(start, end, alpha=0.25, color=color, zorder=1)
