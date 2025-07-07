"""
Memory management for the Gemini Agent Todo application.
Handles conversation history and todo list persistence.
"""

import json
import os
from typing import List, Dict, Any
from datetime import datetime

class MemoryManager:
    """Manages conversation history and todo list persistence."""
    
    def __init__(self, data_dir: str = "data"):
        self.data_dir = data_dir
        self.memory_file = os.path.join(data_dir, "memory.json")
        self.ensure_data_dir()
        self.memory = self.load_memory()
    
    def ensure_data_dir(self):
        """Ensure data directory exists."""
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)
    
    def load_memory(self) -> Dict[str, Any]:
        """Load memory from JSON file."""
        if os.path.exists(self.memory_file):
            try:
                with open(self.memory_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except (json.JSONDecodeError, FileNotFoundError):
                print("Memory file corrupted or not found. Starting fresh.")
        
        # Return default memory structure
        return {
            "conversation_history": [],
            "user_name": None,
            "todos": [],
            "created_at": datetime.now().isoformat(),
            "last_updated": datetime.now().isoformat()
        }
    
    def save_memory(self):
        """Save memory to JSON file."""
        self.memory["last_updated"] = datetime.now().isoformat()
        try:
            with open(self.memory_file, 'w', encoding='utf-8') as f:
                json.dump(self.memory, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Error saving memory: {e}")
    
    def add_conversation(self, user_message: str, assistant_response: str):
        """Add a conversation exchange to history."""
        conversation_entry = {
            "timestamp": datetime.now().isoformat(),
            "user": user_message,
            "assistant": assistant_response
        }
        self.memory["conversation_history"].append(conversation_entry)
        
        # Keep only last 50 conversations to prevent memory bloat
        if len(self.memory["conversation_history"]) > 50:
            self.memory["conversation_history"] = self.memory["conversation_history"][-50:]
        
        self.save_memory()
    
    def get_conversation_history(self) -> List[Dict[str, str]]:
        """Get conversation history."""
        return self.memory["conversation_history"]
    
    def set_user_name(self, name: str):
        """Set user name."""
        self.memory["user_name"] = name
        self.save_memory()
    
    def get_user_name(self) -> str:
        """Get user name."""
        return self.memory.get("user_name", "Friend")
    
    def add_todo(self, task: str) -> str:
        """Add a todo item."""
        
        # Check for duplicates
        existing_tasks = [todo['task'].lower() for todo in self.memory["todos"] if not todo["completed"]]
        if task.lower() in existing_tasks:
            return f"'{task}' is already in your to-do list."
        
        todo_item = {
            "id": len(self.memory["todos"]) + 1,
            "task": task,
            "created_at": datetime.now().isoformat(),
            "completed": False
        }
        self.memory["todos"].append(todo_item)
        self.save_memory()
        return f"Added '{task}' to your to-do list."
    
    def list_todos(self) -> str:
        """List all todo items."""
        todos = [todo for todo in self.memory["todos"] if not todo["completed"]]
        if not todos:
            return "Your to-do list is empty. Great job staying on top of things!"
        
        todo_text = "Your current to-do list:\n"
        for i, todo in enumerate(todos, 1):
            todo_text += f"{i}. {todo['task']}\n"
        
        return todo_text.strip()
    
    def remove_todo(self, task: str) -> str:
        """Remove a todo item by task name."""
        # Handle "all" case
        if task.lower() in ["all", "everything", "all todos", "all tasks"]:
            active_todos = [todo for todo in self.memory["todos"] if not todo["completed"]]
            if not active_todos:
                return "Your to-do list is already empty."
            
            count = len(active_todos)
            for todo in self.memory["todos"]:
                if not todo["completed"]:
                    todo["completed"] = True
            
            self.save_memory()
            return f"Removed all {count} tasks from your to-do list."
        
        # Handle single task removal
        for todo in self.memory["todos"]:
            if todo["task"].lower() == task.lower() and not todo["completed"]:
                todo["completed"] = True
                self.save_memory()
                return f"Removed '{task}' from your to-do list."
        
        return f"Task '{task}' not found in your to-do list."
    
    def get_context_for_llm(self) -> str:
        """Get context string for LLM including user name and recent history."""
        context = f"User's name: {self.get_user_name()}\n"
        
        # Add recent conversation history (last 5 exchanges)
        recent_history = self.memory["conversation_history"][-5:]
        if recent_history:
            context += "\nRecent conversation:\n"
            for entry in recent_history:
                context += f"User: {entry['user']}\n"
                context += f"Assistant: {entry['assistant']}\n"
        
        return context
    
    def get_stats(self) -> Dict[str, Any]:
        """Get memory statistics."""
        active_todos = [todo for todo in self.memory["todos"] if not todo["completed"]]
        completed_todos = [todo for todo in self.memory["todos"] if todo["completed"]]
        
        return {
            "total_conversations": len(self.memory["conversation_history"]),
            "active_todos": len(active_todos),
            "completed_todos": len(completed_todos),
            "user_name": self.get_user_name(),
            "created_at": self.memory.get("created_at"),
            "last_updated": self.memory.get("last_updated")
        }