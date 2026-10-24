import pandas as pd
import plotly.express as px
from sklearn.model_selection import train_test_split

from config import Config


class EcommerceDataset:
    REQUIRED_COLUMNS = {
        "order_date",
        "product_category",
        "region",
        "quantity",
        "unit_price",
        "discount",
        "payment_method",
        "delivery_days",
        "customer_rating",
        "revenue",
    }

    def __init__(self, datapath=Config.DATA_PATH):
        self.datapath = datapath
        self.df = pd.read_csv(datapath)
        missing_columns = self.REQUIRED_COLUMNS.difference(self.df.columns)
        if missing_columns:
            missing = ", ".join(sorted(missing_columns))
            raise ValueError(f"Dataset is missing required columns: {missing}")

    @staticmethod
    def make_features(data):
        gross_sales = data["quantity"] * data["unit_price"]
        return pd.DataFrame(
            {
                "gross_sales": gross_sales,
                "discount_amount": gross_sales * data["discount"],
            },
            index=data.index,
        )

    def split(self):
        X = self.make_features(self.df)
        y = self.df[Config.TARGET]
        return train_test_split(
            X,
            y,
            test_size=Config.TEST_SIZE,
            random_state=Config.RANDOM_STATE,
        )

    def revenue_by_date_chart(self):
        daily_sales = self.df.copy()
        daily_sales["order_date"] = pd.to_datetime(daily_sales["order_date"])
        daily_sales = (
            daily_sales.groupby("order_date", as_index=False)["revenue"]
            .sum()
            .sort_values("order_date")
        )
        return px.line(
            daily_sales,
            x="order_date",
            y="revenue",
            title="Daily revenue",
            labels={"order_date": "Order date", "revenue": "Revenue"},
        )

    def category_chart(self):
        category_sales = (
            self.df.groupby("product_category", as_index=False)["revenue"]
            .sum()
            .sort_values("revenue", ascending=False)
        )
        return px.bar(
            category_sales,
            x="product_category",
            y="revenue",
            title="Revenue by product category",
            labels={"product_category": "Category", "revenue": "Revenue"},
        )
