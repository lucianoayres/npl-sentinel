# -*- coding: utf-8 -*-
"""LlamaIndex_Tutorial.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/github/PradipNichite/Youtube-Tutorials/blob/main/LlamaIndex_Tutorial.ipynb

At its core, LlamaIndex contains a toolkit designed to easily connect LLM’s with your external data.

1.   Creating and Quering Index
2.   Saving and Loading Index
3.   Customize LLM
4.   Customize Prompt
5.   Customize Embedding
"""

!pip install llama-index pypdf sentence_transformers -q

"""By default, we use the OpenAI GPT-3 text-davinci-003 model.

https://gpt-index.readthedocs.io/en/latest/getting_started/installation.html
"""

import os
import openai
openai.api_key = ""
os.environ["OPENAI_API_KEY"] = ""

"""##Creating Index

https://gpt-index.readthedocs.io/en/latest/guides/primer/index_guide.html
"""

from llama_index import VectorStoreIndex, SimpleDirectoryReader
documents = SimpleDirectoryReader('book').load_data()
index = VectorStoreIndex.from_documents(documents)
query_engine = index.as_query_engine()

response = query_engine.query("What is this text about?")
print(response)

response = query_engine.query("who is this text about?")
print(response)

response = query_engine.query("when was this book published")
print(response)

response = query_engine.query("list 5 important points from this book")
print(response)

response = query_engine.query("what naval says about wealth creation")
print(response)

"""##Saving and Loading Index"""

index.storage_context.persist("naval_index")

from llama_index import StorageContext, load_index_from_storage

# rebuild storage context
storage_context = StorageContext.from_defaults(persist_dir="naval_index")
# load index
new_index = load_index_from_storage(storage_context)

new_query_engine = new_index.as_query_engine()
response = new_query_engine.query("who is this text about?")
print(response)

"""##Customizing LLM's

https://gpt-index.readthedocs.io/en/latest/how_to/customization/service_context.html
"""

from llama_index import LLMPredictor, ServiceContext

from langchain.chat_models import ChatOpenAI

llm_predictor = LLMPredictor(llm=ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo"))


service_context = ServiceContext.from_defaults(llm_predictor=llm_predictor)


custom_llm_index = VectorStoreIndex.from_documents(
    documents, service_context=service_context
)

custom_llm_query_engine = custom_llm_index.as_query_engine()
response = custom_llm_query_engine.query("who is this text about?")
print(response)

"""##Custom Prompt"""

from llama_index import Prompt

template = (
    "We have provided context information below. \n"
    "---------------------\n"
    "{context_str}"
    "\n---------------------\n"
    "Given this information, please answer the question and each answer should start with code word AI Demos: {query_str}\n"
)
qa_template = Prompt(template)

query_engine = custom_llm_index.as_query_engine(text_qa_template=qa_template)
response = query_engine.query("who is this text about?")
print(response)

"""##Custom Embedding"""

from langchain.embeddings.huggingface import HuggingFaceEmbeddings
from llama_index import LangchainEmbedding, ServiceContext

# load in HF embedding model from langchain
embed_model = LangchainEmbedding(HuggingFaceEmbeddings(model_name='sentence-transformers/all-MiniLM-L6-v2'))
service_context = ServiceContext.from_defaults(embed_model=embed_model)

new_index = VectorStoreIndex.from_documents(
    documents,
    service_context=service_context,
)

query_engine = new_index.as_query_engine()
response = query_engine.query("list 5 important points from this book")
print(response)

query_engine = new_index.as_query_engine()
response = query_engine.query("what naval says about wealth creation")
print(response)

