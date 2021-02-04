import numpy as np
from sklearn.neighbors import NearestNeighbors

class Ranker():
  def __init__(self, embs, meta):
    """
    embs: numpy array of vectors for each document
    meta: list of arbitrary metainformation with same indexing (used for output) == sample
    """
    self.embs = embs
    self.meta = meta
    #
    self.model = None

  def get_nearest(self, v_query, topn=10, metric='cosine'):
    """
    Outputs indexes of topn nearest vectors from self.embs
    v_query: vector of the query
    topn: how many indexes to output
    metric: see sklearn docs for NearestNeighbors
    """
    self.v_query = v_query
    if self.model is None:
      self.model = NearestNeighbors(metric=metric, n_jobs=-1)
      self.model.fit(self.embs)

    all_neighb = self.model.kneighbors([self.v_query], return_distance=False) # get near neighb
    ixs = all_neighb[0] #
    return ixs
  #
  def get_attributes(self, ixs):
    attrs = [self.meta[i] for i in ixs]
    return attrs