"""
Practice charts built from the CSV files in /data using pandas + Matplotlib.
Run:  python src/csv_visualizations.py
"""
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
DATA, OUT = ROOT / "data", ROOT / "outputs"
OUT.mkdir(exist_ok=True)


def monthly_sales():
    df = pd.read_csv(DATA / "sales_data.csv")
    fig, ax = plt.subplots(figsize=(7, 4.5))
    ax.plot(df["Month"], df["Sales"], marker="o", linewidth=2.5)
    for x, y in zip(df["Month"], df["Sales"]):
        ax.text(x, y + 400, f"{y:,}", ha="center", fontsize=8)
    ax.set(title="Monthly Sales (sales_data.csv)", xlabel="Month", ylabel="Sales")
    ax.grid(True, alpha=0.4)
    fig.savefig(OUT / "csv_monthly_sales.png", dpi=200, bbox_inches="tight")


def product_sales():
    df = pd.read_csv(DATA / "product_sales.csv").sort_values("Sales", ascending=False)
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4.5))
    bars = ax1.bar(df["Category"], df["Sales"],
                   color=["orange"] + ["skyblue"] * (len(df) - 1))
    for b in bars:
        ax1.text(b.get_x() + b.get_width() / 2, b.get_height(),
                 f"{b.get_height():,.0f}", ha="center", va="bottom", fontsize=8)
    ax1.set(title="Sales by Product Category", ylabel="Sales")
    ax1.grid(axis="y", alpha=0.4)
    ax2.pie(df["Sales"], labels=df["Category"], autopct="%1.1f%%", startangle=90,
            explode=[0.08] + [0] * (len(df) - 1))
    ax2.set_title("Category Share")
    fig.tight_layout()
    fig.savefig(OUT / "csv_product_sales.png", dpi=200, bbox_inches="tight")


def employee_salary():
    df = pd.read_csv(DATA / "employee_salary.csv")
    avg = df["Salary"].mean()
    fig, ax = plt.subplots(figsize=(7, 4.5))
    bars = ax.bar(df["Employee"], df["Salary"], color="seagreen")
    for b in bars:
        ax.text(b.get_x() + b.get_width() / 2, b.get_height(),
                f"{b.get_height():,.0f}", ha="center", va="bottom", fontsize=8)
    ax.axhline(avg, color="red", linestyle="--", label=f"Average: {avg:,.0f}")
    ax.set(title="Employee Salary", xlabel="Employee", ylabel="Salary")
    ax.legend(loc="upper left")
    ax.grid(axis="y", alpha=0.4)
    fig.savefig(OUT / "csv_employee_salary.png", dpi=200, bbox_inches="tight")


if __name__ == "__main__":
    monthly_sales()
    product_sales()
    employee_salary()
    print(f"Charts saved to {OUT}")
