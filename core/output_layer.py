from qgis.core import QgsVectorLayer, QgsField
from PyQt5.QtCore import QVariant

def create_output_layer(src_layer, name):
    out = QgsVectorLayer(
        f"{src_layer.wkbType()}?crs={src_layer.crs().authid()}",
        name,
        "memory"
    )

    dp = out.dataProvider()
    dp.addAttributes(src_layer.fields())
    dp.addAttributes([QgsField("cluster", QVariant.Int)])
    out.updateFields()

    return out
