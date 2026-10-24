import streamlit as st

from app import menu
from datamodules.EcommerceDataset import EcommerceDataset


st.set_page_config(page_title="Sales Analysis", page_icon="📊", layout="wide")
menu()
st.title("Sales analysis")

dataset = EcommerceDataset()
df = dataset.df

first, second, third = st.columns(3)
first.metric("Orders", f"{len(df):,}")
second.metric("Total revenue", f"${df['revenue'].sum():,.2f}")
third.metric("Average order revenue", f"${df['revenue'].mean():,.2f}")

left, right = st.columns(2)
left.plotly_chart(dataset.revenue_by_date_chart(), use_container_width=True)
right.plotly_chart(dataset.category_chart(), use_container_width=True)

st.subheader("Dataset preview")
st.dataframe(df.head(20), use_container_width=True)

with st.expander("Summary statistics"):
    st.dataframe(df.describe(), use_container_width=True)
