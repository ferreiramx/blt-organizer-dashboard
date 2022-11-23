import snowflake.connector
import config
import streamlit as st

ctx = snowflake.connector.connect(
    user=config.USER,
    password=config.PASSWORD,
    account=config.ACCOUNT,
    warehouse=config.WAREHOUSE,
    database=config.DATABASE,
    schema=config.SCHEMA
)
cur = ctx.cursor()

# Get event metadata


@st.cache
def load_event_data(event_id):
    # Execute a query to extract the data
    sql = f"""select *
            from EVENTS.EVENTS
            where event_id = {event_id}
            """
    cur.execute(sql)
    # Converting data into a dataframe
    df = cur.fetch_pandas_all()
    return df.to_dict('records')[0] if len(df) > 0 else None

# Get comparable events


@st.cache
def load_similar_events(event_id, price_threshold):
    # Execute a query to extract the data
    sql = f"""with base_event as
                (select event_id, subcategory, city, state, average_ticket_price, channel_type
                from PROD.EVENTS.EVENTS
                where event_id = {event_id}
                )
            select 
                event_id,
                name,
                subcategory,
                city,
                state,
                average_ticket_price,
                channel_type
            from PROD.EVENTS.EVENTS
            where subcategory = (select subcategory from base_event)
            and state = (select state from base_event)
            and channel_type = (select channel_type from base_event)
            and average_ticket_price between (select average_ticket_price from base_event) * {1.0 - price_threshold} and (select average_ticket_price from base_event) * {1.0 + price_threshold}
            and tickets_sold_with_cost > 0
            and event_id <> (select event_id from base_event)
            and ended_at < current_timestamp
            """
    cur.execute(sql)
    # Converting data into a dataframe
    df = cur.fetch_pandas_all()
    return df

# Function to get the total number of bookings by date


@st.cache
def load_bookings_by_date(event_id):
    # Execute a query to extract the data
    sql = f"""select date(convert_timezone('America/Mexico_City', paid_at)) as fecha, count(booking_id) as compras
            from EVENTS.COMPLETED_BOOKINGS
            where event_id in ({','.join(event_id)})
            group by fecha
            order by fecha
            """
    cur.execute(sql)
    # Converting data into a dataframe
    df = cur.fetch_pandas_all()
    return df

# Function to get the total number of customers by age bracket


@st.cache
def load_customers_by_age(event_id):
    # Execute a query to extract the data
    sql = f"""select *
                from EVENTS.CUSTOMER_DEMOGRAPHICS_AGE
                where event_id in ({','.join(event_id)})
                order by age_bracket
                """
    cur.execute(sql)
    # Converting data into a dataframe
    df = cur.fetch_pandas_all()
    return df

# Function to get the total number of customer by gender


@st.cache
def load_customers_by_gender(event_id):
    # Execute a query to extract the data
    sql = f"""select *
                    from EVENTS.CUSTOMER_DEMOGRAPHICS_GENDER
                    where event_id in ({','.join(event_id)})
                    """
    cur.execute(sql)
    # Converting data into a dataframe
    df = cur.fetch_pandas_all()
    return df

# Function to get the total number of bookings by day of the week


@st.cache
def load_bookings_by_week_day(event_id):
    # Execute a query to extract the data
    sql = f"""select dayname(convert_timezone('America/Mexico_City', paid_at)) as dia, count(booking_id) as total_bookings
                from EVENTS.COMPLETED_BOOKINGS
                where event_id in ({','.join(event_id)})
                group by dia
                order by total_bookings
                """
    cur.execute(sql)
    # Converting data into a dataframe
    df = cur.fetch_pandas_all()
    return df
