import main as mn
import streamlit as st
import time
import os

st.title("QuerAI")

uploaded=None

# form=st.sidebar.form(key="my_form")

submitted=st.sidebar.button("submit")
selected=st.sidebar.selectbox("Type of document",options=["pdf_file","Webpage","Youtube Video"],index=None)

query=st.text_input(label="Ask Your Query?",max_chars=50)
search=st.button("search")


try:
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

    if not(uploaded):
        st.header(":red[Hail Hydra! ] :orange[Just kidding, it's QuerAI!] :sunglasses:", divider='rainbow')

        # Displaying the text
        about_text = """I'm just a basic prototype, you know, but I can handle personal documents (in PDF format), webpage content, or YouTube videos like a champ. Go ahead, ask me anything from the stuff you've given me, and I'll do my best to provide answers. Of course, if your question doesn't have anything to do with what I've been given, well, I'm not a mind reader!"""
        st.write(about_text)

        st.info("Make sure to upload your source files first, then click the submit button located at the top of the sidebar. Refer to the sidebar for further instructions.",icon="ℹ️")
        
    if selected and uploaded and query and os.path.exists("__pycache__/main.cpython-311.pyc") and search:
        if selected!="pdf_file" :
            st.write(mn.doc_Query(query))
        else:
            st.write(mn.pdf_Query(query))
except ValueError :
    st.error("Please,give the correct formate of source.",icon="❗")
except IndexError:
    st.error("Can't retrieve information from the source.",icon="❗")
except:
    st.error("Got an error, Retry.",icon="❗")
