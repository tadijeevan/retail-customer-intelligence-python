from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.metrics import mean_absolute_error, mean_squared_error

ROOT = Path(__file__).resolve().parent.parent
REPORTS = ROOT / "reports"
FIGURES = REPORTS / "figures"
INPUT = REPORTS / "monthly_sales.csv"
INCOMPLETE_MONTH = "2011-12"


def load_monthly_sales():
    if not INPUT.exists():
        raise FileNotFoundError(f"Missing input: {INPUT}")

    df = pd.read_csv(INPUT)
    required = {"month", "sales_value"}
    missing = required.difference(df.columns)

    if missing:
        raise ValueError(f"Missing columns: {sorted(missing)}")

    df["month"] = pd.to_datetime(
        df["month"], format="%Y-%m", errors="raise"
    )
    df["sales_value"] = pd.to_numeric(
        df["sales_value"], errors="raise"
    )

    if df[["month", "sales_value"]].isna().any().any():
        raise ValueError("Missing dates or sales values.")

    if df["month"].duplicated().any():
        raise ValueError("Duplicate months found.")

    df = df.sort_values("month").reset_index(drop=True)
    incomplete = pd.Period(INCOMPLETE_MONTH, freq="M")
    df = df[df["month"].dt.to_period("M") != incomplete].copy()
    df = df.reset_index(drop=True)

    if len(df) < 5:
        raise ValueError("Not enough complete months for evaluation.")

    return df


def generate_forecasts(df):
    results = []

    # Start with four training months; predict each next month.
    for i in range(4, len(df)):
        history = df.iloc[:i]

        results.append({
            "month": df.iloc[i]["month"].strftime("%Y-%m"),
            "actual_sales": float(df.iloc[i]["sales_value"]),
            "previous_month_baseline": float(
                history.iloc[-1]["sales_value"]
            ),
            "three_month_moving_average": float(
                history["sales_value"].tail(3).mean()
            ),
            "training_months": len(history),
        })

    predictions = pd.DataFrame(results)

    if predictions.empty:
        raise ValueError("No predictions generated.")

    return predictions


def evaluate_forecasts(predictions):
    actual = predictions["actual_sales"].to_numpy()
    models = {
        "Previous-month baseline": "previous_month_baseline",
        "Three-month moving average": "three_month_moving_average",
    }

    rows = []
    for name, column in models.items():
        predicted = predictions[column].to_numpy()
        rows.append({
            "model": name,
            "evaluation_months": len(actual),
            "mae": mean_absolute_error(actual, predicted),
            "rmse": np.sqrt(mean_squared_error(actual, predicted)),
        })

    return pd.DataFrame(rows).sort_values("mae").reset_index(drop=True)


def main():
    REPORTS.mkdir(parents=True, exist_ok=True)
    FIGURES.mkdir(parents=True, exist_ok=True)

    sales = load_monthly_sales()
    predictions = generate_forecasts(sales)
    metrics = evaluate_forecasts(predictions)

    predictions.to_csv(REPORTS / "forecast_predictions.csv", index=False)
    metrics.to_csv(
        REPORTS / "forecast_model_evaluation.csv", index=False
    )

    months = pd.to_datetime(predictions["month"])
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(months, predictions["actual_sales"],
            marker="o", label="Actual sales")
    ax.plot(months, predictions["previous_month_baseline"],
            marker="o", linestyle="--", label="Previous-month baseline")
    ax.plot(months, predictions["three_month_moving_average"],
            marker="o", linestyle="--", label="Three-month moving average")
    ax.set_title("Monthly Sales Forecast Evaluation")
    ax.set_xlabel("Month")
    ax.set_ylabel("Sales value (£)")
    ax.grid(axis="y", alpha=0.3)
    ax.legend()
    fig.autofmt_xdate()
    fig.tight_layout()
    fig.savefig(FIGURES / "forecast_evaluation.png",
                dpi=150, bbox_inches="tight")
    plt.close(fig)

    print("COMPLETE MONTHS:", len(sales))
    print("EVALUATION PERIOD:",
          sales["month"].min().strftime("%Y-%m"), "to",
          sales["month"].max().strftime("%Y-%m"))
    print("\nMODEL EVALUATION")
    print(metrics.round(2).to_string(index=False))
    print("\nSaved reports/forecast_predictions.csv")
    print("Saved reports/forecast_model_evaluation.csv")
    print("Saved reports/figures/forecast_evaluation.png")
    print("\nNote: This is a small-sample baseline comparison, not a reliable "
          "long-term or seasonal forecast.")


if __name__ == "__main__":
    main()
