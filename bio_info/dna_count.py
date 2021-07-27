"""
Simple bio informatics web application using streamlit library.

credit to @DataProfessor, @FreeCodeCamp on youtube.
"""

import pandas as pd
import streamlit as st
import altair as alt
from PIL import Image


def main():
    image = Image.open("dna-logo.jpg")

    st.image(image, use_column_width=True)

    st.write("""
    # DNA Nucleotide Count Web App
    
    This app counts the nucleotide composition of query DNA!
    ***
    """)

    st.header("Enter DNA Sequence")

    sequence_input = ">DNA Query 2\nGAACACGTGGAGGCAAACAGGAAGGTGAAGAAGAACTTATCCTATCAGGACGGAAGGTCCTGTGCTCGGG\nATCTTCCAGACGTCGCGACTCTAAATTGCCCCCTCTGAGGTCAAGGAACACAAGATGGTTTTGGAAATGC\nTGAACCCGATACATTATAACATCACCAGCATCGTGCCTGAAGCCATGCCTGCTGCCACCATGCCAGTCCT"

    sequence = st.text_area("Sequence Input", sequence_input, height=250)
    sequence = sequence.splitlines()
    sequence
    sequence = sequence[1:]  # Skips the name
    sequence = ''.join(sequence)

    st.write("""
    ***
    """)

    # Prints the input DNA sequence
    st.header('INPUT (DNA Query)')
    sequence

    # DNA nucleotide count header
    st.header('OUTPUT (DNA Nucleotide Count)')

    # 1. Print Dictionary
    st.subheader('1. Print Dictionary')

    def DNA_nucleotide_count(seq: str):
        d = dict([
            ('A', seq.count('A')),
            ('T', seq.count('T')),
            ('G', seq.count('G')),
            ('C', seq.count('C')),
        ])
        return d

    X = DNA_nucleotide_count(sequence)

    X_label = list(X)
    X_values = list(X.values())

    # Print the text
    st.subheader('2. Print Text')
    st.write('There are ' + str(X['A']) + ' adenine (A)')
    st.write('There are ' + str(X['T']) + ' adenine (T)')
    st.write('There are ' + str(X['G']) + ' adenine (G)')
    st.write('There are ' + str(X['C']) + ' adenine (C)')

    # Display a dataframe in stream-lit.
    st.subheader('3. Display DataFrame')
    df = pd.DataFrame.from_dict(X, orient='index')
    df = df.rename({0: 'count'}, axis='columns')
    df.reset_index(inplace=True)
    df = df.rename(columns={'index': 'nucleotide'})
    st.write(df)

    # Display the bar chart using Altair
    st.subheader('4. Display bar chart')
    p = alt.Chart(df).mark_bar().encode(
        x='nucleotide',
        y='count'
    )

    p = p.properties(
        width=alt.Step(80)      # Controls width of the bar
    )
    # This step is very important as we write the object to the screen
    st.write(p)


if __name__ == '__main__':
    main()
