import streamlit as st
import json
import time
from datetime import datetime
from nova_client import NovaClient
from config import Config

# Page configuration
st.set_page_config(
    page_title="NOVA Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Minimalistic NOVA styling
st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Global Styles */
    .main .block-container {
        padding-top: 1rem;
        padding-bottom: 1rem;
        max-width: 1000px;
    }
    
    /* Simple Header */
    .header-container {
        text-align: center;
        margin-bottom: 2rem;
        padding: 1.5rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 12px;
        color: white;
    }
    
    .main-header {
        font-family: 'Inter', sans-serif;
        font-size: 2rem;
        font-weight: 600;
        color: white;
        margin: 0;
    }
    
    .sub-header {
        font-family: 'Inter', sans-serif;
        font-size: 1rem;
        color: rgba(255, 255, 255, 0.9);
        margin: 0.5rem 0 0 0;
        font-weight: 400;
    }
    
    /* Chat Message Styling */
    .chat-message {
        font-family: 'Inter', sans-serif;
        padding: 1rem 1.5rem;
        margin-bottom: 1rem;
        border-radius: 12px;
        line-height: 1.6;
    }
    
    .user-message {
        background-color: #f3f4f6;
        margin-left: 2rem;
        border-left: 3px solid #3b82f6;
    }
    
    .assistant-message {
        background-color: #ffffff;
        border: 1px solid #e5e7eb;
        margin-right: 2rem;
        border-left: 3px solid #9c27b0;
    }
    
    /* Chat History Styling */
    .chat-history-item {
        padding: 0.75rem 1rem;
        margin: 0.5rem 0;
        background-color: #f8fafc;
        border-radius: 8px;
        border-left: 3px solid #3b82f6;
        cursor: pointer;
        transition: all 0.2s ease;
    }
    
    .chat-history-item:hover {
        background-color: #e2e8f0;
    }
    
    .chat-history-item.selected {
        background-color: #dbeafe;
        border-left-color: #1d4ed8;
    }
    
    .chat-history-preview {
        font-size: 0.9rem;
        color: #4b5563;
        margin: 0.25rem 0;
    }
    
    .chat-history-time {
        font-size: 0.8rem;
        color: #6b7280;
    }
    
    /* Hide Streamlit Branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Simple sidebar */
    .css-1d391kg {
        background-color: #f9fafb;
    }
    
    /* Simple button styling */
    .stButton > button {
        font-family: 'Inter', sans-serif;
        border-radius: 6px;
    }
    
    /* Simple input styling */
    .stChatInput > div > div > div > div {
        border-radius: 8px;
        border: 1px solid #d1d5db;
    }
    
    .stChatInput > div > div > div > div:focus-within {
        border-color: #3b82f6;
        box-shadow: 0 0 0 2px rgba(59, 130, 246, 0.1);
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "conversation_history" not in st.session_state:
    st.session_state.conversation_history = []
if "nova_client" not in st.session_state:
    st.session_state.nova_client = None
if "chat_sessions" not in st.session_state:
    st.session_state.chat_sessions = []
if "current_session_id" not in st.session_state:
    st.session_state.current_session_id = None
if "selected_history_item" not in st.session_state:
    st.session_state.selected_history_item = None

def initialize_nova_client():
    """Initialize NOVA client with error handling."""
    try:
        if st.session_state.nova_client is None:
            st.session_state.nova_client = NovaClient()
        return True
    except Exception as e:
        st.error(f"Failed to initialize NOVA client: {str(e)}")
        return False

def display_chat_message(role, content, timestamp=None):
    """Display a chat message with simple ChatGPT-like styling."""
    if role == "user":
        st.markdown(f"""
        <div class="chat-message user-message">
            <strong>You</strong><br>
            {content}
        </div>
        """, unsafe_allow_html=True)
    else:
        # Clean up JSON responses to make them readable
        clean_content = clean_response(content)
        st.markdown(f"""
        <div class="chat-message assistant-message">
            <strong>NOVA</strong><br>
            {clean_content}
        </div>
        """, unsafe_allow_html=True)

def clean_response(response):
    """Clean up JSON responses to make them readable for users."""
    import json
    import re
    
    # Try to parse as JSON first
    try:
        data = json.loads(response)
        
        # If it's a JSON object, format it nicely
        if isinstance(data, dict):
            if 'messages' in data and 'cta' in data:
                # This looks like the specific format you mentioned
                messages = data.get('messages', [])
                cta = data.get('cta', '')
                
                result = ""
                for msg in messages:
                    if 'message' in msg:
                        result += f"**{msg['message']}**\n\n"
                
                if cta:
                    result += f"**Call-to-Action:** {cta}"
                
                return result
            else:
                # Generic JSON formatting
                return json.dumps(data, indent=2)
        else:
            return str(data)
    
    except (json.JSONDecodeError, TypeError):
        # If it's not JSON, return as is
        return response

def save_chat_session():
    """Save current chat session to history."""
    if st.session_state.messages:
        session_id = f"session_{len(st.session_state.chat_sessions) + 1}"
        session_data = {
            "id": session_id,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "messages": st.session_state.messages.copy(),
            "preview": st.session_state.messages[0]["content"][:50] + "..." if st.session_state.messages else "New Chat"
        }
        st.session_state.chat_sessions.append(session_data)
        st.session_state.current_session_id = session_id

def load_chat_session(session_id):
    """Load a specific chat session."""
    for session in st.session_state.chat_sessions:
        if session["id"] == session_id:
            st.session_state.messages = session["messages"].copy()
            st.session_state.current_session_id = session_id
            break

def main():
    # Simple header
    st.markdown("""
    <div class="header-container">
        <h1 class="main-header">NOVA</h1>
        <p class="sub-header">AI Message Crafter by EVOKE AI</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Minimalistic sidebar
    with st.sidebar:
        st.markdown("### 💬 Chat History")
        
        # New chat button
        if st.button("➕ New Chat", type="primary", use_container_width=True):
            st.session_state.messages = []
            st.session_state.conversation_history = []
            st.session_state.current_session_id = None
            st.rerun()
        
        st.markdown("---")
        
        # Display chat history
        if st.session_state.chat_sessions:
            for session in reversed(st.session_state.chat_sessions[-10:]):  # Show last 10
                is_selected = session["id"] == st.session_state.current_session_id
                selected_class = "selected" if is_selected else ""
                
                st.markdown(f"""
                <div class="chat-history-item {selected_class}">
                    <div class="chat-history-preview">{session['preview']}</div>
                    <div class="chat-history-time">{session['timestamp']}</div>
                </div>
                """, unsafe_allow_html=True)
                
                col1, col2 = st.columns([3, 1])
                with col1:
                    if st.button("Load", key=f"load_{session['id']}"):
                        load_chat_session(session["id"])
                        st.rerun()
                with col2:
                    if st.button("🗑️", key=f"delete_{session['id']}"):
                        st.session_state.chat_sessions = [s for s in st.session_state.chat_sessions if s["id"] != session["id"]]
                        if st.session_state.current_session_id == session["id"]:
                            st.session_state.messages = []
                            st.session_state.current_session_id = None
                        st.rerun()
        
        # Save current chat if there are messages
        if st.session_state.messages and st.session_state.current_session_id is None:
            if st.button("💾 Save Chat", use_container_width=True):
                save_chat_session()
                st.rerun()
    
    # Simple chat interface
    if not st.session_state.messages:
        st.markdown("""
        <div style="text-align: center; padding: 2rem; background: #f8fafc; border-radius: 12px; margin-bottom: 1rem;">
            <h3 style="color: #4a5568; margin-bottom: 1rem;">👋 Welcome to NOVA!</h3>
            <p style="color: #718096; margin: 0;">Start a conversation with your AI message crafter.</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Display chat messages
    for message in st.session_state.messages:
        display_chat_message(
            message["role"], 
            message["content"], 
            message.get("timestamp")
        )
    
    # Chat input
    if prompt := st.chat_input("Type your message here..."):
        # Add user message to chat
        timestamp = datetime.now().strftime("%H:%M:%S")
        st.session_state.messages.append({
            "role": "user", 
            "content": prompt, 
            "timestamp": timestamp
        })
        
        # Add to conversation history
        st.session_state.conversation_history.append({
            "role": "user", 
            "content": prompt
        })
        
        # Display user message
        display_chat_message("user", prompt, timestamp)
        
        # Get NOVA response
        if initialize_nova_client():
            with st.spinner("NOVA is thinking..."):
                try:
                    response = st.session_state.nova_client.send_message(
                        prompt, 
                        use_assistant=True
                    )
                    
                    # Add assistant response to chat
                    response_timestamp = datetime.now().strftime("%H:%M:%S")
                    st.session_state.messages.append({
                        "role": "assistant", 
                        "content": response, 
                        "timestamp": response_timestamp
                    })
                    
                    # Add to conversation history
                    st.session_state.conversation_history.append({
                        "role": "assistant", 
                        "content": response
                    })
                    
                    # Display assistant response
                    display_chat_message("assistant", response, response_timestamp)
                    
                except Exception as e:
                    error_msg = f"Sorry, I encountered an error: {str(e)}"
                    st.session_state.messages.append({
                        "role": "assistant", 
                        "content": error_msg, 
                        "timestamp": datetime.now().strftime("%H:%M:%S")
                    })
                    display_chat_message("assistant", error_msg)
        else:
            st.error("Please check your API configuration.")
    
    # Auto-save session after getting a response
    if len(st.session_state.messages) >= 2 and st.session_state.current_session_id is None:
        save_chat_session()

# Simple footer
st.markdown("---")
st.markdown("**NOVA** - AI Message Crafter by EVOKE AI")

if __name__ == "__main__":
    main()
