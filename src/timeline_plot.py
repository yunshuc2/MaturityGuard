import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.ticker as ticker
from datetime import datetime
import pandas as pd
from matplotlib import rcParams
import os

# 设置中文字体
rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'WenQuanYi Zen Hei']
rcParams['axes.unicode_minus'] = False


def plot_timeline(data):
    if not data:
        print("No data provided.")
        return

    # 删除旧图表文件
    if os.path.exists("timeline.png"):
        os.remove("timeline.png")

    # 统一处理日期类型
    for item in data:
        maturity = item['maturity']

        # 处理字符串类型的日期
        if isinstance(maturity, str):
            try:
                maturity = datetime.strptime(maturity, "%Y-%m-%d")
            except ValueError:
                try:
                    maturity = datetime.strptime(maturity, "%m/%d/%Y")
                except ValueError as e:
                    print(f"无法解析日期: {maturity}, 错误: {str(e)}")
                    continue

        # 处理 pandas.Timestamp 类型
        if isinstance(maturity, pd.Timestamp):
            maturity = maturity.to_pydatetime()

        item['maturity'] = maturity

    # 验证数据
    for item in data:
        print(f"Name: {item['name']}, Maturity: {item['maturity']}, Amount: {item['amount']}")

    # 获取日期范围
    min_date = min(item['maturity'] for item in data)
    max_date = max(item['maturity'] for item in data)
    max_amount = max(item['amount'] for item in data)

    plt.figure(figsize=(15, 8))
    ax = plt.gca()

    # 横轴设置
    ax.xaxis.set_major_locator(mdates.MonthLocator(interval=1))
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    plt.xticks(rotation=45)
    ax.set_xlim(min_date, max_date)

    # 纵轴设置
    ax.yaxis.set_major_formatter(ticker.StrMethodFormatter('${x:,.0f}'))
    plt.ylim(0, max_amount * 1.2)

    # 绘制数据点
    for idx, item in enumerate(data):
        plt.plot(
            item['maturity'], item['amount'],
            marker='o', markersize=10,
            label=f"{item['name']} (${item['amount']:,.0f})"
        )
        # 动态调整标注位置
        vertical_offset = 10 + (idx % 3) * 20
        plt.annotate(
            f"{item['maturity'].strftime('%Y-%m-%d')}\n${item['amount']:,.0f}",
            (item['maturity'], item['amount']),
            textcoords="offset points",
            xytext=(0, vertical_offset),
            ha='center',
            fontsize=8
        )

    # 图表美化
    plt.title("投资到期时间轴（横轴为到期日，纵轴为金额）", fontsize=14)
    plt.xlabel("到期日")
    plt.ylabel("金额")
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.tight_layout()

    # 保存并显示
    plt.savefig('timeline.png', dpi=300)
    plt.show()