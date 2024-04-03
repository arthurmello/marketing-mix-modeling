import numpy as np
import pandas as pd
import statsmodels.api as sm

# Set seed for reproducibility
np.random.seed(91)

# Define the DAG relationships and generate data
def generate_data(N_SAMPLES):
    # Generate dates (first day of the week) over 3 years
    dates = pd.date_range(start='2021-01-04', periods=N_SAMPLES, freq='W-FRI')

    # Define Black Friday dates for 2021, 2022, and 2023
    black_friday_dates = [
        pd.Timestamp('2021-11-26'),
        pd.Timestamp('2022-11-25'),
        pd.Timestamp('2023-11-24')
    ]
    # Trends
    sales_trend = [20*i + 2000 for i in range(len(dates))]

    # Determine if each date corresponds to Black Friday
    black_friday = np.array([date in black_friday_dates for date in dates], dtype=int)

    # Define spending variables influenced by Black Friday
    adwords_spending = np.random.randint(1000, 5000, N_SAMPLES) + 2000 * black_friday + [i/10 for i in sales_trend]
    facebookads_spending = np.random.randint(800, 4500, N_SAMPLES) + 1500 * black_friday + [i/10 for i in sales_trend]
    awin_spending = np.random.randint(300, 2000, N_SAMPLES) + 1000 * black_friday + [i/10 for i in sales_trend]
    tiktok_spending = np.random.randint(200, 1500, N_SAMPLES) + 800 * black_friday + [i/10 for i in sales_trend]
    snapchat_spending = np.random.randint(300, 2000, N_SAMPLES) + 1000 * black_friday + [i/10 for i in sales_trend]

    consumer_demand = np.random.randint(5000, 15000, N_SAMPLES) + [i/10 for i in sales_trend]

    # Compute seasonal impact on sales based on the month of the year
    seasonal_impact = np.sin(2 * np.pi * dates.month / 12)  # Assuming a yearly seasonality

    # Compute Sales based on relationships and seasonal impact
    sales = (
        2000 +               # Base sales
        2000-30000 * np.exp(-0.005 * adwords_spending) +
        2000-10000 * np.exp(-0.007 * facebookads_spending) +
        2000-40000 * np.exp(-0.005 * awin_spending) +
        2000-20000 * np.exp(-0.003 * tiktok_spending) +
        2000-50000 * np.exp(-0.004 * snapchat_spending) +
        1.2 * consumer_demand +
        30000 * black_friday +
        500 * seasonal_impact +  # Incorporating seasonal impact on sales
        sales_trend + # Trend
        200 * np.random.randn(N_SAMPLES)  # Adding noise
    )

    # Create DataFrame
    data = pd.DataFrame({
        "Date": dates,
        "Sales": sales,
        "adwords_spending": adwords_spending,
        "facebookads_spending": facebookads_spending,
        "awin_spending": awin_spending,
        "tiktok_spending": tiktok_spending,
        "snapchat_spending": snapchat_spending,
        "black_friday": black_friday
    })

    return data

# Number of samples (52 weeks * 3 years)
N_SAMPLES = 52 * 3

# Generate synthetic data
data = generate_data(N_SAMPLES)

## Adding carryover
data = pd.concat([data, data[[col for col in data.columns if "spending" in col]].shift(1).add_suffix("_t_1")], axis=1)
data = pd.concat([data, data[[col for col in data.columns if "spending" in col]].shift(2).add_suffix("_t_2")], axis=1)

carryover = data.apply(lambda row:
  1000-2000*np.exp(-0.002 * row["adwords_spending_t_1"]) +
  1000-2000*np.exp(-0.003 * row["facebookads_spending_t_1"]) +
  1000-2000*np.exp(-0.002 * row["awin_spending_t_1"]) +
  1000-2000*np.exp(-0.001 * row["tiktok_spending_t_1"]) +
  1000-2000*np.exp(-0.003 * row["snapchat_spending_t_1"]) +

  1000-2000*np.exp(-0.001 * row["adwords_spending_t_2"]) +
  1000-2000*np.exp(-0.002 * row["facebookads_spending_t_2"]) +
  1000-2000*np.exp(-0.001 * row["awin_spending_t_2"]) +
  1000-2000*np.exp(-0.001 * row["tiktok_spending_t_2"]) +
  1000-2000*np.exp(-0.002 * row["snapchat_spending_t_2"])
  , axis=1)

data["Sales"] += carryover.fillna(0)

# Adding missing values
for col in data.columns:
  if "_spending" in col:
    data[col] = data[col].sample(frac=0.99)

# Save data to CSV
cols_to_keep = [
    "Date",
    "Sales",
    "adwords_spending",
    "facebookads_spending",
    "awin_spending",
    "tiktok_spending",
    "snapchat_spending"
    ]

# Adding trend
data = pd.concat([data, data[["Sales"]].shift(1).add_suffix("_t_1")], axis=1)
data = pd.concat([data, data[["Sales"]].shift(2).add_suffix("_t_2")], axis=1)
data["Sales"] = data["Sales"] + 0.02*data["Sales_t_1"].fillna(0) + 0.01*data["Sales_t_2"].fillna(0)
data["Sales"] = data["Sales"].round(0)
data[cols_to_keep].to_csv("data.csv", index=False)

# Add constant term
data['constant'] = 1

# Define independent variables
independent_vars = ["adwords_spending", "facebookads_spending", "awin_spending",
                    "tiktok_spending", "snapchat_spending",
                    "black_friday",
                    "constant"
                    ]

# Define dependent variable
dependent_var = "Sales"

# Fit the OLS model
model = sm.OLS(data[dependent_var], sm.add_constant(data[independent_vars].fillna(0)))
fitted_model = model.fit()

# Print results summary
print(fitted_model.summary())

# Display data summary
print(data.describe())
