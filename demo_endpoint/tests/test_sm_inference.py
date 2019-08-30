import os
from unittest import TestCase

from src.sm_inference import output_fn, input_fn
import torch


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

    def test_output_fn(self):
        # Arrange
        tensor_out = torch.rand((1000, 2))

        # Act
        actual = output_fn(tensor_out, "application/json")

        # Assert
        self.assertIsInstance(actual, str)
