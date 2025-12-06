import streamlit as st
import tempfile
import os

st.title("Job Recommendation System")

resume = st.file_uploader("Upload your resume PDF here.", type=['pdf'])

if resume is not None:
    # create a temporary file
    with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(resume.name)[1]) as temp_file:
        # write the uploaded file's byte to the temp file
        temp_file.write(resume.getvalue())
        filepath = temp_file.name

        st.write(f"Uploaded file name: {resume.name}")
        st.write(f"Temporary filepath: {filepath}")
else:
    st.write("Please upload a file.")

st.subheader("Summary")
st.subheader("Skill Gap")
st.subheader("Road-Map")



jobs = st.multiselect("Select jobs you like the most. ", options=("job 01", "job 02", "job 03"))
location = st.selectbox("Your Location", options=("Sri Lanka", "US"))
submit_btn = st.button("Submit", on_click=None)














