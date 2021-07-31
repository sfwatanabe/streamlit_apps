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
    raw = df.drop(df[df.Age == 'Age'].index)  # Drop the repeating headers
    numeric_cols = ['Rk', 'Age', 'G', 'GS', 'MP', 'FG', 'FGA', 'FG%',
                    '3P', '3PA', '3P%', '2P', '2PA', '2P%', 'eFG%', 'FT', 'FTA', 'FT%',
                    'ORB', 'DRB', 'TRB', 'AST', 'STL', 'BLK', 'TOV', 'PF', 'PTS']
    # Handle the fillna for numerics first
    raw[raw.filter(regex='\w+[%]').columns] = raw[raw.filter(regex='\w+[%]').columns].fillna(0)
    raw[numeric_cols] = raw[numeric_cols].apply(pd.to_numeric)
    player_stats = raw.drop(['Rk'], axis=1)
    return player_stats


def file_download(df: pd.DataFrame):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" ' \
           f'download="player_stats.csv">Download CSV File</a>'
    return href


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

    # Add a link to download the current results to a csv.
    st.markdown(file_download(df_selected_team), unsafe_allow_html=True)

    # Heat-map for the stats!
    if st.button("Intercorrelation Heatmap"):
        st.header("Intercorrelation Matrix Heatmap")

        corr = df_selected_team.corr()
        mask = np.zeros_like(corr)
        mask[np.triu_indices_from(mask)] = True
        with sns.axes_style("white"):
            f, ax = plt.subplots(figsize=(7, 5))
            ax = sns.heatmap(corr, mask=mask, vmax=1, square=True)
        st.pyplot(f)


if __name__ == '__main__':
    main()
