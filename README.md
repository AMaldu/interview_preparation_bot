# interview_preparation_bot

This project aims to provide a structured set of technical interview questions designed for data scientists, focusing on topics such as machine learning, statistics, data manipulation, and programming. It leverages large language models (LLMs) to automatically generate, refine, and evaluate questions based on real-world interview experiences and relevant academic materials. The project uses a combination of Python tools, including Ollama, Elasticsearch, and Jupyter Notebooks, to create an efficient workflow for generating and curating high-quality interview questions.

Claro, aquí tienes una descripción general de tu proyecto que puedes utilizar para el archivo README:
Technical Interview Questions for Data Scientists

This project aims to provide a structured set of technical interview questions designed for data scientists, focusing on topics such as machine learning, statistics, data manipulation, and programming. It leverages large language models (LLMs) to automatically generate, refine, and evaluate questions based on real-world interview experiences and relevant academic materials. The project uses a combination of Python tools, including Ollama, Elasticsearch, and Jupyter Notebooks, to create an efficient workflow for generating and curating high-quality interview questions.
Key Components


# Project Overview


Question Generation with LLMs:
    The project uses the Ollama tool to interact with large language models, specifically Phi3 and Llama2, to generate interview questions automatically.
    Prompts are carefully designed to ensure that the model outputs high-quality, structured questions relevant to data science interviews.
    Generated questions are saved in JSON format for further analysis and refinement.

Ground Truth Data:
    A dataset of questions and answers is used to build a ground truth for evaluating the performance of the language model. This dataset is processed and analyzed in Jupyter Notebooks.

Search and Retrieval with Elasticsearch:
    Elasticsearch is utilized to perform semantic search and k-nearest neighbors (KNN) queries on interview questions, helping retrieve similar or related questions efficiently.
    This system allows for filtering and ranking results based on relevance, ensuring accurate search results during the interview preparation process.

Performance Evaluation:
    The project includes a system for evaluating the performance of the LLMs in generating useful and accurate questions. Custom evaluation metrics for LLMs are employed to measure aspects such as relevance, clarity, and depth of generated content.

Project Workflow:
    The project is managed using Conda environments to ensure that dependencies, such as NumPy, Pandas, and Scikit-learn, are correctly isolated.
    Data and model interactions are managed through Jupyter Notebooks, allowing for an iterative, experiment-driven approach to development.


## Running it

We use pipenv for managing dependencies and Python 3.10

Make sure you have pipenv installed:

```
pip install pipenv
```

Installing the dependencies

```
pipenv install 
```


## Requirements

To run this project locally, ensure you have the following:

    Python 3.10
    Pipenv shell to activate the virtual environment

    Ollama installed in the environment
    Elasticsearch for search and retrieval functionalities


## Dataset

### Columns description


## Ingestion


## Evaluation

For the code for evaluating the system you can check the [rag_gpt notebook](notebooks/rag_gpt2.ipynb)


## Retrieval 

Approach using minsearch without any boosting gave the following metrics:

*'hit_rate': 0.77
*'mrr': 0.94

Usage

    Clone the repository and set up the environment.
    Use the provided Jupyter Notebooks to run the question generation, search, and evaluation workflows.
    Customize the prompts and ground truth data to generate new interview questions or refine existing ones.

Future Work

    Extend the system to handle multiple languages for interview questions.
    Improve the search algorithm to include more sophisticated ranking mechanisms.
    Integrate a scoring system to automatically assess the quality of answers provided to generated questions.

