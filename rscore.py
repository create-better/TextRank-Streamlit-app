import streamlit as st
from text_summarisation import generated_rouge as gr
from text_summarisation import generate_summary as gs
from barchart import rouge_chart as rc

rouge_r = []
rouge_p = []
rouge_f = []

st.title("Rouge Scores")
st.text("ROUGE is a widely used metric by researchers to measure the performance of the summarisation model against human summaries")
passage = st.text_input("Enter the passage")
candi_Text = st.text_input("Enter the candidate text")
summary = gs(passage, 12)
scores = gr(summary, candi_Text)
value = st.button("Get results")
if value:
    st.write("The Summarised text is ::\n")
    st.write(summary)
    st.write("The rouge score is::")
    st.write(scores)
    rouge_r.extend([scores[0]['rouge-1']['r'], scores[0]['rouge-2']['r'], scores[0]['rouge-l']['r']])
    rouge_p.extend([scores[0]['rouge-1']['p'], scores[0]['rouge-2']['p'], scores[0]['rouge-l']['p']])
    rouge_f.extend([scores[0]['rouge-1']['f'], scores[0]['rouge-2']['f'], scores[0]['rouge-l']['f']])
    # rc(rouge_r, rouge_p, rouge_f)

    rouge_Scores = {'recall' : rouge_r, 'precision' : rouge_p, 'f1' : rouge_f}
    st.bar_chart(rouge_Scores)

    