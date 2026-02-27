"""
AIPT 回测引擎
使用真实股票价格 + 季度指标信号进行仓位管理模拟。
"""

import pandas as pd
import numpy as np
import yfinance as yf
from datetime import datetime
from backtest_data import (
    QUARTERLY_DATA, LAYER_TICKERS, BENCHMARK_TICKER,
    BACKTEST_START, BACKTEST_END, DATA_FETCH_START,
    get_phase_allocation,
)


def fetch_all_prices() -> pd.DataFrame:
    """拉取所有标的 + 基准的日度收盘价。"""
    all_tickers = []
    for tickers in LAYER_TICKERS.values():
        all_tickers.extend(tickers)
    all_tickers.append(BENCHMARK_TICKER)
    all_tickers = list(set(all_tickers))

    print(f"📡 正在拉取 {len(all_tickers)} 只标的价格数据...")
    print(f"   标的: {', '.join(all_tickers)}")
    print(f"   时间范围: {DATA_FETCH_START} → {BACKTEST_END}")

    data = yf.download(
        all_tickers,
        start=DATA_FETCH_START,
        end=BACKTEST_END,
        progress=False,
        auto_adjust=True,
        group_by="ticker",
    )

    # 提取收盘价
    closes = pd.DataFrame()
    for ticker in all_tickers:
        try:
            if len(all_tickers) == 1:
                closes[ticker] = data["Close"]
            else:
                closes[ticker] = data[(ticker, "Close")]
        except KeyError:
            print(f"   ⚠️ 无法获取 {ticker} 的数据，跳过")

    closes = closes.ffill().dropna(how="all")
    print(f"   ✅ 获取 {len(closes)} 个交易日数据\n")
    return closes


def compute_layer_returns(closes: pd.DataFrame) -> pd.DataFrame:
    """
    计算各层每日收益率。
    每层内等权配置（如 L1 = MSFT/AMZN/GOOGL 等权）。
    """
    daily_returns = closes.pct_change()
    layer_returns = pd.DataFrame(index=daily_returns.index)

    for layer, tickers in LAYER_TICKERS.items():
        available = [t for t in tickers if t in daily_returns.columns]
        if available:
            layer_returns[layer] = daily_returns[available].mean(axis=1)
        else:
            layer_returns[layer] = 0.0

    # 基准
    if BENCHMARK_TICKER in daily_returns.columns:
        layer_returns["Benchmark"] = daily_returns[BENCHMARK_TICKER]
    else:
        layer_returns["Benchmark"] = 0.0

    return layer_returns


def run_backtest() -> dict:
    """
    执行回测主逻辑。

    返回:
        dict 包含:
        - portfolio_nav: 组合净值 Series
        - benchmark_nav: 基准净值 Series
        - allocations_history: 仓位历史 DataFrame
        - phase_changes: 相位切换列表
        - quarterly_data: 季度数据
        - stats: 统计摘要 dict
    """
    closes = fetch_all_prices()
    layer_returns = compute_layer_returns(closes)

    # 过滤回测区间
    bt_start = pd.Timestamp(BACKTEST_START)
    bt_end = pd.Timestamp(BACKTEST_END)
    mask = (layer_returns.index >= bt_start) & (layer_returns.index <= bt_end)
    layer_returns = layer_returns.loc[mask].copy()

    if layer_returns.empty:
        raise ValueError("回测区间内无数据！请检查日期范围。")

    print(f"🔄 回测区间: {layer_returns.index[0].date()} → {layer_returns.index[-1].date()}")
    print(f"   共 {len(layer_returns)} 个交易日\n")

    # ── 初始化 ─────────────────────────────────
    portfolio_nav = pd.Series(index=layer_returns.index, dtype=float)
    benchmark_nav = pd.Series(index=layer_returns.index, dtype=float)
    allocations_history = pd.DataFrame(
        index=layer_returns.index,
        columns=["L1", "L2", "L3", "L4", "L5"],
        dtype=float,
    )

    portfolio_value = 1_000_000  # 100万初始资金
    benchmark_value = 1_000_000
    phase_changes = []

    # 确定每个交易日对应的季度数据
    def get_quarter_data_for_date(dt):
        """找到给定日期对应的最新季度数据"""
        applicable = None
        for qd in QUARTERLY_DATA:
            if pd.Timestamp(qd.effective_date) <= dt:
                applicable = qd
        return applicable

    current_phase = None

    # ── 逐日模拟 ─────────────────────────────────
    for i, date in enumerate(layer_returns.index):
        qd = get_quarter_data_for_date(date)
        if qd is None:
            continue

        # 检测相位变化
        if qd.phase != current_phase:
            alloc = get_phase_allocation(qd.phase)
            phase_changes.append({
                "date": date,
                "quarter": qd.quarter,
                "phase": qd.phase,
                "label": qd.phase_label,
                "allocation": alloc.copy(),
                "cpi": qd.cpi,
                "rdi": qd.rdi,
                "mqi": qd.mqi,
            })
            current_phase = qd.phase
            print(f"   📊 {date.date()} | {qd.quarter} | {qd.phase_label}")
            print(f"      CPI={qd.cpi} RDI={qd.rdi} MQI={qd.mqi} LPI={qd.lpi}")
            print(f"      仓位: " + " ".join(f"{k}={v*100:.0f}%" for k, v in alloc.items()))

        # 计算当日组合收益
        if i == 0:
            portfolio_nav.iloc[i] = portfolio_value
            benchmark_nav.iloc[i] = benchmark_value
        else:
            daily_ret = layer_returns.iloc[i]
            port_ret = sum(alloc.get(layer, 0) * daily_ret.get(layer, 0)
                          for layer in ["L1", "L2", "L3", "L4", "L5"])
            portfolio_value *= (1 + port_ret)
            benchmark_value *= (1 + daily_ret.get("Benchmark", 0))

            portfolio_nav.iloc[i] = portfolio_value
            benchmark_nav.iloc[i] = benchmark_value

        # 记录当日仓位
        for layer in ["L1", "L2", "L3", "L4", "L5"]:
            allocations_history.loc[date, layer] = alloc.get(layer, 0) * 100

    # ── 计算统计指标 ──────────────────────────────
    portfolio_nav = portfolio_nav.dropna()
    benchmark_nav = benchmark_nav.dropna()

    stats = compute_stats(portfolio_nav, benchmark_nav)

    print("\n" + "=" * 60)
    print("📈 回测统计摘要")
    print("=" * 60)
    print(f"   回测期间: {portfolio_nav.index[0].date()} → {portfolio_nav.index[-1].date()}")
    print(f"   初始资金: $1,000,000")
    print(f"")
    print(f"   {'':20s} {'AIPT组合':>12s} {'SPY基准':>12s}")
    print(f"   {'─'*20} {'─'*12} {'─'*12}")
    print(f"   {'终值':20s} ${stats['portfolio_final']:>11,.0f} ${stats['benchmark_final']:>11,.0f}")
    print(f"   {'总收益率':20s} {stats['portfolio_total_return']:>11.2%} {stats['benchmark_total_return']:>11.2%}")
    print(f"   {'年化收益率':20s} {stats['portfolio_annual_return']:>11.2%} {stats['benchmark_annual_return']:>11.2%}")
    print(f"   {'最大回撤':20s} {stats['portfolio_max_drawdown']:>11.2%} {stats['benchmark_max_drawdown']:>11.2%}")
    print(f"   {'年化波动率':20s} {stats['portfolio_volatility']:>11.2%} {stats['benchmark_volatility']:>11.2%}")
    print(f"   {'夏普比率':20s} {stats['portfolio_sharpe']:>11.2f} {stats['benchmark_sharpe']:>11.2f}")
    print(f"")
    print(f"   🏆 超额收益: {stats['excess_return']:>+.2%}")
    print("=" * 60)

    return {
        "portfolio_nav": portfolio_nav,
        "benchmark_nav": benchmark_nav,
        "allocations_history": allocations_history.dropna(how="all"),
        "phase_changes": phase_changes,
        "quarterly_data": QUARTERLY_DATA,
        "stats": stats,
    }


def compute_stats(portfolio_nav: pd.Series, benchmark_nav: pd.Series) -> dict:
    """计算回测统计指标"""
    trading_days = len(portfolio_nav)
    years = trading_days / 252

    # 总收益率
    port_total = portfolio_nav.iloc[-1] / portfolio_nav.iloc[0] - 1
    bench_total = benchmark_nav.iloc[-1] / benchmark_nav.iloc[0] - 1

    # 年化收益率
    port_annual = (1 + port_total) ** (1 / years) - 1 if years > 0 else 0
    bench_annual = (1 + bench_total) ** (1 / years) - 1 if years > 0 else 0

    # 日度收益率
    port_daily = portfolio_nav.pct_change().dropna()
    bench_daily = benchmark_nav.pct_change().dropna()

    # 年化波动率
    port_vol = port_daily.std() * np.sqrt(252)
    bench_vol = bench_daily.std() * np.sqrt(252)

    # 夏普比率 (假设无风险利率 4.5%)
    rf = 0.045
    port_sharpe = (port_annual - rf) / port_vol if port_vol > 0 else 0
    bench_sharpe = (bench_annual - rf) / bench_vol if bench_vol > 0 else 0

    # 最大回撤
    port_dd = compute_max_drawdown(portfolio_nav)
    bench_dd = compute_max_drawdown(benchmark_nav)

    return {
        "portfolio_final": portfolio_nav.iloc[-1],
        "benchmark_final": benchmark_nav.iloc[-1],
        "portfolio_total_return": port_total,
        "benchmark_total_return": bench_total,
        "portfolio_annual_return": port_annual,
        "benchmark_annual_return": bench_annual,
        "portfolio_volatility": port_vol,
        "benchmark_volatility": bench_vol,
        "portfolio_sharpe": port_sharpe,
        "benchmark_sharpe": bench_sharpe,
        "portfolio_max_drawdown": port_dd,
        "benchmark_max_drawdown": bench_dd,
        "excess_return": port_total - bench_total,
        "trading_days": trading_days,
    }


def compute_max_drawdown(nav: pd.Series) -> float:
    """计算最大回撤"""
    peak = nav.expanding().max()
    drawdown = (nav - peak) / peak
    return drawdown.min()
