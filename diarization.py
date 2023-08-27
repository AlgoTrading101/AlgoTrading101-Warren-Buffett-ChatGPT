"""Diarization functions."""

import numpy as np
from numpy import ndarray
from scipy.stats import mode
from sklearn.cluster import AgglomerativeClustering, KMeans
from sklearn.metrics import silhouette_score
from sklearn.mixture import GaussianMixture


def find_n_speakers(embeddings: ndarray) -> int:
    """Find the best number of speakers in the audio."""
    score_num_speakers = {}

    for num_speakers in range(1, 15):
        clustering = AgglomerativeClustering(num_speakers).fit(embeddings)
        score = silhouette_score(embeddings, clustering.labels_, metric="euclidean")
        score_num_speakers[num_speakers] = score

    best_num_speaker = max(score_num_speakers, key=lambda x: score_num_speakers[x])

    return best_num_speaker


def label_segments_with_speakers(
    final_num_speakers: int, embeddings: ndarray, segments: list
) -> list:
    """Label segments with speakers."""
    kmeans = KMeans(n_clusters=final_num_speakers)
    labels_kmeans = kmeans.fit_predict(embeddings)

    ahc = AgglomerativeClustering(n_clusters=final_num_speakers)
    labels_ahc = ahc.fit_predict(embeddings)

    gmm = GaussianMixture(n_components=final_num_speakers)
    labels_gmm = gmm.fit_predict(embeddings)

    # Majority voting
    labels = np.stack([labels_kmeans, labels_ahc, labels_gmm])
    labels_majority_vote, _ = mode(labels, axis=0)

    for i in range(len(segments)):
        segments[i]["speaker"] = "SPEAKER " + str(labels_majority_vote[i] + 1)

    return segments
