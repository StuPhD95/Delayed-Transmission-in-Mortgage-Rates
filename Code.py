import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.linear_model import RidgeCV, LinearRegression
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score


# ------------------------------------------------------------
# Plot settings
# ------------------------------------------------------------

plt.rcParams.update({
    "xtick.labelsize": 13,
    "ytick.labelsize": 13,
    "axes.labelsize": 15,
    "axes.titlesize": 17,
    "legend.fontsize": 13
})


# ------------------------------------------------------------
# Settings
# ------------------------------------------------------------

start_date = "2010-01-01"
train_fraction = 0.75
fixed_lags = [1, 2]

os.makedirs("Figures", exist_ok=True)


# ------------------------------------------------------------
# Download real market data from FRED
# ------------------------------------------------------------

fred_base = "https://fred.stlouisfed.org/graph/fredgraph.csv?id="

dgs10 = pd.read_csv(fred_base + "DGS10")
mortgage = pd.read_csv(fred_base + "MORTGAGE30US")

dgs10["observation_date"] = pd.to_datetime(dgs10["observation_date"])
mortgage["observation_date"] = pd.to_datetime(mortgage["observation_date"])

dgs10 = dgs10.rename(columns={
    "observation_date": "Date",
    "DGS10": "Treasury10Y"
})

mortgage = mortgage.rename(columns={
    "observation_date": "Date",
    "MORTGAGE30US": "Mortgage30Y"
})

dgs10["Treasury10Y"] = pd.to_numeric(dgs10["Treasury10Y"], errors="coerce")
mortgage["Mortgage30Y"] = pd.to_numeric(mortgage["Mortgage30Y"], errors="coerce")

dgs10 = dgs10[dgs10["Date"] >= start_date]
mortgage = mortgage[mortgage["Date"] >= start_date]


# ------------------------------------------------------------
# Align daily Treasury yields to weekly mortgage-rate dates
# ------------------------------------------------------------

data = pd.merge_asof(
    mortgage.sort_values("Date"),
    dgs10.sort_values("Date"),
    on="Date",
    direction="backward"
)

data = data.dropna().reset_index(drop=True)


# ------------------------------------------------------------
# Use weekly changes
# ------------------------------------------------------------

data["dMortgage30Y"] = data["Mortgage30Y"].diff()
data["dTreasury10Y"] = data["Treasury10Y"].diff()

dw = data.dropna().copy().reset_index(drop=True)


# ------------------------------------------------------------
# Build datasets
# ------------------------------------------------------------

def make_non_delayed_dataset(dw):
    df = pd.DataFrame({
        "dMortgage30Y": dw["dMortgage30Y"],
        "dTreasury10Y_t": dw["dTreasury10Y"]
    }).dropna()

    X = df[["dTreasury10Y_t"]]
    y = df["dMortgage30Y"]

    return df, X, y


def make_delayed_dataset(dw, fixed_lags):
    df = pd.DataFrame({
        "dMortgage30Y": dw["dMortgage30Y"],
        "dTreasury10Y_t": dw["dTreasury10Y"]
    })

    for lag in fixed_lags:
        df[f"dTreasury10Y_t_minus_{lag}"] = dw["dTreasury10Y"].shift(lag)

    df = df.dropna()

    predictors = ["dTreasury10Y_t"] + [
        f"dTreasury10Y_t_minus_{lag}" for lag in fixed_lags
    ]

    X = df[predictors]
    y = df["dMortgage30Y"]

    return df, X, y


def time_train_test_split(X, y, train_fraction):
    split = int(train_fraction * len(X))

    X_train = X.iloc[:split]
    X_test = X.iloc[split:]
    y_train = y.iloc[:split]
    y_test = y.iloc[split:]

    return X_train, X_test, y_train, y_test


def evaluate_model(model, X_train, X_test, y_train, y_test):
    model.fit(X_train, y_train)

    pred_train = model.predict(X_train)
    pred_test = model.predict(X_test)

    return {
        "train_R2": r2_score(y_train, pred_train),
        "test_R2": r2_score(y_test, pred_test),
        "test_RMSE": np.sqrt(mean_squared_error(y_test, pred_test)),
        "test_MAE": mean_absolute_error(y_test, pred_test)
    }, pred_train, pred_test


# ------------------------------------------------------------
# Non-delayed benchmark
# ------------------------------------------------------------

df_non, X_non, y_non = make_non_delayed_dataset(dw)

X_non_train, X_non_test, y_non_train, y_non_test = time_train_test_split(
    X_non,
    y_non,
    train_fraction
)

non_delayed_model = LinearRegression()

non_delayed_metrics, non_delayed_pred_train, non_delayed_pred_test = evaluate_model(
    non_delayed_model,
    X_non_train,
    X_non_test,
    y_non_train,
    y_non_test
)


# ------------------------------------------------------------
# Delayed model
# ------------------------------------------------------------

df_delay, X_delay, y_delay = make_delayed_dataset(dw, fixed_lags)

X_delay_train, X_delay_test, y_delay_train, y_delay_test = time_train_test_split(
    X_delay,
    y_delay,
    train_fraction
)

delayed_model = RidgeCV(alphas=np.logspace(-6, 2, 50))

delayed_metrics, delayed_pred_train, delayed_pred_test = evaluate_model(
    delayed_model,
    X_delay_train,
    X_delay_test,
    y_delay_train,
    y_delay_test
)


# ------------------------------------------------------------
# Results table
# ------------------------------------------------------------

results = pd.DataFrame([
    {
        "Model": "Non-delayed benchmark",
        "Predictors": "dTreasury10Y_t",
        **non_delayed_metrics
    },
    {
        "Model": "Delayed model",
        "Predictors": "dTreasury10Y_t, dTreasury10Y_{t-1}, dTreasury10Y_{t-2}",
        **delayed_metrics
    }
])

baseline_rmse = results.loc[
    results["Model"] == "Non-delayed benchmark",
    "test_RMSE"
].iloc[0]

results["RMSE_improvement_vs_non_delayed_%"] = (
    100 * (baseline_rmse - results["test_RMSE"]) / baseline_rmse
)

coef_table = pd.DataFrame({
    "Predictor": X_delay.columns,
    "Coefficient": delayed_model.coef_
})

print("\nModel comparison:")
print(results.round(6))

print("\nDelayed model coefficients:")
print(coef_table.round(6))

print(f"\nRidge alpha selected: {delayed_model.alpha_:.6f}")

improvement = results.loc[
    results["Model"] == "Delayed model",
    "RMSE_improvement_vs_non_delayed_%"
].iloc[0]

print("\nREADME-ready result:")
if improvement > 0:
    print(
        f"The delayed model reduces out-of-sample RMSE by "
        f"{improvement:.2f}% relative to the non-delayed benchmark."
    )
else:
    print(
        f"The delayed model does not improve the non-delayed benchmark. "
        f"Out-of-sample RMSE changes by {improvement:.2f}%."
    )

results.to_csv("Mortgage_Delay_Model_Results.csv", index=False)
coef_table.to_csv("Mortgage_Delayed_Model_Coefficients.csv", index=False)


# ------------------------------------------------------------
# Plot 1: Rate levels
# ------------------------------------------------------------

fig, ax = plt.subplots(figsize=(12, 6))

ax.plot(data["Date"], data["Treasury10Y"], label="10-year Treasury yield")
ax.plot(data["Date"], data["Mortgage30Y"], label="30-year fixed mortgage rate")

ax.set_title("10-Year Treasury Yield and 30-Year Fixed Mortgage Rate")
ax.set_xlabel("Date", labelpad=12)
ax.set_ylabel("Rate (%)", labelpad=12)
ax.legend()

plt.tight_layout()
plt.savefig("Figures/Mortgage_Treasury_Levels.png", dpi=300, bbox_inches="tight")
plt.show()


# ------------------------------------------------------------
# Plot 2: Weekly changes
# ------------------------------------------------------------

fig, ax = plt.subplots(figsize=(12, 6))

ax.plot(
    dw.index,
    dw["dTreasury10Y"],
    label="Weekly change in 10Y Treasury yield",
    alpha=0.8
)

ax.plot(
    dw.index,
    dw["dMortgage30Y"],
    label="Weekly change in 30Y mortgage rate",
    alpha=0.8
)

ax.set_title("Weekly Changes in Treasury Yields and Mortgage Rates")
ax.set_xlabel("Observation", labelpad=12)
ax.set_ylabel("Weekly change, percentage points", labelpad=12)
ax.legend()

plt.tight_layout()
plt.savefig("Figures/Mortgage_Treasury_Weekly_Changes.png", dpi=300, bbox_inches="tight")
plt.show()


# ------------------------------------------------------------
# Plot 3: Out-of-sample RMSE comparison
# ------------------------------------------------------------

fig, ax = plt.subplots(figsize=(9, 6))

ax.bar(results["Model"], results["test_RMSE"])

ax.set_title("Out-of-Sample RMSE: Non-Delayed vs Delayed Model")
ax.set_xlabel("Model", labelpad=12)
ax.set_ylabel("Test RMSE", labelpad=12)

for i, value in enumerate(results["test_RMSE"]):
    ax.text(i, value + 0.002, f"{value:.4f}", ha="center")

plt.tight_layout()
plt.savefig("Figures/Mortgage_Delay_RMSE_Comparison.png", dpi=300, bbox_inches="tight")
plt.show()


# ------------------------------------------------------------
# Plot 4: RMSE improvement
# ------------------------------------------------------------

fig, ax = plt.subplots(figsize=(9, 6))

ax.bar(results["Model"], results["RMSE_improvement_vs_non_delayed_%"])
ax.axhline(0, linewidth=1)

ax.set_title("RMSE Improvement Relative to Non-Delayed Benchmark")
ax.set_xlabel("Model", labelpad=12)
ax.set_ylabel("RMSE improvement (%)", labelpad=12)

for i, value in enumerate(results["RMSE_improvement_vs_non_delayed_%"]):
    offset = 0.7 if value >= 0 else -1.5
    ax.text(i, value + offset, f"{value:.2f}%", ha="center")

plt.tight_layout()
plt.savefig("Figures/Mortgage_Delay_RMSE_Improvement.png", dpi=300, bbox_inches="tight")
plt.show()


# ------------------------------------------------------------
# Plot 5: Delayed model coefficients
# ------------------------------------------------------------

fig, ax = plt.subplots(figsize=(10, 6))

ax.bar(coef_table["Predictor"], coef_table["Coefficient"])
ax.axhline(0, linewidth=1)

ax.set_title("Estimated Delayed Model Coefficients")
ax.set_xlabel("Predictor", labelpad=12)
ax.set_ylabel("Coefficient", labelpad=12)

plt.xticks(rotation=25, ha="right")

plt.tight_layout()
plt.savefig("Figures/Mortgage_Delayed_Model_Coefficients.png", dpi=300, bbox_inches="tight")
plt.show()


# ------------------------------------------------------------
# Plot 6: Actual vs predicted mortgage-rate changes
# ------------------------------------------------------------

fig, ax = plt.subplots(figsize=(12, 6))

ax.plot(
    y_delay_test.index,
    y_delay_test,
    label="Actual mortgage-rate change",
    alpha=0.8
)

ax.plot(
    y_delay_test.index,
    delayed_pred_test,
    label="Predicted by delayed model",
    alpha=0.8
)

ax.set_title("Actual vs Predicted Mortgage-Rate Changes")
ax.set_xlabel("Test-sample observation", labelpad=12)
ax.set_ylabel("Weekly mortgage-rate change, percentage points", labelpad=12)
ax.legend()

plt.tight_layout()
plt.savefig("Figures/Mortgage_Actual_vs_Predicted_Delayed_Model.png", dpi=300, bbox_inches="tight")
plt.show()