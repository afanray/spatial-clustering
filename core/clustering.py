from sklearn.cluster import KMeans

def run_clustering(X, params):
    k = params.get("k", 5)

    model = KMeans(
        n_clusters=k,
        random_state=42,
        n_init="auto"
    )

    return model.fit_predict(X)
