import os
from unittest import TestCase

import numpy as np

from sm_inference import input_fn


class TestInput_fn(TestCase):
    def test_input_fn(self):
        # Arrange
        img_name = os.path.join(os.path.dirname(__file__), "images", "39672681_1302d204d1.jpg")
        with open(img_name, "rb") as f:
            image_bytes = f.read()

        # Act
        actual = input_fn(image_bytes, "application/binary")

        # Assert
        self.assertEqual(len(actual.shape), 4)
