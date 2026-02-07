def classFactory(iface):
    from .main_plugin import SpatialClusteringPlugin
    return SpatialClusteringPlugin(iface)
