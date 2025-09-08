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
            st.secrets.get('OPENAI_API_KEY') or
            "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"
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
    
    def get_or_create_assistant(self) -> str:
        """
        Get existing NOVA assistant or create a new one.
        
        Returns:
            str: Assistant ID
        """
        try:
            # If we already have an assistant ID, return it
            if self.assistant_id:
                return self.assistant_id
            
            # List existing assistants to find NOVA
            assistants = self.client.beta.assistants.list()
            for assistant in assistants.data:
                if assistant.name == self.assistant_name:
                    self.assistant_id = assistant.id
                    return self.assistant_id
            
            # Create new NOVA assistant if not found
            assistant = self.client.beta.assistants.create(
                name=self.assistant_name,
                instructions=f"You are {self.assistant_name}, a helpful AI assistant. You are knowledgeable, friendly, and always ready to help with any questions or tasks.",
                model="gpt-4o-mini",
                tools=[{"type": "code_interpreter"}]
            )
            self.assistant_id = assistant.id
            return self.assistant_id
            
        except Exception as e:
            raise Exception(f"Failed to get or create assistant: {str(e)}")
    
    def create_thread(self) -> str:
        """
        Create a new conversation thread.
        
        Returns:
            str: Thread ID
        """
        try:
            thread = self.client.beta.threads.create()
            self.thread_id = thread.id
            return self.thread_id
        except Exception as e:
            raise Exception(f"Failed to create thread: {str(e)}")
    
    def send_message(self, message: str, use_assistant: bool = True) -> str:
        """
        Send a message to NOVA and get a response.
        
        Args:
            message (str): The message to send to NOVA
            use_assistant (bool): Whether to use the specific assistant or general chat
            
        Returns:
            str: NOVA's response
        """
        try:
            if use_assistant and self.assistant_id:
                return self._send_message_to_assistant(message)
            else:
                return self._send_message_to_chat(message)
        except Exception as e:
            return f"Error communicating with {self.assistant_name}: {str(e)}"
    
    def _send_message_to_assistant(self, message: str) -> str:
        """
        Send message to specific OpenAI Assistant.
        
        Args:
            message (str): The message to send
            
        Returns:
            str: Assistant's response
        """
        try:
            # Get or create assistant
            assistant_id = self.get_or_create_assistant()
            
            # Create thread if needed
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
                assistant_id=assistant_id
            )
            
            # Wait for completion
            while run.status in ['queued', 'in_progress', 'requires_action']:
                time.sleep(1)
                run = self.client.beta.threads.runs.retrieve(
                    thread_id=self.thread_id,
                    run_id=run.id
                )
            
            if run.status == 'completed':
                # Get the latest message
                messages = self.client.beta.threads.messages.list(
                    thread_id=self.thread_id
                )
                return messages.data[0].content[0].text.value
            else:
                return f"Assistant run failed with status: {run.status}"
                
        except Exception as e:
            return f"Error with assistant: {str(e)}"
    
    def _send_message_to_chat(self, message: str, model: str = "gpt-4o-mini", temperature: float = 0.7) -> str:
        """
        Send message using general chat completions API.
        
        Args:
            message (str): The message to send
            model (str): The OpenAI model to use
            temperature (float): Controls randomness
            
        Returns:
            str: Model's response
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
            return f"Error with chat completion: {str(e)}"
    
    def send_conversation(self, messages: List[Dict[str, str]], model: str = "gpt-4", temperature: float = 0.7) -> str:
        """
        Send a conversation history to NOVA.
        
        Args:
            messages (List[Dict[str, str]]): List of message dictionaries with 'role' and 'content'
            model (str): The OpenAI model to use (default: gpt-4)
            temperature (float): Controls randomness (0.0 to 1.0, default: 0.7)
            
        Returns:
            str: NOVA's response
        """
        try:
            # Add system message if not present
            if not messages or messages[0].get('role') != 'system':
                messages.insert(0, {"role": "system", "content": f"You are {self.assistant_name}, a helpful AI assistant."})
            
            response = self.client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=temperature
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            return f"Error communicating with {self.assistant_name}: {str(e)}"
    
    def get_available_models(self) -> List[str]:
        """
        Get list of available OpenAI models.
        
        Returns:
            List[str]: List of available model names
        """
        try:
            models = self.client.models.list()
            return [model.id for model in models.data]
        except Exception as e:
            print(f"Error fetching models: {str(e)}")
            return []
    
    def create_assistant(self, name: str = None, instructions: str = None, model: str = "gpt-4") -> Dict[str, Any]:
        """
        Create a new OpenAI assistant (if you want to use the Assistants API).
        
        Args:
            name (str): Name for the assistant
            instructions (str): Instructions for the assistant
            model (str): Model to use for the assistant
            
        Returns:
            Dict[str, Any]: Assistant creation response
        """
        try:
            assistant = self.client.beta.assistants.create(
                name=name or self.assistant_name,
                instructions=instructions or f"You are {self.assistant_name}, a helpful AI assistant.",
                model=model
            )
            return {
                "id": assistant.id,
                "name": assistant.name,
                "model": assistant.model,
                "created_at": assistant.created_at
            }
        except Exception as e:
            return {"error": f"Error creating assistant: {str(e)}"}
    
    def list_assistants(self) -> List[Dict[str, Any]]:
        """
        List all available assistants.
        
        Returns:
            List[Dict[str, Any]]: List of assistant information
        """
        try:
            assistants = self.client.beta.assistants.list()
            return [
                {
                    "id": assistant.id,
                    "name": assistant.name,
                    "model": assistant.model,
                    "created_at": assistant.created_at,
                    "instructions": assistant.instructions[:100] + "..." if len(assistant.instructions) > 100 else assistant.instructions
                }
                for assistant in assistants.data
            ]
        except Exception as e:
            return [{"error": f"Failed to list assistants: {str(e)}"}]
    
    def set_assistant_by_id(self, assistant_id: str) -> bool:
        """
        Set the assistant ID to use a specific assistant.
        
        Args:
            assistant_id (str): The assistant ID to use
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # Verify the assistant exists
            assistant = self.client.beta.assistants.retrieve(assistant_id)
            self.assistant_id = assistant_id
            self.assistant_name = assistant.name
            return True
        except Exception as e:
            return False
    
    def get_assistant_info(self) -> Dict[str, Any]:
        """
        Get information about the current assistant.
        
        Returns:
            Dict[str, Any]: Assistant information
        """
        try:
            if not self.assistant_id:
                return {"error": "No assistant ID set"}
            
            assistant = self.client.beta.assistants.retrieve(self.assistant_id)
            return {
                "id": assistant.id,
                "name": assistant.name,
                "model": assistant.model,
                "instructions": assistant.instructions,
                "tools": [tool.type for tool in assistant.tools],
                "created_at": assistant.created_at
            }
        except Exception as e:
            return {"error": f"Failed to get assistant info: {str(e)}"}
    
    def health_check(self) -> Dict[str, Any]:
        """
        Check if the API connection is working.
        
        Returns:
            Dict[str, Any]: Health check status
        """
        try:
            # Test basic API connection
            models = self.client.models.list()
            
            # Test assistant functionality if we have an assistant ID
            assistant_info = None
            if self.assistant_id:
                try:
                    assistant_info = self.get_assistant_info()
                except:
                    pass
            
            # Simple test message
            response = self.send_message("Hello, are you working?", use_assistant=False)
            
            return {
                "status": "healthy",
                "assistant_name": self.assistant_name,
                "assistant_id": self.assistant_id,
                "api_connected": True,
                "assistant_info": assistant_info,
                "test_response": response[:100] + "..." if len(response) > 100 else response
            }
        except Exception as e:
            return {
                "status": "unhealthy",
                "assistant_name": self.assistant_name,
                "assistant_id": self.assistant_id,
                "api_connected": False,
                "error": str(e)
            }


# Example usage and testing
if __name__ == "__main__":
    # Initialize NOVA client
    nova = NovaClient()
    
    # Health check
    print("=== NOVA Health Check ===")
    health = nova.health_check()
    print(json.dumps(health, indent=2))
    print()
    
    # Test basic message
    print("=== Testing Basic Message ===")
    response = nova.send_message("Hello NOVA! Can you tell me a joke?")
    print(f"NOVA: {response}")
    print()
    
    # Test conversation
    print("=== Testing Conversation ===")
    conversation = [
        {"role": "user", "content": "What's the weather like?"},
        {"role": "assistant", "content": "I don't have access to real-time weather data, but I can help you find weather information if you tell me your location."},
        {"role": "user", "content": "I'm in New York. Can you help me understand what I should wear today?"}
    ]
    response = nova.send_conversation(conversation)
    print(f"NOVA: {response}")
    print()
    
    # List available models
    print("=== Available Models ===")
    models = nova.get_available_models()
    print(f"Found {len(models)} models")
    for model in models[:5]:  # Show first 5 models
        print(f"- {model}")
    if len(models) > 5:
        print(f"... and {len(models) - 5} more")
