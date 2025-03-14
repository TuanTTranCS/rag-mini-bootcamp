import tkinter as tk
from tkinter import scrolledtext, font
import time
from datetime import datetime
import os
from dotenv import load_dotenv

# Load the environment variables
load_dotenv()
from workshop_code.indexer_components.preprocessors import GITHUB_BLOG_POST, ARXIV_RAG_SURVEY_PAPER
from workshop_code.agents import NaiveQaRagAgent

class MockNaiveQaRagAgent:
    def __init__(self):
        vectorizer = None
        self._indexer = None
        self._retriever = None
        self._generator = None

    def query(self, query: str) -> str:
        
        completion = "Naive RAG is the earliest methodology in the RAG research paradigm, "+ \
            "following a traditional process of indexing, retrieval, and generation within a \"Retrieve-Read\" framework. "+\
            "It involves cleaning and extracting raw data, segmenting text into smaller chunks, " + \
            "encoding them into vector representations, and storing them in a vector database for efficient " + \
            "similarity searches. Naive RAG represents the initial stage of RAG development before" + \
            "Advanced RAG and Modular RAG were introduced to address its limitations."
        return completion
    
    def index(self, doc_uri):
        return None

class ChatWindow:
    def __init__(self, master):
        self.master = master
        master.title("Q&A Agent")
        master.geometry("1000x700")

        

         # Set up fonts
        default_font = font.nametofont("TkDefaultFont")
        default_font.configure(size=12)  # Increased default font size
        
        text_font = font.Font(family="Helvetica", size=14)  # Custom font for text areas

        # Create radio buttons for doc_uri selection
        self.doc_uri_var = tk.StringVar(value=ARXIV_RAG_SURVEY_PAPER)
        radio_frame = tk.Frame(master)
        radio_frame.pack(fill='x', padx=10, pady=10)

        tk.Radiobutton(radio_frame, text="ArXiv RAG Survey Paper", variable=self.doc_uri_var, 
                       value=ARXIV_RAG_SURVEY_PAPER, font=default_font, command=self.update_doc_uri).pack(side='left')
        tk.Radiobutton(radio_frame, text="GitHub Blog Post", variable=self.doc_uri_var, 
                       value=GITHUB_BLOG_POST, font=default_font, command=self.update_doc_uri).pack(side='left')



        # Create and set up the chat display
        self.chat_display = scrolledtext.ScrolledText(master, state='disabled', font=text_font, wrap=tk.WORD)
        self.chat_display.pack(expand=True, fill='both', padx=10, pady=10)

        # Create the input area
        input_frame = tk.Frame(master)
        input_frame.pack(fill='x', padx=10, pady=10)

        self.input_box = tk.Entry(input_frame, font=text_font)
        self.input_box.pack(side='left', expand=True, fill='x', ipady=5)
        self.input_box.bind("<Return>", self.send_message)

        self.send_button = tk.Button(input_frame, text="Send", command=self.send_message, font=default_font)
        self.send_button.pack(side='right')

        # Set up the Q&A agent
        self.qa_agent = NaiveQaRagAgent()
        self.update_doc_uri()

        # Display a startup message
        startup_message = os.getenv('STARTUP_MESSAGE', 'Welcome to the Q&A Agent! How can I assist you today?')
        self.display_message(startup_message, is_user=False)

    def update_doc_uri(self):
        doc_uri = self.doc_uri_var.get()
        self.qa_agent.index(doc_uri)
        time.sleep(int(os.getenv('INDEXING_WAIT_TIME', '5')))  # Wait for indexing to complete
        update_message = f"Document updated to: {doc_uri}. " + \
            "Change document by selecting one of the radio buttons on the top."
        self.display_message(update_message, is_user=False)

    def send_message(self, event=None):
        question = self.input_box.get().strip()
        if question:
            # Display user message
            self.display_message(question, is_user=True)
            
            # Get and display agent's response
            answer = self.qa_agent.query(question)
            self.display_message(answer, is_user=False)
            
            # Clear the input box
            self.input_box.delete(0, 'end')

    def display_message(self, message, is_user=False):
        self.chat_display.config(state='normal')
        time_display = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        if is_user:
            self.chat_display.tag_configure("right", justify="right")
            self.chat_display.insert(tk.END, f"You ({time_display}): {message}\n", "right")
            self.chat_display.tag_add("blue", self.chat_display.index("end-2l"), self.chat_display.index("end-1c"))
            self.chat_display.tag_configure("blue", foreground="blue")
        else:
            self.chat_display.insert(tk.END, f"Agent ({time_display}): {message}\n")
            self.chat_display.tag_add("green", self.chat_display.index("end-2l"), self.chat_display.index("end-1c"))
            self.chat_display.tag_configure("green", foreground="green")
        
        self.chat_display.insert(tk.END, "\n")
        self.chat_display.config(state='disabled')
        self.chat_display.see(tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    chat_app = ChatWindow(root)
    root.mainloop()