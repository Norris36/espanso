import os
import openai 
import pyperclip as py
import csv
from datetime import datetime
import re
# Load the .env file
from dotenv import load_dotenv
load_dotenv()


# openai.api_type         = os.getenv("OPENAI_TYPE")
# openai.api_base         = os.getenv("OPENAI_BASE")
# openai.api_version      = os.getenv("OPENAI_VERSION")
# openai.api_key          = os.getenv("OPENAI_KEY")



# from textwrap3 import wrap

def process_text(text):
    # Code tag to look for
    code_tag = '```'

    # If code tag is present in the text
    if code_tag in text:
        # Split the text by the code tag
        parts = text.split(code_tag)

        # Initialize an empty string to store the processed text
        processed_text = ''

        # Iterate over the parts
        for i, part in enumerate(parts):
            # If it's a code block, just append it as is
            if i % 2 != 0:
                processed_text += code_tag + part + code_tag
            else:
                # If it's not a code block, split into sentences and append with a line break
                sentences = wrap(part, width=120)
                processed_text += sentences+ "\n "

        return processed_text
    else:
        # If there is no code_tag in the text, wrap the text to have a width of 120 characters per line
        wrapped_text = wrap(text, width=120)
        wrapped_text = '\n'.join(wrapped_text)
        return wrapped_text


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
sql_message = [{"role":"system","content":"""
            You will act as my junior developer. You have 10 years experience, and deliver very efficeint code.
            I want you to act as a SQL Junior Analyst.
            Assume im working in a SQL editor, and that you are writing SQL code for me.
            You will get requests, and will provide ready to run code in first go every time, with documentation of the code.
            You should always insert line by line documentation in the sql code, and nowhere else.    
            ----------------------
            Here is a good example:
            my request:
            -- fix the below sql query
            select * 

            from ANALYTICS.DOTCOM.ALL_ORDERS_COMPLETED 
            where 
                product_sku = '61465'
                and country = 'US'
                and coupon not cotain 'RMA'
            limit 100
            
            Your perfect reply:
            -- Selecting all columns in the table
            SELECT * 
            -- Setting the table we are callinf from
            FROM ANALYTICS.DOTCOM.ALL_ORDERS_COMPLETED 
            -- Defining that we only want to see orders with the product_sku set to 61465 and country set to US and no RMA coupons
            WHERE 
                product_sku = '61465'
                AND country = 'US'
                AND coupon NOT LIKE '%RMA%'
            LIMIT 100;
            ---------------------
            Here is a good example:
            my request:
            -- comment out all of the below sql
            select * 
            from ANALYTICS.DOTCOM.ALL_ORDERS_COMPLETED 
            where 
                product_sku = '61465'
                and country = 'US'
                and coupon not contain 'RMA'
            limit 100

            your perfect reply:
            --select * 
            --from ANALYTICS.DOTCOM.ALL_ORDERS_COMPLETED 
            --where 
            --  product_sku = '61465'
            --  and country = 'US'
            --  and coupon not cotain 'RMA'
            --limit 100
            ----------------------- 
            Here is a good example:
            my request:
            -- uncomment out all of the below sql
            --select * 
            --from ANALYTICS.DOTCOM.ALL_ORDERS_COMPLETED 
            --where 
            --  product_sku = '61465'
            --  and country = 'US'
            --  and coupon not cotain 'RMA'
            --limit 100

            your perfect reply:
            select * 
            from ANALYTICS.DOTCOM.ALL_ORDERS_COMPLETED 
            where 
                product_sku = '61465'
                and country = 'US'
                and coupon not cotain 'RMA'
            limit 100
            -----------------------            
            """},
            {"role":"user",
             "content": f'{prompt}'}
            #{"role":"assistant","content":"[your evaluation from 0 to 100, start with numbers] \n [your reasoning for the evaluation]"}
            ] 

message = base_message

if prompt[0] == '#' or 'write a function' in prompt:
    message = code_message
if prompt[0] == '-' and prompt[1] == '--':
    message = sql_message
else:
    message = base_message


# response = openai.ChatCompletion.create(
#     deployment_id = 'gpt-35-turbo',
#     engine = 'gpt-35-turbo',
#     messages = message,
#     temperature = 0.2,
#     max_tokens = 2000,
#     top_p = 0.95,
#     frequency_penalty = 0,
#     presence_penalty = 0,
#     stop = None
# )

# response = response['choices'][0]['message']['content']

response = 'dont use this'

timestamp = int(datetime.utcnow().timestamp())

path = r'C:\Users\jbay\AppData\Roaming\espanso\match\scripts\gpt_log.csv'

with open(get_log_path(), mode='a', newline='') as file:
    writer = csv.writer(file)
    writer.writerow([prompt, response, timestamp])

#response = process_text(response)

print(response)