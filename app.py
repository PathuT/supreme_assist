import os
from dotenv import load_dotenv
import streamlit as st
import google.generativeai as genai

# Page configuration
st.set_page_config(
    page_title="Supreme Assist - Legal AI Assistant",
    page_icon="⚖️",
    layout="wide"
)

# Custom CSS for better styling including loading animation
st.markdown("""
    <style>
    .main-header {
        color: #1E3A8A;
        padding: 1rem;
        border-bottom: 2px solid #E5E7EB;
        margin-bottom: 2rem;
        text-align: center;
        background-color: #F8FAFC;
    }
    .chat-message-user {
        background-color: #1E40AF;
        color: white;
        padding: 1rem;
        border-radius: 15px;
        margin: 1rem 2rem 1rem 8rem;
        position: relative;
    }
    .chat-message-assistant {
        background-color: #F1F5F9;
        color: #1E293B;
        padding: 1rem;
        border-radius: 15px;
        margin: 1rem 8rem 1rem 2rem;
        border: 1px solid #E2E8F0;
        position: relative;
    }
    .user-label, .assistant-label {
        font-size: 0.8rem;
        position: absolute;
        top: -1.2rem;
        color: #64748B;
    }
    .disclaimer {
        background-color: #FEF2F2;
        color: #991B1B;
        padding: 1rem;
        border-radius: 10px;
        margin-top: 2rem;
        border: 1px solid #FEE2E2;
        font-size: 0.9rem;
    }
    .stButton>button {
        background-color: #1E40AF;
        color: white;
        border-radius: 8px;
        padding: 0.5rem 2rem;
        border: none;
    }
    .stButton>button:hover {
        background-color: #1E3A8A;
    }
    div[data-testid="stToolbar"] {
        display: none;
    }
    .stTextInput>div>div>input {
        background-color: #F8FAFC;
        border-radius: 8px;
    }
    .loading-container {
        display: flex;
        justify-content: center;
        align-items: center;
        padding: 2rem;
    }
    .loading-spinner {
        border: 4px solid #f3f3f3;
        border-top: 4px solid #1E40AF;
        border-radius: 50%;
        width: 40px;
        height: 40px;
        animation: spin 1s linear infinite;
    }
    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    </style>
    """, unsafe_allow_html=True)

# Load environment variables
load_dotenv()

# Configure Gemini API
genai.configure(api_key=os.environ["GEMINI_API_KEY"])

# Model configuration
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

# Initialize model
model = genai.GenerativeModel(
    model_name="gemini-1.5-pro",
    generation_config=generation_config,
    system_instruction=(
        "You are an expert in laws and your role is to assist junior counsels and law students. "
        "Your task is to engage in conversations about law, answer legal questions, provide "
        "real-time information on case law based on user input queries. Ensure that your explanations are clear and precise "
        "using legal terminology in a way that is understandable for your audience. Provide accurate, "
        "fast, and user-friendly responses using the Gemini API. Aim to help users strengthen their legal knowledge "
        "offer relevant case law examples and practical applications. Also provide some real example cases "
        "related to the questions asked remember that strictly no other topics if I ask you other out of the topic "
        "If questions are from other domain do not respond."
    ),
)

# Initialize session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

def clear_chat():
    st.session_state.chat_history = []
    st.success("Chat history cleared.")
    st.rerun()

# Header
st.markdown('<h1 class="main-header">⚖️ Supreme Assist<br/><span style="font-size: 1.2rem; color: #64748B;">Your Personal Criminal Law Assistant</span></h1>', unsafe_allow_html=True)

# Display chat history above the input box
if st.session_state.chat_history:
    st.markdown("### Conversation")
    for entry in st.session_state.chat_history:
        if entry["role"] == "user":
            st.markdown(f"""
                <div class="chat-message-user">
                    <div class="user-label">You</div>
                    {entry['content']}
                </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
                <div class="chat-message-assistant">
                    <div class="assistant-label">Supreme Assist</div>
                    {entry['content']}
                </div>
            """, unsafe_allow_html=True)

# Input box and buttons
user_input = st.text_input("Ask your legal question:", key="user_input", 
                           placeholder="Type your question here...", value="")

# Button row
button_col1, button_col2, button_col3 = st.columns([1, 1, 2])
with button_col1:
    submit = st.button("Submit")
with button_col2:
    if st.button("Clear History"):
        clear_chat()

# Process chat
if submit and user_input:
    try:
        # Add user message to chat
        st.session_state.chat_history.append({"role": "user", "content": user_input})
        
        # Show loading spinner
        with st.spinner("Working..."):
            # Format chat history
            formatted_history = [
                {"role": entry["role"], "parts": [{"text": entry["content"]}]}
                for entry in st.session_state.chat_history
            ]
            
            # Get response
            chat_session = model.start_chat(history=formatted_history)
            response = chat_session.send_message(user_input)
            
            # Add assistant response
            st.session_state.chat_history.append({"role": "model", "content": response.text})
        
        # Rerun to update chat display
        st.rerun()
        
    except Exception as e:
        st.error(f"An error occurred: {e}")

# Disclaimer
st.markdown("""
    <div class="disclaimer">
        <strong>📢 Disclaimer:</strong> Supreme Assist is an AI-driven tool created to help users explore and understand general legal principles. While we strive to offer accurate and insightful information, Supreme Assist does not replace professional legal advice. For assistance with specific legal issues, please consult a qualified attorney who can provide personalized guidance.
    </div>
""", unsafe_allow_html=True)
