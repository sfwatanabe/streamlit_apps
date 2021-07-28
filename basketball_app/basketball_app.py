"""
NBA Player Stats Explorer - EDA Tool to show visualizations for some basketball.

base64 -> enables the ascii to byte conversion.
"""
import base64

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns



def page_intro():
    """
    Setup the page header and markdown for the introduction paragraph.
    """
    # Setup the title for the page and write some markdown to the html page.
    st.title('NBA Player Stats Explorer')
    st.markdown("""
    This app performs simple web scraping of NBA player stats data!  
    * **Python libraries:** base64, pandas, streamlit
    * **Data source:** [Basketball-reference.com](https://www.basketball-reference.com)
    
    """)


# Web scraping of NBA player stats that will also cache results in streamlit
@st.cache
def load_data(year: str) -> pd.DataFrame:
    url = f"https://www.basketball-reference.com/leagues/NBA_{year}_per_game.html"
    html = pd.read_html(url, header=0)
    df = html[0]
    raw = df.drop(df[df.Age == 'Age'].index)    # Drop the repeating headers
    raw = raw.fillna(0)
    player_stats = raw.drop(['Rk'], axis=1)
    return player_stats


def main():
    """
    Main application logic for the NBA EDA stream-lit application that allows for
    filtering and exporting of data!
    """
    page_intro()
    # Setup the title and selection options for the sidebar on hover.
    st.sidebar.header('User Input Features')
    selected_year = st.sidebar.selectbox('Year',
                                         list(reversed(range(1950, 2020))))
    stats = load_data(str(selected_year))
    # Sidebar team selection
    sorted_unique_team = sorted(stats.Tm.unique())
    selected_team = st.sidebar.multiselect('Team', sorted_unique_team,
                                           sorted_unique_team)
    # Sidebar position selection
    unique_pos = ['C', 'PF', 'SF', 'PG', 'SG']
    selected_pos = st.sidebar.multiselect('Position', unique_pos, unique_pos)

    # Filtering the data using our selection sidebar options
    df_selected_team = stats[(stats.Tm.isin(selected_team)) & (stats.Pos.isin(selected_pos))]

    st.header('Display Player Stats of Selected Team(s)')
    st.write(f"Data Dimension: {df_selected_team.shape[0]} rows and "
             f"{df_selected_team.shape[1]} columns.")
    st.dataframe(df_selected_team)

    # Download the NBA

if __name__ == '__main__':
    main()
