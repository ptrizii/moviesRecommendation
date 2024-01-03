# film_recommendation.py

import numpy as np
import pandas as pd

# Global variables to store loaded data
metadata = None
embedding = None


def load_data():
    global metadata, embedding
    # Load metadata and embedding data only if not already loaded
    if metadata is None or embedding is None:
        # Load embedding data
        embedding = np.load('Dataset/embd_title_overview/complete-embd.npy')
        # Load metadata (replace 'metadata.csv' with your actual metadata file)
        metadata = pd.read_csv('Dataset/metadata_summary.csv')
        # metadata = metadata.loc[:9000].reset_index(drop=True)


def get_recommendations(query_index, data, embedding, k=10):
    # query_index = query_title
    data_sorted = data.copy()
    # calculated weighted sim
    similarity_scores = weight_similarity(
        query_index, embedding, data['genres'])
    data_sorted['similarity'] = similarity_scores
    # # sorted the list
    data_sorted = data_sorted.sort_values(by='similarity', ascending=False)
    data_sorted = data_sorted[1:k+1]
    
    return data_sorted



def jaccard_score(set1, set2):
    intersection = len(set1.intersection(set2))
    union = len(set1.union(set2))
    return intersection / union if union != 0 else 0


def jaccard_similarity(index, genre):
    # Split genres and convert into list
    genre_set = genre.apply(lambda x: set(x.split(', '))).to_list()
    jaccard_similarities = []
    set1 = genre_set[index]

    for i in range(len(genre_set)):
        scores = []
        set2 = genre_set[i]
        score = jaccard_score(set1, set2)

        jaccard_similarities.append(score)

    jaccard_similarities = np.array(jaccard_similarities)
    return jaccard_similarities


def cosine_score(embd1, embd2):
    dot_product = np.dot(embd1, embd2)
    norm_vec1 = np.linalg.norm(embd1)
    norm_vec2 = np.linalg.norm(embd2)
    # Calculate cosim score
    cosim_score = dot_product / (norm_vec1 * norm_vec2)
    return cosim_score


def cosine_similarity(embd_query, embedding):
    scores = []
    for i in range(len(embedding)):
        score = cosine_score(embd_query, embedding[i])
        scores.append(score)

    scores = np.array(scores)
    return scores


def weight_similarity(query_index, embedding, genres):
    # Define weight for each similarity
    w_jac = 0.3
    w_cos = 0.7

    # Calculate jaccard scores
    jaccard_scores = jaccard_similarity(query_index, genres)
    # Initialize an array to store the cosine scores
    cosine_scores = np.zeros_like(jaccard_scores)

    # Check if Jaccard score is not zero, then calculate cosine scores
    non_zero_jaccard_indices = np.nonzero(jaccard_scores)
    if len(non_zero_jaccard_indices[0]) > 0:
        non_zero_indices = non_zero_jaccard_indices[0]
        # Calculate cosine scores for non-zero Jaccard scores
        cosine_scores[non_zero_indices] = cosine_similarity(
            embedding[query_index], embedding[non_zero_indices])

    # calculate weighted similarity
    weigted_jaccard = jaccard_scores*w_jac
    weighted_cosine = cosine_scores*w_cos

    similarity_scores = weigted_jaccard + weighted_cosine

    return similarity_scores




# if __name__ == "__main__":
#     main()
