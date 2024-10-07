# interview_preparation_bot

This project aims to provide a structured set of technical interview questions designed for data scientists, focusing on topics such as machine learning, statistics, data manipulation, and programming. It leverages large language models (LLMs) to automatically generate, refine, and evaluate questions based on real-world interview experiences and relevant academic materials. The project uses a combination of Python tools, including Ollama, Elasticsearch, and Jupyter Notebooks, to create an efficient workflow for generating and curating high-quality interview questions.

Claro, aquí tienes una descripción general de tu proyecto que puedes utilizar para el archivo README:
Technical Interview Questions for Data Scientists

This project aims to provide a structured set of technical interview questions designed for data scientists, focusing on topics such as machine learning, statistics, data manipulation, and programming. It leverages large language models (LLMs) to automatically generate, refine, and evaluate questions based on real-world interview experiences and relevant academic materials. The project uses a combination of Python tools, including Ollama, Elasticsearch, and Jupyter Notebooks, to create an efficient workflow for generating and curating high-quality interview questions.
Key Components

## Dataset


## Tehnologies

* minsearch
* Llama2
* Flask as the API interface


## Running it

We use pipenv for managing dependencies and Python 3.10

Make sure you have pipenv installed:

```bash
pip install pipenv
```

## Running it with Docker

```bash
docker-compose up
```
To test or change something in the Dockerfile, use the following command:

```bash
docker build -t chatbot .

docker run -it --rm  \
    -v "$(pwd)/data/gold:/data/gold" \
    -e DATA_PATH="/data/gold/data.csv" \
    -p 5000:5000  \
       chatbot
    
```

## Preparing the application

Before using the app we need to initialize the database

We can do it by running the [db_prep.py](chatbot/db_prep.py) script:

```bash
cd chatbot


pipenv shell 


export POSTGRES_HOST=localhost 

python db_prep.py
```

## Running locally
### Installing the dependencies

In case you want to run it locally, you need to manally prepare the environment and install all the dependencies

```bash
pipenv install --dev
```
### Running the flask Application

Run the following command for running the application locally:

```bash
pipenv shell 
export POSTGRES_HOST=localhost 
python app.py

```

## Prerequisites

- Ensure you have [Ollama](https://ollama.com) installed on your system.

### Llama2 setup

1. Start the Ollama server:

```bash
ollama serve
```

2. Pull the Llama2 model:

```bash
ollama pull llama2
```

## Using the application

### Testing the flask application:

```bash
URL="http://127.0.0.1:5000"
DATA='{"question": "what is the scope of a data scientist?"}'

curl -X POST \
    -H "Content-Type: application/json" \
    -d "${DATA}" \
    "${URL}/ask"
```


### The answer will look similar to this:

```json
"conversation_id": "4b31952c-6c04-41ec-971d-649cc2c85807",
  "question": "what is the scope of a data scientist?",
  "result": "A data scientist's scope typically involves working on various aspects of the machine learning (ML) lifecycle, including data preparation, model development, deployment, and maintenance. The specific responsibilities may vary depending on the company, team, and job title, but some common tasks include:\n\n1. Data analysis: Cleaning, processing, and interpreting large datasets to extract insights and identify patterns.\n2. Model development: Building, training, and validating ML models using various techniques, such as supervised and unsupervised learning, deep learning, and reinforcement learning.\n3. Deployment: Integrating trained models into production environments, ensuring they are scalable and reliable.\n4. Maintenance: Monitoring model performance, updating or refreshing models as needed, and addressing any issues that arise.\n5. Collaboration: Working closely with cross-functional teams, such as engineering, product management, and business stakeholders, to identify ML opportunities and solve complex problems.\n6. Communication: Presenting findings and insights to stakeholders, communicating results effectively, and explaining technical concepts to non-technical audiences.\n7. Data visualization: Creating informative and engaging visualizations to help communicate insights and findings to stakeholders.\n8. Algorithm selection: Choosing the most appropriate algorithms and techniques for a given problem or dataset, based on factors such as data quality, complexity, and scalability.\n9. Hyperparameter tuning: Optimizing model performance by adjusting hyperparameters, which are parameters that control the behavior of ML models.\n10. Model evaluation: Assessing the performance of ML models using various metrics and techniques, such as cross-validation, to ensure they are accurate and robust.\n\nOverall, a data scientist's scope involves working on a wide range of tasks related to data analysis, model development, deployment, and maintenance, with a focus on leveraging ML techniques to drive business impact."

```

Alternatively you can use [test.py](test.py) for testing purposes:

```bash
pipenv run python test.py

```


### Feedback

TBD

## Requirements

To run this project locally, ensure you have the following:

    Python 3.10
    Pipenv shell to activate the virtual environment

    Ollama installed in the environment
    Elasticsearch for search and retrieval functionalities




### Columns description


## Ingestion


## Evaluation

For the code for evaluating the system you can check the [rag_llama2 notebook](notebooks/rag_llama2.ipynb)


## Retrieval 

Approach using minsearch without any boosting gave the following metrics:

*'hit_rate': 0.77
*'mrr': 0.62

The optimized minsearch function gave the following metrics:

*'hit_rate': 0.83
*'mrr': 0.67

The best boosting parameter:

```
'boost': 0.21
```

## Rag Flow

LLM-as-a-judge as been used as metric to evaluate the quality of the RAG Flow 

Among 229 records:

* X RELEVANT : 213 (93%)
* Y PARTLY RELEVANT : 16 (6%)
* Z IRRELEVANT : 0

