import streamlit as st
import pandas as pd
from plotly.subplots import make_subplots

import plotly.express as px
import plotly.graph_objects as go

# Load data
df = pd.read_csv('https://raw.githubusercontent.com/rhafaelc/Google-Advanced-Data-Analytics-Capstone/refs/heads/main/HR_capstone_dataset.csv')

# Rename columns
df.rename(columns={
    'average_montly_hours': 'average_monthly_hours', 
    'time_spend_company': 'tenure', 
    'Work_accident': 'work_accident', 
    'promotion_last_5years': 'promotion_last_5_years',
    'Department': 'department'
}, inplace=True)

# Drop duplicates
df = df.drop_duplicates()

# Streamlit app
st.title('Human Resource Analysis')

# Distribution of Tenure
st.subheader('Distribution of Tenure')
fig = px.box(df, x='tenure', title='Distribution of Tenure')
st.plotly_chart(fig)

# Number of Employees that Left vs Stayed
st.subheader('Number of Employees that Left vs Stayed')
left_counts = df['left'].value_counts()
fig = px.pie(values=left_counts, names=left_counts.index, title='Number of Employees that Left vs Stayed')
st.plotly_chart(fig)

# Histograms
st.subheader('Histograms of Various Features')
fig = make_subplots(rows=2, cols=3, subplot_titles=(
    'Histogram of Satisfaction Level', 'Histogram of Last Evaluation', 'Histogram of Number of Projects',
    'Histogram of Average Monthly Hours', 'Histogram of Tenure'))

# Plot histogram for satisfaction_level
fig.add_trace(go.Histogram(x=df[df['left'] == 0]['satisfaction_level'], name='Stayed', opacity=0.75), row=1, col=1)
fig.add_trace(go.Histogram(x=df[df['left'] == 1]['satisfaction_level'], name='Left', opacity=0.75), row=1, col=1)

# Plot histogram for last_evaluation
fig.add_trace(go.Histogram(x=df[df['left'] == 0]['last_evaluation'], name='Stayed', opacity=0.75), row=1, col=2)
fig.add_trace(go.Histogram(x=df[df['left'] == 1]['last_evaluation'], name='Left',  opacity=0.75), row=1, col=2)

# Plot histogram for number_project
fig.add_trace(go.Histogram(x=df[df['left'] == 0]['number_project'], name='Stayed', opacity=0.75), row=1, col=3)
fig.add_trace(go.Histogram(x=df[df['left'] == 1]['number_project'], name='Left',  opacity=0.75), row=1, col=3)

# Plot histogram for average_monthly_hours
fig.add_trace(go.Histogram(x=df[df['left'] == 0]['average_monthly_hours'], name='Stayed', opacity=0.75), row=2, col=1)
fig.add_trace(go.Histogram(x=df[df['left'] == 1]['average_monthly_hours'], name='Left',  opacity=0.75), row=2, col=1)

# Plot histogram for tenure
fig.add_trace(go.Histogram(x=df[df['left'] == 0]['tenure'], name='Stayed', opacity=0.75), row=2, col=2)
fig.add_trace(go.Histogram(x=df[df['left'] == 1]['tenure'], name='Left',  opacity=0.75), row=2, col=2)

# Update layout
fig.update_layout(barmode='overlay', height=800, width=1200, showlegend=True)
fig.update_traces(opacity=0.75)
st.plotly_chart(fig)

# Attrition Rate by Last Evaluation Score
st.subheader('Attrition Rate by Last Evaluation Score')
bins = pd.cut(df['last_evaluation'], bins=[0, 0.5, 0.75, 1], labels=['Low', 'Medium', 'High'])
attrition_rate = df.groupby(bins, observed=False)['left'].mean().round(4) * 100

fig = px.bar(
    x=attrition_rate.index,
    y=attrition_rate.values,
    labels={'x': 'Last Evaluation Score', 'y': 'Attrition Rate (%)'},
    title='Attrition Rate by Last Evaluation Score',
    text=attrition_rate.values,
    color=attrition_rate.values
)

fig.update_layout(
    xaxis_title='Last Evaluation Score',
    yaxis_title='Attrition Rate (%)',
    title='Attrition Rate by Last Evaluation Score'
)

st.plotly_chart(fig)

# Box plot of Satisfaction Level by Left
st.subheader('Satisfaction Level by Left')
fig = px.box(df, x='left', y='satisfaction_level', color='left')
st.plotly_chart(fig)

left_by_department = df[df['left'] == 1].groupby('department').size().reset_index(name='left').sort_values(by=  'left', ascending=False)
# Number of Employees that Left by Department
st.subheader('Number of Employees that Left by Department')
fig = px.bar(left_by_department, x='department', y='left', title='Number of Employees that Left by Department')
st.plotly_chart(fig)