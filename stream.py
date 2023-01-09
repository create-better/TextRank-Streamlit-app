import streamlit as st
from text_summarisation import generate_summary as gs

st.title("Text Summarisation using NLP")
st.text("The model uses pagerank algorithm and cosine similarity for extractive summarisation.")
# st.selectbox("Source of the text::", ['URL','Text entered manually', 'File (.txt, .pdf, .doc)'])
value = st.text_input("Enter the text for summarisation")
summary = gs(value, 8)
result = st.button("Summarize")
if result:
    st.write(summary)

