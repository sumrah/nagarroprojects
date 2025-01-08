import streamlit as st
from PyPDF2 import PdfReader
import fitz  # PyMuPDF
from PIL import Image
import io
import pytesseract
from langchain.text_splitter import RecursiveCharacterTextSplitter
import os
from langchain_google_genai import GoogleGenerativeAIEmbeddings
import google.generativeai as genai
from langchain.vectorstores import FAISS
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains.question_answering import load_qa_chain
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv
import json

load_dotenv()
os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Session state to keep track of the current session's queries
if "session_history" not in st.session_state:
    st.session_state.session_history = []

general_responses = {
    "hi": "Hello! How can I help you today?",
    "hello": "Hi there! What would you like to know?",
    "how are you": "I'm an AI, so I don't have feelings, but I'm here to help you! How can I assist you?",
    "what is your name": "I'm your AI assistant. What can I do for you?"
}

def get_pdf_text(pdf_docs):
    text = ""
    for pdf in pdf_docs:
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages:
            text += page.extract_text()
    return text

def get_pdf_images(pdf_docs):
    images = []
    for pdf in pdf_docs:
        doc = fitz.open(stream=pdf.read(), filetype="pdf")
        for page in doc:
            pix = page.get_pixmap()
            img = Image.open(io.BytesIO(pix.tobytes()))
            images.append(img)
    return images

def get_text_from_images(images):
    text = ""
    for img in images:
        text += pytesseract.image_to_string(img)
    return text

def get_text_chunks(text):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=10000, chunk_overlap=1000)
    chunks = text_splitter.split_text(text)
    return chunks

def get_vector_store(text_chunks):
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    vector_store = FAISS.from_texts(text_chunks, embedding=embeddings)
    vector_store.save_local("faiss_index")

def get_conversational_chain():
    prompt_template = """
    Answer the question as detailed as possible from the provided context, make sure to provide all the details, if the answer is not in
    provided context just say, "not related", don't provide the wrong answer\n\n
    Context:\n {context}?\n
    Question: \n{question}\n

    Answer:
    """

    model = ChatGoogleGenerativeAI(model="gemini-pro", temperature=0.3)
    prompt = PromptTemplate(template=prompt_template, input_variables=["context", "question"])
    chain = load_qa_chain(model, chain_type="stuff", prompt=prompt)
    return chain

def user_input(user_question):
    user_question_lower = user_question.lower()
    
    # Load the knowledge base
    knowledge_base = load_knowledge_base()
    
    # Check for general responses
    if user_question_lower in general_responses:
        response = {"output_text": general_responses[user_question_lower]}
    elif user_question in knowledge_base:
        response = {"output_text": knowledge_base[user_question]}
    else:
        embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
        new_db = FAISS.load_local("faiss_index", embeddings, allow_dangerous_deserialization=True)
        docs = new_db.similarity_search(user_question)
        chain = get_conversational_chain()
        response = chain({"input_documents": docs, "question": user_question}, return_only_outputs=True)
        
        # Check if the response is not related
        if "not related" in response["output_text"].lower() or "answer is not available" in response["output_text"].lower() or "provided context" in response["output_text"].lower():
            response["output_text"] = "not related"
            log_unanswered_question(user_question)
            if user_question not in knowledge_base:
                update_knowledge_base(user_question, response["output_text"])

    
    log_history(user_question, response["output_text"])
    st.session_state.session_history.append({"question": user_question, "response": response["output_text"]})
    st.write("Reply: ", response["output_text"])

def log_history(question, response):
    with open("query_history.txt", "a") as file:
        file.write(f"Question: {question}\n")
        file.write(f"Response: {response}\n\n")

def log_unanswered_question(question):
    with open("unanswered_questions.txt", "a") as file:
        file.write(f"{question}\n")

def update_knowledge_base(question, answer):
    with open("knowledge_base.json", "r") as file:
        knowledge_base = json.load(file)
    knowledge_base[question] = answer
    with open("knowledge_base.json", "w") as file:
        json.dump(knowledge_base, file)

def load_knowledge_base():
    try:
        with open("knowledge_base.json", "r") as file:
            knowledge_base = json.load(file)
    except FileNotFoundError:
        knowledge_base = {}
    return knowledge_base

def main():
    st.set_page_config("Chat PDF")
    st.header("Chat with  your MediBuddy💁")
    user_question = st.text_input("Ask a Question from the PDF Files")

    if user_question:
        user_input(user_question)

    with st.sidebar:
        st.title("Menu:")
        pdf_docs = st.file_uploader("Upload your PDF Files and Click on the Submit & Process Button", accept_multiple_files=True, type=["pdf"])
        if st.button("Submit & Process"):
            if pdf_docs:
                with st.spinner("Processing..."):
                    raw_text = get_pdf_text(pdf_docs)
                    images = get_pdf_images(pdf_docs)
                    image_text = get_text_from_images(images)
                    combined_text = raw_text + image_text
                    text_chunks = get_text_chunks(combined_text)
                    get_vector_store(text_chunks)
                    st.success("Done")
            else:
                st.error("No files were uploaded.")

        st.title("Chat History")
        session_history = st.session_state.get('session_history', [])
        for entry in session_history:
            st.write(f"**Question:** {entry['question']}")
            st.write(f"**Response:** {entry['response']}")
            st.write("---")

if __name__ == "__main__":
    if not os.path.exists("knowledge_base.json"):
        with open("knowledge_base.json", "w") as file:
            json.dump({}, file)
    main()
