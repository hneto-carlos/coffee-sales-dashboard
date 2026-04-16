import pandas as pd

# 1. LOAD DATA
df = pd.read_excel('data/raw/coffee_shop_sales.xlsx')

# 2. STANDARDIZE COLUMN NAMES
df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_')

# 3. DATA TYPE CORRECTIONS
# Convert date
df['transaction_date'] = pd.to_datetime(df['transaction_date'])

# Convert time (keep as datetime for flexibility)
df['transaction_time'] = pd.to_datetime(
    df['transaction_time'], format='%H:%M:%S'
)

# 4. CREATE BUSINESS METRICS
# Revenue
df['revenue'] = df['transaction_qty'] * df['unit_price']

# 5. CREATE TIME FEATURES

df['hour'] = df['transaction_time'].dt.hour
df['day'] = df['transaction_date'].dt.day_name()
df['month'] = df['transaction_date'].dt.month_name()

# Numeric versions (for sorting in Power BI)
df['day_num'] = df['transaction_date'].dt.dayofweek
df['month_num'] = df['transaction_date'].dt.month

# 6. SELECT FINAL COLUMNS

df_export = df[[
    'transaction_date',
    'hour',
    'day',
    'day_num',
    'month',
    'month_num',
    'store_location',
    'product_category',
    'product_type',
    'transaction_qty',
    'unit_price',
    'revenue'
]]

# 7. FINAL CLEANING
# Remove missing values if any
df_export = df_export.dropna()

# Ensure correct types
df_export['transaction_qty'] = df_export['transaction_qty'].astype(int)
df_export['unit_price'] = df_export['unit_price'].astype(float)
df_export['revenue'] = df_export['revenue'].astype(float)

# 8. EXPORT CLEAN DATA
df_export.to_csv('data/processed/coffee_sales_clean.csv', index=False)

print("Data cleaned and exported successfully.")