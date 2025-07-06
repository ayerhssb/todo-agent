"""
Gemini LLM integration for LangChain.
"""

import google.generativeai as genai
from langchain_core.language_models.llms import LLM
from langchain_core.callbacks.manager import CallbackManagerForLLMRun
from typing import Optional, List, Any
from .config import Config

class GeminiLLM(LLM):
    """Custom LangChain LLM wrapper for Google Gemini."""
    
    model_name: str = "gemini-1.5-flash"
    temperature: float = 0.1  # Lower temperature for more consistent tool use
    max_tokens: int = 1000
    genai_model: Any = None
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Configure Gemini API
        genai.configure(api_key=Config.GEMINI_API_KEY)
        self.genai_model = genai.GenerativeModel(self.model_name)
    
    @property
    def _llm_type(self) -> str:
        return "gemini"
    
    def _call(
        self,
        prompt: str,
        stop: Optional[List[str]] = None,
        run_manager: Optional[CallbackManagerForLLMRun] = None,
        **kwargs: Any,
    ) -> str:
        """Call the Gemini API."""
        try:
            # Configure generation parameters for better consistency
            generation_config = genai.types.GenerationConfig(
                temperature=self.temperature,
                max_output_tokens=self.max_tokens,
                candidate_count=1,
                stop_sequences=stop if stop else None,
            )
            
            # Generate response
            response = self.genai_model.generate_content(
                prompt,
                generation_config=generation_config,
                safety_settings={
                    genai.types.HarmCategory.HARM_CATEGORY_HARASSMENT: genai.types.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
                    genai.types.HarmCategory.HARM_CATEGORY_HATE_SPEECH: genai.types.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
                    genai.types.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: genai.types.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
                    genai.types.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: genai.types.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
                }
            )
            
            # Extract text from response
            if response.text:
                return response.text.strip()
            else:
                return "I apologize, but I couldn't generate a response. Please try again."
                
        except Exception as e:
            print(f"Error calling Gemini API: {e}")
            return f"Sorry, I encountered an error: {str(e)}"
    
    @property
    def _identifying_params(self) -> dict:
        """Return identifying parameters."""
        return {
            "model_name": self.model_name,
            "temperature": self.temperature,
            "max_tokens": self.max_tokens,
        }

def create_gemini_llm(temperature: float = 0.1, max_tokens: int = 1000) -> GeminiLLM:
    """Create and return a configured Gemini LLM instance."""
    return GeminiLLM(
        model_name="gemini-1.5-flash",
        temperature=temperature,
        max_tokens=max_tokens
    )