"""
KSGA Mart Malaysia - Sales Performance Analysis (Jan-Jun 2026)

Solves Activities 1-9 of the scenario brief with Matplotlib.
Run:  python src/ksga_mart_dashboard.py          (saves PNGs to outputs/)
      python src/ksga_mart_dashboard.py --show   (also opens the windows)
"""
import argparse
from pathlib import Path

import matplotlib
import matplotlib.pyplot as plt

# ----------------------------------------------------------------- dataset
months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun"]
sales = [120000, 135000, 128000, 150000, 165000, 180000]
expenses = [85000, 90000, 88000, 95000, 98000, 102000]
profit = [35000, 45000, 40000, 55000, 67000, 78000]
customers = [1200, 1320, 1250, 1450, 1580, 1700]
regions = ["Northern", "Central", "Southern", "East Coast", "East Malaysia"]
region_sales = [95000, 180000, 120000, 85000, 110000]

BASE, HIGHLIGHT = "skyblue", "orange"
OUT = Path(__file__).resolve().parent.parent / "outputs"


def save(fig, name):
    OUT.mkdir(exist_ok=True)
    fig.savefig(OUT / name, dpi=200, bbox_inches="tight")


# -------------------------------------------------------- reusable drawers
def draw_monthly_sales_bar(ax):
    top = sales.index(max(sales))
    colors = [HIGHLIGHT if i == top else BASE for i in range(len(sales))]
    bars = ax.bar(months, sales, color=colors)
    for b in bars:
        ax.text(b.get_x() + b.get_width() / 2, b.get_height(),
                f"RM {b.get_height():,.0f}", ha="center", va="bottom", fontsize=8)
    ax.set(title="Monthly Sales", xlabel="Month", ylabel="Sales (RM)")
    ax.set_ylim(0, max(sales) * 1.12)
    ax.grid(axis="y", alpha=0.4)


def draw_sales_trend(ax):
    ax.plot(months, sales, marker="o", linewidth=3, label="Sales")
    for x, y in zip(months, sales):
        ax.text(x, y + 2500, f"{y:,}", ha="center", fontsize=8)
    ax.set(title="Monthly Sales Trend", xlabel="Month", ylabel="Sales (RM)")
    ax.set_ylim(min(sales) * 0.9, max(sales) * 1.1)
    ax.grid(True, alpha=0.4)
    ax.legend()


def draw_regional_barh(ax):
    pairs = sorted(zip(region_sales, regions))  # ascending -> top bar is highest
    vals, names = zip(*pairs)
    colors = [BASE] * (len(vals) - 1) + [HIGHLIGHT]
    bars = ax.barh(names, vals, color=colors)
    for b in bars:
        ax.text(b.get_width() + 1500, b.get_y() + b.get_height() / 2,
                f"RM {b.get_width():,.0f}", va="center", fontsize=8)
    ax.set(title="Regional Sales", xlabel="Sales (RM)")
    ax.set_xlim(0, max(vals) * 1.25)


def draw_region_pie(ax):
    top = region_sales.index(max(region_sales))
    explode = [0.1 if i == top else 0 for i in range(len(regions))]
    ax.pie(region_sales, labels=regions, autopct="%1.1f%%",
           explode=explode, startangle=90)
    ax.set_title("Regional Sales Contribution")


# -------------------------------------------------------------- activities
def activity_1():
    fig, ax = plt.subplots(figsize=(8, 5))
    draw_monthly_sales_bar(ax)
    save(fig, "01_monthly_sales_bar.png")


def activity_2():
    fig, ax = plt.subplots(figsize=(8, 5))
    draw_sales_trend(ax)
    save(fig, "02_sales_trend_line.png")


def activity_3():
    gaps = [s - e for s, e in zip(sales, expenses)]
    i = gaps.index(max(gaps))
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(months, sales, marker="o", color="tab:blue", label="Sales")
    ax.plot(months, expenses, marker="s", color="tab:red", label="Expenses")
    ax.vlines(months[i], expenses[i], sales[i], colors="gray", linestyles="dashed")
    ax.annotate(f"Largest gap: {months[i]}\nRM {gaps[i]:,}",
                xy=(months[i], (sales[i] + expenses[i]) / 2),
                xytext=(months[i - 2], sales[i] * 0.97),
                arrowprops=dict(arrowstyle="->"), ha="center")
    ax.set(title="Sales vs Expenses", xlabel="Month", ylabel="Amount (RM)")
    ax.legend(loc="lower right")
    ax.grid(True, alpha=0.4)
    save(fig, "03_sales_vs_expenses.png")
    print(f"Activity 3 -> largest gap: {months[i]} (RM {gaps[i]:,})")


def activity_4():
    fig, ax = plt.subplots(figsize=(8, 5))
    draw_regional_barh(ax)
    save(fig, "04_regional_sales_barh.png")


def activity_5():
    fig, ax = plt.subplots(figsize=(8, 5))
    bars = ax.bar(months, profit, color="seagreen", label="Profit (bar)")
    ax.plot(months, profit, color="red", marker="o", label="Profit trend")
    for b in bars:
        ax.text(b.get_x() + b.get_width() / 2, b.get_height() + 1000,
                f"{b.get_height():,.0f}", ha="center", fontsize=8)
    ax.set(title="Monthly Profit", ylabel="Profit (RM)")
    ax.set_ylim(0, max(profit) * 1.15)
    ax.grid(axis="y", alpha=0.4)
    ax.legend(loc="upper left")
    save(fig, "05_profit_bar_line.png")


def activity_6():
    growth = [customers[i] - customers[i - 1] for i in range(1, len(customers))]
    best = growth.index(max(growth)) + 1
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(months, customers, marker="o", linewidth=3, label="Customers")
    for x, y in zip(months, customers):
        ax.text(x, y + 15, str(y), ha="center", fontsize=8)
    ax.set(title="Customer Growth", xlabel="Month", ylabel="Customers")
    ax.grid(True, alpha=0.4)
    ax.legend()
    save(fig, "06_customer_growth.png")
    print(f"Activity 6 -> highest customer growth: {months[best]} (+{max(growth)})")


def activity_7():
    fig, ax = plt.subplots(figsize=(7, 7))
    draw_region_pie(ax)
    save(fig, "07_region_pie.png")


def activity_8_9():
    """Dashboard (Activity 8) saved under the filename required by Activity 9."""
    fig, axes = plt.subplots(2, 2, figsize=(14, 9))
    draw_monthly_sales_bar(axes[0, 0])
    draw_sales_trend(axes[0, 1])
    draw_regional_barh(axes[1, 0])
    draw_region_pie(axes[1, 1])
    fig.suptitle("KSGA Mart Malaysia - Sales Dashboard (Jan-Jun 2026)",
                 fontsize=16, fontweight="bold")
    fig.tight_layout()
    save(fig, "ABC_Mart_Dashboard.png")  # filename exactly as the brief asks


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--show", action="store_true", help="display the figures")
    args = parser.parse_args()
    if not args.show:
        matplotlib.use("Agg")
    for fn in (activity_1, activity_2, activity_3, activity_4, activity_5,
               activity_6, activity_7, activity_8_9):
        fn()
    print(f"Charts saved to {OUT}")
    if args.show:
        plt.show()


if __name__ == "__main__":
    main()
