import streamlit as st
import pandas as pd
import altair as alt
import plotly.graph_objs as go
import plotly.express as px
import load as l
import numpy as np
st.markdown("""
    <style>
    body {
        background-color: rgb(49, 51, 63);
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1 style='text-align: center; color: white;background: black;'>Consumer Financial Dashboard</h1>", unsafe_allow_html=True)
hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """



st.markdown(hide_streamlit_style, unsafe_allow_html=True) 
data = l.load1_b()

# Create state filter
states = [state for state in np.unique(data['state'])]
states.remove('state')
states.append('All')

selected_state = st.selectbox('Select State', states)
filtered_data = data
if selected_state!='All':

# Filter data based on selected state
    filtered_data = data[data['state'] == selected_state]


# Calculate KPIs
kpi_1 = len(filtered_data['compliant_ids'])
kpi_2 = len(filtered_data[filtered_data['company_respopnse'].isin(['Closed with explanation','Closed with non-monetary relief','Closed with monetary relief'])])
kpi_3 = len(filtered_data[filtered_data['timely']=='Yes'])
kpi_4 = len(filtered_data[filtered_data['company_respopnse']=='In progress'])

# Display KPIs
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.markdown("<h4 style='text-align: center; color: #030303;background: white;'>Total No of Complains</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; font-size: 36px; font-weight: bold; color: #030303;'>{:,.0f}</p>".format(kpi_1), unsafe_allow_html=True)

with col2:
    st.markdown("<h4 style='text-align: center; color: #030303;background: white;'>Total No of complains with closed status</h3>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; font-size: 36px; font-weight: bold; color: #030303;'>{:,.0f}</p>".format(kpi_2), unsafe_allow_html=True)

with col3:
    st.markdown("<h4 style='text-align: center; color:#030303;background: white;'>Timely responded compalins</h3>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; font-size: 36px; font-weight: bold; color: #030303;'>{:,.0f}</p>".format(kpi_3), unsafe_allow_html=True)

with col4:

    st.markdown("<h4 style='text-align: center; color: #030303;background: white;'>Totla No of compalins with In progress status</h3>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; font-size: 36px; font-weight: bold; color: #030303;'>{:,}</p>".format(kpi_4), unsafe_allow_html=True)

data= filtered_data.groupby(['products']).count()
complints_count=data['compliant_ids'].values
product=data.index
bar_data={'products':[p for p in product],'compliant':[c  for c in complints_count]}
bar_data=pd.DataFrame(bar_data)

chart_1 = alt.Chart(bar_data).mark_bar().encode(
    x='products',
    y='compliant'
).properties(
    width=250,
    height=200
)
data=filtered_data.groupby(['date_recive']).count()
complints_count=data['compliant_ids'].values
dates=data.index
line_data={'date_recive':[d for d in dates],'compliant':[c  for c in complints_count]}
line_data=pd.DataFrame(line_data)
chart_2 = alt.Chart(line_data).mark_line().encode(
    x='date_recive',
    y='compliant'
).properties(
    width=250,
    height=200
)
data=filtered_data.groupby(['submitted_via']).count()
complints_count=data['compliant_ids'].values
submitted_via=data.index
pie_data={'submitted_via':[d for d in submitted_via],'compliant':[c  for c in complints_count]}
pie_data=pd.DataFrame(pie_data)
col1, col2 = st.columns(2)
with col1:
    st.subheader('No of Complaints VS Product')
with col2:
    st.subheader('No of Complaints VS Date')
st.altair_chart(chart_1 | chart_2, use_container_width=True)
# st.altair_chart(chart_3 | chart_4, use_container_width=True)
labels = filtered_data['submitted_via'].unique()
values = filtered_data['submitted_via'].value_counts().tolist()
print(values)
fig3 = go.Figure(data=[go.Pie(labels=labels, values=values)])
fig3.update_layout(
    height=500,
    width=500
)
data=filtered_data.groupby(['issues','sub_issue'])['compliant_ids'].count().reset_index()
fig4 = px.treemap( data, path=['issues', 'sub_issue'], values='compliant_ids', width=600, height=400)
fig3.update_layout(
    height=400,
    width=300
)
col1, col2 = st.columns(2)
with col1:
    st.subheader('percentage of Compliants againts each Channel')
with col2:
    st.subheader('Number of Compliants Over Issue &subissue')
col1, col2 = st.columns(2)
with col1:
    st.plotly_chart(fig3)
with col2:
    st.plotly_chart(fig4)
