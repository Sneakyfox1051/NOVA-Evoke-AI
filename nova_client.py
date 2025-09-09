import os
import json
import time
from typing import Dict, List, Optional, Any
from openai import OpenAI
from dotenv import load_dotenv
import streamlit as st

# Load environment variables
load_dotenv()

class NovaClient:
    """
    A Python client for interacting with the NOVA OpenAI Assistant.
    """
    
    def __init__(self, api_key: Optional[str] = None, assistant_id: Optional[str] = None):
        """
        Initialize the NOVA client.
        
        Args:
            api_key (str, optional): OpenAI API key. If not provided, 
                                   will try to load from environment variables or use default.
            assistant_id (str, optional): Your specific OpenAI Assistant ID. If not provided,
                                        will try to load from environment or use default.
        """
        # Try multiple sources for API key
        self.api_key = (
            api_key or 
            os.getenv('OPENAI_API_KEY') or 
            st.secrets.get('OPENAI_API_KEY')
        )
        
        if not self.api_key:
            raise ValueError("OpenAI API key is required. Set OPENAI_API_KEY environment variable or pass it directly.")
        
        self.client = OpenAI(api_key=self.api_key)
        self.assistant_name = "NOVA"
        
        # Try multiple sources for assistant ID
        self.assistant_id = (
            assistant_id or 
            os.getenv('OPENAI_ASSISTANT_ID') or 
            st.secrets.get('OPENAI_ASSISTANT_ID') or
            "asst_XTd5ExJ9KUTLyrFkzkzPZa2f"  # Your specific assistant ID
        )
        
        # Initialize thread for conversations
        self.thread_id = None

    def health_check(self) -> Dict[str, Any]:
        """
        Check if the NOVA client is properly configured and can connect to OpenAI.
        
        Returns:
            Dict containing health status and configuration info
        """
        try:
            # Test basic API connection
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": "Hello"}],
                max_tokens=10
            )
            
            # Test assistant access
            assistant = self.client.beta.assistants.retrieve(self.assistant_id)
            
            return {
                "status": "healthy",
                "assistant_name": assistant.name,
                "assistant_id": self.assistant_id,
                "api_connected": True,
                "model": assistant.model
            }
            
        except Exception as e:
            return {
                "status": "unhealthy",
                "assistant_name": self.assistant_name,
                "assistant_id": self.assistant_id,
                "api_connected": False,
                "error": str(e)
            }

    def get_or_create_assistant(self) -> str:
        """
        Get the existing assistant or create a new one if it doesn't exist.
        
        Returns:
            str: The assistant ID
        """
        try:
            # Try to retrieve the existing assistant
            assistant = self.client.beta.assistants.retrieve(self.assistant_id)
            return assistant.id
        except Exception:
            # If assistant doesn't exist, create a new one
            assistant = self.client.beta.assistants.create(
                name=self.assistant_name,
                instructions=f"You are {self.assistant_name}, a helpful AI assistant. You are knowledgeable, friendly, and always ready to help with any questions or tasks.",
                model="gpt-4o-mini",
                tools=[{"type": "code_interpreter"}]
            )
            return assistant.id

    def create_thread(self) -> str:
        """
        Create a new conversation thread.
        
        Returns:
            str: The thread ID
        """
        thread = self.client.beta.threads.create()
        self.thread_id = thread.id
        return thread.id

    def list_assistants(self) -> List[Dict[str, Any]]:
        """
        List all available assistants.
        
        Returns:
            List of assistant information
        """
        try:
            assistants = self.client.beta.assistants.list()
            return [
                {
                    "id": assistant.id,
                    "name": assistant.name,
                    "model": assistant.model,
                    "created_at": assistant.created_at
                }
                for assistant in assistants.data
            ]
        except Exception as e:
            print(f"Error listing assistants: {e}")
            return []

    def set_assistant_by_id(self, assistant_id: str) -> bool:
        """
        Set the assistant by ID.
        
        Args:
            assistant_id (str): The assistant ID to use
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            assistant = self.client.beta.assistants.retrieve(assistant_id)
            self.assistant_id = assistant_id
            return True
        except Exception as e:
            print(f"Error setting assistant: {e}")
            return False

    def get_assistant_info(self) -> Optional[Dict[str, Any]]:
        """
        Get information about the current assistant.
        
        Returns:
            Dict containing assistant information or None if error
        """
        try:
            assistant = self.client.beta.assistants.retrieve(self.assistant_id)
            return {
                "id": assistant.id,
                "name": assistant.name,
                "model": assistant.model,
                "instructions": assistant.instructions,
                "created_at": assistant.created_at
            }
        except Exception as e:
            print(f"Error getting assistant info: {e}")
            return None

    def _send_message_to_assistant(self, message: str) -> str:
        """
        Send a message to the specific assistant using the Assistants API.
        
        Args:
            message (str): The message to send
            
        Returns:
            str: The assistant's response
        """
        try:
            # Ensure we have a thread
            if not self.thread_id:
                self.create_thread()
            
            # Add message to thread
            self.client.beta.threads.messages.create(
                thread_id=self.thread_id,
                role="user",
                content=message
            )
            
            # Run the assistant
            run = self.client.beta.threads.runs.create(
                thread_id=self.thread_id,
                assistant_id=self.assistant_id
            )
            
            # Wait for completion
            while run.status in ['queued', 'in_progress', 'cancelling']:
                time.sleep(1)
                run = self.client.beta.threads.runs.retrieve(
                    thread_id=self.thread_id,
                    run_id=run.id
                )
            
            if run.status == 'completed':
                # Get the response
                messages = self.client.beta.threads.messages.list(
                    thread_id=self.thread_id
                )
                
                # Get the latest assistant message
                for msg in messages.data:
                    if msg.role == "assistant":
                        return msg.content[0].text.value
                
                return "No response received from assistant."
            else:
                return f"Assistant run failed with status: {run.status}"
                
        except Exception as e:
            return f"Error communicating with assistant: {str(e)}"

    def _send_message_to_chat(self, message: str, model: str = "gpt-4o-mini", temperature: float = 0.7) -> str:
        """
        Send a message using the Chat Completions API.
        
        Args:
            message (str): The message to send
            model (str): The model to use
            temperature (float): The temperature setting
            
        Returns:
            str: The assistant's response
        """
        try:
            response = self.client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": f"You are {self.assistant_name}, a helpful AI assistant."},
                    {"role": "user", "content": message}
                ],
                temperature=temperature
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            return f"Error communicating with chat API: {str(e)}"

    def send_message(self, message: str, use_assistant: bool = True, model: str = "gpt-4o-mini", temperature: float = 0.7) -> str:
        """
        Send a message to NOVA.
        
        Args:
            message (str): The message to send
            use_assistant (bool): Whether to use the specific assistant or general chat
            model (str): The model to use (for chat completions)
            temperature (float): The temperature setting (for chat completions)
            
        Returns:
            str: The assistant's response
        """
        if use_assistant:
            return self._send_message_to_assistant(message)
        else:
            return self._send_message_to_chat(message, model, temperature)

    def clear_conversation(self):
        """Clear the current conversation thread."""
        self.thread_id = None

    def get_conversation_history(self) -> List[Dict[str, str]]:
        """
        Get the conversation history from the current thread.
        
        Returns:
            List of conversation messages
        """
        if not self.thread_id:
            return []
        
        try:
            messages = self.client.beta.threads.messages.list(
                thread_id=self.thread_id
            )
            
            history = []
            for msg in messages.data:
                if msg.role in ["user", "assistant"]:
                    content = msg.content[0].text.value if msg.content else ""
                    history.append({
                        "role": msg.role,
                        "content": content,
                        "timestamp": msg.created_at
                    })
            
            return history
            
        except Exception as e:
            print(f"Error getting conversation history: {e}")
            return []

    def export_conversation(self, filename: str = None) -> str:
        """
        Export the conversation history to a JSON file.
        
        Args:
            filename (str): The filename to save to (optional)
            
        Returns:
            str: The filename where the conversation was saved
        """
        if not filename:
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            filename = f"nova_conversation_{timestamp}.json"
        
        history = self.get_conversation_history()
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(history, f, indent=2, ensure_ascii=False)
        
        return filename

    def import_conversation(self, filename: str) -> bool:
        """
        Import a conversation history from a JSON file.
        
        Args:
            filename (str): The filename to load from
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                history = json.load(f)
            
            # Create a new thread
            self.create_thread()
            
            # Add messages to the thread
            for msg in history:
                if msg["role"] == "user":
                    self.client.beta.threads.messages.create(
                        thread_id=self.thread_id,
                        role="user",
                        content=msg["content"]
                    )
                elif msg["role"] == "assistant":
                    self.client.beta.threads.messages.create(
                        thread_id=self.thread_id,
                        role="assistant",
                        content=msg["content"]
                    )
            
            return True
            
        except Exception as e:
            print(f"Error importing conversation: {e}")
            return False

    def get_usage_stats(self) -> Dict[str, Any]:
        """
        Get usage statistics for the current session.
        
        Returns:
            Dict containing usage statistics
        """
        try:
            # This is a placeholder - OpenAI doesn't provide real-time usage stats
            # You would need to track this yourself or use the usage API
            return {
                "messages_sent": 0,  # Placeholder
                "tokens_used": 0,    # Placeholder
                "cost_estimate": 0.0  # Placeholder
            }
        except Exception as e:
            return {"error": str(e)}

    def __str__(self) -> str:
        """String representation of the NOVA client."""
        return f"NovaClient(assistant_id={self.assistant_id}, thread_id={self.thread_id})"

    def __repr__(self) -> str:
        """Detailed string representation of the NOVA client."""
        return f"NovaClient(assistant_id={self.assistant_id}, thread_id={self.thread_id}, api_connected={self.client is not None})"
