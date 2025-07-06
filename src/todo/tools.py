"""
LangChain tools for todo management and conversation.
"""

from langchain.tools import tool
from typing import Optional
from .memory import MemoryManager

# Global memory manager instance
memory_manager = None

def initialize_tools(data_dir: str = "data") -> MemoryManager:
    """Initialize the memory manager for tools."""
    global memory_manager
    memory_manager = MemoryManager(data_dir)
    return memory_manager

@tool
def add_todo(task: str) -> str:
    """
    Add a new task to the user's to-do list.
    
    Args:
        task: The task description to add to the to-do list
        
    Returns:
        Confirmation message about the task being added
    """
    if not memory_manager:
        return "Memory system not initialized. Please contact support."
    
    return memory_manager.add_todo(task)

@tool
def list_todos() -> str:
    """
    List all active tasks in the user's to-do list.
    
    Returns:
        A formatted list of all active to-do items
    """
    if not memory_manager:
        return "Memory system not initialized. Please contact support."
    
    return memory_manager.list_todos()

@tool
def remove_todo(task: str) -> str:
    """
    Remove a task from the user's to-do list.
    
    Args:
        task: The exact task description to remove from the to-do list
        
    Returns:
        Confirmation message about the task being removed
    """
    if not memory_manager:
        return "Memory system not initialized. Please contact support."
    
    return memory_manager.remove_todo(task)

@tool
def get_user_name() -> str:
    """
    Get the user's name if it has been set.
    
    Returns:
        The user's name or a default greeting
    """
    if not memory_manager:
        return "Friend"
    
    return memory_manager.get_user_name()

@tool
def set_user_name(name: str) -> str:
    """
    Set or update the user's name.
    
    Args:
        name: The user's name to remember
        
    Returns:
        Confirmation message about the name being saved
    """
    if not memory_manager:
        return "Memory system not initialized. Please contact support."
    
    memory_manager.set_user_name(name)
    return f"Nice to meet you, {name}! I'll remember your name."

@tool
def get_memory_stats() -> str:
    """
    Get statistics about the user's memory and activity.
    
    Returns:
        A formatted string with memory statistics
    """
    if not memory_manager:
        return "Memory system not initialized. Please contact support."
    
    stats = memory_manager.get_stats()
    
    stats_text = f"""
 Your Activity Stats:
• Name: {stats['user_name']}
• Active todos: {stats['active_todos']}
• Completed todos: {stats['completed_todos']}
• Total conversations: {stats['total_conversations']}
• Account created: {stats['created_at'][:10] if stats['created_at'] else 'Unknown'}
• Last updated: {stats['last_updated'][:10] if stats['last_updated'] else 'Unknown'}
    """.strip()
    
    return stats_text

# List of all available tools
ALL_TOOLS = [
    add_todo,
    list_todos,
    remove_todo,
    get_user_name,
    set_user_name,
    get_memory_stats
]