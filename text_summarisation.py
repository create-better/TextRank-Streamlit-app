"""
Created on : 03 - 01 - 2023 ( Tuesday )
Source : 
1. https://towardsdatascience.com/understand-text-summarization-and-create-your-own-summarizer-in-python-b26a9f09fc70
2. https://towardsdatascience.com/introduction-to-text-summarization-with-rouge-scores-84140c64b471
3. https://github.com/m-chanakya/shortstories
Created by : Dhanya. B
Topic : Text Summarisation with NLP

Algorithm working:
1. Split the passage into sentences and leave only the alphabets behind.
2. Now, create a zero matrix in size = n x n , where n -  number of sentences.
3. Then calculate the similarity between each sentence and for same sentences the value is 0.
4. Similarity is found by,
    - lowercasing the sentence
    - finding unique words from both sentences
    - removing stopwords
    - incrementing the count by each occurrence
    - then we find the (cosine distance --> ?) and use cos_simi = 1 - cosine distance
5. Then we use the networkx lib to do the following
    - creating graph using nx.from_numpy_array()
    - finding the scores using nx.pagerank()
6. Rank the sentences in descending order
7. Create the summary
8. Send the summary to find the rouge score of the candidate and reference summaries

"""

from nltk.corpus import stopwords
from nltk.cluster.util import cosine_distance
import numpy as np
import networkx as nx
from rouge import Rouge

ROUGE = Rouge()
 
def read_article(file_name):
    article = file_name.split(". ")
    sentences = []

    for sentence in article:
        print(sentence)
        sentences.append(sentence.replace("[^a-zA-Z]", " ").split(" "))
    sentences.pop() 
    
    return sentences

def sentence_similarity(sent1, sent2, stopwords=None):
    if stopwords is None:
        stopwords = []
 
    sent1 = [w.lower() for w in sent1]
    sent2 = [w.lower() for w in sent2]
 
    all_words = list(set(sent1 + sent2))
 
    vector1 = [0] * len(all_words)
    vector2 = [0] * len(all_words)
 
    # build the vector for the first sentence
    for w in sent1:
        if w in stopwords:
            continue
        vector1[all_words.index(w)] += 1
 
    # build the vector for the second sentence
    for w in sent2:
        if w in stopwords:
            continue
        vector2[all_words.index(w)] += 1
 
    return 1 - cosine_distance(vector1, vector2)
 
def build_similarity_matrix(sentences, stop_words):
    # Create an empty similarity matrix
    similarity_matrix = np.zeros((len(sentences), len(sentences)))
 
    for idx1 in range(len(sentences)):
        for idx2 in range(len(sentences)):
            if idx1 == idx2: #ignore if both are same sentences
                continue 
            similarity_matrix[idx1][idx2] = sentence_similarity(sentences[idx1], sentences[idx2], stop_words)

    return similarity_matrix


def generated_rouge(summary_text, ref_text):
    score = ROUGE.get_scores(summary_text, ref_text)
    return score


def generate_summary(file_name, top_n):
    stop_words = stopwords.words('english')
    summarize_text = []

    # Step 1 - Read text anc split it
    sentences =  read_article(file_name)

    # Step 2 - Generate Similary Martix across sentences
    sentence_similarity_martix = build_similarity_matrix(sentences, stop_words)

    # Step 3 - Rank sentences in similarity martix
    sentence_similarity_graph = nx.from_numpy_array(sentence_similarity_martix)
    scores = nx.pagerank(sentence_similarity_graph)

    # Step 4 - Sort the rank and pick top sentences
    ranked_sentence = sorted(((scores[i],s) for i,s in enumerate(sentences)), reverse=True)    
    # print("Indexes of top ranked_sentence order are ", ranked_sentence)    

    for i in range(top_n):
      summarize_text.append(" ".join(ranked_sentence[i][1]))

    # Step 5 - Offcourse, output the summarize text
    print("Summarize Text: \n", ". ".join(summarize_text))

    summary_text = ". ".join(summarize_text)

    return summary_text

    #generated_rouge(summary_text)

