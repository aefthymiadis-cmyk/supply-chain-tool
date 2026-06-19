
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

st.set_page_config(page_title="Supply Chain AI Manager Dashboard", layout="wide")

# -----------------------------
# DATA
# -----------------------------
product_sales = {
    "TShirt": [400,450,520,600,680,710],
    "Shoes": [220,250,270,300,310,320],
    "Hat": [180,170,165,160,155,150]
}

inventory_data = {
    "TShirt": {"Stock": 300, "DailyDemand": 25},
    "Shoes": {"Stock": 150, "DailyDemand": 15},
    "Hat": {"Stock": 80, "DailyDemand": 8}
}

suppliers = pd.DataFrame({
    "Supplier": ["Alpha Textiles","Global Apparel","Express Clothing","Premium Footwear","Fashion Hats EU"],
    "Product": ["TShirt","TShirt","TShirt","Shoes","Hat"],
    "Cost": [10,11,12,14,8],
    "LeadTime": [5,6,3,8,4],
    "Reliability": [95,90,85,88,92]
})

# -----------------------------
# SIDEBAR
# -----------------------------
menu = st.sidebar.selectbox("Navigation", ["Executive Dashboard","Forecasting","Inventory","Suppliers","KPIs","AI Assistant"])

# -----------------------------
# EXECUTIVE DASHBOARD
# -----------------------------
if menu == "Executive Dashboard":
    st.title("📊 Executive Summary")

    alerts = []

    for p in inventory_data:
        stock = inventory_data[p]["Stock"]
        demand = inventory_data[p]["DailyDemand"]
        days_cover = stock / demand

        if days_cover < 5:
            alerts.append(f"🔴 {p} low stock risk ({days_cover:.1f} days cover)")

    st.metric("Total Products", len(inventory_data))
    st.metric("Products", len(alerts))

    st.subheader("Alerts")
    for a in alerts:
        st.write(a)

# -----------------------------
# FORECASTING + DIAGNOSIS
# -----------------------------
if menu == "Forecasting":
    st.title("📊 Forecasting & Diagnosis")

    product = st.selectbox("Product", list(product_sales.keys()))

    growth = st.slider("Growth %", -30, 50, 10)

    sales = np.array(product_sales[product])

    forecast = sales * (1 + growth/100)

    trend = "Stable"
    if forecast[-1] > sales[-1]:
        trend = "Increasing"
    elif forecast[-1] < sales[-1]:
        trend = "Decreasing"

    st.subheader("Sales History")
    st.write(sales)

    st.subheader("Forecast")
    st.write(forecast)

    st.info(f"Trend Diagnosis: {trend}")

    fig = px.line(x=range(len(sales)), y=[sales, forecast], labels={"x":"Month","value":"Sales"})
    st.plotly_chart(fig)

# -----------------------------
# INVENTORY
# -----------------------------
if menu == "Inventory":
    st.title("📦 Inventory Planning")

    product = st.selectbox("Product", list(inventory_data.keys()))

    stock = inventory_data[product]["Stock"]
    demand = inventory_data[product]["DailyDemand"]

    lead_time = st.number_input("Lead Time", 5)

    days_cover = stock / demand
    reorder_point = demand * lead_time * 1.5

    st.metric("Stock", stock)
    st.metric("Days Cover", round(days_cover,2))

    if days_cover < lead_time:
        st.error("🔴 STOCKOUT RISK")
    else:
        st.success("🟢 OK")

# -----------------------------
# SUPPLIERS
# -----------------------------
if menu == "Suppliers":
    st.title("🚚 Supplier Management")

    product = st.selectbox("Product", suppliers["Product"].unique())

    df = suppliers[suppliers["Product"] == product].copy()

    df["Score"] = df["Reliability"]*0.5 - df["LeadTime"]*0.3 - df["Cost"]*0.2

    st.dataframe(df)

    best = df.loc[df["Score"].idxmax(),"Supplier"]
    st.success(f"Best Supplier: {best}")

    fig = px.bar(df, x="Supplier", y="Score")
    st.plotly_chart(fig)

# -----------------------------
# KPIs
# -----------------------------
if menu == "KPIs":
    st.title("📈 KPIs")

    forecast_accuracy = 0.91
    turnover = 7.8
    service = 0.95

    st.metric("Forecast Accuracy", f"{forecast_accuracy*100:.1f}%")
    st.metric("Inventory Turnover", turnover)
    st.metric("Service Level", f"{service*100:.1f}%")

# -----------------------------
# AI ASSISTANT
# -----------------------------
if menu == "AI Assistant":
    st.title("🤖 Manager Assistant")

    stock = st.number_input("Stock", 100)
    forecast = st.number_input("Forecast", 200)
    lead = st.number_input("Lead Time", 5)

    if stock < forecast:
        st.warning("Increase inventory to avoid stockout.")

    if lead > 7:
        st.warning("Switch supplier due to high lead time.")

    if stock > forecast * 1.5:
        st.info("Overstock risk detected.")
