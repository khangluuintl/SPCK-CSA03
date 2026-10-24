import pandas as pd
import plotly.express as px
import streamlit as st

from app import menu
from config import Config
from datamodules.EcommerceDataset import EcommerceDataset
from models.EcommerceSalesModule import EcommerceSalesModule


st.set_page_config(page_title="Revenue Prediction", page_icon="🔮", layout="wide")
menu()
st.title("Revenue prediction")
st.write(
    "The model estimates revenue from gross sales and the discount amount, "
    "using a reproducible 80/20 train-test split."
)

dataset = EcommerceDataset()
X_train, X_test, y_train, y_test = dataset.split()
model = EcommerceSalesModule().train(X_train, y_train)
y_pred = model.predict(X_test)
scores = model.evaluate(y_test, y_pred)

first, second, third = st.columns(3)
first.metric("Mean absolute error", f"${scores['Mean Absolute Error']:,.4f}")
second.metric("Root mean squared error", f"${scores['Root Mean Squared Error']:,.4f}")
third.metric("R-squared", f"{scores['R-squared']:.6f}")

st.subheader("Test-set predictions")
comparison = pd.DataFrame(
    {"Actual revenue": y_test.to_numpy(), "Predicted revenue": y_pred}
)
chart = px.scatter(
    comparison,
    x="Actual revenue",
    y="Predicted revenue",
    title="Actual vs. predicted revenue",
    opacity=0.6,
)
axis_min = min(comparison.min())
axis_max = max(comparison.max())
chart.add_shape(
    type="line",
    x0=axis_min,
    y0=axis_min,
    x1=axis_max,
    y1=axis_max,
    line={"color": "red", "dash": "dash"},
)
st.plotly_chart(chart, use_container_width=True)

st.subheader("Predict a saved or custom order")
saved_records = st.session_state.get("sales_records", [])
if saved_records:
    selected = st.selectbox(
        "Saved order",
        options=range(len(saved_records)),
        format_func=lambda index: (
            f"Order {index + 1}: "
            f"{saved_records[index]['quantity']} x "
            f"${saved_records[index]['unit_price']:.2f}, "
            f"{saved_records[index]['discount']:.0%} discount"
        ),
    )
    record = saved_records[selected]
else:
    st.info("No saved orders yet. You can enter a custom order below.")
    record = None

with st.form("custom_prediction"):
    quantity = st.number_input("Quantity", min_value=1, value=1, key="pred_quantity")
    unit_price = st.number_input(
        "Unit price", min_value=0.01, value=100.0, step=1.0, key="pred_unit_price"
    )
    discount = st.number_input(
        "Discount (0 to 1)",
        min_value=0.0,
        max_value=1.0,
        value=0.0,
        step=0.01,
        key="pred_discount",
    )
    predict_custom = st.form_submit_button("Predict custom order")

if predict_custom:
    record = {
        "quantity": int(quantity),
        "unit_price": float(unit_price),
        "discount": float(discount),
    }
    st.success(f"Estimated revenue: ${model.predict(dataset.make_features(pd.DataFrame([record])))[0]:,.2f}")

if record is not None:
    if st.button("Predict selected saved order"):
        features = dataset.make_features(pd.DataFrame([record]))
        estimate = model.predict(features)[0]
        st.success(f"Estimated revenue: ${estimate:,.2f}")

st.caption(f"Data file: {Config.DATA_PATH.name}")
