# AI Phase Transition Model（AIPT）

## 命名由来

本仓库采用 **相位转移理论风格** 的命名：

- **全称**：AI Phase Transition Model  
- **简称**：AIPT  

**含义**：类比物理中的相变——

- 从扩张 → 收缩  
- 从泡沫 → 坍塌  
- 从无序 → 有序  

---

## v1.0：相位雷达

用 **5 个核心变量** 判断当前处于哪个周期阶段，并自动映射到五层仓位结构。

### 周期阶段（四相位）

| 阶段 | 名称 |
|------|------|
| Phase 1 | 军备竞赛扩张期 |
| Phase 2 | 效率分化期 |
| Phase 3 | 收益兑现期 |
| Phase 4 | 资本收缩期 |

### 五个雷达维度

| 指标 | 含义 | 简要判断 |
|------|------|----------|
| **CPI**  CapEx 动能指数 | CapEx 增速 − 收入增速 | >20% 军备竞赛，0~20% 正常扩张，<0 收缩 |
| **RDI** 需求兑现指数 | 云收入增速 + 数据中心收入增速 | >40% 强需求，25~40% 健康，<20% 放缓 |
| **MQI** 利润质量指数 | 云利润率变化 + FCF 增速 | 上升=效率提升，连续下降=警报 |
| **LPI** 流动性压力指数 | 10Y 利率 + 信用利差变化 | 上升=收紧，下降=宽松 |
| **PCI** 价格确认指数 | 龙头新高 + 200 日线 + 财报后反应 | 综合价格确认 |

### 相位判断与仓位映射

- **Phase 1 扩张期**：CPI>20, RDI>30, MQI 稳定 → 仓位示例 `L1:35, L2:30, L3:15, L4:10, L5:10`
- **Phase 2 效率分化期**：CPI>20, RDI 下降, MQI 分化 → `L1:30, L2:15, L3:20, L4:20, L5:15`
- **Phase 3 收益兑现期**：CPI 0~10, MQI 上升 → `L1:40, L2:10, L3:15, L4:20, L5:15`
- **Phase 4 资本收缩期**：CPI<0, RDI<20, LPI 上升, PCI 恶化 → `L1:20, L2:5, L3:20, L4:30, L5:25`

### 代码结构

```
config.py           # 配置（标的、权重等）
data_fetch.py       # 数据获取（yfinance，可换 API）
indicators.py       # 五维指标计算（CPI/RDI/MQI/LPI/PCI）
phase_classifier.py # 相位分类 (classify_phase)
allocation_mapper.py# 仓位映射 (allocation_by_phase)
report.py           # 报告输出
main.py             # 入口（当前为手动测试值，可接真实数据）
```

**运行**（建议在虚拟环境中）：

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/python main.py
```

### 当前阶段判断（2026 早期）

CapEx 仍高、云增速尚可、利润压力出现、龙头波动加大 → 更接近 **Phase 1 → Phase 2 过渡**（军备竞赛后段，效率开始被市场审视）。

### 后续升级方向

- A. 完整可运行 Python 模板  
- B. 回测模块  
- C. 可视化仪表盘（Streamlit）  
- D. 情绪/期权数据  
