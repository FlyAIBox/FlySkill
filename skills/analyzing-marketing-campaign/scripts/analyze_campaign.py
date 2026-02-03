import pandas as pd
import numpy as np

# 读取数据 - 跳过第一行(标题使用中文顿号分隔)，手动指定列名
column_names = ['日期', '营销活动名称', '渠道', '受众分群', '展示次数', '点击次数', '转化次数', '支出', '收入', '订单数']
df = pd.read_csv('material/campaign_data_week1_china.csv', skiprows=1, names=column_names)

print("=" * 80)
print("营销活动数据分析报告")
print("=" * 80)

print("\n" + "=" * 60)
print("一、数据质量检查")
print("=" * 60)

# 1. 检查缺失值
print("\n【缺失值统计】")
missing_stats = df.isnull().sum()
for col in df.columns:
    if missing_stats[col] > 0:
        print(f"  {col}: {missing_stats[col]} 条缺失 ({missing_stats[col]/len(df)*100:.1f}%)")

# 2. 检查异常值
print("\n【数据异常检查】")
print(f"  总记录数: {len(df)} 条")
print(f"  负值支出: {(df['支出'] < 0).sum()} 条")
print(f"  负值收入: {(df['收入'] < 0).sum()} 条")
print(f"  展示次数为0: {(df['展示次数'] == 0).sum()} 条")

# 检查展示次数为空的情况
empty_impr = df['展示次数'].isna() | (df['展示次数'].astype(str).str.strip() == '')
print(f"  展示次数为空/未记录: {empty_impr.sum()} 条")

# 统计各渠道展示次数缺失情况
print("\n【按渠道 - 展示次数缺失情况】")
for channel in df['渠道'].unique():
    channel_data = df[df['渠道'] == channel]
    missing = channel_data['展示次数'].isna().sum() + (channel_data['展示次数'].astype(str).str.strip() == '').sum()
    print(f"  {channel}: {missing}/{len(channel_data)} 条缺失")

print("\n" + "=" * 60)
print("二、漏斗分析 - CTR & CVR")
print("=" * 60)

# 历史基准
benchmarks = {
    '微信广告': {'ctr': 0.025, 'cvr': 0.038, 'note': '社交生态基准'},
    '百度推广': {'ctr': 0.050, 'cvr': 0.045, 'note': '搜索广告基准'},
    '抖音广告': {'ctr': 0.020, 'cvr': 0.009, 'note': '短视频流基准'},
    '小程序推送': {'ctr': 0.150, 'cvr': 0.021, 'note': '私域/Retargeting基准'}
}

# 按渠道计算指标
results = []

for channel, benchmark in benchmarks.items():
    channel_data = df[df['渠道'] == channel].copy()

    # 处理展示次数 - 过滤空值
    channel_data['展示次数'] = pd.to_numeric(channel_data['展示次数'], errors='coerce')

    # 计算汇总指标
    total_impr = channel_data['展示次数'].sum()
    total_clicks = channel_data['点击次数'].sum()
    total_conv = channel_data['转化次数'].sum()

    # 计算比率
    if total_impr > 0:
        ctr = total_clicks / total_impr
    else:
        ctr = np.nan

    if total_clicks > 0:
        cvr = total_conv / total_clicks
    else:
        cvr = np.nan

    if not np.isnan(ctr):
        ctr_diff = (ctr - benchmark['ctr']) / benchmark['ctr'] * 100
    else:
        ctr_diff = np.nan

    if not np.isnan(cvr):
        cvr_diff = (cvr - benchmark['cvr']) / benchmark['cvr'] * 100
    else:
        cvr_diff = np.nan

    results.append({
        'channel': channel,
        'impressions': total_impr,
        'clicks': total_clicks,
        'conversions': total_conv,
        'ctr': ctr,
        'cvr': cvr,
        'ctr_bench': benchmark['ctr'],
        'cvr_bench': benchmark['cvr'],
        'ctr_diff': ctr_diff,
        'cvr_diff': cvr_diff,
        'note': benchmark['note']
    })

# 打印结果表格
print(f"\n{'渠道':<12} {'展示次数':>12} {'点击次数':>10} {'转化次数':>10} {'CTR实际':>10} {'CTR目标':>10} {'差异':>10} {'CVR实际':>10} {'CVR目标':>10} {'差异':>10}")
print("-" * 120)

for r in results:
    ctr_str = f"{r['ctr']*100:.2f}%" if not np.isnan(r['ctr']) else "N/A"
    cvr_str = f"{r['cvr']*100:.2f}%" if not np.isnan(r['cvr']) else "N/A"
    ctr_diff_str = f"{r['ctr_diff']:+.1f}%" if not np.isnan(r['ctr_diff']) else "N/A"
    cvr_diff_str = f"{r['cvr_diff']:+.1f}%" if not np.isnan(r['cvr_diff']) else "N/A"

    print(f"{r['channel']:<12} {r['impressions']:>12,} {r['clicks']:>10,} {r['conversions']:>10,} "
          f"{ctr_str:>10} {r['ctr_bench']*100:>9.1f}% {ctr_diff_str:>10} "
          f"{cvr_str:>10} {r['cvr_bench']*100:>9.1f}% {cvr_diff_str:>10}")

print("\n" + "=" * 60)
print("三、关键发现")
print("=" * 60)

for r in results:
    print(f"\n【{r['channel']} - {r['note']}】")

    if not np.isnan(r['ctr_diff']):
        if r['ctr_diff'] >= 0:
            print(f"  ✓ CTR: {r['ctr']*100:.2f}% > 目标 {r['ctr_bench']*100:.1f}% (超出 {r['ctr_diff']:+.1f}%)")
        else:
            print(f"  ✗ CTR: {r['ctr']*100:.2f}% < 目标 {r['ctr_bench']*100:.1f}% (低于 {r['ctr_diff']:.1f}%)")
    else:
        print(f"  ⚠ CTR: 无法计算 - 展示次数数据缺失")

    if not np.isnan(r['cvr_diff']):
        if r['cvr_diff'] >= 0:
            print(f"  ✓ CVR: {r['cvr']*100:.2f}% > 目标 {r['cvr_bench']*100:.1f}% (超出 {r['cvr_diff']:+.1f}%)")
        else:
            print(f"  ✗ CVR: {r['cvr']*100:.2f}% < 目标 {r['cvr_bench']*100:.1f}% (低于 {r['cvr_diff']:.1f}%)")
    else:
        print(f"  ⚠ CVR: 无法计算 - 点击次数为0")

# 数据质量警告
print("\n" + "=" * 60)
print("四、数据质量警告")
print("=" * 60)

mini_prog_missing = df[df['渠道'] == '小程序推送']['展示次数'].isna().sum() + \
                    (df[df['渠道'] == '小程序推送']['展示次数'].astype(str).str.strip() == '').sum()

if mini_prog_missing > 0:
    print(f"\n⚠ 小程序推送渠道有 {mini_prog_missing} 条记录的展示次数数据缺失")
    print(f"   这导致无法准确计算该渠道的CTR指标")
    print(f"   建议：联系数据提供商补充展示次数数据")

print("\n" + "=" * 60)
print("五、汇总统计")
print("=" * 60)

total_spend = df['支出'].sum()
total_revenue = df['收入'].sum()
total_orders = df['订单数'].sum()
roas = total_revenue / total_spend if total_spend > 0 else 0
profit = total_revenue - total_spend
profit_margin = profit / total_revenue * 100 if total_revenue > 0 else 0

print(f"\n  总支出: ¥{total_spend:,.2f}")
print(f"  总收入: ¥{total_revenue:,.2f}")
print(f"  总订单数: {total_orders:,}")
print(f"  ROAS (广告回报率): {roas:.2f}x")
print(f"  利润: ¥{profit:,.2f}")
print(f"  利润率: {profit_margin:.1f}%")

print("\n" + "=" * 80)
print("六、效率分析 (ROAS / CPA / 净利润)")
print("=" * 80)

# 成本假设
SHIPPING_COST_PER_ORDER = 8.0  # 每单物流成本
PRODUCT_COST_PERCENT = 0.35    # 产品成本占比 35%

# 目标基准
TARGET_ROAS = 4.0
MAX_CPA = 50.0

# 计算效率指标
efficiency_results = []

for r in results:
    channel_data = df[df['渠道'] == r['channel']]

    total_spend = channel_data['支出'].sum()
    total_revenue = channel_data['收入'].sum()
    total_conversions = channel_data['转化次数'].sum()
    total_orders = channel_data['订单数'].sum()

    # ROAS = 收入 / 支出
    roas = total_revenue / total_spend if total_spend > 0 else 0

    # CPA = 支出 / 转化次数
    cpa = total_spend / total_conversions if total_conversions > 0 else 0

    # 净利润 = 收入 - 总成本
    # 总成本 = 支出 + (订单数 × 物流成本) + (收入 × 产品成本占比)
    shipping_cost = total_orders * SHIPPING_COST_PER_ORDER
    product_cost = total_revenue * PRODUCT_COST_PERCENT
    total_cost = total_spend + shipping_cost + product_cost
    net_profit = total_revenue - total_cost

    efficiency_results.append({
        'channel': r['channel'],
        'spend': total_spend,
        'revenue': total_revenue,
        'conversions': total_conversions,
        'orders': total_orders,
        'roas': roas,
        'cpa': cpa,
        'shipping_cost': shipping_cost,
        'product_cost': product_cost,
        'total_cost': total_cost,
        'net_profit': net_profit,
        'profit_margin': net_profit / total_revenue * 100 if total_revenue > 0 else 0
    })

# 打印效率分析表格
print(f"\n{'渠道':<12} {'支出':>12} {'收入':>12} {'ROAS':>10} {'目标':>8} {'CPA':>10} {'限额':>8} {'净利润':>12} {'利润率':>10}")
print("-" * 110)

for e in efficiency_results:
    roas_str = f"{e['roas']:.2f}x"
    roas_target_str = f"{TARGET_ROAS:.1f}x"
    cpa_str = f"¥{e['cpa']:.2f}"
    cpa_limit_str = f"¥{MAX_CPA:.0f}"
    profit_str = f"¥{e['net_profit']:,.0f}"
    margin_str = f"{e['profit_margin']:.1f}%"

    # 添加状态标记
    roas_status = "✓" if e['roas'] >= TARGET_ROAS else "✗"
    cpa_status = "✓" if e['cpa'] <= MAX_CPA else "✗"
    profit_status = "✓" if e['net_profit'] > 0 else "✗"

    print(f"{e['channel']:<12} ¥{e['spend']:>10,.2f} ¥{e['revenue']:>10,.2f} "
          f"{roas_str:>9} {roas_target_str:>7} "
          f"{cpa_status} {cpa_str:>8} {cpa_limit_str:>7} "
          f"{profit_status} {profit_str:>11} {margin_str:>9}")

print("\n" + "-" * 80)
print("图例: ✓ 达标  ✗ 未达标")

# 详细成本分析
print("\n" + "=" * 80)
print("七、详细成本结构分析")
print("=" * 80)

print(f"\n{'渠道':<12} {'广告支出':>12} {'物流成本':>12} {'产品成本':>12} {'总成本':>12} {'总收入':>12} {'净利润':>12}")
print("-" * 100)

for e in efficiency_results:
    print(f"{e['channel']:<12} ¥{e['spend']:>10,.2f} ¥{e['shipping_cost']:>10,.2f} "
          f"¥{e['product_cost']:>10,.2f} ¥{e['total_cost']:>10,.2f} "
          f"¥{e['revenue']:>10,.2f} ¥{e['net_profit']:>10,.2f}")

# 效率评估总结
print("\n" + "=" * 80)
print("八、效率评估总结")
print("=" * 80)

for e in efficiency_results:
    print(f"\n【{e['channel']}】")

    # ROAS评估
    if e['roas'] >= TARGET_ROAS:
        print(f"  ✓ ROAS: {e['roas']:.2f}x >= 目标 {TARGET_ROAS:.1f}x (达标)")
    else:
        gap = ((e['roas'] - TARGET_ROAS) / TARGET_ROAS) * 100
        print(f"  ✗ ROAS: {e['roas']:.2f}x < 目标 {TARGET_ROAS:.1f}x (低于 {gap:.1f}%)")

    # CPA评估
    if e['cpa'] <= MAX_CPA:
        print(f"  ✓ CPA: ¥{e['cpa']:.2f} <= 限额 ¥{MAX_CPA:.0f} (达标)")
    else:
        over = ((e['cpa'] - MAX_CPA) / MAX_CPA) * 100
        print(f"  ✗ CPA: ¥{e['cpa']:.2f} > 限额 ¥{MAX_CPA:.0f} (超出 {over:.1f}%)")

    # 净利润评估
    if e['net_profit'] > 0:
        print(f"  ✓ 净利润: ¥{e['net_profit']:,.2f} (盈利, 利润率 {e['profit_margin']:.1f}%)")
    else:
        print(f"  ✗ 净利润: ¥{e['net_profit']:,.2f} (亏损)")

print("\n" + "=" * 80)
print("九、优化建议")
print("=" * 80)

# 找出表现最好和最差的渠道
ctr_valid = [r for r in results if not np.isnan(r['ctr_diff'])]
cvr_valid = [r for r in results if not np.isnan(r['cvr_diff'])]

if ctr_valid:
    best_ctr = max(ctr_valid, key=lambda x: x['ctr_diff'])
    worst_ctr = min(ctr_valid, key=lambda x: x['ctr_diff'])

    print(f"\n【CTR表现】")
    print(f"  最佳: {best_ctr['channel']} (超出目标 {best_ctr['ctr_diff']:+.1f}%)")
    print(f"  需改进: {worst_ctr['channel']} (低于目标 {worst_ctr['ctr_diff']:.1f}%)")

if cvr_valid:
    best_cvr = max(cvr_valid, key=lambda x: x['cvr_diff'])
    worst_cvr = min(cvr_valid, key=lambda x: x['cvr_diff'])

    print(f"\n【CVR表现】")
    print(f"  最佳: {best_cvr['channel']} (超出目标 {best_cvr['cvr_diff']:+.1f}%)")
    print(f"  需改进: {worst_cvr['channel']} (低于目标 {worst_cvr['cvr_diff']:.1f}%)")

# 效率指标建议
print(f"\n【效率指标建议】")

best_roas = max(efficiency_results, key=lambda x: x['roas'])
best_cpa = min(efficiency_results, key=lambda x: x['cpa'])
best_profit = max(efficiency_results, key=lambda x: e['net_profit'])

print(f"  最高ROAS: {best_roas['channel']} ({best_roas['roas']:.2f}x)")
print(f"  最低CPA: {best_cpa['channel']} (¥{best_cpa['cpa']:.2f})")
print(f"  最高净利润: {best_profit['channel']} (¥{best_profit['net_profit']:,.2f})")

# 找出需要改进的渠道
print(f"\n【需重点关注】")

for e in efficiency_results:
    issues = []
    if e['roas'] < TARGET_ROAS:
        issues.append(f"ROAS不达标 ({e['roas']:.2f}x < {TARGET_ROAS:.1f}x)")
    if e['cpa'] > MAX_CPA:
        issues.append(f"CPA超限 (¥{e['cpa']:.2f} > ¥{MAX_CPA:.0f})")
    if e['net_profit'] <= 0:
        issues.append(f"净利润为负 (¥{e['net_profit']:,.2f})")

    if issues:
        print(f"  {e['channel']}: {', '.join(issues)}")

print("\n" + "=" * 80)
