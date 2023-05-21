import requests
from env import *
from Personality import *
prompt1 = ""

class Interaction:
    def __init__(self):
        self.init()

    def init(self):
        global prompt
        while True:
            global change_story
            change_story = input("Start a new conversation? ")
            print(f"Response: {change_story}")
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
        starting_line = input("What would you like your starting line to be? ")
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
        formatted_text = f"{name}: {message}"
        global prompt1
        prompt1 = prompt + "\n" + "You: " + starting_line + "\n" + formatted_text
        print(formatted_text)

    def interact(self):
        global prompt, prompt1
        while True:
            user_input = input("You: ")
            new_prompt = prompt1 + "\n" + "You: " + user_input
            # for debug purposes, print(new_prompt)
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
            response_setup = requests.post(url=f'{Koblod_LINK}/api/v1/generate', json=payload)
            r = response_setup.json()
            generated_text = r['results'][0]['text']
            name = generated_text.split(":")[0].strip()
            message = ":".join(generated_text.split(":")[1:]).strip()
            formatted_text = f"{name}: {message}"
            print(formatted_text)

Interaction()
