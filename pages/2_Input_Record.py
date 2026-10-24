import streamlit as st

from app import menu


st.set_page_config(page_title="Add a Sales Record", page_icon="🛒", layout="wide")
menu()
st.title("Add a sales record for prediction")
st.write("Enter the order details that determine the estimated revenue.")

with st.form("sales_record"):
    quantity = st.number_input("Quantity", min_value=1, max_value=1000, value=1)
    unit_price = st.number_input(
        "Unit price", min_value=0.01, value=100.0, step=1.0
    )
    discount = st.number_input(
        "Discount (0 to 1)", min_value=0.0, max_value=1.0, value=0.0, step=0.01
    )
    submitted = st.form_submit_button("Save record")

if submitted:
    record = {
        "quantity": int(quantity),
        "unit_price": float(unit_price),
        "discount": float(discount),
    }
    st.session_state.setdefault("sales_records", []).append(record)
    st.success("Record saved. Open Revenue prediction to estimate its revenue.")

records = st.session_state.get("sales_records", [])
if records:
    st.subheader("Saved records")
    st.dataframe(records, use_container_width=True)
