import streamlit as st
import plotly.graph_objects as go
from sklearn.preprocessing import MinMaxScaler
from tools.seasonality_tools import normalizationBySeasonality
from tools.data_tools import *


def page_timeseries():
    df = load_data()
    st.title("Time Series")
    st.write("""In this section, we are going to visualize the data thought the time by zip code""") # Revisar ingles
    st.header("Zip Code Selection")
    st.write("The available zip codes are those that have more than 72 registers in the database to achieve the maximum accuracy and have enough amount of data to show valuable charts")  # Revisar ingles
    option = st.selectbox(
        'Select a zip code to view the historical trends',
        list(set(df['zip_code'].values)))

    df_filtered_raw = df[df['zip_code'] == option]
    df_filtered = to_clean_time_series(df_filtered_raw)
    st.write(df_filtered)

    st.subheader('Line plot')
    fig = go.Figure(data=go.Scatter(x=df_filtered.index,
                                    y=df_filtered.appts, mode='lines+markers'))
    st.plotly_chart(fig, use_container_width=True)

    #chart_data = df_filtered['appts']
    # st.line_chart(chart_data)

    scaler = MinMaxScaler()

    df_filtered_normalized = df_filtered.copy(deep=True)
    df_filtered_normalized['appts'] = scaler.fit_transform(
        df_filtered['appts'].values.reshape(-1, 1))

    st.subheader('Line plot with Min-Max normalization')
    fig = go.Figure(data=go.Scatter(x=df_filtered_normalized.index,
                                    y=df_filtered_normalized.appts, mode='lines+markers'))
    st.plotly_chart(fig, use_container_width=True)

    #chart_data_filtered = df_filtered_normalized['appts']
    # st.line_chart(chart_data_filtered)

    df_filtered_season_normalized_raw = normalizationBySeasonality(
        df_filtered_raw, normalizationType='submean')
    df_filtered_season_normalized = to_clean_time_series(
        df_filtered_season_normalized_raw)

    st.subheader('Line plot with Season normalization')
    fig = go.Figure(data=go.Scatter(x=df_filtered_season_normalized.index,
                                    y=df_filtered_season_normalized.appts, mode='lines+markers'))
    st.plotly_chart(fig, use_container_width=True)

    #season_scaler = MinMaxScaler()
    #df_filtered_season_normalized_minmax = df_filtered_season_normalized.copy(deep=True)
    # df_filtered_season_normalized_minmax['appts'] = season_scaler.fit_transform(
    #    df_filtered_season_normalized['appts'].values.reshape(-1, 1))

    #st.subheader('Line plot with Season Min-Max normalization')
    # fig = go.Figure(data=go.Scatter(x=df_filtered_season_normalized_minmax.index,
    #                                y=df_filtered_season_normalized_minmax.appts, mode='lines+markers'))
    #st.plotly_chart(fig, use_container_width=True)
