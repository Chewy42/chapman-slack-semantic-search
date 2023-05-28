from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.text_splitter import CharacterTextSplitter
from langchain.llms import OpenAI
from langchain.chains import RetrievalQA
from langchain.document_loaders import TextLoader
from dotenv import load_dotenv
import os

load_dotenv()

vector_database = {}
text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
embeddings = OpenAIEmbeddings(openai_api_key=os.environ["OPENAI_API_KEY"])

data_folder_path = "catalog_text_files"
data_files = os.listdir(data_folder_path)

for file_name in data_files:
    if file_name.endswith(".txt"):
        file_path = os.path.join(data_folder_path, file_name)
        loader = TextLoader(file_path, encoding="utf-8")
        documents = loader.load()
        texts = text_splitter.split_documents(documents)
        docsearch = Chroma.from_documents(texts, embeddings, persist_directory="db")
        vector_database[file_name] = docsearch

qa = RetrievalQA.from_chain_type(llm=OpenAI(), chain_type="stuff", retriever=docsearch.as_retriever())

query = input("Ask me a question: ")
print(qa.run(query))
