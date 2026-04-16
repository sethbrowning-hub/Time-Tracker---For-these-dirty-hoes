import streamlit as st
import pandas as pd

# --- APP CONFIG ---
st.set_page_config(page_title="Strategic Labor Tracker", layout="wide")
st.title("🎯 Strategic Labor Command Center")
st.markdown("### Capacity vs. Demand Dashboard")

# --- 1. STAFFING DATA (The Capacity) ---
# Defining your team and their specific 8-hour daily buckets
staff_data = {
    "Skill Set": [
        "CSR3", "Return Tech", "Installations", "Gunsmith L2", 
        "Gunsmith L1", "Compressor Tech", "Gun Builder", 
        "Archery Crossbow", "Archery Bow"
    ],
    "Staff Names": [
        "Stacey, Ted", "EP, BG", "CG", "BM (L2)", 
        "BM (L1)", "MO", "Unassigned", "Unassigned", "Unassigned"
    ],
    "Daily Capacity (Hrs)": [16, 16, 8, 8, 8, 8, 8, 8, 8] # Based on your 40hr/wk per person
}
df_staff = pd.DataFrame(staff_data)

# --- 2. SIDEBAR - DEMAND ENTRY ---
st.sidebar.header("📥 Input Daily Demand")
st.sidebar.info("Enter the total hours of work queued for today per skill.")

user_demand = {}
for skill in staff_data["Skill Set"]:
    user_demand[skill] = st.sidebar.number_input(f"Hours for {skill}", min_value=0.0, value=0.0, step=0.5)

# --- 3. CALCULATIONS ---
df_staff['Current Demand'] = df_staff['Skill Set'].map(user_demand)
df_staff['Available Hours'] = df_staff['Daily Capacity (Hrs)'] - df_staff['Current Demand']
df_staff['Utilization %'] = (df_staff['Current Demand'] / df_staff['Daily Capacity (Hrs)']) * 100

# --- 4. THE DASHBOARD ---
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("Labor Utilization by Skill Set")
    
    # Create a color-coded bar chart
    def color_bars(val):
        if val > 100: return 'background-color: #ff4b4b; color: white' # Red
        if val > 80: return 'background-color: #ffa500' # Orange
        return 'background-color: #28a745; color: white' # Green

    st.dataframe(df_staff.style.applymap(color_bars, subset=['Utilization %']).format(precision=1))

with col2:
    st.subheader("Strategic Insights")
    overloaded = df_staff[df_staff['Utilization %'] > 100]
    underloaded = df_staff[df_staff['Utilization %'] < 70]
    
    if not overloaded.empty:
        st.error(f"⚠️ **Alert:** {len(overloaded)} departments are over capacity!")
        for _, row in overloaded.iterrows():
            st.write(f"- **{row['Skill Set']}** needs {abs(row['Available Hours'])} extra hours.")
    else:
        st.success("✅ All departments are within capacity.")

# --- 5. VISUAL CHART ---
st.bar_chart(df_staff, x="Skill Set", y="Utilization %")