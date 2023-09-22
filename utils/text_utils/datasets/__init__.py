from typing import Dict

from utils.text_utils.datasets.base_text_detection_dataset import (  # noqa
    BaseTextDetectionDataset,
    BaseTextDetectionSample,
    BaseTextDetectionAnnotation)
from utils.text_utils.datasets.ICDAR2003 import ICDAR2003_dataset
from utils.text_utils.datasets.MSRA_TD500 import MSRA_TD500_dataset
from utils.text_utils.datasets.StreetViewText import SVT_dataset
from utils.text_utils.datasets.NEOCR import NEOCR_dataset

datasets: Dict[str, BaseTextDetectionDataset] = {
    'ICDAR2003': ICDAR2003_dataset,
    'MSRA_TD500': MSRA_TD500_dataset,
    'NEOCR': NEOCR_dataset,
    'StreetViewText': SVT_dataset
}
