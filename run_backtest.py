#!/usr/bin/env python3
"""
AIPT 实盘回测入口
从 2025-01-01 到 2026-02-27，用真实市场数据验证模型仓位管理效果。
"""

from backtest_engine import run_backtest
from backtest_report import generate_backtest_report


def main():
    print("=" * 60)
    print("🚀 AIPT 实盘回测模拟")
    print("   AI Phase Transition Model — Backtest with Real Data")
    print("   回测区间: 2025-01-02 → 2026-02-27")
    print("=" * 60)
    print()

    # 1. 运行回测引擎
    results = run_backtest()

    # 2. 生成可视化报告
    generate_backtest_report(results)

    print("\n🎯 回测完成！")
    print(f"   查看图表: backtest_output/")


if __name__ == "__main__":
    main()
