import streamlit as st
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
import os


def load_any_document(file):
    # this will get the extention from the file name ex:".pdf" ".docx" and many more
    import os

    name, extention = os.path.splitext(file)
    # this loads pdf
    if extention == ".pdf":
        from langchain.document_loaders import PyPDFLoader

        print(f"loading...{file}")
        loader = PyPDFLoader(file)
        # this loads docx file
    elif extention == ".docx":
        from langchain.document_loaders import Docx2txtLoader

        print(f"loadings {file=}")
        loader = Docx2txtLoader(file)
        # you can add many other formats as you needed using elif funtion
        # this below code will return none and intimate that the given document was not supported
    elif extention == ".txt":
        from langchain.document_loaders import TextLoader

        print(f"loadings {file=}")
        loader = TextLoader(file)

    else:
        print("Document format is not Supporting")
        return None
    # this is loading the data fron the file and returning data and compliting the function
    data = loader.load_and_split()
    return data


def chunk_data(data, chunk_size=100, chunk_overlap=20):
    from langchain.text_splitter import RecursiveCharacterTextSplitter

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=len,
    )
    chunks = text_splitter.split_documents(data)
    return chunks


def create_embeddings(chunks):
    embeddings = OpenAIEmbeddings()
    vectorstore = Chroma.from_documents(documents=chunks, embedding=embeddings)
    return vectorstore


def ask_get_answers(vector_store, q, k=3):
    from langchain.chains import RetrievalQA
    from langchain.chat_models import ChatOpenAI

    llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.7, verbose=True)
    retriever = vector_store.as_retriever(
        search_type="similarity", search_kwargs={"k": k}
    )
    # retriver=vector_store.similarity_search(query=q,k=3)
    chain = RetrievalQA.from_chain_type(
        llm=llm, chain_type="stuff", retriever=retriever
    )
    answer = chain.run(q)
    return answer


def calculate_embedding_cost(texts):
    import tiktoken

    enc = tiktoken.encoding_for_model("text-embedding-ada-002")
    total_tokens = sum([len(enc.encode(page.page_content)) for page in texts])
    cost_usd = total_tokens / 1000 * 0.0004
    # print(f"Total Tokens: {total_tokens}")
    # print(f"Embedding Cost in USD: {total_tokens / 1000 * 0.0004:.6f}")
    return total_tokens, cost_usd


if __name__ == "__main__":
    import os
    from dotenv import load_dotenv, find_dotenv

    load_dotenv(find_dotenv(), override=True)

    st.header("Chat Bot")

    with st.sidebar:
        api_key = st.text_input("Provide Open Ai Api Key ")
        if api_key:
            os.environ["OPENAI_API_KEY"] = api_key

        upload_file = st.file_uploader(
            "upload Your Document", type=[".pdf", ".docx", ".txt"]
        )

        chunk_size = st.number_input(
            "Chunk Sixe", min_value=100, max_value=2048, value=512
        )

        k = st.number_input("k", min_value=1, max_value=100, value=5)

        add_data = st.button("Add Data")

        if upload_file and add_data:
            with st.spinner("Reading , Chunking and Embedding file"):
                bytes_data = upload_file.read()
                file_name = os.path.join("File/", upload_file.name)
                with open(file_name, "wb") as f:
                    f.write(bytes_data)

                data = load_any_document(file_name)
                chunks = chunk_data(data=data, chunk_size=chunk_size)
                st.write(f"Chunk Size : {chunk_size} and Chunks: {len(chunks)}")

                tokens, embeddingcost = calculate_embedding_cost(chunks)
                f"embedding cost : {embeddingcost:4f}"

                vector_store = create_embeddings(chunks=chunks)

                st.session_state.vs = vector_store
                "File Uploaded Successfully"
    if q := st.text_input(" Ask Questions Relating to the Document"):
        if "vs" in st.session_state:
            vector_store = st.session_state.vs

            st.write(f"k:{k}")
            answer = ask_get_answers(vector_store=vector_store, q=q, k=k)
            st.text_area("LLM answer", value=answer)

    st.divider()

    if "history" not in st.session_state:
        st.session_state.history = ""

    value = f"Q: {q}  \n A: {answer}"
    st.session_state.history = f'{value} \n {"_" * 100} \n {st.session_state.history}'
    h = st.session_state.history
    st.text_area("chat history", value=h, key="history", height=400)
