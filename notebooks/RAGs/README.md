# RAG 
## What is RAG?

## Which are the components of RAG?


### Techniques used: Chunking. Why chunking?

Splitting text into chunks before passing it to a RAG (Retrieval-Augmented Generation) model is beneficial for several reasons.

1. Input Length Limitations

Language models have a maximum input length, typically measured in tokens. Chunking the text ensures that you can fit the text within these limitations, allowing the model to handle the input effectively.

2. Improved Information Retrieval

We can improve the retrieval system so it can find more specific and relevant pieces of information. This enhances the precision of the generated answers, as the model is working with smaller, more focused chunks rather than trying to process a large, noisy dataset.

3. More Precise Context

Chunks contain smaller, more self-contained pieces of information. When the model generates responses based on smaller chunks, it’s less likely to lose context or produce irrelevant output.

4. Computational Efficiency

Smaller chunks reduce the computational load. Additionally, retrieval queries are faster because you're working with smaller portions of data at a time.

5. Easier Hyperparameter Optimization

When using chunks, it becomes easier to optimize model hyperparameters in a controlled way. You can fine-tune parameters like the number of documents to retrieve or the size of the context window based on chunk size, allowing for a better balance between performance and precision.

6. Reduced Noise and Redundancy

Chunking allows the RAG system to better filter out noise and redundancy. This reduces the chances of irrelevant information affecting the generated answers.

## Chunking a book 

Our book follows a structured format with chapters, sections, and subsections that provide natural chunking points. 

However I found that one chapter has 5665 words so further chunking is needed.





Evaluation

offline evaluation

    - cosine similarity
    - LLM as a judge (answer original --> answer_llm / question --> answer_llm)



online evaluation

    - A/B tests
    - experiments
    - user feedback