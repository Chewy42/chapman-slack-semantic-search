"""
Copyright (c) 2023 by Matthew Favela
Protected under the MIT License
"""


from chromadb import Client
from chromadb.config import Settings
from chromadb.utils import embedding_functions
import openai
from dotenv import load_dotenv
import os

load_dotenv()

def initialize_chroma_db():
    client = Client(Settings(
        chroma_db_impl="duckdb+parquet",
        persist_directory=".chapdb/" 
    ))

    openai_ef = embedding_functions.OpenAIEmbeddingFunction(
                    api_key=os.getenv("OPENAI_API_KEY"),
                    model_name="text-embedding-ada-002"
                )
    
    openai.api_key = os.getenv("OPENAI_API_KEY")
    openai.organization = os.getenv("OPENAI_ORG")

    return client, openai_ef

client, openai_ef = initialize_chroma_db()

def create_collection(collection_name):
    return client.create_collection(name=collection_name, embedding_function=openai_ef)

def delete_collection(collection_name):
    return client.delete_collection(name=collection_name)

def extract_docs_and_ids_from_txt(path_to_txt, catalog_year):
    text = ""
    with open(path_to_txt, "r") as f:
        text = f.read()
    paragraphs = text.split("\n\n")

    ids = []

    for paragraph in paragraphs:
        subj_name = paragraph.split(" ")[1].split("\n")[0]
        cat_num = paragraph.split(" ")[2].split("\n")[0]
        id = str(catalog_year) + subj_name + cat_num
        ids.append(id)

    return paragraphs, ids

def add_docs_to_collection(collection_name, documents, ids):
    collection = client.get_collection(name=collection_name, embedding_function=openai_ef)
    collection.add(ids=ids, documents=documents)

def query_collection(collection_name, q):
    collection = client.get_collection(name=collection_name, embedding_function=openai_ef)
    return collection.query(n_results=10, query_texts=q)

def get_answer_from_gpt(students_question, query_result):
    resmsg = f"Students Question: {students_question}\n\n Vector DB Query Result: {query_result}"
    response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are an AI academic advisor for Chapman University. A students question and query response from a vector database will be given for you to answer. Be straight to the point with the answer"},
        {"role": "user", "content": resmsg},
        ],
    max_tokens=500,
    temperature=0
    )

    return response['choices'][0]['message']['content']

#create_collection("2020-SoftwareEngineeringMajor")

#docs, ids = extract_docs_and_ids_from_txt("2020-SoftwareEngineeringMajor.txt", 2020) # file name and catalog year

#add_docs_to_collection("2020-SoftwareEngineeringMajor", docs, ids)

def example():
    example_student_question = "What are the prerequisities for human computer interaction?"
    example_db_response = query_collection("2020-SoftwareEngineeringMajor", example_student_question)["documents"]
    example_answer = get_answer_from_gpt(example_student_question, example_db_response)
    print(example_answer)


question = input("Enter an course related question: ")
db_response = query_collection("2020-SoftwareEngineeringMajor", question)["documents"]
answer = get_answer_from_gpt(question, db_response)
print(answer)