import os
import openai 
import pyperclip as py
import csv
from datetime import datetime
# Load the .env file
from dotenv import load_dotenv
load_dotenv()


openai.api_type         = os.getenv("OPENAI_TYPE")
openai.api_base         = os.getenv("OPENAI_BASE")
openai.api_version      = os.getenv("OPENAI_VERSION")
openai.api_key          = os.getenv("OPENAI_KEY")


def get_log_path():
   # The `return os.path.join(os.path.dirname(__file__), "data.csv")` line of code is returning the
   # full path of the `data.csv` file by joining the directory path of the current file with the
   # filename `data.csv`.
   return os.path.join(os.path.dirname(__file__), "gpt_log.csv")

#py.copy('Is greece bigger than Italy? ')

prompt = py.paste().strip()

base_message = [{"role":"system","content":"""
            You will act as my personal assistant.
            You have 15 years expeirence, and are generally considered to be lazy, but very specific in your deliveries.  
            You should always reply with a complete solution, no questions, always a solution and no follow up quesitons.
            You will solve my tasks in a clear and to the point, without introducing or providing context, just an answer please.
            Each task you solve should be delivered with out reflection or other comments or introductions, except if it is specifically requested"""},
            {"role":"user",
             "content": f'{prompt}'}
            #{"role":"assistant","content":"[your evaluation from 0 to 100, start with numbers] \n [your reasoning for the evaluation]"}
            ] 
code_message = [{"role":"system","content":"""
            You will act as my junior developer. You have 10 years experience, and deliver very efficeint code.
            I'm very busy, so your solutions should always be one shot wonders, no follow up questions, just a solution.
            You should always insert line by line documentation in the code, so that i can easily read and comprehend the code.
            You will never write descriptoins before the code or after. Only line by line documentation, or a documentation forr the functions.
            
            If i start my message with # its of the up most importace that you assume the output is going streat in a python file. 
            
            Here is a good example of how you should reply to my messages:
                
                
            """},
            {"role":"user",
             "content": f'{prompt}'}
            #{"role":"assistant","content":"[your evaluation from 0 to 100, start with numbers] \n [your reasoning for the evaluation]"}
            ] 

message = base_message

if prompt[0] == '#' or 'write a function' in prompt:
    message = code_message
else:
    message = base_message


response = openai.ChatCompletion.create(
    deployment_id = 'gpt-35-turbo',
    engine = 'gpt-35-turbo',
    messages = message,
    temperature = 0.2,
    max_tokens = 400,
    top_p = 0.95,
    frequency_penalty = 0,
    presence_penalty = 0,
    stop = None
)

response = response['choices'][0]['message']['content']

timestamp = int(datetime.utcnow().timestamp())

path = r'C:\Users\jbay\AppData\Roaming\espanso\match\scripts\gpt_log.csv'

with open(get_log_path(), mode='a', newline='') as file:
    writer = csv.writer(file)
    writer.writerow([prompt, response, timestamp])

print(response)