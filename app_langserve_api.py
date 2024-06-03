from typing import List

from fastapi import FastAPI

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI
from langserve import add_routes

import streamlit as st
import os
from dotenv import load_dotenv
load_dotenv()

SECRET_KEY = os.getenv("OPENAI_API_KEY")


# 1. Create prompt Template
system_template = "Translate the following into {language}"
prompt_template = ChatPromptTemplate.from_messages([
    ('system', system_template),
    ('user', '{text}')
])


# streamlit framework

st.title('Streamlit With OPENAI')
input_text=st.text_input("language")
input_text1=st.text_input("translate language")

# 2. Create Model
model = ChatOpenAI(openai_api_key=SECRET_KEY)


# 3. Create the parser
parser = StrOutputParser()

# 4. Chain creation
chain = prompt_template | model | parser


# 5.  App Defination
app = FastAPI(
  title="LangChain Server",
  version="1.0",
  description="A simple API server using LangChain's Runnable interfaces",
)


# 6. Adding chain route
add_routes(
    app,
    chain,
    path="/chain"
)

# for expose in langsmith
# if __name__ == "main":
#     import uvicorn

#     uvicorn.run(app, host="localhost", port=8000)

# for expose in streamlit
if input_text:
    st.write(chain.invoke({'language':input_text,'text':input_text1}))   

# http://localhost:8501/