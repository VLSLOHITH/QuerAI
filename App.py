import main as mn
import streamlit as st
import time
import os

st.title("QuerAI")

uploaded=None

# form=st.sidebar.form(key="my_form")

submitted=st.sidebar.button("submit")
st.sidebar.info("please upload your source before asking the questions",icon="i")
selected=st.sidebar.selectbox("Type of document",options=["pdf_file","Webpage","Youtube Video"],index=None)

query=st.text_input(label="Ask Your Query?",max_chars=50)


if selected=="pdf_file":
    uploaded=st.sidebar.file_uploader("Choose Your PDF File",type="pdf")
    if uploaded and submitted:
        data=mn.pdf_loader(uploaded)
        mn.Str_vector_store(data)
elif selected=="Webpage":
    uploaded=st.sidebar.text_input(label="Paste Your URL")
    if uploaded and submitted:
        data=mn.url_loader(uploaded)
        mn.Doc_vector_store(data)
elif selected=="Youtube Video":
    uploaded=st.sidebar.text_input(label="Paste the url of the Youtube Video")
    if uploaded and submitted:
        data=mn.Youtube_loader(uploaded)
        mn.Doc_vector_store(data)

search=st.button("search")

if selected and uploaded and query and os.path.exists("__pycache__/main.cpython-311.pyc") and search:
    if selected!="pdf_file" :
        st.write(mn.doc_Query(query))
    else:
        st.write(mn.pdf_Query(query))
