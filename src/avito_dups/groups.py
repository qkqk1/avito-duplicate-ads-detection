import numpy as np
import pandas as pd
from scipy.sparse import coo_matrix
from scipy.sparse.csgraph import connected_components


def pair_groups(first_ids: np.ndarray, second_ids: np.ndarray) -> np.ndarray:
    n_pairs = len(first_ids)
    codes, uniques = pd.factorize(np.concatenate([first_ids, second_ids]))
    left = codes[:n_pairs]
    right = codes[n_pairs:]
    n_items = len(uniques)
    graph = coo_matrix((np.ones(n_pairs), (left, right)), shape=(n_items, n_items))
    _, labels = connected_components(graph, directed=False)
    return labels[left]
