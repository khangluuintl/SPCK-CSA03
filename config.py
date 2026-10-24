from pathlib import Path


class Config:
    ROOT_DIR = Path(__file__).resolve().parent
    DATA_PATH = ROOT_DIR / "ecommerce_sales_analytics_5000.csv"
    TARGET = "revenue"
    RANDOM_STATE = 42
    TEST_SIZE = 0.2
