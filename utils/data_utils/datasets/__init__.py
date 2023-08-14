from typing import Dict

from utils.data_utils.datasets.base_dataset import (  # noqa
    BaseDataset, BaseSample, BaseAnnotation)
from utils.data_utils.datasets.ICDAR2003 import ICDAR2003_dataset
from utils.data_utils.datasets.MSRA_TD500 import MSRA_TD500_dataset
from utils.data_utils.datasets.StreetViewText import SVT_dataset
from utils.data_utils.datasets.NEOCR import NEOCR_dataset

datasets: Dict[str, BaseDataset] = {
    'ICDAR2003': ICDAR2003_dataset,
    'MSRA_TD500': MSRA_TD500_dataset,
    'NEOCR': NEOCR_dataset,
    'StreetViewText': SVT_dataset
}
