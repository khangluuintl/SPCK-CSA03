import streamlit as st


def menu():
    st.sidebar.page_link("app.py", label="Home")
    st.sidebar.page_link("pages/1_Data_Analysis.py", label="Sales analysis")
    st.sidebar.page_link("pages/2_Input_Record.py", label="Add a sales record")
    st.sidebar.page_link("pages/3_Prediction.py", label="Revenue prediction")


if __name__ == "__main__":
    st.set_page_config(
        page_title="E-commerce Sales Analytics",
        page_icon="📈",
        layout="wide",
    )

    st.title("E-commerce Sales Analytics")
    st.write(
        "Explore the sales dataset, enter an order, and use linear regression "
        "to estimate revenue."
    )

    menu()
