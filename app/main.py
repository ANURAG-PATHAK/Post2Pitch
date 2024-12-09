import streamlit as st

st.title("Post2Pitch")

url_input = st.text_input("Enter job posting URL:", value="https://jobs.nike.com/job/R-38844")
uploaded_resume = st.file_uploader("Upload your resume")
submit_button = st.button("Submit")

if submit_button: 
    st.code("hello", language="markdown")