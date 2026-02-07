from qgis.PyQt.QtWidgets import QAction, QDialog
from qgis.core import QgsApplication, QgsProject, Qgis
from qgis.utils import iface

from .core.feature_engineering import build_features
from .core.clustering import run_clustering
from .core.clustering_task import SpatialClusteringTask
from .core.output_layer import create_output_layer
from .core.writer import write_clusters

from .utils.validation import validate_inputs
from .utils.styling import apply_cluster_style
from .utils.logger import log


class SpatialClusteringPlugin:

    def __init__(self, iface):
        self.iface = iface
        self.action = None
        self.dialog = None

    def initGui(self):
        self.action = QAction("Spatial Clustering", self.iface.mainWindow())
        self.action.triggered.connect(self.run)
        self.iface.addPluginToMenu("&Spatial Clustering", self.action)

    def unload(self):
        self.iface.removePluginMenu("&Spatial Clustering", self.action)

    def run(self):
        if not self.dialog:
            self.dialog = QDialog()  # load UI via uic if needed
        self.dialog.show()
        
    def start_clustering(self, layer, fields, k, output_name):
        validate_inputs(layer, fields)

        params = {"k": k}

        task = SpatialClusteringTask(
            layer,
            fields,
            params,
            callbacks={
                "build_features": build_features,
                "cluster": run_clustering,
                "on_success": lambda r: self.on_success(r, layer, output_name),
                "on_error": self.on_error
            }
        )

        QgsApplication.taskManager().addTask(task)
        
    def on_success(self, result, src_layer, output_name):
        fids, labels = result

        out = create_output_layer(
            src_layer,
            output_name or "Cluster_Result"
        )

        write_clusters(out, src_layer, fids, labels)
        QgsProject.instance().addMapLayer(out)
        apply_cluster_style(out)
        
    def on_error(self, error):
        iface.messageBar().pushMessage(
            "Spatial Clustering",
            "Proses gagal, cek log",
            level=Qgis.Critical
        )
        log(error, Qgis.Critical)




