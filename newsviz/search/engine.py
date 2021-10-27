# Copyright © 2021 Andrej Ilin. All rights reserved.
# Copyright © 2021 Denis Sidorenko. All rights reserved.
# Copyright © 2021 Sviatoslav Kovalev. All rights reserved.
#    This file is part of NewsViz Project.
#
#    NewsViz Project is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    NewsViz Project is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with NewsViz Project.  If not, see <https://www.gnu.org/licenses/>.
from sklearn.neighbors import NearestNeighbors


class Ranker:
    def __init__(self, embs, meta, metric="cosine"):
        """
        embs: numpy array of vectors for each document
        meta: list of arbitrary metainformation with same
        indexing (used for output) == sample
        """
        self.embs = embs
        self.meta = meta

        self.model = NearestNeighbors(metric=metric, n_jobs=-1)
        self.model.fit(self.embs)

    def get_nearest(self, v_query, topn=10):
        """
        Outputs indexes of topn nearest vectors from self.embs
        v_query: vector of the query
        topn: how many indexes to output
        metric: see sklearn docs for NearestNeighbors
        """
        all_neighb = self.model.kneighbors([v_query], topn, return_distance=False)
        ixs = all_neighb[0]
        return ixs

    def get_attributes(self, ixs):
        """
        Outputs metainformation for vectors
        which of indexes  == `ixs`(from get_nearest)
        """
        attrs = [self.meta[i] for i in ixs]
        return attrs
