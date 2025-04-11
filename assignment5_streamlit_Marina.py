import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Set the page configuration
st.set_page_config(page_title="Lebanon Tourism Dashboard", layout="wide")



# Title
st.title("Exploring Lebanon's Exquisite Cities")
st.image(r"Lebanon Tourism.png", caption="أهلا وسهلا. Welcome. Bienvenue.", use_container_width=True)
st.markdown("""
Need guidance for your next trip to Lebanon?  
You can use these tools to discover Lebanon's finest cities and what they have to offer!
""")

st.markdown("---")

# Load the dataset
file_path = r"Tourism Lebanon 2023.csv"
tourism = pd.read_csv(file_path)

# Clean up column names
tourism.columns = tourism.columns.str.strip()

# Section 1: Stacked Bar Chart for Top 20 Towns
st.header("Top 20 Towns with the Most Hotels, Restaurants, and Cafes")
st.markdown("""
Gathering around food with friends and family is a staple in Lebanon, which is why you will see so many cafes and restaurants.  
With hotels nearby, you’ll be sure to witness the spirit of Lebanese people as you hear loud conversations and laughter.  
  
**P.S.** If you hear a loud smack on a table followed by an uproar, rest assured, it is most definitely a group of close friends playing a friendly yet competitive game of cards!  
(Common favorites include a game called *Tarneeb*.)
""")
# Aggregating the data
tourism_summary = tourism.groupby("Town")[[
    "Total number of hotels",
    "Total number of restaurants",
    "Total number of cafes"
]].sum()

tourism_summary["Total Establishments"] = (
    tourism_summary["Total number of hotels"]
    + tourism_summary["Total number of restaurants"]
    + tourism_summary["Total number of cafes"]
)

top_towns = tourism_summary.sort_values(by="Total Establishments", ascending=False).head(20).reset_index()

# Plotting
bar_fig = px.bar(
    top_towns,
    x="Town",
    y=["Total number of hotels", "Total number of restaurants", "Total number of cafes"],
    title="Top 20 Towns with the Most Hotels, Restaurants, and Cafes",
    labels={"value": "Count", "Town": "Town"},
    barmode="stack"
)
st.plotly_chart(bar_fig, use_container_width=True)

# Section 2: Dropdown for Tourism Index
st.header("Towns by Tourism Index and Initiatives")
st.markdown("Wanna know which towns have invested time and money into raising their tourist indeces? Find out using the dropdown tab below:")

# Replace NaNs with 0 for initiative column
tourism["Existence of initiatives and projects in the past five years to improve the tourism sector - exists"] = \
    tourism["Existence of initiatives and projects in the past five years to improve the tourism sector - exists"].fillna(0)

# Get unique Tourism Index values
unique_indexes = sorted(tourism["Tourism Index"].dropna().unique())

# Dropdown menu
selected_index = st.selectbox("Select a Tourism Index", unique_indexes)

# Filter data by selected index
filtered_df = tourism[tourism["Tourism Index"] == selected_index]

# Horizontal bar chart
bar_trace = go.Bar(
    x=filtered_df["Existence of initiatives and projects in the past five years to improve the tourism sector - exists"],
    y=filtered_df["Town"],
    orientation='h',
    marker=dict(color='teal')
)

fig = go.Figure(data=[bar_trace])
fig.update_layout(
    title=f"Towns with Tourism Index = {selected_index}",
    xaxis_title="Existence of initiatives in the past 5 years",
    yaxis_title="Town",
    showlegend=False,
    height=600
)

st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

st.markdown("""
Thank you for looking through my visuals.  
My name is **Marina Markarian**, and I am publishing these as I practice using **Streamlit** and storytelling techniques for my **Data Visualization** class.
""")


