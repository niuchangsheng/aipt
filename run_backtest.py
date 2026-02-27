#!/usr/bin/env python3
"""
AIPT 实盘回测入口
支持通过命令行参数指定回测区间。
用法:
    python run_backtest.py                          # 使用默认区间
    python run_backtest.py --start 2024-04-01       # 指定起始日
    python run_backtest.py --start 2025-01-02 --end 2026-02-27
"""

import argparse
from backtest_data import BACKTEST_START, BACKTEST_END
from backtest_engine import run_backtest
from backtest_report import generate_backtest_report


def main():
    parser = argparse.ArgumentParser(description="AIPT 实盘回测模拟")
    parser.add_argument("--start", type=str, default=BACKTEST_START,
                        help=f"回测起始日期 (默认: {BACKTEST_START})")
    parser.add_argument("--end", type=str, default=BACKTEST_END,
                        help=f"回测结束日期 (默认: {BACKTEST_END})")
    args = parser.parse_args()

    start_date = args.start
    end_date = args.end

    print("=" * 60)
    print("🚀 AIPT 实盘回测模拟")
    print("   AI Phase Transition Model — Backtest with Real Data")
    print(f"   回测区间: {start_date} → {end_date}")
    print("=" * 60)
    print()

    # 1. 运行回测引擎
    results = run_backtest(start_date=start_date, end_date=end_date)

    # 2. 生成可视化报告（保存到以区间命名的子目录）
    subdir = f"{start_date}_{end_date}"
    generate_backtest_report(results, subdir=subdir)

    print("\n🎯 回测完成！")
    print(f"   查看图表: backtest_output/{subdir}/")


if __name__ == "__main__":
    main()
