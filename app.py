import streamlit as st
import re
from helper import scrape_text_from_urls, retrieve_relevant_chunks, get_answer_from_mistral, create_faiss_index

# Q&A Tool title and wide layout
st.set_page_config(layout="wide")
st.markdown("<h1 style='color: green; text-align: center;font-weight: bold;'>🔗🌐 Web Content Q&A Tool 🧠🤖</h1>", unsafe_allow_html=True)

# Handling multiple URLs inputs
st.markdown("<p style = 'font-weight: bold;'>Enter Website URLs</p>", unsafe_allow_html=True)
urls_input = st.text_area("")
st.markdown("<p style = 'font-weight: italic;color: red'>URLs must be separated only by a comma (comma-separated)</p>", unsafe_allow_html=True)


if st.button("Extract Content"):
    urls = [url.strip() for url in urls_input.split(",") if url.strip()]
    
    if not urls:
        st.error("Please enter at least one valid URL.")
    else:
        # Scraping the text from URLs
        texts = scrape_text_from_urls(urls)
        if any("Error" in text for text in texts):
            # Error handling for loading multiple URLs
            st.error("Some URLs could not be fetched. Check the extracted text for details.")
        else:
            st.session_state["texts"] = texts
            # Creating FAISS index of the extracted text
            st.session_state["index"], st.session_state["chunks"] = create_faiss_index(texts)
            st.success("Content Extracted & Indexed Successfully!")

# Handling Question-Answer part
if "texts" in st.session_state:
    question = st.text_input("Ask a Question about the Extracted Content")

    # Initializing session state for chunk display
    if "show_chunks" not in st.session_state:
        st.session_state.show_chunks = False

    # Generating Answer
    if st.button("Get Answer"):
        retrieved_chunks = retrieve_relevant_chunks(
            question, 
            st.session_state["index"], 
            st.session_state["chunks"], 
            num_results=5  # Considering top 5 chunks for retrieval
        )

        # Combining chunks for context
        context = " ".join(retrieved_chunks)
        # Extracting unprocessed answer
        raw_answer = get_answer_from_mistral(context, question)
        # Preparing the processed answer
        match = re.search(r'ANSWER:\s*(.*)', raw_answer, re.IGNORECASE)
        answer = match.group(1).strip() if match else ""

        # Storing results in session state to persist across interactions
        st.session_state["answer"] = answer
        st.session_state["retrieved_chunks"] = retrieved_chunks
        st.session_state["show_chunks"] = False  # Reseting the chunk visibility

    # Displaying stored answer
    if "answer" in st.session_state:
        if st.session_state["answer"]:
            st.write(f"**ANSWER**: {st.session_state['answer']}")

            # Toggle button for reference chunks
            if st.button("Check reference chunks"):
                st.session_state["show_chunks"] = not st.session_state.get("show_chunks", False)

            # Displaying chunks if toggled
            if st.session_state.get("show_chunks", False):
                st.write("### Raw Retrieved Context from the URLs as a reference")
                st.write(st.session_state["retrieved_chunks"])
        else:
            st.warning("No answer found in the extracted content.")