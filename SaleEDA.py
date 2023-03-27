import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd,os

st.set_page_config(page_title="Superstore!!!", page_icon=":bar_chart:",layout="wide")

# st.set_page_config(page_title="Sales Dashboard", page_icon=":bar_chart:", layout="wide")
st.title(" :bar_chart: Sample Supersore EDA")
# st.write('<style>div.block-container{padding-top:1rem;}</style>', unsafe_allow_html=True)
f = st.file_uploader(":file_folder: Upload a file", type=(["csv","txt","xlsx","xls"]),)
if f is not None:
            path_in = f.name
            st.write(path_in)
            df=pd.read_csv(path_in,encoding = "ISO-8859-1")
else:
        os.chdir(r"C:\Users\abhisheak-saraswat\Streamlit")
        df=pd.read_csv(r"SampleSuperstore.csv",encoding = "ISO-8859-1")

# st.subheader("Hello ,let's learn how to display Samplesuperstone data")

col5, col6 = st.columns((2))
df["Order Date"] = pd.to_datetime(df["Order Date"])
startDate = pd.to_datetime(df['Order Date'].min())
endDate = pd.to_datetime(df['Order Date'].max())

with col5:
        date1=pd.to_datetime(st.date_input("Start Date",startDate))
with col6:
        date2=pd.to_datetime(st.date_input("End Date",endDate))
df=df[(df["Order Date"]>=date1) & (df["Order Date"]<=date2)]

st.sidebar.header("Choose your filter :")

region=st.sidebar.multiselect('Pick the Region', df['Region'].unique())
if not region:
        df2 = df.copy()
else:
        df2= df[df['Region'].isin(region)]
state=st.sidebar.multiselect('Pick the State', df2['State'].unique())
if not state:
        df3 = df2.copy()
else:
        df3= df2[df2['State'].isin(state)]
city=st.sidebar.multiselect('Pick the City', df3['City'].unique())

if not region and not state and not city :
    filtered_df=df
elif not state and not city:
        filtered_df = df[df['Region'].isin(region)]
elif not region and not city:
        filtered_df = df[df['State'].isin(state)]
elif state and city:
        filtered_df = df3[df3['State'].isin(state) & df3['City'].isin(city)]
elif region and city:
        filtered_df = df3[df3['Region'].isin(region) & df3['City'].isin(city)]
elif region and state:
        filtered_df = df3[df3['Region'].isin(region) & df3['State'].isin(state)]
elif city:
        filtered_df = df3[df3['City'].isin(city)]
else:
        filtered_df = df3[df3['Region'].isin(region) & df3['State'].isin(state) & df3['City'].isin(city)]


category_df=filtered_df.groupby(by=["Category"],as_index=False).sum()
#st.write(category_df)
with col5:
        st.subheader("Category wise Sales")
        fig = px.bar(category_df, x='Category', y='Sales',text = ['${:,.2f}'.format(x) for x in category_df['Sales']], template ="seaborn")
        st.plotly_chart(fig, use_container_width=True,height=200)
with col6:
        st.subheader("Region wise Sales")
        fig = px.pie(filtered_df,values="Sales",names="Region",hole=.5)
        fig.update_traces(text=filtered_df["Region"],textposition='outside')
        st.plotly_chart(fig, use_container_width=True)


filtered_df['month_year'] = filtered_df['Order Date'].dt.to_period('M')
st.subheader("Time Series Analysis")
linechart = pd.DataFrame(filtered_df.groupby(filtered_df['month_year'].dt.strftime('%Y : %b'))['Sales'].sum()).reset_index()
fig2 = px.line(linechart, x="month_year", y="Sales",labels={"Sales": "Amount"},height=500, width=1000,template="gridon")
st.plotly_chart(fig2, use_container_width=True)

st.subheader("Hierarchical view of Sales using TreeMap")
fig8 = px.treemap(filtered_df,path = ['Region','Category','Sub-Category'],values="Sales",hover_data=['Sales'],
                   color = "Sub-Category")

fig8.update_layout(width=800, height=650)
st.plotly_chart(fig8, use_container_width=True)

# Pie chart for sub-categor
# 
chart1, chart2 = st.columns((2))
with chart1:
        st.subheader('Segment Wise Sales')
        fig = px.pie(filtered_df,values="Sales",names="Segment",template="plotly_dark")
        fig.update_traces(text=filtered_df["Segment"],textposition='inside')
        st.plotly_chart(fig, use_container_width=True)        
with chart2:
        st.subheader('Category Wise Sales')
        fig = px.pie(filtered_df,values="Sales",names="Category",template="gridon")
        fig.update_traces(text=filtered_df["Category"],textposition='inside')
        st.plotly_chart(fig, use_container_width=True)  


st.subheader(":point_right: Month wise Sub-Category Sales Summary")
with st.expander("Summary"):
        filtered_df['month'] = filtered_df['Order Date'].dt.month_name()
        sub_category_year = pd.pivot_table(data=filtered_df,values='Sales',index=['Sub-Category'],columns='month')
        st.write(sub_category_year.style.background_gradient(cmap='Blues'))


with st.expander(":point_down: Click here to Display Data in Table"):
        fig4 = go.Figure(data=[go.Table(
        header=dict(values=list(['Region','State','City','Category','Sales','Profit','Quantity']),
                        fill_color='#22222F',
                        align='center',
                        font = dict(color = '#FFC300',size = 15)),
        cells=dict(values=[df.Region,df.State,df.City,df.Category,df.Sales, df.Profit, df.Quantity],
                fill_color='black',
                align='center',
                font = dict(color = 'white', size = 11)))
        ])

        st.plotly_chart(fig4,use_container_width=True)


data1=px.scatter(filtered_df,x='Sales',y='Profit',size='Quantity')
data1['layout'].update(title='Relationshhip Between Sales And Profits using Scatter Plot.',
                      titlefont=dict(size=20),
                      xaxis=dict(title='Sales',titlefont=dict(size=19)),
                      yaxis=dict(title='Profit',titlefont=dict(size=19)))

st.plotly_chart(data1,use_container_width=True)

# https://www.kaggle.com/code/alaasedeeq/superstore-data-analysis-with-plotly/notebook

import plotly.figure_factory as ff
with st.expander("Sample_Table"):
        df_sample = df[0:5][["Region","State","City","Category","Sales","Profit","Quantity"]]
        fig6 =  ff.create_table(df_sample,colorscale='Cividis')
        st.plotly_chart( fig6,use_container_width=True)
        # st.write(sub_category_year.style.background_gradient(cmap='Blues'))

with st.expander("View Data"):
     st.write(filtered_df.iloc[:100,1:20:2].style.background_gradient(cmap='Oranges'))
