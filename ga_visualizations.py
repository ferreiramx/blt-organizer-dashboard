import streamlit as st
import snowflake.connector
import pandas as pd
import plotly.express as px

# Event ID
EVENT_ID = '201898'

# Snowflake connector parameters
USER = 'DBT'
PASSWORD = '3382bPfNx9vSTJGEQc9oK4rR82ReJD'
ACCOUNT = 'dzb74710.us-east-1'
WAREHOUSE = 'TRANSFORM'
DATABASE = 'PROD'
SCHEMA = 'EVENTS'

ctx = snowflake.connector.connect(
        user=USER,
        password=PASSWORD,
        account=ACCOUNT,
        warehouse=WAREHOUSE,
        database=DATABASE,
        schema=SCHEMA
        )

cur = ctx.cursor()

def load_bookings_by_date():
    # Execute a query to extract the data
    sql = f"""select date(paid_at) as fecha, count(booking_id) as compras 
            from EVENTS.COMPLETED_BOOKINGS 
            where event_id = {EVENT_ID}
            group by fecha 
            order by fecha """
    cur.execute(sql)
    # Converting data into a dataframe
    df = cur.fetch_pandas_all()
    return df

# Streamlit page title
st.title('Boletia GA')

# Show bookings by date
st.subheader('Compras por dia')
data = load_bookings_by_date()

# Create visualizations for COMPRAS
fig = px.line(data, x="FECHA", y="COMPRAS")
st.plotly_chart(fig, use_container_width=True)

def load_customers_age():
    # Execute a query to extract the data
    sql = f"""select *
                from EVENTS.CUSTOMER_DEMOGRAPHICS_AGE
                where event_id = {EVENT_ID}
                order by AGE_BRACKET
                """
    cur.execute(sql)
    # Converting data into a dataframe
    df = cur.fetch_pandas_all()
    return df

# Create visualization for EDAD
st.subheader('Edad')
data = load_customers_age()
fig = px.bar(data, y="AGE_BRACKET", x="TOTAL_BOOKINGS", orientation='h')
st.plotly_chart(fig, use_container_width=True)