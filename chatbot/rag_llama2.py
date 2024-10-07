


# In[18]:


query = 'Which skills are important for a data scietist?'
print(rag(query))


# ## Retrieval evaluation

# In[19]:


import pandas as pd

df = pd.read_csv('../data/ground_truth_data.csv')
df


# In[20]:


df_questions = df[['question', 'text_id']]


# In[21]:


ground_truth = df_questions.to_dict(orient = 'records')
ground_truth[0]


# In[22]:


ground_truth[0]


# In[23]:


def hit_rate(relevance_total):
    cnt = 0

    for line in relevance_total:
        if isinstance(line, (list, tuple)) and True in line:
            cnt += 1
        # elif line is True:
        #     cnt += 1

    return cnt / len(relevance_total)


# In[24]:


def mrr(relevance_total):
    total_score = 0.0
    num_queries = len(relevance_total)

    for line in relevance_total:
        query_score = 0.0
        for rank in range(len(line)):
            if line[rank] == True:
                query_score = 1 / (rank + 1)
                break  # Solo necesitamos el primero que sea True

        total_score += query_score

    # Evitar división por cero si no hay consultas
    return total_score / num_queries if num_queries > 0 else 0.0


# In[25]:


def minsearch_search(query):
    boost = {}
    # boost = {'text': 3.0, 'section': 0.5}
    
    results = index.search(
        query=query,
        filter_dict = {},
        boost_dict=boost,
        num_results=5)

    return results



# In[26]:


from tqdm.auto import tqdm


def evaluate(ground_truth, search_function):
    relevance_total = []

    for q in tqdm(ground_truth):
        doc_id = q['text_id']
        results = search_function(q)
        relevance = [d['text_id'] == doc_id for d in results]
        relevance_total.append(relevance)

    return {
        'hit_rate': hit_rate(relevance_total),
        'mrr': mrr(relevance_total),
    }


# In[27]:


from tqdm.auto import tqdm


# In[28]:


evaluate(ground_truth, lambda q: minsearch_search(q['question']))


# ## Hyperparams Optimization
# 

# In[29]:


def minsearch_search(query, boost_value):
    boost = {'text': boost_value}
    
    results = index.search(
        query=query,
        filter_dict={},
        boost_dict=boost,
        num_results=5
    )
    return results


# In[30]:


from hyperopt import fmin, tpe, hp, STATUS_OK, Trials
from hyperopt.pyll import scope


# In[31]:


df_val = df_questions[:100]
df_test = df_questions[100:]


# In[32]:


space = {
    'temperature': hp.uniform('temperature', 0.6, 1.2),   
    'top_p': hp.uniform('top_p', 0.7, 1.0),               
    'max_length': hp.quniform('max_length', 512, 1024, 1), 
    'boost': hp.uniform('boost', 0, 3),
    
}


# In[33]:


def objective(params):
    print(f"Evaluating with params: {params}")
    
    # Aquí puedes usar Llama2 con los parámetros y retornar la métrica
    temperature = params['temperature']
    top_p = params['top_p']
    max_length = int(params['max_length'])
    boost_value = params['boost']
    
    # Simula la ejecución de Llama2 con los hiperparámetros
    response = rag(query)

    # Calcula las métricas que deseas (hit rate y MRR)
    hit_rate_value = hit_rate(response)  # Asegúrate de que la función hit_rate esté bien definida
    mrr_value = mrr(response)
    
    # Invertir las métricas si estamos minimizando
    loss = - (hit_rate_value + mrr_value)
    
    return {'loss': loss, 'status': STATUS_OK}

# Inicializar Trials para almacenar resultados
trials = Trials()

# Ejecución de la optimización con TPE (Tree-structured Parzen Estimator)
best = fmin(
    fn=objective,
    space=space,
    algo=tpe.suggest,
    max_evals=10,  # Número de iteraciones a ejecutar
    trials=trials
)

# Guardar los mejores hiperparámetros
print(f"Best hyperparameters: {best}")


# In[34]:


best_temperature = best['temperature']
best_top_p = best['top_p']
best_max_length = int(best['max_length'])
boost = best['boost']
# response = rag(query)
# print(response)


# In[35]:


import json

with open('../data/best_hyperparams.json', 'w') as f:
    json.dump(best, f)


# In[36]:


gt_val = df_val.to_dict(orient='records')


# In[37]:


def minsearch_search_optimized(query, boost):
    # boost = {'text': 3.0, 'section': 0.5}
    
    results = index.search(
        query=query,
        filter_dict = {},
        boost_dict=boost,
        num_results=5)

    return results


# In[38]:


boost = {'text': best['boost']}
         
evaluate(gt_val, lambda q: minsearch_search_optimized(q['question'], boost))
# para mirar cuanto da con los mejores hyperparam 


# A little bit better :)

# ## RAG Evaluation

# In[39]:


prompt1_template = """
You are an expert evaluator for a RAG system.
Your task is to analyze the relevance of the generated answer compared to the original answer provided.
Based on the relevance and similarity of the generated answer to the original answer, you will classify
it as "NON_RELEVANT", "PARTLY_RELEVANT", or "RELEVANT".

Here is the data for evaluation:

Original Answer: {answer_orig}
Generated Question: {question}
Generated Answer: {answer_llm}

Please analyze the content and context of the generated answer in relation to the original
answer and provide your evaluation in parsable JSON without using code blocks:

{{
  "Relevance": "NON_RELEVANT" | "PARTLY_RELEVANT" | "RELEVANT",
  "Explanation": "[Provide a brief explanation for your evaluation]"
}}
""".strip()

prompt2_template = """
You are an expert evaluator for a Retrieval-Augmented Generation (RAG) system.
Your task is to analyze the relevance of the generated answer to the given question.
Based on the relevance of the generated answer, you will classify it
as "NON_RELEVANT", "PARTLY_RELEVANT", or "RELEVANT".

Here is the data for evaluation:

Question: {question}
Generated Answer: {answer_llm}

Please analyze the content and context of the generated answer in relation to the question
and provide your evaluation in parsable JSON without using code blocks:

{{
  "Relevance": "NON_RELEVANT" | "PARTLY_RELEVANT" | "RELEVANT",
  "Explanation": "[Provide a brief explanation for your evaluation]"
}}
""".strip()


# In[40]:


len(ground_truth) 


# In[49]:


ground_truth[0]


# In[41]:


record = ground_truth[0]
question = record['question']
answer_llm = rag(question)


# In[42]:


print(answer_llm)


# In[43]:


prompt = prompt2_template.format(question = question , answer_llm = answer_llm)
print(prompt)


# In[46]:


search_results = minsearch_search_optimized(query, boost)
relevance = generate_answer(prompt, search_results)

print(relevance)


# In[51]:


for record in tqdm(ground_truth):
    print(record)


# In[ ]:





# In[ ]:





# In[ ]:





# In[53]:


evaluations = []

for record in tqdm(ground_truth):
    question = record['question']
    answer_llm = rag(question)
    
    prompt = prompt2_template.format(question = question , answer_llm = answer_llm)
    search_results = minsearch_search_optimized(query, boost)
    relevance = generate_answer(prompt, search_results)
    evaluations.append((record['question'], answer_llm, relevance))


# In[55]:


evaluations[0]


# In[60]:


df_eval = pd.DataFrame(evaluations, columns=['Question', 'Response', 'Evaluation'])


# In[61]:


df_eval


# In[68]:


import re 

def categorize_evaluation(text):
    if re.search(r'"NON_RELEVANT"', text):
        return "NON_RELEVANT"
    elif re.search(r'"PARTLY_RELEVANT"', text):
        return "PARTLY_RELEVANT"
    elif re.search(r'"RELEVANT"', text):
        return "RELEVANT"
    else:
        return "UNKNOWN"

df_eval['Category'] = df_eval['Evaluation'].apply(categorize_evaluation)

category_counts = df_eval['Category'].value_counts()


# In[69]:


category_counts


# In[71]:


normalized_counts = df_eval['Category'].value_counts(normalize= True)
normalized_counts


# In[ ]:




