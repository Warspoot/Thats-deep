import os
import openai
from env import *

openai.api_key = OPENAI_API_KEY

prompt = ""

class GPTsetup:
    @staticmethod
    def chat():
        while True:
            while True:
                global prompt
                prompt = input("Write a valid prompt: ")
                if prompt == None:
                    print("Please enter a valid prompt.")
                else:
                    print(f"Prompt: {prompt}")
                    break

            messages =[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": prompt},    
            ]

            chat_completeion = openai.ChatCompletion.create(
                model ="gpt-3.5-turbo",
                messages = messages
            )  

            response = chat_completeion.choices[0].message.content
            print(response)
            
GPTsetup.chat()

