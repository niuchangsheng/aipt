# 五个雷达维度指标计算（规则可解释、易于替换数据源）


def compute_cpi(capex_growth, revenue_growth):
    """CapEx 动能指数：CapEx 增速 - 收入增速。"""
    return capex_growth - revenue_growth


def compute_rdi(cloud_growth, dc_growth):
    """需求兑现指数：云收入增速 + 数据中心收入增速（此处取平均作为标量）。"""
    return (cloud_growth + dc_growth) / 2


def compute_mqi(margin_change, fcf_growth):
    """利润质量指数：云业务利润率变化 + FCF 增速。"""
    return margin_change + fcf_growth


def compute_lpi(rate_change, credit_spread_change):
    """流动性压力指数：10Y 利率变化 + 信用利差变化。"""
    return rate_change + credit_spread_change


def compute_pci(price_series):
    """价格确认指数：基于是否跌破 200 日线等（简化：跌破=0，否则=50）。"""
    if price_series is None or len(price_series) < 200:
        return 50  # 数据不足时默认中性
    ma200 = price_series.rolling(200).mean()
    below_ma = price_series.iloc[-1] < ma200.iloc[-1]
    return 0 if below_ma else 50
