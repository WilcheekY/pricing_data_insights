import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

priceCatcher = pd.read_csv('./Bestseller_.csv')
priceCatcher.Price.describe()

# Remove price ranges for outlier
priceCatcher = priceCatcher.rename(columns={'Price':'INR_price'})
print('Price:',sorted(priceCatcher.INR_price.unique()))
priceCatcher.loc[(priceCatcher.INR_price < 500) & (priceCatcher.INR_price > 200)]
priceCatcher = priceCatcher.rename(columns={'INR_Price':'MYR_price'})
priceCatcher['Price'] = priceCatcher.MYR_Price['Price'] * 0.0535
print('Price:',sorted(priceCatcher.MYR_price.unique()))
priceCatcher.loc[(priceCatcher.MYR_price < 10) & (priceCatcher.INR_price > 5)]

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