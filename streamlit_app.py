import streamlit as st
import requests

# Get the API key from Streamlit secrets
# Make sure you have a .streamlit/secrets.toml file with your API_KEY
try:
    api_key = st.secrets["API_KEY"]
except (FileNotFoundError, KeyError):
    st.error("API_KEY not found. Please add it to your Streamlit secrets.")
    st.stop()

# Initialize conversation history in session state
if "conversation_history" not in st.session_state:
    st.session_state["conversation_history"] = []

# Function to send a message to the API
def send_message(msg):
    url = 'https://ibyakzxxxigaxgyhmuts.supabase.co/functions/v1/agentpi-api'
    headers = {
        'Authorization': f'Bearer {api_key}',
        'apikey': api_key,
        'Content-Type': 'application/json'
    }
    data = {
        'message': msg,
        'conversationHistory': st.session_state["conversation_history"]
    }
    
    try:
        response = requests.post(url, json=data, headers=headers)
        response.raise_for_status()  # Raise an exception for bad status codes
        result = response.json()

        if result.get('success'):
            # Update conversation history from the successful response
            st.session_state["conversation_history"] = result["data"]["conversationHistory"]
            return result["data"]["response"]
        else:
            return f"Error: {result.get('message', 'Unknown error from API')}"
            
    except requests.exceptions.RequestException as e:
        return f"An error occurred: {e}"
    except Exception as e:
        return f"An unexpected error occurred: {e}"

# --- Streamlit User Interface ---
st.title("AI Assistant Chat")
st.write("This application interacts with an AI agent. You can ask it to perform tasks like parsing a PDF from a URL.")

# Display conversation history
for i, turn in enumerate(st.session_state.conversation_history):
    if turn.get('role') == 'user':
        st.chat_message("user").write(turn['content'])
    elif turn.get('role') == 'assistant':
        st.chat_message("assistant").write(turn['content'])

# User input
if prompt := st.chat_input("Enter your message"):
    st.chat_message("user").write(prompt)
    
    with st.spinner("AI is thinking..."):
        response = send_message(prompt)
        st.chat_message("assistant").write(response)

# Button to clear the conversation
if st.sidebar.button("Clear Conversation"):
    st.session_state["conversation_history"] = []
    st.rerun()

