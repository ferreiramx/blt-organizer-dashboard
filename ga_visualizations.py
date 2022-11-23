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

# Streamlit page title
st.title('BOLETIA Google Analytics')
st.subheader(f'EVENTO: {EVENT_ID}')

# Function to get the total number of bookings by date
def load_bookings_by_date():
    # Execute a query to extract the data
    sql = f"""select date(paid_at) as fecha, count(booking_id) as compras 
            from EVENTS.COMPLETED_BOOKINGS 
            where event_id = {EVENT_ID}
            group by fecha 
            order by fecha
            """
    cur.execute(sql)
    # Converting data into a dataframe
    df = cur.fetch_pandas_all()
    return df

# Create visualization for COMPRAS
st.subheader('Compras')
data = load_bookings_by_date()
fig = px.line(data, x="FECHA", y="COMPRAS")
st.plotly_chart(fig, use_container_width=True)

# Function to get the total number of customers by age bracket
def load_customers_by_age():
    # Execute a query to extract the data
    sql = f"""select *
                from EVENTS.CUSTOMER_DEMOGRAPHICS_AGE
                where event_id = {EVENT_ID}
                order by age_bracket
                """
    cur.execute(sql)
    # Converting data into a dataframe
    df = cur.fetch_pandas_all()
    return df

# Create visualization for EDAD
st.subheader('Edad')
data = load_customers_by_age()
fig = px.bar(data, y="AGE_BRACKET", x="TOTAL_BOOKINGS", orientation='h')
st.plotly_chart(fig, use_container_width=True)

# Function to get the total number of customer by gender
def load_customers_by_gender():
    # Execute a query to extract the data
    sql = f"""select *
                    from EVENTS.CUSTOMER_DEMOGRAPHICS_GENDER
                    where event_id = {EVENT_ID}
                    """
    cur.execute(sql)
    # Converting data into a dataframe
    df = cur.fetch_pandas_all()
    return df

# Create visualization for GENERO
st.subheader('Genero')
data = load_customers_by_gender()
fig = px.pie(data, values='TOTAL_BOOKINGS', names='GENDER', hole=.3)
st.plotly_chart(fig, use_container_width=True)

# Function to get the total number of bookings by day of the week
def load_bookings_by_week_day():
    # Execute a query to extract the data
    sql = f"""select dayname(paid_at) as dia, count(booking_id) as total_bookings
                from EVENTS.COMPLETED_BOOKINGS
                where event_id = {EVENT_ID}
                group by dia
                order by total_bookings
                """
    cur.execute(sql)
    # Converting data into a dataframe
    df = cur.fetch_pandas_all()
    return df

# Create visualization for COMPRAS POR DIA DE LA SEMANA
st.subheader('En que dia de la semana compran mas')
data = load_bookings_by_week_day()
fig = px.bar(data, y="DIA", x="TOTAL_BOOKINGS", orientation='h')
st.plotly_chart(fig, use_container_width=True)