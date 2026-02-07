def write_clusters(out_layer, src_layer, fids, labels):
    dp = out_layer.dataProvider()
    cluster_map = dict(zip(fids, labels))

    feats = []
    for feat in src_layer.getFeatures():
        new_feat = feat.clone()
        new_feat.setFields(out_layer.fields())
        new_feat["cluster"] = int(cluster_map[feat.id()])
        feats.append(new_feat)

    dp.addFeatures(feats)
