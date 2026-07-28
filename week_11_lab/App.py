import sqlite3
import pandas as pd
import streamlit as st

# Configure the Streamlit page layout
st.set_page_config(layout="wide")

st.title("Hanoi Real Estate & AI Market Dashboard 🏠")

# Function to connect to SQLite and load data into Pandas
@st.cache_data
def load_data():
    conn = sqlite3.connect("housing_market.db")
    # Query properties table (where we updated the AI predictions)
    query = "SELECT * FROM properties"
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

# Fetch data
df = load_data()

# Display interactive dataframe
st.subheader("Data Overview")
st.dataframe(df, use_container_width=True)

# Step 5: Visualizing AI Insights (The Final Product)
# Feature Engineering: Create price_difference column
df['price'] = pd.to_numeric(df['price'], errors='coerce')
if 'ai_predicted_price' in df.columns:
    df['ai_predicted_price'] = pd.to_numeric(df['ai_predicted_price'], errors='coerce')
    df['price_difference'] = df['ai_predicted_price'] - df['price']

# Sidebar Filter
st.sidebar.header("Filter Options")
property_types = ["All"] + list(df['type'].dropna().unique())
selected_type = st.sidebar.selectbox("Select Property Type:", property_types)

# Filter DataFrame based on sidebar selection
if selected_type != "All":
    filtered_df = df[df['type'] == selected_type].copy()
else:
    filtered_df = df.copy()

# Summary Metrics
st.markdown("---")
st.subheader("Market Metrics")
col1, col2, col3 = st.columns(3)

col1.metric("Total Properties", len(filtered_df))
col2.metric("Avg Listed Price", f"{filtered_df['price'].mean():.2f} B VND" if not filtered_df.empty else "0 B VND")

if 'ai_predicted_price' in filtered_df.columns and not filtered_df.empty:
    avg_pred = filtered_df['ai_predicted_price'].mean()
    col3.metric("Avg AI Predicted Price", f"{avg_pred:.2f} B VND")

# Bar Chart Comparison (Top 10 properties)
st.markdown("---")
st.subheader("Price vs AI Predicted Price (Top 10)")

if not filtered_df.empty and 'ai_predicted_price' in filtered_df.columns:
    top_10 = filtered_df.head(10).set_index('address')[['price', 'ai_predicted_price']]
    top_10.columns = ['Listed Price', 'AI Predicted Price']
    st.bar_chart(top_10)