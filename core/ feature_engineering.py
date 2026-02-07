import numpy as np

def build_features(layer, fields, weights=None):
    X = []
    fids = []

    for feat in layer.getFeatures():
        row = [feat[f] or 0 for f in fields]

        if weights:
            neigh_ids = weights.get(feat.id(), [])
            row.append(len(neigh_ids))  # contoh spatial lag

        X.append(row)
        fids.append(feat.id())

    return np.array(X), fids
