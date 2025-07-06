"""
Enhanced CLI interface for the Gemini Todo Agent.
Provides a smooth conversational experience.
"""

import os
import sys
from typing import Optional
# import readline  # For better input handling
from colorama import  Fore, Style, init

from .agent import GeminiTodoAgent
from .config import Config

# Initialize colorama for cross-platform colored output
init(autoreset=True)

class TodoCLI:
    """Command-line interface for the todo agent."""
    
    def __init__(self, data_dir: str = "data"):
        """Initialize the CLI with the agent."""
        self.data_dir = data_dir
        self.agent: Optional[GeminiTodoAgent] = None
        self.running = True
        
        # CLI commands
        self.commands = {
            '/help': self.show_help,
            '/stats': self.show_stats,
            '/reset': self.reset_conversation,
            '/export': self.export_todos,
            '/clear': self.clear_screen,
            '/quit': self.quit_app,
            '/exit': self.quit_app,
        }
    
    def initialize_agent(self) -> bool:
        """Initialize the agent with error handling."""
        try:
            print(f"{Fore.YELLOW}Initializing Gemini Todo Agent...{Style.RESET_ALL}")
            
            # Validate configuration
            Config.validate()
            
            # Create agent
            self.agent = GeminiTodoAgent(self.data_dir)
            
            print(f"{Fore.GREEN}✓ Agent initialized successfully!{Style.RESET_ALL}")
            return True
            
        except ValueError as e:
            print(f"{Fore.RED}❌ Configuration Error: {e}{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}Please check your .env file and ensure GEMINI_API_KEY is set.{Style.RESET_ALL}")
            return False
        except Exception as e:
            print(f"{Fore.RED}❌ Initialization Error: {e}{Style.RESET_ALL}")
            return False
    
    def show_welcome(self):
        """Display welcome message and instructions."""
        print(f"{Fore.CYAN}{'='*60}")
        print(f"{Fore.CYAN}🤖 GEMINI TODO AGENT")
        print(f"{Fore.CYAN}{'='*60}")
        print(f"{Fore.WHITE}Your AI-powered personal todo assistant")
        print(f"{Fore.WHITE}Type '/help' for commands or just start chatting!")
        print(f"{Fore.CYAN}{'='*60}{Style.RESET_ALL}")
        
        if self.agent:
            welcome_msg = self.agent.get_welcome_message()
            print(f"{Fore.GREEN}🤖 Assistant: {welcome_msg}{Style.RESET_ALL}")
    
    def show_help(self):
        """Display help information."""
        help_text = f"""
{Fore.CYAN}Available Commands:{Style.RESET_ALL}
{Fore.YELLOW}/help{Style.RESET_ALL}    - Show this help message
{Fore.YELLOW}/stats{Style.RESET_ALL}   - Show memory and usage statistics
{Fore.YELLOW}/reset{Style.RESET_ALL}   - Reset conversation history (keeps todos)
{Fore.YELLOW}/export{Style.RESET_ALL}  - Export todos to view all items
{Fore.YELLOW}/clear{Style.RESET_ALL}   - Clear the screen
{Fore.YELLOW}/quit{Style.RESET_ALL}    - Exit the application

{Fore.CYAN}Example Conversations:{Style.RESET_ALL}
• "Add 'Buy groceries' to my todo list"
• "What's on my todo list?"
• "Remove 'finish project' from my todos"
• "My name is Alice"
• "Show me my stats"

{Fore.CYAN}Natural Language:{Style.RESET_ALL}
Just chat naturally! The agent understands context and remembers your name.
        """
        print(help_text)
    
    def show_stats(self):
        """Display agent statistics."""
        if not self.agent:
            print(f"{Fore.RED}Agent not initialized.{Style.RESET_ALL}")
            return
        
        stats = self.agent.get_stats()
        print(f"\n{Fore.CYAN}📊 Your Statistics:{Style.RESET_ALL}")
        print(f"{Fore.WHITE}👤 Name: {stats['user_name']}")
        print(f"{Fore.WHITE}📝 Active Todos: {stats['active_todos']}")
        print(f"{Fore.WHITE}✅ Completed Todos: {stats['completed_todos']}")
        print(f"{Fore.WHITE}💬 Total Conversations: {stats['total_conversations']}")
        print(f"{Fore.WHITE}🤖 AI Model: {stats['llm_model']}")
        print(f"{Fore.WHITE}⚙️ Tools Available: {stats['tools_available']}{Style.RESET_ALL}")
    
    def reset_conversation(self):
        """Reset conversation history."""
        if not self.agent:
            print(f"{Fore.RED}Agent not initialized.{Style.RESET_ALL}")
            return
        
        confirm = input(f"{Fore.YELLOW}Are you sure you want to reset conversation history? (y/N): {Style.RESET_ALL}")
        if confirm.lower() in ['y', 'yes']:
            self.agent.reset_conversation()
            print(f"{Fore.GREEN}✓ Conversation history reset. Your todos are preserved.{Style.RESET_ALL}")
        else:
            print(f"{Fore.BLUE}Reset cancelled.{Style.RESET_ALL}")
    
    def export_todos(self):
        """Export and display all todos."""
        if not self.agent:
            print(f"{Fore.RED}Agent not initialized.{Style.RESET_ALL}")
            return
        
        todos = self.agent.export_todos()
        
        if not todos:
            print(f"{Fore.BLUE}No todos found.{Style.RESET_ALL}")
            return
        
        print(f"\n{Fore.CYAN}📋 All Your Todos:{Style.RESET_ALL}")
        
        active_todos = [todo for todo in todos if not todo['completed']]
        completed_todos = [todo for todo in todos if todo['completed']]
        
        if active_todos:
            print(f"\n{Fore.YELLOW}🔄 Active Todos:{Style.RESET_ALL}")
            for i, todo in enumerate(active_todos, 1):
                print(f"{Fore.WHITE}  {i}. {todo['task']} (Created: {todo['created_at'][:10]})")
        
        if completed_todos:
            print(f"\n{Fore.GREEN}✅ Completed Todos:{Style.RESET_ALL}")
            for i, todo in enumerate(completed_todos, 1):
                print(f"{Fore.WHITE}  {i}. {todo['task']} (Created: {todo['created_at'][:10]})")
    
    def clear_screen(self):
        """Clear the terminal screen."""
        os.system('cls' if os.name == 'nt' else 'clear')
        self.show_welcome()
    
    def quit_app(self):
        """Quit the application."""
        print(f"{Fore.GREEN}👋 Thanks for using Gemini Todo Agent! Goodbye!{Style.RESET_ALL}")
        self.running = False
    
    def process_input(self, user_input: str) -> str:
        """Process user input and return response."""
        user_input = user_input.strip()
        
        if not user_input:
            return ""
        
        # Handle commands
        if user_input.startswith('/'):
            command = user_input.split()[0].lower()
            if command in self.commands:
                self.commands[command]()
                return ""
            else:
                return f"{Fore.RED}Unknown command: {command}. Type '/help' for available commands.{Style.RESET_ALL}"
        
        # Handle regular conversation
        if not self.agent:
            return f"{Fore.RED}Agent not initialized. Please restart the application.{Style.RESET_ALL}"
        
        try:
            response = self.agent.chat(user_input)
            return f"{Fore.GREEN}🤖 Assistant: {response}{Style.RESET_ALL}"
        except Exception as e:
            return f"{Fore.RED}❌ Error: {str(e)}{Style.RESET_ALL}"
    
    def run(self):
        """Main CLI loop."""
        # Initialize agent
        if not self.initialize_agent():
            return
        
        # Show welcome
        self.show_welcome()
        
        print(f"\n{Fore.CYAN}Type your message and press Enter to chat, or type '/help' for commands.{Style.RESET_ALL}")
        
        # Main conversation loop
        while self.running:
            try:
                # Get user input
                user_input = input(f"\n{Fore.BLUE}You: {Style.RESET_ALL}").strip()
                
                # Process input
                response = self.process_input(user_input)
                
                # Show response
                if response:
                    print(response)
                
            except KeyboardInterrupt:
                print(f"\n{Fore.YELLOW}Interrupted by user. Type '/quit' to exit gracefully.{Style.RESET_ALL}")
            except EOFError:
                print(f"\n{Fore.GREEN}Goodbye!{Style.RESET_ALL}")
                break
            except Exception as e:
                print(f"{Fore.RED}❌ Unexpected error: {str(e)}{Style.RESET_ALL}")

def main():
    """Main entry point for the CLI."""
    cli = TodoCLI()
    cli.run()

if __name__ == "__main__":
    main()