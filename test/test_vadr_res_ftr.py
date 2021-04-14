import os
import unittest

from flask import current_app
from flask_testing import TestCase

from manage import app
from main.utils.vadr_runner import VadrResultsFtr

class TestVadrResultsFtr(TestCase):
    def create_app(self):
        app.config.from_object('main.config.DevelopmentConfig')
        return app

    def test_load_from_file(self):
        test_file = "/app/test/test_data/results.vadr.ftr"
        vrf = VadrResultsFtr(test_file)
        self.assertTrue(len(vrf.features) == 54)
        self.assertTrue(vrf.seq_vadr_status == "FAIL")
        self.assertTrue(vrf.features[0] == {
            "type": "gene",
            "name": "ORF1ab",
            "start": "275",
            "end": "21606",
            "seq_coords": "275..21606:+",
            "alerts": "-"
        })
        self.assertTrue(vrf.features[1] == {
            "type": "CDS",
            "name": "ORF1ab_polyprotein",
            "start": "275",
            "end": "21606",
            "seq_coords": "275..13485:+,13485..21606:+",
            "alerts": "CDS_HAS_STOP_CODON(cdsstopn),POSSIBLE_FRAMESHIFT(fstukcnf),INDEFINITE_ANNOTATION_END(indf3pst)"
        })
