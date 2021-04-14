import os
import unittest

from ..utils.vadr_runner import VadrResultsFtr

class TestVadrResultsFtr(TestCase):

    def test_load_from_file(self):
        test_file = "test_data/results.vadr.ftr"
        VadrResultsFtr(test_file)