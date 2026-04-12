# from dotenv import load_dotenv
# import os
# from livekit import api

# load_dotenv()

# LIVEKIT_API_KEY = os.getenv("LIVEKIT_API_KEY")
# LIVEKIT_API_SECRET = os.getenv("LIVEKIT_API_SECRET")

# token = api.AccessToken('LIVEKIT_API_KEY','LIVEKIT_API_SECRET') \
#         .with_identity("user1") \ 
#         .with_name("Mukesh") \ 

import requests

def ask_llm(user_input):
    sys_prompt = """
You are Phantom, Mukesh's personal assistant.
Rules:
- Answer in 1-2 lines only
- Be clear and helpful
"""
    
    prompt = sys_prompt+"\nUser: "+user_input+"\nAssistant"
    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "phi",   # best for your 8GB RAM
                "prompt": prompt,
                "stream": False
            }
        )
    except Exception as e:
        return "Error connecting to AI"
    