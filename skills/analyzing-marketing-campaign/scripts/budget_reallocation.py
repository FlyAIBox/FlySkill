import pandas as pd
import numpy as np

# 读取数据
column_names = ['日期', '营销活动名称', '渠道', '受众分群', '展示次数', '点击次数', '转化次数', '支出', '收入', '订单数']
df = pd.read_csv('material/campaign_data_week1_china.csv', skiprows=1, names=column_names)

# 成本假设
SHIPPING_COST_PER_ORDER = 8.0
PRODUCT_COST_PERCENT = 0.35

# 目标基准
TARGET_ROAS = 4.0
MAX_CPA = 50.0

# 用户约束
USER_REALLOCATION_LIMIT = 10000.0  # 总调配限额 ¥10,000
PER_CHANNEL_INCREASE_CAP = 0.15    # 单渠道增幅上限 15%

print("=" * 80)
print("预算重新分配方案")
print("=" * 80)

# 按渠道汇总数据
channel_summary = []
for channel in df['渠道'].unique():
    channel_data = df[df['渠道'] == channel]

    total_spend = channel_data['支出'].sum()
    total_revenue = channel_data['收入'].sum()
    total_conversions = channel_data['转化次数'].sum()
    total_orders = channel_data['订单数'].sum()

    roas = total_revenue / total_spend if total_spend > 0 else 0
    cpa = total_spend / total_conversions if total_conversions > 0 else 0

    shipping_cost = total_orders * SHIPPING_COST_PER_ORDER
    product_cost = total_revenue * PRODUCT_COST_PERCENT
    total_cost = total_spend + shipping_cost + product_cost
    net_profit = total_revenue - total_cost

    channel_summary.append({
        'channel': channel,
        'spend': total_spend,
        'conversions': total_conversions,
        'roas': roas,
        'cpa': cpa,
        'net_profit': net_profit
    })

print("\n" + "=" * 80)
print("一、渠道分类表")
print("=" * 80)

# 分类结果
classifications = []

for ch in channel_summary:
    # 规则 0: 检查最低数据门槛
    if ch['conversions'] < 50:
        category = 'INSUFFICIENT_DATA'
        action = 'MAINTAIN'
        change_pct = 0.0
    else:
        # 规则 1: 按顺序应用分类规则
        roas_target_pct = (ch['roas'] / TARGET_ROAS) * 100
        cpa_limit_pct = (ch['cpa'] / MAX_CPA) * 100

        # PAUSE - 需要用户陈述连续3周以上负向，暂不触发
        # DECREASE_HEAVY
        if (ch['roas'] < TARGET_ROAS * 0.5 and ch['net_profit'] <= 0) or \
           (ch['cpa'] > MAX_CPA * 1.5 and ch['net_profit'] <= 0) or \
           (ch['roas'] < TARGET_ROAS and cpa_limit_pct > 100 and ch['net_profit'] <= 0):
            category = 'DECREASE_HEAVY'
            action = 'DECREASE_HEAVY'
            change_pct = -0.45
        # INCREASE - 必须满足所有条件
        elif ch['roas'] >= TARGET_ROAS * 1.15 and ch['cpa'] <= MAX_CPA * 0.8 and ch['net_profit'] > 0:
            category = 'INCREASE'
            action = 'INCREASE'
            change_pct = 0.15
        # DECREASE_LIGHT
        elif ch['roas'] < TARGET_ROAS * 0.8 or ch['cpa'] > MAX_CPA * 1.2:
            category = 'DECREASE_LIGHT'
            action = 'DECREASE_LIGHT'
            change_pct = -0.25
        # MAINTAIN
        else:
            category = 'MAINTAIN'
            action = 'MAINTAIN'
            change_pct = 0.0

    classifications.append({
        'channel': ch['channel'],
        'roas': ch['roas'],
        'roas_target_pct': (ch['roas'] / TARGET_ROAS) * 100,
        'cpa': ch['cpa'],
        'cpa_limit_pct': (ch['cpa'] / MAX_CPA) * 100,
        'net_profit': ch['net_profit'],
        'category': category,
        'action': action,
        'change_pct': change_pct,
        'current_budget': ch['spend']
    })

# 打印分类表
print(f"\n{'渠道':<12} {'ROAS':>8} {'目标达成率':>12} {'CPA':>10} {'达到上限率':>14} {'净利润':>14} {'分类结果':<18}")
print("-" * 100)

for c in classifications:
    roas_str = f"{c['roas']:.2f}x"
    roas_pct_str = f"{c['roas_target_pct']:.1f}%"
    cpa_str = f"¥{c['cpa']:.2f}"
    cpa_pct_str = f"{c['cpa_limit_pct']:.1f}%"
    profit_str = f"¥{c['net_profit']:,.0f}"

    print(f"{c['channel']:<12} {roas_str:>8} {roas_pct_str:>12} {cpa_str:>10} {cpa_pct_str:>14} {profit_str:>14} {c['category']:<18}")

print("\n" + "=" * 80)
print("二、预算调整计算步骤")
print("=" * 80)

# 规则 2: 计算预算变更

# 第 1 步: 计算削减额
print("\n【第 1 步】计算削减额")
print("-" * 60)

decrease_channels = [c for c in classifications if c['change_pct'] < 0]
total_freed_budget = 0

for c in decrease_channels:
    decrease_amount = abs(c['current_budget'] * c['change_pct'])
    total_freed_budget += decrease_amount
    print(f"  {c['channel']}: ¥{c['current_budget']:,.2f} × {abs(c['change_pct'])*100:.0f}% = ¥{decrease_amount:,.2f}")

print(f"\n  释放预算总计: ¥{total_freed_budget:,.2f}")

# 第 2 步: 分配给 INCREASE 类别的渠道
print("\n【第 2-3 步】按净利润比例分配给 INCREASE 类别渠道")
print("-" * 60)

increase_channels = [c for c in classifications if c['change_pct'] > 0]

if increase_channels:
    # 计算权重
    total_profit_increase = sum([c['net_profit'] for c in increase_channels])

    for c in increase_channels:
        weight = c['net_profit'] / total_profit_increase if total_profit_increase > 0 else 0
        proposed_increase = total_freed_budget * weight

        # 第 4 步: 应用单渠道上限
        max_increase = c['current_budget'] * PER_CHANNEL_INCREASE_CAP
        final_increase = min(proposed_increase, max_increase)

        c['weight'] = weight
        c['proposed_increase'] = proposed_increase
        c['max_increase'] = max_increase
        c['final_increase'] = final_increase

        print(f"  {c['channel']}:")
        print(f"    权重: {weight*100:.1f}% (净利润 ¥{c['net_profit']:,.0f} / ¥{total_profit_increase:,.0f})")
        print(f"    建议增加额: ¥{proposed_increase:,.2f}")
        print(f"    单渠道上限(15%): ¥{max_increase:,.2f}")
        print(f"    应用上限后: ¥{final_increase:,.2f}")

    # 计算实际分配总额
    total_final_increase = sum([c['final_increase'] for c in increase_channels])

    print(f"\n  所有增加额总和: ¥{total_final_increase:,.2f}")

    # 检查是否超过用户总调配限额
    if total_final_increase > USER_REALLOCATION_LIMIT:
        print(f"\n  ⚠ 超过用户总调配限额 (¥{USER_REALLOCATION_LIMIT:,.2f})，需要缩放")

        scale_factor = USER_REALLOCATION_LIMIT / total_final_increase
        print(f"  缩放因子: {scale_factor:.4f}")

        for c in increase_channels:
            original = c['final_increase']
            c['final_increase'] = c['final_increase'] * scale_factor
            print(f"    {c['channel']}: ¥{original:,.2f} → ¥{c['final_increase']:,.2f}")

        total_final_increase = sum([c['final_increase'] for c in increase_channels])
        print(f"\n  缩放后增加额总和: ¥{total_final_increase:,.2f}")
else:
    total_final_increase = 0
    print("  没有需要增加预算的渠道")

# 第 5 步: 计算未分配结余
unallocated = total_freed_budget - total_final_increase

print("\n【第 5 步】未分配结余")
print("-" * 60)
print(f"  释放预算: ¥{total_freed_budget:,.2f}")
print(f"  已分配增加额: ¥{total_final_increase:,.2f}")
print(f"  可用储备金: ¥{unallocated:,.2f}")

print("\n" + "=" * 80)
print("三、最终调整表")
print("=" * 80)

# 计算最终预算
print(f"\n{'渠道':<12} {'当前预算':>14} {'变更额':>14} {'新预算':>14} {'变更比例':>12} {'分类':<18}")
print("-" * 100)

total_current = 0
total_change = 0
total_new = 0

for c in classifications:
    if c['change_pct'] < 0:
        change = -abs(c['current_budget'] * c['change_pct'])
    elif c['change_pct'] > 0:
        change = c.get('final_increase', 0)
    else:
        change = 0

    new_budget = c['current_budget'] + change
    change_pct_str = f"{change/c['current_budget']*100:+.1f}%"

    total_current += c['current_budget']
    total_change += change
    total_new += new_budget

    print(f"{c['channel']:<12} ¥{c['current_budget']:>12,.2f} ¥{change:>+13,.2f} ¥{new_budget:>12,.2f} {change_pct_str:>12} {c['category']:<18}")

# 添加储备金行
if unallocated > 0:
    print(f"{'储备金':<12} {'-':>14} ¥{unallocated:>+13,.2f} ¥{unallocated:>12,.2f} {'-':>12} {'RESERVE':<18}")
    total_new += unallocated

print("-" * 100)
print(f"{'合计':<12} ¥{total_current:>12,.2f} ¥{total_change:>+13,.2f} ¥{total_new:>12,.2f}")

print("\n" + "=" * 80)
print("四、分类依据说明")
print("=" * 80)

for c in classifications:
    print(f"\n【{c['channel']} - {c['category']}】")
    print(f"  转化次数: {c['current_budget']:.0f} 次 >= 50次 ✓")

    if c['category'] == 'INCREASE':
        print(f"  ✓ ROAS {c['roas']:.2f}x >= {TARGET_ROAS * 1.15:.2f}x (目标的115%)")
        print(f"  ✓ CPA ¥{c['cpa']:.2f} <= ¥{MAX_CPA * 0.8:.2f} (上限的80%)")
        print(f"  ✓ 净利润 ¥{c['net_profit']:,.0f} > 0")
    elif c['category'] == 'DECREASE_HEAVY':
        if c['roas'] < TARGET_ROAS * 0.5:
            print(f"  ✗ ROAS {c['roas']:.2f}x < {TARGET_ROAS * 0.5:.2f}x (目标的50%) 且 净利润 <= 0")
        elif c['cpa'] > MAX_CPA * 1.5:
            print(f"  ✗ CPA ¥{c['cpa']:.2f} > ¥{MAX_CPA * 1.5:.2f} (上限的150%) 且 净利润 <= 0")
        else:
            print(f"  ✗ ROAS < 目标 且 CPA > 上限 且 净利润 <= 0 (三项全败)")
    elif c['category'] == 'DECREASE_LIGHT':
        if c['roas'] < TARGET_ROAS * 0.8:
            print(f"  ✗ ROAS {c['roas']:.2f}x < {TARGET_ROAS * 0.8:.2f}x (目标的80%)")
        else:
            print(f"  ✗ CPA ¥{c['cpa']:.2f} > ¥{MAX_CPA * 1.2:.2f} (上限的120%)")
    elif c['category'] == 'MAINTAIN':
        print(f"  不满足增减条件，维持当前预算")

print("\n" + "=" * 80)
print("五、执行摘要")
print("=" * 80)

decrease_count = len([c for c in classifications if c['change_pct'] < 0])
increase_count = len([c for c in classifications if c['change_pct'] > 0])
maintain_count = len([c for c in classifications if c['change_pct'] == 0])

print(f"\n  需削减预算渠道: {decrease_count} 个")
print(f"  需增加预算渠道: {increase_count} 个")
print(f"  维持预算渠道: {maintain_count} 个")
print(f"\n  预计释放预算: ¥{total_freed_budget:,.2f}")
print(f"  预计增加预算: ¥{total_final_increase:,.2f}")
print(f"  可用储备金: ¥{unallocated:,.2f}")

print("\n" + "=" * 80)
