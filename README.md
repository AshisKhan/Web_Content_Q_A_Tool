**Web Content Q&A Tool (RAG + Mistral 7B)**
- A Streamlit-based tool that allows users to input one or more URLs, extract webpage content, and ask questions based on the extracted text using Mistral 7B.

**Features**
- Multi-URL Support – Extracts and processes content from multiple web pages.
- Retrieval-Augmented Generation (RAG) – Ensures answers are based strictly on scraped content.
- Efficient Text Chunking & Retrieval – Uses FAISS for fast content search.
- Streamlit UI – Simple web interface for easy interaction.
- Mistral 7B Integration – Generates responses using Hugging Face API.

**Project Structure**

 web-content-qa-tool
 
│--  app.py                ( # Streamlit UI for the application)

│--  helper.py             ( # Helper functions for scraping, indexing, retrieval, and answering)

│--  requirements.txt      ( # Dependencies required to run the project)

│--  .env                  ( # API Key (not included in GitHub or may include the .env inside .gitignore file))

│--  README.md             ( # Documentation (this file))

**Installation & Setup (Local Machine)**

1️) Clone the Repository

git clone https://github.com/AshisKhan/Web_Content_Q_A_Tool.git

cd Web_Content_Q_A_Tool

2️) Create a Virtual Environment (Recommended)

python -m venv venv

venv\Scripts\activate   # for Windows

source venv/bin/activate  # for Mac/Linux

3️) Install Dependencies

pip install -r requirements.txt

4️) Set Up API Key

Since the .env file is ignored in Git, create it manually:

echo API_KEY="your_huggingface_api_key" > .env

**Verify by opening:**
- notepad .env  # Windows
- cat .env      # Mac/Linux

**Running the Application**:
streamlit run app.py
The app will open in your default web browser(http://localhost:8501/)

**Deploying on Streamlit Cloud**

1️) Push Code to GitHub:
- git add .
- git commit -m "Initial commit"
- git branch -M main
- git remote add origin https://github.com/your_username/your_repository.git
- git push -u origin main
  
2️) Set API Key in Streamlit Cloud
Go to Streamlit Cloud (streamlit.io).

Deploy your repository.

Add API Key in Secrets Management:

[general]

API_KEY="your_huggingface_api_key"

3️) Deploy

Streamlit will automatically deploy the app.

Future GitHub updates will reflect automatically.

**How to Use**:
- Enter URLs – Input one or multiple webpage URLs.
- Extract Content – The tool scrapes and indexes the webpage text.
- Ask a Question – Query the content using a natural language question.
- Get an Answer – The model retrieves relevant chunks and provides a response.
- Check reference chunks (extracted from URLs) for the asked question if require.

**Live Demo**
visit for a live demo:
[Live App](https://ashis-khan-web-content-q-a-tool-app.streamlit.app/)

**Contact**
For questions or issues, open a GitHub Issue or email at "khanashis1996@gmail.com"
