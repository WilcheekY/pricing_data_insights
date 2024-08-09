import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

#! python3
# README.md - Corrects pricing in produce bestseller spreadsheet.
csv_price = pd.read_csv('myntra_products_catalog.csv', encoding='unicode_escape')
csv_price = csv_price.rename(columns={'Price':'INR_Price'})
csv_price['MYR_Price'] = [round (x*0.0528) for x in csv_price['INR_Price']]
csv_price.insert(5, 'MYR_Price', csv_price.pop('MYR_Price')) 

bestseller_csv_price = csv_price.to_excel('Bestseller_.xlsx', index=False)
priceCatcher = pd.read_excel('./Bestseller_.xlsx')
priceCatcher.Price.describe()

# Remove price ranges for outlier
priceCatcher.loc[(priceCatcher.INR_price < 500) & (priceCatcher.INR_price > 200)]
print('Price:',sorted(priceCatcher.INR_price.unique()))
priceCatcher.loc[(priceCatcher.MYR_price < 50) & (priceCatcher.INR_price > 20)]
print('Price:',sorted(priceCatcher.MYR_price.unique()))

# Define price ranges for grouping
price_bins = [0, 500, 1000, 1500, 2000, 3000, 5000, 10000, 20000, 30000, 50000, float('inf')]
price_labels = ['<500', '500-1000', '1000-1500', '1500-2000', '2000-3000', '3000-5000', '5000-10000',
                '10000-20000', '20000-30000', '30000-50000', '>50000']

# Bin the 'Price (INR)' data
df['PriceRange'] = pd.cut(df['Price'], bins=price_bins, labels=price_labels, right=False)

# Count the number of products in each price range
price_range_counts = df['PriceRange'].value_counts().sort_index()

# Plotting the data
plt.figure(figsize=(12, 6))
price_range_counts.plot(kind='line', marker='o')

plt.title('Number of Products in Each Price Range')
plt.xlabel('Price Range')
plt.ylabel('Number of Products')
plt.xticks(range(len(price_labels)), price_labels, rotation=45)
plt.tight_layout()
plt.grid()

plt.show()

# Brand popularity analysis
top_brands = df['ProductBrand'].value_counts().head(30).index
brand_counts = df['ProductBrand'].value_counts().head(30)

# Calculate average price for each of the top 20 brands
avg_prices = df[df['ProductBrand'].isin(top_brands)].groupby('ProductBrand')['Price_(INR)'].mean().reindex(top_brands)

# Plotting the data
fig, ax1 = plt.subplots(figsize=(12, 8))

# Bar graph for number of products
color="skyblue"
ax1.set_xlabel('Brand')
ax1.set_ylabel('Number of Products', color='#19aade')
ax1.bar(brand_counts.index, brand_counts.values, color=color)
ax1.tick_params(axis='y', labelcolor='#19aade')
ax1.set_xticks(range(len(brand_counts.index)))
ax1.set_xticklabels(brand_counts.index, rotation=45, ha='right')

# Line graph for average price
ax2 = ax1.twinx()
color = '#142459'
ax2.set_ylabel('Average Price (INR)', color='#213B91')
ax2.plot(avg_prices.index, avg_prices.values, color=color, marker='o')
ax2.tick_params(axis='y', labelcolor='#213B91')

# Title and layout
plt.title('Top 20 Brands by Popularity')
fig.tight_layout()

# Show the plot
plt.show()
