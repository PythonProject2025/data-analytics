from enum import Enum

class UIState(Enum):

    DEFAULT = "default"
    OUTLIER_DETECTION = "outlier_detection"
    INTERPOLATION = "interpolation"
    SMOOTHING = "smoothing"
    ISOLATION_FOREST = "isolation_forest"
    IQR = "iqr"
    SHOW_SLIDER = "show_slider"
    SHOW_COLUMN = "show_column"
