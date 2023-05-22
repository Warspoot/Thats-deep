import requests
from env import *
from Personality import *
from decimal import Decimal, getcontext
import subprocess

prompt1 = ""
headers = ""

class Interaction:
    def __init__(self):
        self.init()

    def terminal(text):
        # Command to print the text in a new terminal window
        global open
        open = ""
        if open == "":
            open = False
        command = ['start', 'cmd', '/Q', '/K', 'echo', text]

        # Open the new terminal and print the text
        if open == False:
            subprocess.Popen(command, shell=True)
        open = True

    def init(self):
        global prompt
        global headers
        headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json',
        }
        while True:
            global change_story
            change_story = input("Start a new conversation? \n Response: ")
            if change_story not in ["Yes", "No", "yes", "no", "y", "n"]:
                print("Invalid Response")
                return
            
            if change_story in ["No", "no", "n"]:
                print("Continuing previous conversation")
                self.interact()
                break

            if change_story in ["Yes", "yes", "y",]:
                print("Starting a new story")
                requests.delete(url=f'{Koblod_LINK}/api/v1/delete')
                self.newstory()
                self.interact()
                break

    def newstory(self):
        response = requests.delete(url = f"{Koblod_LINK}/api/v1/story")
        starting_line = input("What would you like your starting line to be? \n You: ")
        print(prompt + "You: " + starting_line)
        payload = {
            "prompt": f"{prompt} You: {starting_line}",
            "use_story": False,
            "use_memory": True,
            "use_authors_note": False,
            "use_world_info": False,
            "rep_pen": 1.02,
            "rep_pen_range": 256,
            "rep_pen_slope": 0.8,
            "temperature": 0.8,
            "tfs": 0.96,
            "top_a": 0.01,
            "top_k": 15,
            "top_p": 0.94,
            "typical": 0.98,
            "sampler_order": [6, 4, 3, 2, 0, 1, 5]
        }

        response_setup = requests.post(url=f'{Koblod_LINK}/api/v1/generate', json=payload)
        r = response_setup.json()
        generated_text = r['results'][0]['text']
        name = generated_text.split(":")[0].strip()
        message = ":".join(generated_text.split(":")[1:]).strip()
        global formatted_text
        formatted_text = f"{name}: {message}"
        global prompt1
        prompt1 = prompt + "\n" + "You: " + starting_line
        prompt2 = prompt1 + "\n" + formatted_text
        global promptlist
        promptlist = starting_line + "\n" + formatted_text
        json = {
            "prompt" : f"{prompt2}"
        }
        response = requests.post(url=f"{Koblod_LINK}/api/v1/story/end", json = json)
        print(formatted_text)

    def interact(self):
        global prompt, prompt1, promptlist, formatted_text
        memory = {
                "value": f"{prompt}"
            }
            
        response = requests.put(url = f"{Koblod_LINK}/api/v1/config/memory", json = memory)
        response = requests.get(url=f"{Koblod_LINK}/api/v1/config/memory")
        response = response.json()

        while True:
            user_input = input("You: ")
            new_prompt = prompt1 + "\n" + formatted_text + "You: " + user_input
            # for debug purposes, print(new_prompt)

            #count the tokens used in the prompt
            count = len(new_prompt)
            getcontext().prec = 28  # Number of significant digits
            getcontext().rounding = 'ROUND_HALF_UP'  # Rounding mode
            tokenperchar = Decimal('2432') / Decimal('735')
            tokencount = Decimal(f'{count}') / Decimal(f'{tokenperchar}')
            tokencount = tokencount.quantize(Decimal('1'))
            maxtoken = 943
            Token_usage = f"{tokencount} out of {maxtoken} tokens used."
            print(f"Token Usage: \n {Token_usage}")
            pyperclip.copy(new_prompt)

            #creates the json prompt
            promptlist = promptlist + "\n" + user_input + "\n"

            #send the prompt through the api
            payload = {
                "prompt": f"{new_prompt}",
                "use_story": False,
                "use_memory": False,
                "use_authors_note": False,
                "use_world_info": False,
                "rep_pen": 1.02,
                "rep_pen_range": 256,
                "rep_pen_slope": 0.8,
                "temperature": 0.8,
                "tfs": 0.96,
                "top_a": 0.01,
                "top_k": 15,
                "top_p": 0.94,
                "typical": 0.98
            }
            prompt1 = new_prompt
            response_setup = requests.post(url=f'{Koblod_LINK}/api/v1/generate', json=payload, headers=headers)
            r = response_setup.json()
            generated_text = r['results'][0]['text']
            name = generated_text.split(":")[0].strip()
            message = ":".join(generated_text.split(":")[1:]).strip()
            formatted_text = f"{name}: {message}"
            print(formatted_text)

Interaction()
