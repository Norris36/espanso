import os
import openai 
import pyperclip as py
import csv
from datetime import datetime
import pandas as pd
import re
import numpy as np
import time
# Load the .env file
from dotenv import load_dotenv
load_dotenv()


openai.api_type         = os.getenv("OPENAI_TYPE")
openai.api_base         = os.getenv("OPENAI_BASE")
openai.api_version      = os.getenv("OPENAI_VERSION")
openai.api_key          = os.getenv("OPENAI_KEY")

def vector_similarity(vec1,vec2):
    """
    Returns the similarity between two vectors.
    
    Because OpenAI Embeddings are normalized to length 1, the cosine similarity is the same as the dot product.
    """
    return np.dot(np.array(vec1), np.array(vec2))

def get_embedding(text):
    tries = 0
    if isinstance(text, str):
        pass
    else:
        return None
    try:
        result = openai.Embedding.create(
            engine='text-embedding-ada-002',
            model='text-embedding-ada-002',
            input=text
        )
        return result["data"][0]["embedding"]
    except Exception as e:
        #print(f"Error: {e}")
        time.sleep(7)
        if tries < 3:
            get_embedding(text)
            tries += 1
            #print(tries)
        else:
            return None

def cleaner(text):
    if isinstance(text, str):
        list = []

        text = text.replace('[', '')
        text = text.replace(']', '')

        for j in text.split(','):
            j = j.strip()
            list.append(float(j))
        return list
    else:
        return text

def my_reader(path):
    embeddings = []
    df = pd.read_csv(path)
    for i in range(len(df)):
        x = df.at[i, 'embedding']
        y = cleaner(x)
        embeddings.append(y)
        
    df['embedding'] = embeddings
    return df

def embed_prompt_lookup(question: str, df: pd.DataFrame) -> str:
    # Your code remains unchanged until this line
    prompt_embedding = get_embedding(question)

    # Filter out rows with None values in the 'embedding' column
    valid_df = df[df['embedding'].notna()]

    # Get prompt similarity with embeddings
    df['prompt_similarity'] = np.nan  # Initialize a new column with NaN values

    for index, row in valid_df.iterrows():
        vector = list(row['embedding'])
        similarity = vector_similarity(vector, prompt_embedding)
        df.at[index, 'prompt_similarity'] = similarity
        
    # Rest of the code remains unchanged
    # get most similar summary
    top_3_similar = df.nlargest(3, 'prompt_similarity')
    summaries = top_3_similar['text'].tolist()

    prompt = f"""
            Only answer the question below if you have 100% certainty of the facts, use the context below to answer.
            You are an expert role writer. You will get three roles, which are similar to my query, and you will write a 50-word role description.
            Below are prior examples of roles, which you can base the description on. 
            You should not end the description with My first command...
            The format for the trigger is as follows:
            Here is some context:
            {summaries[0]}
            {summaries[1]}
            {summaries[2]}
            Q: {question} \n\n
            A:"""
    # Use OpenAI to get the most similar answer
    response = openai.Completion.create(
        engine = 'text-davinci-003', # Use the text-davinci-003 engine
        prompt=prompt, # Use the prompt created above
        temperature=0, # Set the temperature to 0
        max_tokens=500, # Set the maximum tokens to 500
        model="text-davinci-003" # Use the text-davinci-003 model
    )
    return response["choices"][0]["text"].strip(" \n")

question = py.paste().strip()

df = my_reader(r'C:\Users\jbay\AppData\Roaming\espanso\match\scripts\assistant_generator.csv')

answer = embed_prompt_lookup(question, 
                             df = df)

print(answer)