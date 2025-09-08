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

# NOVA Message Crafter SaaS styling
st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Global Styles */
    .main .block-container {
        padding-top: 1rem;
        padding-bottom: 1rem;
        max-width: 1200px;
    }
    
    /* Header with Logo and Branding */
    .header-container {
        text-align: center;
        margin-bottom: 2rem;
        padding: 2rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 16px;
        color: white;
    }
    
    .logo-section {
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 1rem;
        margin-bottom: 1rem;
    }
    
    .logo {
        width: 60px;
        height: 60px;
        background: rgba(255, 255, 255, 0.2);
        border-radius: 16px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 28px;
        color: white;
        font-weight: bold;
        backdrop-filter: blur(10px);
        border: 2px solid rgba(255, 255, 255, 0.3);
    }
    
    .main-header {
        font-family: 'Inter', sans-serif;
        font-size: 2.5rem;
        font-weight: 700;
        color: white;
        margin: 0;
        text-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    }
    
    .sub-header {
        font-family: 'Inter', sans-serif;
        font-size: 1.1rem;
        color: rgba(255, 255, 255, 0.9);
        margin: 0.5rem 0 0 0;
        font-weight: 400;
    }
    
    .company-badge {
        display: inline-block;
        background: rgba(255, 255, 255, 0.2);
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-size: 0.9rem;
        font-weight: 500;
        margin-top: 1rem;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.3);
    }
    
    /* Message Crafter Specific Styling */
    .message-craft-section {
        background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
        padding: 2rem;
        border-radius: 16px;
        margin-bottom: 2rem;
        border: 1px solid #e2e8f0;
    }
    
    .craft-features {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 1rem;
        margin: 1.5rem 0;
    }
    
    .feature-card {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        text-align: center;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
        border: 1px solid #e2e8f0;
        transition: all 0.3s ease;
    }
    
    .feature-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);
    }
    
    .feature-icon {
        font-size: 2rem;
        margin-bottom: 1rem;
    }
    
    .feature-title {
        font-weight: 600;
        color: #1f2937;
        margin-bottom: 0.5rem;
    }
    
    .feature-desc {
        font-size: 0.9rem;
        color: #6b7280;
    }
    
    /* Chat Message Styling */
    .chat-message {
        font-family: 'Inter', sans-serif;
        padding: 1.5rem;
        margin-bottom: 1rem;
        border-radius: 16px;
        line-height: 1.6;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
        border: 1px solid #e2e8f0;
    }
    
    .user-message {
        background: linear-gradient(135deg, #e3f2fd 0%, #f0f8ff 100%);
        margin-left: 3rem;
        border-left: 4px solid #3b82f6;
    }
    
    .assistant-message {
        background: linear-gradient(135deg, #f3e5f5 0%, #fce4ec 100%);
        margin-right: 3rem;
        border-left: 4px solid #9c27b0;
    }
    
    .message-type-badge {
        display: inline-block;
        background: #667eea;
        color: white;
        padding: 0.25rem 0.75rem;
        border-radius: 12px;
        font-size: 0.8rem;
        font-weight: 500;
        margin-bottom: 0.5rem;
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
        transform: translateX(4px);
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
    
    /* Sidebar styling */
    .css-1d391kg {
        background-color: #f9fafb;
    }
    
    /* Button styling */
    .stButton > button {
        font-family: 'Inter', sans-serif;
        border-radius: 6px;
        transition: all 0.2s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-1px);
    }
    
    /* Input styling */
    .stChatInput > div > div > div > div {
        border-radius: 8px;
        border: 1px solid #d1d5db;
    }
    
    .stChatInput > div > div > div > div:focus-within {
        border-color: #3b82f6;
        box-shadow: 0 0 0 2px rgba(59, 130, 246, 0.1);
    }
    
    /* Metrics styling */
    .metric-container {
        background-color: #f8fafc;
        padding: 1rem;
        border-radius: 8px;
        border: 1px solid #e2e8f0;
        margin: 1rem 0;
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
    # Header with NOVA Message Crafter branding
    st.markdown("""
    <div class="header-container">
        <div class="logo-section">
            <div class="logo">N</div>
            <div>
                <h1 class="main-header">NOVA</h1>
                <p class="sub-header">AI Message Crafter</p>
            </div>
        </div>
        <div class="company-badge">Developed by EVOKE AI</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Message Crafter Features Section
    st.markdown("""
    <div class="message-craft-section">
        <h2 style="text-align: center; color: #1f2937; margin-bottom: 1rem;">🎯 Craft Perfect Messages with AI</h2>
        <p style="text-align: center; color: #6b7280; margin-bottom: 2rem;">Transform your communication with intelligent message crafting powered by advanced AI technology</p>
        
        <div class="craft-features">
            <div class="feature-card">
                <div class="feature-icon">📧</div>
                <div class="feature-title">Email Marketing</div>
                <div class="feature-desc">Craft compelling email campaigns and newsletters</div>
            </div>
            <div class="feature-card">
                <div class="feature-icon">📱</div>
                <div class="feature-title">Social Media</div>
                <div class="feature-desc">Create engaging posts for all platforms</div>
            </div>
            <div class="feature-card">
                <div class="feature-icon">💼</div>
                <div class="feature-title">Business Communication</div>
                <div class="feature-desc">Professional messages and proposals</div>
            </div>
            <div class="feature-card">
                <div class="feature-icon">🎨</div>
                <div class="feature-title">Creative Writing</div>
                <div class="feature-desc">Stories, content, and creative pieces</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar with message crafting tools
    with st.sidebar:
        st.markdown("### 🛠️ Message Crafting Tools")
        
        # Quick message templates
        st.markdown("#### 📝 Quick Templates")
        template_buttons = [
            ("📧", "Email Campaign", "Create a compelling email campaign"),
            ("📱", "Social Post", "Craft a social media post"),
            ("💼", "Business Proposal", "Write a professional proposal"),
            ("🎯", "Marketing Copy", "Generate marketing content"),
            ("📰", "Newsletter", "Create a newsletter"),
            ("💬", "Customer Support", "Draft a support response")
        ]
        
        for emoji, title, desc in template_buttons:
            if st.button(f"{emoji} {title}", key=f"template_{title}", help=desc):
                prompt = f"Help me create a {title.lower()}. {desc}"
                st.session_state.messages.append({
                    "role": "user", 
                    "content": prompt, 
                    "timestamp": datetime.now().strftime("%H:%M:%S")
                })
                st.rerun()
        
        st.markdown("---")
        
        # Chat history
        st.markdown("#### 💬 Message History")
        
        # Save current session if there are messages
        if st.session_state.messages and st.session_state.current_session_id is None:
            if st.button("💾 Save Current Session"):
                save_chat_session()
                st.rerun()
        
        # Display chat history
        if st.session_state.chat_sessions:
            for session in reversed(st.session_state.chat_sessions[-5:]):  # Show last 5
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
                    if st.button(f"Load", key=f"load_{session['id']}"):
                        load_chat_session(session["id"])
                        st.rerun()
                with col2:
                    if st.button(f"🗑️", key=f"delete_{session['id']}"):
                        st.session_state.chat_sessions = [s for s in st.session_state.chat_sessions if s["id"] != session["id"]]
                        if st.session_state.current_session_id == session["id"]:
                            st.session_state.messages = []
                            st.session_state.current_session_id = None
                        st.rerun()
        
        st.markdown("---")
        
        # Settings
        st.markdown("#### ⚙️ Crafting Settings")
        
        # Status check
        if initialize_nova_client():
            st.success("✅ NOVA Ready")
        else:
            st.error("❌ NOVA Not Ready")
        
        # Clear current chat
        if st.button("🗑️ Clear Session"):
            st.session_state.messages = []
            st.session_state.conversation_history = []
            st.session_state.current_session_id = None
            st.rerun()
        
        # Model selection
        model = st.selectbox("AI Model", ["gpt-4o-mini", "gpt-4", "gpt-3.5-turbo"], index=0)
        
        # Creativity level
        temperature = st.slider("Creativity Level", 0.0, 1.0, 0.7, 0.1, help="Higher = more creative, Lower = more focused")
        
        # Stats
        if st.session_state.messages:
            st.markdown("#### 📊 Session Stats")
            st.metric("Messages Crafted", len(st.session_state.messages))
            user_messages = len([msg for msg in st.session_state.messages if msg["role"] == "user"])
            st.metric("Your Requests", user_messages)
    
    # Message Crafting Interface
    st.markdown("### 🎯 Message Crafting Studio")
    
    # Welcome message if no messages
    if not st.session_state.messages:
        st.markdown("""
        <div style="text-align: center; padding: 2rem; background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%); border-radius: 16px; margin-bottom: 1rem;">
            <h3 style="color: #4a5568; margin-bottom: 1rem;">🚀 Ready to Craft Amazing Messages!</h3>
            <p style="color: #718096; margin-bottom: 1rem;">Tell NOVA what kind of message you want to create, or use the quick templates in the sidebar.</p>
            <div style="display: flex; justify-content: center; gap: 1rem; flex-wrap: wrap;">
                <span style="background: #667eea; color: white; padding: 0.5rem 1rem; border-radius: 20px; font-size: 0.9rem;">📧 Email Marketing</span>
                <span style="background: #667eea; color: white; padding: 0.5rem 1rem; border-radius: 20px; font-size: 0.9rem;">📱 Social Media</span>
                <span style="background: #667eea; color: white; padding: 0.5rem 1rem; border-radius: 20px; font-size: 0.9rem;">💼 Business</span>
                <span style="background: #667eea; color: white; padding: 0.5rem 1rem; border-radius: 20px; font-size: 0.9rem;">🎨 Creative</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Display chat messages
    for message in st.session_state.messages:
        display_chat_message(
            message["role"], 
            message["content"], 
            message.get("timestamp")
        )
    
    # Message crafting input
    if prompt := st.chat_input("Describe the message you want to create..."):
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
            with st.spinner("NOVA is crafting your message..."):
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

# Footer with EVOKE AI branding
st.markdown("---")
st.markdown("""
<div style="text-align: center; padding: 2rem; background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%); border-radius: 12px; margin-top: 2rem;">
    <h4 style="color: #1f2937; margin-bottom: 0.5rem;">🤖 NOVA - AI Message Crafter</h4>
    <p style="color: #6b7280; margin: 0;">Developed by <strong>EVOKE AI</strong> • Powered by OpenAI</p>
    <p style="color: #9ca3af; font-size: 0.9rem; margin: 0.5rem 0 0 0;">Transform your communication with intelligent message crafting</p>
</div>
""", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
