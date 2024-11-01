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

## Hyperparameters

temperature: Controls the model's creativity.
top_p: Limits the selected words to an accumulated probability.
top_k: Restricts options to the k most probable words.
frequency_penalty and presence_penalty: Penalize word repetition in text generation.
max_tokens: Maximum length of the generated text.
repetition_penalty: Controls the probability of word repetition.


### Default hyperparameters

The hyperparameters I chose were a general starting point commonly used for balancing coherence, creativity, and relevance in generative models like Llama2. Here’s a breakdown of why I set each one as I did:

    Temperature (0.7):
        Temperature controls randomness in the model's output. Lower values (e.g., 0.2 - 0.5) make the output more deterministic, while higher values (0.8 - 1.0) increase diversity.
        0.7 is often a good middle ground: it encourages the model to be creative without straying too far from the prompt context.

    Top-p (0.9):
        Top-p, also known as nucleus sampling, restricts choices to the smallest set of words that have a cumulative probability mass above a certain threshold (in this case, 90%).
        This setting allows the model to sample from a more focused subset of words, improving relevance and coherence in the generated responses.

    Top-k (40):
        Top-k limits the model to choosing from the top 40 most probable tokens at each generation step.
        Using top-k and top-p together helps balance randomness and coherence, particularly when combined with a middle-range temperature.

    Frequency Penalty (0.5) & Presence Penalty (0.4):
        These penalties discourage the model from repeating the same words too frequently, improving text variety and natural flow.
        A frequency penalty of 0.5 and a presence penalty of 0.4 are moderate values that help reduce redundancy without overly restricting the model's choices.

    Max Tokens (200):
        Max tokens define the maximum length of the generated output.
        Setting this to 200 provides enough space for a complete answer while avoiding overly lengthy or verbose responses.

    Repetition Penalty (1.1):
        Repetition penalty helps prevent the model from looping or repeating phrases.
        A value of 1.1 slightly discourages repetition without strongly impacting coherence.



Evaluation

offline evaluation

    - cosine similarity
    - LLM as a judge (answer original --> answer_llm / question --> answer_llm)



online evaluation

    - A/B tests
    - experiments
    - user feedback