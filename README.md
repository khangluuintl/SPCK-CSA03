# E-commerce Sales Analytics

A Streamlit multipage app for exploring the e-commerce sales dataset and
predicting order revenue with linear regression.

## Run the app

From this directory, install the dependencies and start Streamlit:

```powershell
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

The app uses `ecommerce_sales_analytics_5000.csv` from this directory. The
sidebar links to sales analysis, order entry, and revenue prediction.

## Model

The linear regression model predicts `revenue` using `gross_sales` and
`discount_amount`, derived from quantity, unit price, and discount. It reports
MAE, RMSE, and R-squared on a reproducible 80/20 train-test split.
