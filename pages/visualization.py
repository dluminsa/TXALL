import pandas as pd 
import streamlit as st 
import os
import numpy as np
import random
import time
from pathlib import Path
from streamlit_gsheets import GSheetsConnection
import plotly.express as px
import plotly.graph_objects as go
conn = st.connection('gsheets', type=GSheetsConnection)

df = conn.read(worksheet='TXML', usecols=list(range(16)), ttl=5)
df = df.dropna(how='all')
dfs=[]
weeeks = df['WEEK'].unique()
for each in weeeks:
    dfa = df[df['WEEK']==each]
    dfa = dfa.drop_duplicates(subset=['FACILITY'], keep = 'last')
    dfs.append(dfa)
df = pd.concat(dfs)
#file = r"C:\Users\Desire Lumisa\Downloads\TXML (5).xlsx"
#df = pd.read_excel(file)
st.sidebar.subheader('Filter from here ')
week = st.sidebar.multiselect('Pick a week', df['WEEK'].unique())
file2 = r'ALL.xlsx'
dfx = pd.read_excel(file2)
#create for the state
if not week:
    df2 = df.copy()
else:
    df2 = df[df['WEEK'].isin(week)]

#create for district
district = st.sidebar.multiselect('Choose a district', df2['DISTRICT'].unique())
if not district:
    df3 = df2.copy()
else:
    df3 = df2[df2['DISTRICT'].isin(district)]
 
#for facility
facility = st.sidebar.multiselect('Choose a facility', df3['FACILITY'].unique())

#Filter Week, District, Facility

if not week and not district and not facility:
    filtered_df = df
elif not district and not facility:
    filtered_df = df[df['WEEK'].isin(week)]
elif not week and not facility:
    filtered_df = df[df['DISTRICT'].isin(district)]
elif district and facility:
    filtered_df = df3[df['DISTRICT'].isin(district)& df3['FACILITY'].isin(facility)]
elif week and facility:
    filtered_df = df3[df['WEEK'].isin(week)& df3['FACILITY'].isin(facility)]
elif week and district:
    filtered_df = df3[df['WEEK'].isin(week)& df3['DISTRICT'].isin(district)]
elif facility:
    filtered_df = df3[df3['FACILITY'].isin(facility)]
else:
    filtered_df = df3[df3['WEEK'].isin(week) & df3['DISTRICT'].isin(district)&df3['FACILITY'].isin(facility)]
#################################################################################################
st.divider()
reporteddistrict = list(filtered_df['DISTRICT'].unique())
dfy = dfx[dfx['DISTRICT'].isin(reporteddistrict )]

reportedfacilities = list(filtered_df['FACILITY'].unique())
noted = dfy[~dfy['FACILITY'].isin(reportedfacilities)]
noted = noted['FACILITY'].unique()
cols,cold,colf = st.columns([1,2,1])
cold.markdown("**FACILITIES THAT DIDN'T REPORT**")
number = len(noted)
#nota = np.asarray([noted])
#notb = pd.DataFrame(nota, columns=["DIDN'T REPORT"])
colq,colt = st.columns(2)
colq.markdown(f'{number} facilities in **{reporteddistrict}** have not reported this week')
with colt:
    #with st.expander("Facilities that didn't submit"):
     #    st.write(nota)  
    button = st. button('**Click here to view them**')
    if button: 
          nota = pd.DataFrame(noted)
          st.write(f'{nota}')
st.divider()
#############################################################################################
pot = filtered_df['POTENTIAL'].sum()
Q2 = filtered_df['Q2 CURR'].sum()
ti = filtered_df['TI'].sum()
new = filtered_df['TX NEW'].sum()
uk = pot -Q2-ti
los = filtered_df['TXML'].sum()
to  = filtered_df['TO'].sum()
q3 = filtered_df['Q3 CURR'].sum()
labels = ["Q2 Curr", "TI", "TX NEW", 'Unkown',"Potential", "TXML", "TO", "Q3 Curr"]
values = [Q2, ti, new, uk, pot, -los, -to, q3]
measure = ["absolute", "relative", "relative","relative", "total", "relative", "relative", "total"]
# Create the waterfall chart
fig = go.Figure(go.Waterfall(
    name="Waterfall",
    orientation="v",
    measure=measure,
    x=labels,
    textposition="outside",
    text=[f"{v}" for v in values],
    y=values
))

# Add titles and labels and adjust layout properties
fig.update_layout(
    title="Waterfall Analysis",
    xaxis_title="Categories",
    yaxis_title="Values",
    showlegend=True,
    height=425,  # Adjust height to ensure the chart fits well
    margin=dict(l=20, r=20, t=60, b=20),  # Adjust margins to prevent clipping
    yaxis=dict(automargin=True)
)
# Show the plot
#fig.show()
#st.title("Waterfall Chart in Streamlit")
st.plotly_chart(fig)
########################################################################################
#LINE GRAPHS
st.divider()
st.subheader('TXML PERFORMANCE')
grouped = filtered_df.groupby('WEEK').sum(numeric_only=True).reset_index()

melted = grouped.melt(id_vars=['WEEK'], value_vars=['Q2 CURR', 'Q3 CURR', 'POTENTIAL'],
                            var_name='OUTCOME', value_name='Total')

melted2 = grouped.melt(id_vars=['WEEK'], value_vars=['TXML', 'TO'],
                            var_name='OUTCOME', value_name='Total')
fig2 = px.line(melted, x='WEEK', y='Total', color='OUTCOME', markers=True,
              title='Trends in TXML and TO', labels={'WEEK':'WEEK', 'Total': 'No. of clients', 'OUTCOME': 'Outcomes'})

fig3 = px.line(melted2, x='WEEK', y='Total', color='OUTCOME', markers=True, color_discrete_sequence=['blue','red'],
              title='Trends in TXML and TO', labels={'WEEK':'WEEK', 'Total': 'No. of clients', 'OUTCOME': 'Outcomes'})

fig2.update_layout(
    width=800,  # Set the width of the plot
    height=400,  # Set the height of the plot
    xaxis=dict(showline=True, linewidth=1, linecolor='black'),  # Show x-axis line
    yaxis=dict(showline=True, linewidth=1, linecolor='black')   # Show y-axis line
)

fig3.update_layout(
    width=800,  # Set the width of the plot
    height = 400,  # Set the height of the plot
    xaxis=dict(showline=True, linewidth=1, linecolor='black'),  # Show x-axis line
    yaxis=dict(showline=True, linewidth=1, linecolor='black')   # Show y-axis line
)

colx,coly = st.columns([2,1])
with colx:
    st.plotly_chart(fig2, use_container_width= True)

with coly:
    st.plotly_chart(fig3, use_container_width= True)
    #st.plotly_chart(fig3, use_container_width=True)
############################################################################################
group = grouped[grouped['WEEK']>22]
melted = group.melt(id_vars=['WEEK'], value_vars=['Q2 CURR', 'POTENTIAL', 'Q3 CURR'],
                            var_name='OUTCOME', value_name='Total')
fig5 = px.bar(
    melted,
    x='WEEK',
    y='Total',
    color='OUTCOME',
    title='Trends in TXML and TO',
    labels={'WEEK': 'WEEK', 'Total': 'No. of clients', 'OUTCOME': 'Outcomes'},
    barmode='group'  # Group bars by 'OUTCOME'
)

# Update the layout of the plot
fig5.update_layout(
    width=800,  # Set the width of the plot
    height=400,  # Set the height of the plot
    xaxis=dict(
        showline=True,  # Show x-axis line
        linewidth=1,    # Width of the x-axis line
        linecolor='black'  # Color of the x-axis line
    ),
    yaxis=dict(
        showline=True,  # Show y-axis line
        linewidth=1,    # Width of the y-axis line
        linecolor='black'  # Color of the y-axis line
    )
)

# To display the figure (assuming you are in a Jupyter notebook or a compatible environment)
st.plotly_chart(fig5, use_container_width= True)
#############################################################################################
#HIGHEST TXML 
st.divider()
current_time = time.localtime()
k = time.strftime("%V", current_time)
k= 24
k = int(k)
m = k-1
highest = filtered_df[filtered_df['TXML']>100]
#highest = highest.sort_values(by =['TX ML'], ascending = False)
highest = highest.sort_values(by=['TXML'])#, ascending=False)
highesta = highest[highest['WEEK']==k]
highestb = highest[highest['WEEK']==m]
coly, colu = st.columns([2,1])
if highesta.shape[0]==0:
    st.write("These facilities/facility have no high TXML or there is no report for them this week")
else:
    figa = px.bar(
    highesta,
    x='TXML',
    y='FACILITY',
    orientation='h',
    title='Facilities with highest TXML THIS WEEK',
    labels={'TXML': 'TXML Value', 'FACILITY': 'Facility'}
     )
with coly:
     st.plotly_chart(figa, use_container_width=True)
if highestb.shape[0]==0:
    st.write("These facilities/facility have no high TXML or there is no report for them last week")
else:
    figk = px.bar(
    highestb,
    x='TXML',
    y='FACILITY',
    orientation='h',
    title='Facilities with highest TXML LAST WEEK',
    labels={'TXML': 'TXML Value', 'FACILITY': 'Facility'}
     )
    with colu:
        st.plotly_chart(figb, use_container_width=True)
        highest = highest[['FACILITY', 'TXML']]
        highest. set_index('FACILITY', inplace= True)
        highest['TXML'] = highest['TXML'].astype(int)
        st.markdown('##')
        with st.expander('HIGHEST TXML'):
                 st.table(highest)
#############################################################################################
st.divider()
col1, col2,col3 = st.columns(3)
col2.write('**VL SECTION**')
meltvl = grouped.melt(id_vars='WEEK', value_vars=['EXPECTED', 'HAS VL'], var_name='PERFORMANCE', value_name='VL COVERAGE')

fig4 = px.line(meltvl, x='WEEK', y='VL COVERAGE', color='PERFORMANCE', markers=True, color_discrete_sequence=['blue','red'],
              title='Weekly VL Trend', labels={'WEEK':'WEEK', 'VL COVERAGE': 'No. BLED', 'PERFORMANCE': 'performance'})

fig4.update_layout(
    width=800,  # Set the width of the plot
    height=400,  # Set the height of the plot
    xaxis=dict(showline=True, linewidth=1, linecolor='black'),  # Show x-axis line
    yaxis=dict(showline=True, linewidth=1, linecolor='black')   # Show y-axis line
)


col1, col2 = st.columns(2)
with col1:
     st.plotly_chart(fig4, use_container_width=True)
     poorvl = filtered_df[filtered_df['VL COV (%)']<95]
     poorvl= poorvl.sort_values(by = ['VL COV (%)'])
     poorvl = poorvl[['DISTRICT', 'FACILITY','VL COV (%)']]
     poorvl.set_index('DISTRICT', inplace=True)
     with st.expander('FACILITIES WITH POOR VL COV'):
         st.dataframe(poorvl)
with col2:
    pied = filtered_df[['HAS VL', 'NO VL']]
    melted = pied.melt(var_name='Category', value_name='values')
    fig = px.pie(melted, values= 'values', names='Category', hole=0.5)
    #fig.update_traces(text = 'VL COVERAGE', text_position='Outside')
    st.plotly_chart(fig, use_container_width=True)

st.divider()
st.subheader('ALL DATA SET')
all = filtered_df[filtered_df['WEEK']>22]
st.write(all)
