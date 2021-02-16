import streamlit as st
from timeseries import page_timeseries
from prediction import page_prediction


def main():
    pages = {
        "Time Series": page_timeseries,
        "Prediction": page_prediction,
    }
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Select your page", tuple(pages.keys()))

    # Display the selected page
    pages[page]()


if __name__ == "__main__":
    main()
