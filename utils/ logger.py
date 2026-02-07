from qgis.core import QgsMessageLog, Qgis

def log(message, level=Qgis.Info):
    QgsMessageLog.logMessage(
        message,
        "SpatialClustering",
        level
    )
