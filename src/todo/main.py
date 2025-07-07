"""
Gemini Agent Todo - Day 3 Complete Application
A conversational AI agent that manages todo lists using Google Gemini and LangChain.
"""

import os
import sys
import argparse
from dotenv import load_dotenv

# from src.todo.config import Config
from src.todo.cli import TodoCLI

# Load environment variables
load_dotenv()

def check_dependencies():
    """Check if all required dependencies are available."""
    try:
        print("✓ All dependencies are installed")
        return True
    except ImportError as e:
        print(f"Missing dependency: {e}")
        print("Please install dependencies with: uv add langchain langgraph google-generativeai colorama")
        return False

def main():
    """Main application entry point."""
    parser = argparse.ArgumentParser(description="Gemini Todo Agent - AI-powered todo management")
    parser.add_argument("--data-dir", default="data", help="Directory for storing data files")
    parser.add_argument("--test", action="store_true", help="Run component tests")
    parser.add_argument("--version", action="version", version="Gemini Todo Agent 1.0.0")
    
    args = parser.parse_args()
    
    # Check dependencies
    if not check_dependencies():
        return 1
    
    # Run tests if requested
    if args.test:
        from src.todo.test_components import run_all_tests
        return run_all_tests()
    
    # Check API key
    if not os.getenv('GEMINI_API_KEY'):
        print("GEMINI_API_KEY not found in environment variables")
        print("Please create a .env file with your API key:")
        print("GEMINI_API_KEY=your_api_key_here")
        return 1
    
    # Run the CLI application
    try:
        cli = TodoCLI(data_dir=args.data_dir)
        cli.run()
        return 0
    except KeyboardInterrupt:
        print("\nGoodbye!")
        return 0
    except Exception as e:
        print(f"Application error: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())