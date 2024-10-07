import ingest

import ollama
client = ollama.Client()


index = ingest.ingest_data()

def search(query, boost= None):
    if boost is None:
        boost = {}
    
    results = index.search(
        query=query,
        filter_dict = {},
        boost_dict=boost,
        num_results=5
    )

    return results



prompt_template = """
You are an assistant preparing a candidate for a data science job interview. 
Based on the provided context, please provide a concise and accurate answer to the following question in plain text format without any additional formatting.

QUESTION: {question}

CONTEXT:
{context}

The answer has to be plain text
""".strip()



def build_prompt(query, search_results):
    context = ""
    
    for doc in search_results:
        text = doc['chunk_text']
            
        context += f"Text: {text}\n\n"

    prompt = prompt_template.format(question=query, context=context).strip()
    return prompt




def generate_answer(query, search_results):
    message_content = build_prompt(query, search_results)
    
    response = client.chat(model="llama2", messages=[{"role": "user", "content": message_content}])
    
    if 'message' in response and 'content' in response['message']:
        content = response['message']['content']
        
        return content.strip()  
    return ""  



def rag(query):
    search_results = search(query)
    response = generate_answer(query, search_results)
    return response

    
