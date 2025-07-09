"""
Core Agent implementation using LangChain.
Integrates LLM, memory, and tools for todo management.
"""

from langchain.agents import AgentExecutor, create_react_agent
from langchain.memory import ConversationBufferMemory
from langchain_core.prompts import PromptTemplate
from langchain_core.tools import Tool
from typing import Dict, Any, List
import logging

from .llm import create_gemini_llm
from .tools import initialize_tools, ALL_TOOLS
from .memory import MemoryManager

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class GeminiTodoAgent:
    """Main agent class that handles conversations and todo management."""
    
    def __init__(self, data_dir: str = "data"):
        """Initialize the agent with memory and tools."""
        self.data_dir = data_dir
        self.memory_manager = initialize_tools(data_dir)
        self.llm = create_gemini_llm()
        self.tools = ALL_TOOLS
        self.agent_executor = self._create_agent()
        
        logger.info("Gemini Todo Agent initialized successfully")
    
    def _create_agent_prompt(self) -> PromptTemplate:
        """Create the agent prompt template with proper ReAct format."""
        template = """You are a helpful personal assistant that manages todo lists and holds conversations.

Your capabilities:
- Add, remove, and list todo items
- Remember the user's name and conversation history
- Provide helpful responses and maintain context
- Be friendly and conversational

Available tools:
{tools}

Use the following format EXACTLY:

Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question

IMPORTANT: If the user is just greeting or having casual conversation, respond directly without using tools unless they specifically ask about todos or their name.

Current user context: {context}

Question: {input}
Thought: {agent_scratchpad}"""
        
        return PromptTemplate(
            template=template,
            input_variables=["input", "context", "tools", "tool_names", "agent_scratchpad"]
        )
    
    def _create_agent(self) -> AgentExecutor:
        """Create the LangChain agent executor."""
        try:
            # Create the prompt
            prompt = self._create_agent_prompt()
            
            # Create the agent
            agent = create_react_agent(
                llm=self.llm,
                tools=self.tools,
                prompt=prompt
            )
            
            # Create agent executor with better error handling
            agent_executor = AgentExecutor(
                agent=agent,
                tools=self.tools,
                verbose=False,  # Enable verbose for debugging
                handle_parsing_errors=True,
                max_iterations=10,  # Reduced iterations
                max_execution_time=30,  # Reduced timeout
                return_intermediate_steps=False
            )
            
            return agent_executor
            
        except Exception as e:
            logger.error(f"Error creating agent: {e}")
            raise
    
    def chat(self, user_input: str) -> str:
        """
        Process user input and return agent response.
        
        Args:
            user_input: The user's message
            
        Returns:
            Agent's response
        """
        try:
            # Simple responses for basic greetings
            user_lower = user_input.lower()
            if user_lower in ['hi', 'hello', 'hey', 'good morning', 'good afternoon', 'good evening']:
                user_name = self.memory_manager.get_user_name()
                response = f"Hello {user_name}! How can I help you today? I can manage your todos or just chat with you."
                self.memory_manager.add_conversation(user_input, response)
                return response
            
            # Get context for the conversation
            context = self.memory_manager.get_context_for_llm()
            
            # Prepare input for agent
            agent_input = {
                "input": user_input,
                "context": context,
                "tools": "\n".join([f"{tool.name}: {tool.description}" for tool in self.tools]),
                "tool_names": ", ".join([tool.name for tool in self.tools])
            }
            
            # Get response from agent
            response = self.agent_executor.invoke(agent_input)
            agent_response = response["output"]
            
            # Save conversation to memory
            self.memory_manager.add_conversation(user_input, agent_response)
            
            return agent_response
            
        except Exception as e:
            logger.error(f"Error in chat: {e}")
            error_response = f"I apologize, but I encountered an error: {str(e)}. Please try again."
            self.memory_manager.add_conversation(user_input, error_response)
            return error_response
    
    def get_stats(self) -> Dict[str, Any]:
        """Get agent and memory statistics."""
        stats = self.memory_manager.get_stats()
        stats.update({
            "agent_type": "Gemini Todo Agent",
            "tools_available": len(self.tools),
            "llm_model": self.llm.model_name
        })
        return stats
    
    def reset_conversation(self):
        """Reset conversation history but keep todos."""
        self.memory_manager.memory["conversation_history"] = []
        self.memory_manager.save_memory()
        logger.info("Conversation history reset")
    
    def export_todos(self) -> List[Dict[str, Any]]:
        """Export all todos for backup."""
        return self.memory_manager.memory["todos"]
    
    def get_welcome_message(self) -> str:
        """Get a personalized welcome message."""
        user_name = self.memory_manager.get_user_name()
        stats = self.memory_manager.get_stats()
        
        if user_name and user_name != "Friend":
            welcome = f"Welcome back, {user_name}! "
        else:
            welcome = "Hello! I'm your personal todo assistant. "
        
        welcome += f"You have {stats['active_todos']} active todos. How can I help you today?"
        
        return welcome