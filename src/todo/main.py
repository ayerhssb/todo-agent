import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def main():
    print("Gemini Agent Todo - Hey yo, ready to tick off your todos!")
    
    # Check if API key is loaded
    api_key = os.getenv('GEMINI_API_KEY')
    if api_key:
        print("Gemini API Key loaded successfully")
    else:
        print("API Key not found. Please check your .env file")
    
    print(f"\nUsing UV for dependency management")
    print(f"Python version: {os.sys.version}")
    
    print("\nBasic setup...")

if __name__ == "__main__":
    main()