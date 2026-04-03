import pandas as pd
import matplotlib.pyplot as plt

# -------------------------------
# STEP 1: LOAD DATA
# -------------------------------
sales_df = pd.read_csv("sales_data.csv", encoding="latin1")
customer_df = pd.read_csv("customer_data.csv", encoding="latin1")

# Clean columns
sales_df.columns = sales_df.columns.str.strip().str.upper()
customer_df.columns = customer_df.columns.str.strip().str.upper()

print("\nSales Columns:", sales_df.columns)
print("Customer Columns:", customer_df.columns)

# -------------------------------
# STEP 2: DATA CLEANING
# -------------------------------
sales_df.fillna(sales_df.mean(numeric_only=True), inplace=True)
sales_df.fillna(sales_df.mode().iloc[0], inplace=True)

customer_df.fillna(customer_df.mode().iloc[0], inplace=True)

sales_df.drop_duplicates(inplace=True)
customer_df.drop_duplicates(inplace=True)

# -------------------------------
# STEP 3: DATE PROCESSING
# -------------------------------
sales_df["DATE"] = pd.to_datetime(sales_df["DATE"])

sales_df["YEAR"] = sales_df["DATE"].dt.year
sales_df["MONTH"] = sales_df["DATE"].dt.month
sales_df["DAY"] = sales_df["DATE"].dt.day

# -------------------------------
# STEP 4: MONTHLY SALES
# -------------------------------
monthly_sales = sales_df.groupby("MONTH")["TOTAL_SALES"].sum()
print("\nMonthly Sales:\n", monthly_sales)

# -------------------------------
# STEP 5: FILTERING (MULTIPLE CONDITIONS)
# -------------------------------
filtered_data = sales_df[
    (sales_df["TOTAL_SALES"] > 500) &
    (sales_df["REGION"] == "North")
]

print("\nFiltered Data:\n", filtered_data.head())

# -------------------------------
# STEP 6: STRING OPERATIONS
# -------------------------------
sales_df["PRODUCT"] = sales_df["PRODUCT"].str.upper()

# -------------------------------
# STEP 7: MERGE DATASETS
# -------------------------------
merged_df = pd.merge(sales_df, customer_df, on="CUSTOMER_ID", how="inner")

print("\nMerged Data:\n", merged_df.head())

# -------------------------------
# STEP 8: CUSTOMER ANALYSIS
# -------------------------------
customer_sales = merged_df.groupby("CUSTOMER_ID")["TOTAL_SALES"].sum()

top_customer = customer_sales.idxmax()
top_value = customer_sales.max()

print("\nTop Customer:", top_customer, "Sales:", top_value)

# -------------------------------
# STEP 9: PIVOT TABLE
# -------------------------------
pivot_table = pd.pivot_table(
    merged_df,
    values="TOTAL_SALES",
    index="REGION",
    columns="PRODUCT",
    aggfunc="sum"
)

print("\nPivot Table:\n", pivot_table)

# -------------------------------
# STEP 10: VISUALIZATION
# -------------------------------

# Monthly Sales Trend
monthly_sales.plot(kind="line", marker="o")
plt.title("Monthly Sales Trend")
plt.xlabel("Month")
plt.ylabel("Sales")
plt.show()

# Top 5 Customers
customer_sales.sort_values(ascending=False).head(5).plot(kind="bar")
plt.title("Top 5 Customers")
plt.show()

# -------------------------------
# STEP 11: FINAL REPORT
# -------------------------------
print("\n===== CUSTOMER SALES REPORT =====")
print(f"Total Revenue: {sales_df['TOTAL_SALES'].sum():.2f}")
print(f"Total Customers: {merged_df['CUSTOMER_ID'].nunique()}")
print(f"Top Customer: {top_customer} - {top_value:.2f}")