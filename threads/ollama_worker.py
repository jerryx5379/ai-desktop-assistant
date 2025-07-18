import json
from PySide6.QtCore import QObject, Signal
import requests

from PySide6.QtCore import QObject, Signal

class OllamaWorker(QObject):
    MAX_CONTEXT_MESSAGES = 2
    SYS_INSTRUC = "You are a personal AI assistant. Keep your responses concise to the prompt"
    MODEL = "gemma3n:e2b"

    text_chunk = Signal(str) # these are class vars but act as instance vars?
    finished  = Signal()

    def __init__(self, user_prompt):
        super().__init__()

        self.user_prompt = user_prompt
        self.messages = [{"role":"system", "content": OllamaWorker.SYS_INSTRUC}]

    def stream_ollama(self):
        self.update_chat_context(role="user", message=self.user_prompt)
        url = "http://localhost:11434/api/chat"
        data = self.get_data()

        with requests.post(url, json=data, stream=True) as response:
            response.raise_for_status() 
            
            assis_response = ""
            for line in response.iter_lines():
                if line:
                    chunk = json.loads(line.decode("utf-8"))\
                    
                    if chunk.get("done",False):
                        total_tokens = chunk.get("eval_count", 0)
                        total_time = chunk.get("eval_duration", 1) / (10**9)
                        prompt_time = chunk.get("prompt_eval_duration", 1) / (10**9)
                        #print(assis_response)
                        #print(f"\nTokens: {total_tokens}")
                        #print(f"Tk/s: {total_tokens/total_time}")
                        #print(f"Prompt_time: {prompt_time}")

                    new_text = chunk["message"]["content"]
                    
                    assis_response += new_text 
                    self.text_chunk.emit(new_text)
        
        self.update_chat_context(role="assistant", message=assis_response)
        self.finished.emit()


    def update_chat_context(self, role:str, message:str): 
        self.messages.append({"role":role,"content":message})
        if len(self.messages) > self.MAX_CONTEXT_MESSAGES+1:
            self.messages.pop(1)

    def get_data(self):
        model = OllamaWorker.MODEL
        data = {
            "model": model,
            "messages": self.messages
        }
        return data
    
    