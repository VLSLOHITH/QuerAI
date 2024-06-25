from langchain_openai import OpenAI,OpenAIEmbeddings
from langchain.prompts import PromptTemplate
from langchain_community.document_loaders import UnstructuredURLLoader,YoutubeLoader,ImageCaptionLoader
import PyPDF2
from langchain.chains import LLMChain,RetrievalQAWithSourcesChain
from langchain.vectorstores.faiss import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.indexes import VectorstoreIndexCreator
import os
import streamlit as st

os.environ["OPENAI_API_KEY"]=st.secrets["OPENAI_API_KEY"]


def Embeddings():
    return OpenAIEmbeddings()

def Doc_vector_store(data):
    text_splitter=RecursiveCharacterTextSplitter(separators=["\n\n","\n","."," "],
                                        chunk_size=1000,
                                        chunk_overlap=200
                                        )
    docs=text_splitter.split_documents(data)

    vectorDB=FAISS.from_documents(docs,Embeddings())

    vectorDB.save_local("vectorDB")

def Str_vector_store(data):
    text_splitter=RecursiveCharacterTextSplitter(separators=["\n\n","\n","."," "],
                                        chunk_size=1000,
                                        chunk_overlap=200
                                        )
    docs=text_splitter.split_text(data)

    vectorDB=FAISS.from_texts(docs,Embeddings())

    vectorDB.save_local("vectorDB")


def Youtube_loader(url):
    loader=YoutubeLoader.from_youtube_url(url)

    data=loader.load()

    return data

def url_loader(url):
    if type(url)!=list:
        url=[url]
    loader=UnstructuredURLLoader(urls=url)

    data=loader.load()

    return data

def pdf_loader(pdf_file):
    
    pdf_reader=PyPDF2.PdfReader(pdf_file)

    data=""

    for page in pdf_reader.pages:
        data+=page.extract_text()

    return data


def pdf_Query(question,k=4):

    llm=OpenAI(model="gpt-3.5-turbo-instruct",max_tokens=100)

    vector_index=FAISS.load_local("vectorDB",Embeddings())

    docs=vector_index.similarity_search(question,k=k)
    
    docs_page_content=" ".join(d.page_content for d in docs)


    prompts=PromptTemplate(
        input_variables=["question","docs"],
        template="""You are a given a question and a pdf document and your duity is to get the answers exclusively from the given pdf document and if it does not relate to the content then just say that "It's not there in pdf." but if it contains in the document then give only the answer in brief.question asked:{question}, pdf document:{docs} and also try to give summery if user ask for it.
        """,
    )

    chain=LLMChain(llm=llm,prompt=prompts)

    response=chain.run(question=question,docs=docs_page_content)

    return response

def doc_Query(query):
    llm=OpenAI(temperature=0.7,max_tokens=500)

    vector_index=FAISS.load_local("vectorDB",Embeddings())

    chains=RetrievalQAWithSourcesChain.from_llm(llm=llm,retriever=vector_index.as_retriever())

    response=chains.invoke(input={"question":query})

    return response["answer"]






