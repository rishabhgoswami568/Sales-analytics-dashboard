# Sales Analytics & Business Intelligence Dashboard

An interactive dashboard for exploring retail sales performance using Streamlit, pandas, and Plotly.

## Features
- Revenue, profit, order, units-sold, and profit-margin KPIs
- Date, region, and category filters
- Monthly revenue/profit trends
- Category and region comparisons
- Top products by revenue
- Automatically generated basic business insights
- Download filtered records as CSV

## Run locally
1. Install Python 3.10 or newer.
2. Open a terminal in this folder.
3. Create and activate a virtual environment (optional but recommended).
4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
5. Start the app:
   ```bash
   streamlit run app.py
   ```
6. Open the local URL printed by Streamlit.

## Data
`data/sales_data.csv` is a small synthetic sample dataset created for demonstration. Replace it with authorized business data that uses the same columns.

Columns: `order_id`, `order_date`, `region`, `category`, `product`, `quantity`, `unit_price`, `unit_cost`.

## Metrics
- Revenue = quantity × unit price
- Profit = revenue − (quantity × unit cost)
- Profit margin = total profit ÷ total revenue × 100

## Portfolio note
Describe this as a demo using synthetic data unless you replace the dataset with verified real-world data. Do not claim business impact that you have not measured.
