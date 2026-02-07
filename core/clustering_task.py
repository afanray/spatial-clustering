# from qgis.core import QgsTask
# import traceback

# class SpatialClusteringTask(QgsTask):

#     def __init__(self, layer, fields, params, callbacks):
#         super().__init__("Spatial Clustering", QgsTask.CanCancel)
#         self.layer = layer
#         self.fields = fields
#         self.params = params
#         self.callbacks = callbacks
#         self.result = None
#         self.exception = None

#     def run(self):
#         try:
#             self.setProgress(10)

#             X, fids = self.callbacks["build_features"](
#                 self.layer, self.fields
#             )

#             if self.isCanceled():
#                 return False

#             self.setProgress(60)

#             labels = self.callbacks["cluster"](X, self.params)

#             self.result = (fids, labels)
#             self.setProgress(100)
#             return True

#         except Exception:
#             self.exception = traceback.format_exc()
#             return False

#     def finished(self, success):
#         if not success:
#             self.callbacks["on_error"](self.exception)
#         else:
#             self.callbacks["on_success"](self.result)


from qgis.core import QgsTask
import traceback


class SpatialClusteringTask(QgsTask):
    """
    QgsTask untuk spatial clustering dengan spatial weights opsional.
    """

    def __init__(self, layer, fields, params, callbacks):
        """
        params:
            {
              "k": int,
              "use_weights": bool,
              "weight_type": "queen" | "rook" | "knn",
              "k_neighbors": int (optional, for knn)
            }

        callbacks:
            {
              "build_features": func,
              "cluster": func,
              "weights": func (optional),
              "on_success": func,
              "on_error": func
            }
        """
        super().__init__("Spatial Clustering", QgsTask.CanCancel)

        self.layer = layer
        self.fields = fields
        self.params = params
        self.callbacks = callbacks

        self.result = None
        self.exception = None

    # --------------------------------------------------
    # BACKGROUND THREAD
    # --------------------------------------------------
    def run(self):
        try:
            self.setProgress(5)

            # 1️⃣ Spatial weights (optional)
            weights = None
            if self.params.get("use_weights", False):
                if "weights" not in self.callbacks:
                    raise ValueError("Spatial weights callback tidak tersedia")

                weights = self.callbacks["weights"](
                    self.layer,
                    self.params.get("weight_type", "queen"),
                    self.params.get("k_neighbors", 5)
                )

            if self.isCanceled():
                return False

            self.setProgress(30)

            # 2️⃣ Feature engineering
            X, fids = self.callbacks["build_features"](
                self.layer,
                self.fields,
                weights
            )

            if self.isCanceled():
                return False

            self.setProgress(65)

            # 3️⃣ Clustering
            labels = self.callbacks["cluster"](X, self.params)

            self.result = {
                "fids": fids,
                "labels": labels,
                "weights_used": weights is not None
            }

            self.setProgress(100)
            return True

        except Exception:
            self.exception = traceback.format_exc()
            return False

    # --------------------------------------------------
    # UI THREAD
    # --------------------------------------------------
    def finished(self, success):
        if not success:
            self.callbacks["on_error"](self.exception)
            return

        self.callbacks["on_success"](self.result)
