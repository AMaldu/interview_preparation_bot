 # Experimentation with different retrieval methods

 This folder contains notebooks where you can find the analysis of different retrieval methods applied to the project but before that let's briefly explain some concepts.

 ## What is a retrieval?

 Retrieval, or information retrieval, is the process of searching for and retrieving relevant data from a large set of information. In the context of data science it usually refers to finding specific documents, passages, or data points that answer a given query.

 ## How Does Retrieval Work?

The basic retrieval process involves:

1. User Query: A user poses a question or search expression.
2. Index: The retrieval system has previously indexed a set of documents or data, allowing for fast searching.
3. Search and Matching: The system compares the query to the index and finds the most relevant documents based on certain criteria.
4. Ranking: Retrieved documents are ranked by relevance using a specific metric or algorithm.
5. Results: The most relevant documents or pieces of information are presented to the user.


## Common Retrieval Methods

Retrieval methods can be categorized based on the type of search, model, or technique used. Here are the most common ones:

1. Keyword-based Retrieval: Simple, traditional keyword matching.
2. Vector Space Model (VSM): Uses vector similarity (e.g., cosine similarity) for ranking.
3. BM25: An advanced term-based ranking model often used in modern search engines.
4. Dense Retrieval: Embedding-based retrieval that uses vector similarity in high-dimensional space.
5. K-Nearest Neighbors (KNN): Finds k most similar documents based on vector distance.
6. Neural Retrieval: Deep learning models that learn to rank documents based on context and semantics.


## Which Retrieval Methods you are going to find in this project?

1. **Semantic search**: focuses on understanding the meaning or context of words in a query, rather than relying on exact keyword matches. It retrieves documents that are contextually or conceptually relevant to the query, even if the exact keywords do not match.

2. **Text-Vector Search**: is a type of search where both the query and the documents are transformed into vector representations, and search is performed by computing the similarity between these vectors. It is embedding-based retrieval, where the text is embedded into a multi-dimensional space.








Here is an example of architecture for semantic search:

 <div align="center">
     <img src="../../images/retrieval-schema.png" alt="Retrieval Schema" width="800" />
 </div>

 ## Why using retrieval?

 Whether or not retrieval is necessary depends on the type of application or task you're working on. Retrieval becomes essential when you need to access relevant information from a large collection of data, particularly when you’re dealing with:

 1. Large Data Sets
 2. Question answering systems
 3. Recommendation systems
 4. Information retrieval tasks in NLP