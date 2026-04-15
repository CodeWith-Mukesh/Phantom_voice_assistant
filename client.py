import requests

def ask_llm(user_input):
    sys_prompt = """
You are Phantom an voice assstant.
Created by 'Mukesh' as his personal assistant.

you have to Always Answer in 1-2 lines only .
you have to Be clear and helpful.
"""
    prompt = sys_prompt + user_input
    try:
        response = requests.post(
            "http://127.0.0.1:11434/api/generate",
            json={
                "model": "phi",    #Can use big models also.
                "prompt": prompt,
                "stream": True 
            },
            stream=True,
            timeout=60
        )

        full_response = ""

        for line in response.iter_lines():
            if line:
                data = line.decode("utf-8")
                import json
                json_data = json.loads(data)

                full_response += json_data.get("response", "")

        return full_response.strip()

    except Exception as e:
        print("ERROR:", e)
        return "Error connecting to AI"
    
