from qgis.core import (
    QgsSymbol,
    QgsRendererCategory,
    QgsCategorizedSymbolRenderer
)

def apply_cluster_style(layer, field="cluster"):
    idx = layer.fields().indexFromName(field)
    categories = []

    for value in layer.uniqueValues(idx):
        symbol = QgsSymbol.defaultSymbol(layer.geometryType())
        symbol.setRandomColor()
        categories.append(
            QgsRendererCategory(value, symbol, str(value))
        )

    renderer = QgsCategorizedSymbolRenderer(field, categories)
    layer.setRenderer(renderer)
    layer.triggerRepaint()
