import streamlit as st
import pandas as pd
import plotly.express as px
import utils


# Sidebar
st.sidebar.header("Configuración")
event_id = st.sidebar.text_input("Event ID", "201898")
event_data = utils.load_event_data(event_id)
price_threshold = st.sidebar.slider(
    "% rango de precio", min_value=0.0, max_value=1.0, value=0.1)

# Streamlit page title
st.title('Dashboard Analítica')
st.subheader(f"EVENTO: {event_data['NAME']}")

st.subheader("Eventos similares")
similar_events = utils.load_similar_events(event_id, price_threshold)
st.dataframe(similar_events)

# Columns
L, R = st.columns(2)


# Create visualization for COMPRAS
L.subheader('Compras')
data = utils.load_bookings_by_date([event_id])
fig = px.line(data, x="FECHA", y="COMPRAS")
L.plotly_chart(fig, use_container_width=True)
R.subheader('Compras - Eventos similares')
comp_data = utils.load_bookings_by_date(
    similar_events["EVENT_ID"].astype(str).values.tolist())
fig = px.line(comp_data, x="FECHA", y="COMPRAS")
R.plotly_chart(fig, use_container_width=True)


# Create visualization for EDAD
L.subheader('Edad')
data = utils.load_customers_by_age([event_id])
fig = px.bar(data, y="AGE_BRACKET", x="TOTAL_BOOKINGS", orientation='h')
L.plotly_chart(fig, use_container_width=True)
R.subheader('Edad - Eventos similares')
comp_data = utils.load_customers_by_age(
    similar_events["EVENT_ID"].astype(str).values.tolist())
fig = px.bar(comp_data, y="AGE_BRACKET", x="TOTAL_BOOKINGS", orientation='h')
R.plotly_chart(fig, use_container_width=True)


# Create visualization for GENERO
L.subheader('Genero')
data = utils.load_customers_by_gender([event_id])
fig = px.pie(data, values='TOTAL_BOOKINGS', names='GENDER', hole=.3)
L.plotly_chart(fig, use_container_width=True)
R.subheader('Genero - Eventos similares')
comp_data = utils.load_customers_by_gender(similar_events["EVENT_ID"].astype(str).values.tolist())
fig = px.pie(comp_data, values='TOTAL_BOOKINGS', names='GENDER', hole=.3)
R.plotly_chart(fig, use_container_width=True)


# Create visualization for COMPRAS POR DIA DE LA SEMANA
L.subheader('En que dia de la semana compran mas')
data = utils.load_bookings_by_week_day([event_id])
fig = px.bar(data, y="DIA", x="TOTAL_BOOKINGS", orientation='h')
L.plotly_chart(fig, use_container_width=True)
R.subheader('Eventos similares')
comp_data = utils.load_bookings_by_week_day(similar_events["EVENT_ID"].astype(str).values.tolist())
fig = px.bar(comp_data, y="DIA", x="TOTAL_BOOKINGS", orientation='h')
R.plotly_chart(fig, use_container_width=True)
