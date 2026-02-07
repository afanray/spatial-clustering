from qgis.core import QgsSpatialIndex

def queen_weights(layer):
    index = QgsSpatialIndex(layer.getFeatures())
    neighbors = {}

    for f in layer.getFeatures():
        bbox_ids = index.intersects(f.geometry().boundingBox())
        neighs = []

        for i in bbox_ids:
            if i == f.id():
                continue
            g = layer.getFeature(i).geometry()
            if f.geometry().touches(g) or f.geometry().intersects(g):
                neighs.append(i)

        neighbors[f.id()] = neighs

    return neighbors
