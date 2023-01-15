from nltk.corpus import stopwords
from nltk.cluster.util import cosine_distance
import numpy as np
import networkx as nx

def read_article(text):
    filedata = text.split(". ")
    article = filedata[0].split(". ")
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
    for w in sent1:
        if w in stopwords:
            continue
        vector1[all_words.index(w)] += 1
    for w in sent2:
        if w in stopwords:
            continue
        vector2[all_words.index(w)] += 1
    return 1 - cosine_distance(vector1, vector2)

def build_similarity_matrix(sentences, stop_words):
    similarity_matrix = np.zeros((len(sentences), len(sentences)))
    for _, idx1 in enumerate(sentences):
        for _, idx2 in enumerate(sentences):
            if idx1 == idx2:
                continue 
            similarity_matrix[idx1][idx2] = sentence_similarity(sentences[idx1], sentences[idx2], stop_words)
    return similarity_matrix

def generate_summary(file_name, top_n=5):
    stop_words = stopwords.words('english')
    summarize_text = []
    sentences =  read_article(file_name)
    sentence_similarity_martix = build_similarity_matrix(sentences, stop_words)
    sentence_similarity_graph = nx.from_numpy_array(sentence_similarity_martix)
    scores = nx.pagerank(sentence_similarity_graph)
    ranked_sentence = sorted(((scores[i],s) for i,s in enumerate(sentences)), reverse=True)
    print("Indexes of top ranked_sentence order are ", ranked_sentence)
    for i in range(top_n):
        summarize_text.append(" ".join(ranked_sentence[i][1]))
    print("Summarize Text: \n", ". ".join(summarize_text))
    

generate_summary("""the software and server teams. And there's no indication that he plans to sell the company, which he bought in October for $44 billion and quickly took private. So it's clear that he wants to still be involved in the company's operation, but it's unclear just how much. 

It's hard to imagine the hard driving businessman who made a major spectacle of firing Twitter's entire executive team and dissolved the board when he took over simply stepping aside at this point. But he has also in his short reign allowed the whim of polls to make several major decisions. 

Regardless of who eventually takes over as CEO, they'll be taking over a company that is almost unrecognizable compared to just a few months ago. Roughly 70 percent of the staff have either been laid off or quit. Advertisers have fled the platform as hate speech and trolls have thrived. And the content moderation and safety efforts have completely stagnated. The company is also now facing increasing pressure from the government on a number of fronts. 

All products recommended by Engadget are selected by our editorial team, independent of our parent company. Some of our stories include affiliate links. If you buy something through one of these links, we may earn an affiliate commission. All prices are correct at the time of publishing.""")