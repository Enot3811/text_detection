"""API class for connecting `BaseDataset` classes family and viewer gui."""

import sys
from pathlib import Path
from typing import List, Dict

sys.path.append(str(Path(__file__).parents[4]))
from utils.data_utils.datasets import BaseDataset, BaseSample


class ViewerDataset:

    class Subset:
        def __init__(
            self, subset: List[BaseSample], start_idx: int = 0
        ) -> None:
            self._subset = subset
            self._current_idx = start_idx

        def __getitem__(self, idx: int):
            return self._subset[idx]
        
        def next_sample(self) -> BaseSample:
            """Get a next sample and increment a current index.

            If the incremented index is out of bounds it will be returned
            to start of a subset.

            Returns
            -------
            BaseSample
                The got sample.
            """
            self._current_idx = (self._current_idx + 1) % len(self._subset)
            return self._subset[self._current_idx]
        
        def previous_sample(self) -> BaseSample:
            """Get a next sample and decrement a current index.

            If the decremented index is out of bounds it will be returned
            to end of a subset.

            Returns
            -------
            BaseSample
                The got sample.
            """
            idx = self._current_idx - 1
            self._current_idx = idx if idx >= 0 else len(self._subset) - 1
            return self._subset[self._current_idx]
        
        def set_index(self, idx: int):
            """Set a new value for subset's index.

            Parameters
            ----------
            idx : int
                The new value for the index.
            """
            self._current_idx = idx

        def get_current_sample(self) -> BaseSample:
            """Get a current sample.

            Returns
            -------
            BaseSample
                The current sample.
            """
            return self._subset[self._current_idx]

    def __init__(self, dataset: BaseDataset) -> None:
        self.dset = dataset
        self.subsets: Dict[str, self.Subset] = {
            subset_name: self.Subset(dataset[subset_name])
            for subset_name in ('train', 'val', 'test')
            if len(dataset[subset_name]) != 0
        }
        self.current_subset = list(self.subsets.keys())[0]

    def __getitem__(self, subset_name: str):
        return self.subsets[subset_name]

    def available_subsets(self) -> List[str]:
        """Get names of available subsets.

        Returns
        -------
        List[str]
            The names of available subsets.
        """
        return [subset_name for subset_name in self.subsets]
    
    def get_current_subset(self) -> 'Subset':
        """Get a current subset.

        Returns
        -------
        List[BaseSample]
            The current subset.
        """
        return self.subsets[self.current_subset]
    
    def set_current_subset(self, subset_name: str):
        """Set a new value for current subset.

        Parameters
        ----------
        subset_name : str
            The new value for current subset.
        """
        self.current_subset = subset_name

    def next_sample(self) -> BaseSample:
        """Get a next sample of a current subset and increment its index.

        If the incremented index is out of bounds it will be returned
        to start of a subset.

        Returns
        -------
        BaseSample
            The next sample of the current subset.
        """
        return self.subsets[self.current_subset].next_sample()
    
    def previous_sample(self) -> BaseSample:
        """Get a previous sample of a current subset and decrement its index.

        If the decremented index is out of bounds it will be returned
        to end of a subset.

        Returns
        -------
        BaseSample
            The previous sample of the current subset.
        """
        return self.subsets[self.current_subset].previous_sample()
    
    def get_current_sample(self) -> BaseSample:
        """Get a current sample of a current subset.

        Returns
        -------
        BaseSample
            The current sample of the current subset.
        """
        return self.get_current_subset().get_current_sample()
