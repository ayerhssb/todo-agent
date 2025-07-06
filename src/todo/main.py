"""
Main entry point for the Gemini Agent Todo application.
Day 2: Testing components
"""

import os
from dotenv import load_dotenv
from src.todo.config import Config
from src.todo.memory import MemoryManager
from src.todo.tools import initialize_tools, ALL_TOOLS
from src.todo.llm import create_gemini_llm

# Load environment variables
load_dotenv()

def test_memory_system():
    """Test the memory management system."""
    print("Testing Memory System...")
    print("=" * 40)
    
    # Initialize memory
    memory = MemoryManager()
    
    # Test todo operations
    print(memory.add_todo("Learn LangChain"))
    print(memory.add_todo("Build Gemini Agent"))
    print(memory.list_todos())
    
    # Test conversation history
    memory.add_conversation("Hello!", "Hi there! How can I help you?")
    memory.set_user_name("Developer")
    
    # Get stats
    stats = memory.get_stats()
    print(f"\n Memory Stats:")
    print(f"   User: {stats['user_name']}")
    print(f"   Active todos: {stats['active_todos']}")
    print(f"   Conversations: {stats['total_conversations']}")
    
    print("Memory system test complete!\n")

def test_tools():
    """Test the LangChain tools."""
    print("Testing Tools...")
    print("=" * 40)
    
    # Initialize tools
    memory = initialize_tools()
    
    # Test each tool
    print("Testing add_todo:")
    print(ALL_TOOLS[0].run("Test task from tool"))
    
    print("\nTesting list_todos:")
    print(ALL_TOOLS[1].run({}))
    
    print("\nTesting set_user_name:")
    print(ALL_TOOLS[4].run("Alice"))
    
    print("\nTesting get_memory_stats:")
    print(ALL_TOOLS[5].run({}))
    
    print("Tools test complete!\n")

def test_llm():
    """Test the Gemini LLM integration."""
    print("Testing Gemini LLM...")
    print("=" * 40)
    
    try:
        # Validate config first
        Config.validate()
        print("Configuration validated")
        
        # Create LLM
        llm = create_gemini_llm()
        print("Gemini LLM created")
        
        # Test simple prompt
        response = llm("Say hello and introduce yourself as a helpful assistant.")
        print(f"LLM Response: {response}")
        
        print("LLM test complete!\n")
        
    except Exception as e:
        print(f"LLM test failed: {e}")
        print("Make sure your GEMINI_API_KEY is set in .env file\n")

def main():
    """Main function to run Day 2 tests."""
    print("Gemini Agent Todo - Day 2 Testing")
    print("=" * 50)
    
    # Check if API key is loaded
    api_key = os.getenv('GEMINI_API_KEY')
    if api_key:
        print("Gemini API Key loaded")
    else:
        print("Gemini API Key not found. Please check your .env file")
        return
    
    print(f"Using UV for dependency management")
    print(f"Python version: {os.sys.version}\n")
    
    # Run tests
    test_memory_system()
    test_tools()
    test_llm()
    
    print("Day 2 Component Tests Complete!")
    print("\nNext steps for Day 3:")
    print("1. Create the LangChain Agent")
    print("2. Add conversation loop")
    print("3. Polish the user experience")
    print("4. Create comprehensive README")

if __name__ == "__main__":
    main()