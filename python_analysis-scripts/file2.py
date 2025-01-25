# Importing libraries
import pandas as pd

# Loading the data
brands = pd.read_csv("brands.csv") 
finance = pd.read_csv("finance.csv")
info = pd.read_csv("info.csv")
reviews = pd.read_csv("reviews.csv")

# Merge the data and drop null values
merged_df = info.merge(finance, on="product_id")
merged_df = merged_df.merge(reviews, on="product_id")
merged_df = merged_df.merge(brands, on="product_id")
merged_df.dropna(inplace=True)

# Add price labels based on listing_price quartiles
merged_df["price_label"] = pd.qcut(merged_df["listing_price"], q=4, labels=["Budget", "Average", "Expensive", "Elite"])
# Alternatively, avoiding pd.qcut(), get the individual quantiles and use pd.cut()
# twenty_fifth = merged_df["listing_price"].quantile(0.25)
# median = merged_df["listing_price"].quantile(0.5)
# seventy_fifth = merged_df["listing_price"].quantile(0.75) 
# maximum = merged_df["listing_price"].max()
# merged_df["price_label"] = pd.cut(merged_df["listing_price"], bins=[0, twenty_fifth, median, seventy_fifth, maximum], labels=["Budget", "Average", "Expensive", "Elite"], include_lowest=True)

# Group by brand and price_label to get volume and mean revenue
adidas_vs_nike = merged_df.groupby(["brand", "price_label"], as_index=False).agg(
    num_products=("price_label", "count"), 
    mean_revenue=("revenue", "mean")
).round(2)

print(adidas_vs_nike)

# Store the length of each description
merged_df["description_length"] = merged_df["description"].str.len()

# Upper description length limits
lengthes = [0, 100, 200, 300, 400, 500, 600, 700]

# Description length labels
labels = ["100", "200", "300", "400", "500", "600", "700"]

# Cut into bins
merged_df["description_length"] = pd.cut(merged_df["description_length"], bins=lengthes, labels=labels)

# Group by the bins
description_lengths = merged_df.groupby("description_length", as_index=False).agg(
    mean_rating=("rating", "mean"), 
    total_reviews=("reviews", "sum")
).round(2)

print(description_lengths)
