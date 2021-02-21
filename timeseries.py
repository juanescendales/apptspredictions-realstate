import streamlit as st
import plotly.graph_objects as go
from sklearn.preprocessing import MinMaxScaler
from tools.seasonality_tools import normalizationBySeasonality
from tools.data_tools import *

@st.cache()
def calculate_periods():
    months_name = ['January', 'February', 'March', 'April', 'May', 'June',
                   'July', 'August', 'September', 'October', 'November', 'December']
    months_number = ['01', '02', '03', '04', '05',
                     '06', '07', '08', '09', '10', '11', '12']
    days = ['01', '16']
    periods = [month+'-'+day for month in months_name for day in days]
    periods_number = [month+'-' +
                      day for month in months_number for day in days]

    dictionary_encoding = {periods[i]:periods_number[i] for i in range(len(periods))}

    return periods,periods_number,dictionary_encoding

def filter_item(row):
        if(len(row) == 0):
            return None
        else:
            return row['appts_per_listing'].to_numpy()[0]

def period_plot(df,periods,subheader,years,dictionary_encoding):

    if(len(periods) != 0):
        fig = go.Figure()
        for period in periods:
            y_edge = [filter_item(df[df['start_date'] == str(
                year)+'-'+dictionary_encoding[period]]) for year in years]
            fig.add_trace(go.Scatter(x=[str(year) for year in years], y=y_edge,
                                     mode='lines+markers',
                                     name=str(period), connectgaps=True))

        st.subheader(subheader)
        st.plotly_chart(fig, use_container_width=True)

def plot_time_series(df, years, subheader,periods,periods_number):
    

    if(len(years) != 0):

        fig = go.Figure()
        for year in years:
            y_edge = [filter_item(df[df['start_date'] == str(
                year)+'-'+period_number]) for period_number in periods_number]
            fig.add_trace(go.Scatter(x=periods, y=y_edge,
                                     mode='lines+markers',
                                     name=str(year), connectgaps=True))

        st.subheader(subheader)
        st.plotly_chart(fig, use_container_width=True)


def page_timeseries():
    periods_list,periods_number_list,dictionary_encoding = calculate_periods()
    df = load_data()
    years_list = get_years(df)
    st.title("Time Series")
    st.write("""In this section, we are going to visualize the data thought the time by zip code""")  # Revisar ingles
    st.subheader("Zip Code Selection")
    st.write("The available zip codes are those that have more than 72 registers in the database to achieve the maximum accuracy and have enough amount of data to show valuable charts")  # Revisar ingles
    option = st.selectbox(
        'Select a zip code to view the historical trends',
        list(set(df['zip_code'].values)))

    df_filtered_raw = df[df['zip_code'] == option]
    df_filtered = to_clean_time_series(df_filtered_raw)
    st.write(df_filtered)

    st.subheader("Time series plot")
    years = st.multiselect(
        'Select the years you want to visualize', years_list)

    plot_time_series(df_filtered_raw, years, 'Line Plot',periods_list,periods_number_list)

    st.subheader("Period comparison plot")
    periods = st.multiselect(
        'Select the periods you want to visualize', periods_list)

    period_plot(df_filtered_raw,periods,'Line Plot',years_list,dictionary_encoding)
    

    # chart_data = df_filtered['appts_per_listing']
    # st.line_chart(chart_data)

    """ 
    scaler = MinMaxScaler()

    df_filtered_normalized = df_filtered.copy(deep=True)
    df_filtered_normalized['appts_per_listing'] = scaler.fit_transform(
        df_filtered['appts_per_listing'].values.reshape(-1, 1))

    st.subheader('Line plot with Min-Max normalization')
    fig = go.Figure(data=go.Scatter(x=df_filtered_normalized.index,
                                    y=df_filtered_normalized.appts_per_listing, mode='lines+markers'))
    st.plotly_chart(fig, use_container_width=True)"""

    # chart_data_filtered = df_filtered_normalized['appts_per_listing']
    # st.line_chart(chart_data_filtered)

    """df_filtered_season_normalized_raw = normalizationBySeasonality(
        df_filtered_raw, normalizationType='submean')
    df_filtered_season_normalized = to_clean_time_series(
        df_filtered_season_normalized_raw)

    st.subheader('Line plot with Season normalization')
    fig = go.Figure(data=go.Scatter(x=df_filtered_season_normalized.index,
                                    y=df_filtered_season_normalized.appts_per_listing, mode='lines+markers'))
    st.plotly_chart(fig, use_container_width=True)"""

    # season_scaler = MinMaxScaler()
    # df_filtered_season_normalized_minmax = df_filtered_season_normalized.copy(deep=True)
    # df_filtered_season_normalized_minmax['appts_per_listing'] = season_scaler.fit_transform(
    #    df_filtered_season_normalized['appts_per_listing'].values.reshape(-1, 1))

    # st.subheader('Line plot with Season Min-Max normalization')
    # fig = go.Figure(data=go.Scatter(x=df_filtered_season_normalized_minmax.index,
    #                                y=df_filtered_season_normalized_minmax.appts_per_listing, mode='lines+markers'))
    # st.plotly_chart(fig, use_container_width=True)
