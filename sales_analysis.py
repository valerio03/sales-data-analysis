import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime, timedelta

# Generate sample sales data
np.random.seed(42)
dates = pd.date_range(start='2023-01-01', end='2023-12-31', freq='D')
products = ['Laptop', 'Smartphone', 'Tablet', 'Headphones', 'Smartwatch', 
            'Camera', 'Speaker', 'Monitor', 'Keyboard', 'Mouse']
regions = ['North', 'South', 'East', 'West', 'Central']

data = []
for date in dates:
    for _ in range(np.random.randint(5, 15)):
        product = np.random.choice(products)
        region = np.random.choice(regions)
        quantity = np.random.randint(1, 10)
        
        # Price varies by product
        price_map = {
            'Laptop': 899, 'Smartphone': 699, 'Tablet': 399,
            'Headphones': 149, 'Smartwatch': 299, 'Camera': 799,
            'Speaker': 199, 'Monitor': 349, 'Keyboard': 79, 'Mouse': 49
        }
        price = price_map[product]
        revenue = quantity * price
        
        data.append({
            'Date': date,
            'Product': product,
            'Region': region,
            'Quantity': quantity,
            'Price': price,
            'Revenue': revenue
        })

df = pd.DataFrame(data)

# Add month column for aggregation
df['Month'] = df['Date'].dt.to_period('M')

print("Sales Data Analysis")
print("=" * 60)
print(f"\nDataset Overview:")
print(f"Total Records: {len(df)}")
print(f"Date Range: {df['Date'].min()} to {df['Date'].max()}")
print(f"Total Revenue: ${df['Revenue'].sum():,.2f}")
print("\nFirst few records:")
print(df.head(10))

# 1. Monthly Sales Trend Analysis
monthly_sales = df.groupby('Month')['Revenue'].sum().reset_index()
monthly_sales['Month'] = monthly_sales['Month'].astype(str)

plt.figure(figsize=(14, 5))

plt.subplot(1, 3, 1)
plt.plot(monthly_sales['Month'], monthly_sales['Revenue'], 
         marker='o', linewidth=2, markersize=8, color='#2E86AB')
plt.xlabel('Month', fontsize=11, fontweight='bold')
plt.ylabel('Revenue ($)', fontsize=11, fontweight='bold')
plt.title('Monthly Sales Trend', fontsize=13, fontweight='bold', pad=15)
plt.xticks(rotation=45, ha='right')
plt.grid(True, alpha=0.3, linestyle='--')
plt.ticklabel_format(style='plain', axis='y')
plt.tight_layout()

# 2. Top-Selling Products by Revenue
product_sales = df.groupby('Product')['Revenue'].sum().sort_values(ascending=False)

plt.subplot(1, 3, 2)
colors = plt.cm.viridis(np.linspace(0.3, 0.9, len(product_sales)))
bars = plt.barh(product_sales.index, product_sales.values, color=colors)
plt.xlabel('Revenue ($)', fontsize=11, fontweight='bold')
plt.ylabel('Product', fontsize=11, fontweight='bold')
plt.title('Top-Selling Products', fontsize=13, fontweight='bold', pad=15)
plt.ticklabel_format(style='plain', axis='x')
plt.grid(True, alpha=0.3, axis='x', linestyle='--')
plt.tight_layout()

# Add value labels
for i, bar in enumerate(bars):
    width = bar.get_width()
    plt.text(width, bar.get_y() + bar.get_height()/2, 
             f'${width:,.0f}', ha='left', va='center', 
             fontsize=9, fontweight='bold')

# 3. Regional Sales Performance
regional_sales = df.groupby('Region')['Revenue'].sum().sort_values(ascending=False)

plt.subplot(1, 3, 3)
colors = plt.cm.plasma(np.linspace(0.3, 0.9, len(regional_sales)))
bars = plt.bar(regional_sales.index, regional_sales.values, color=colors, width=0.6)
plt.xlabel('Region', fontsize=11, fontweight='bold')
plt.ylabel('Revenue ($)', fontsize=11, fontweight='bold')
plt.title('Regional Sales Performance', fontsize=13, fontweight='bold', pad=15)
plt.ticklabel_format(style='plain', axis='y')
plt.grid(True, alpha=0.3, axis='y', linestyle='--')
plt.tight_layout()

# Add value labels on bars
for bar in bars:
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2., height,
             f'${height:,.0f}', ha='center', va='bottom', 
             fontsize=9, fontweight='bold')

plt.tight_layout()
plt.savefig('sales_analysis_dashboard.png', dpi=300, bbox_inches='tight')
print("\n" + "=" * 60)
print("Visualizations saved as 'sales_analysis_dashboard.png'")
print("=" * 60)
plt.show()

# Print Summary Statistics
print("\n" + "=" * 60)
print("SALES ANALYSIS SUMMARY")
print("=" * 60)

print("\nTop 3 Products by Revenue:")
for i, (product, revenue) in enumerate(product_sales.head(3).items(), 1):
    print(f"{i}. {product}: ${revenue:,.2f}")

print("\nTop 3 Regions by Revenue:")
for i, (region, revenue) in enumerate(regional_sales.head(3).items(), 1):
    print(f"{i}. {region}: ${revenue:,.2f}")

print("\nMonthly Statistics:")
print(f"Average Monthly Revenue: ${monthly_sales['Revenue'].mean():,.2f}")
print(f"Best Month: {monthly_sales.loc[monthly_sales['Revenue'].idxmax(), 'Month']} "
      f"(${monthly_sales['Revenue'].max():,.2f})")
print(f"Worst Month: {monthly_sales.loc[monthly_sales['Revenue'].idxmin(), 'Month']} "
      f"(${monthly_sales['Revenue'].min():,.2f})")

print("\n" + "=" * 60)
print("Analysis Complete!")
print("=" * 60)