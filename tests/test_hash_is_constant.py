import hashlib

import numpy
from PIL import ImageFilter
from PIL import Image

import imagehash
from tests import TestImageHash


def _calculate_segment_properties(segment):
	length = len(segment)
	min_y = min(coord[0] for coord in segment)
	min_x = min(coord[1] for coord in segment)
	max_y = max(coord[0] for coord in segment)
	max_x = max(coord[1] for coord in segment)
	return {
		"length": length,
		"min_x": min_x,
		"min_y": min_y,
		"max_x": max_x,
		"max_y": max_y
	}


class Test(TestImageHash):
	def setUp(self):
		self.image = self.get_data_image()
		self.peppers = self.get_data_image("peppers.png")

	def test_average_hash(self):
		result_hash = imagehash.average_hash(self.image)
		known_hash = "ffd7918181c9ffff"
		self.assertEqual(str(result_hash), known_hash)

	def test_phash(self):
		result_hash = imagehash.phash(self.image)
		known_hash = "ba8c84536bd3c366"
		self.assertEqual(str(result_hash), known_hash)

	def test_dhash(self):
		result_hash = imagehash.dhash(self.image)
		known_hash = "0026273b2b19550e"
		self.assertEqual(str(result_hash), known_hash)

	def test_whash(self):
		result_hash = imagehash.whash(self.image)
		known_hash = "ffd391818181a5e7"
		self.assertEqual(str(result_hash), known_hash)

	def test_color_hash(self):
		result_hash = imagehash.colorhash(self.image)
		known_hash = "07007000000"
		self.assertEqual(str(result_hash), known_hash)

	def test_crop_resistant_hash(self):
		result_hash = imagehash.crop_resistant_hash(self.peppers)
		known_hash = "c4d9f1e3e1c18101,706c6e66464c99b9,98d8f1ecd8f0f0e1,a282c0c49acc6dbd,b1f39b99e1c1b1b1,3a7ece1c9df4fcb9"
		self.assertEqual(str(result_hash), known_hash)

	def test_crop_resistant_segmentation(self):
		# Image pre-processing
		self.assertEqual(hashlib.md5(self.peppers.tobytes()).hexdigest(), "7c19bbf1c9184471ebb2e7e0086910c6")
		image = self.peppers.convert("L")
		self.assertEqual(hashlib.md5(image.tobytes()).hexdigest(), "61442e74c83cfea67d182481c24c5f3e")
		image = image.resize((300, 300), Image.ANTIALIAS)
		self.assertEqual(hashlib.md5(image.tobytes()).hexdigest(), "72f73a3ae87d7ae47be84dccb7ad106d")
		# Add filters
		image = image.filter(ImageFilter.GaussianBlur()).filter(ImageFilter.MedianFilter())
		pixels = numpy.array(image).astype(numpy.float32)
		self.assertEqual(hashlib.md5(image.tobytes()).hexdigest(), "3ae9f318f68a2d7c122256fbda6ca5ec")
		# Segment
		segments = imagehash._find_all_segments(pixels, 128, 500)
		known_segment_count = 6
		self.assertEqual(len(segments), known_segment_count)
		known_segments = sorted([
			{'length': 591, 'min_x': 20, 'min_y': 0, 'max_x': 60, 'max_y': 31},
			{'length': 1451, 'min_x': 61, 'min_y': 0, 'max_x': 156, 'max_y': 58},
			{'length': 12040, 'min_x': 157, 'min_y': 0, 'max_x': 299, 'max_y': 147},
			{'length': 3452, 'min_x': 0, 'min_y': 111, 'max_x': 97, 'max_y': 191},
			{'length': 8701, 'min_x': 112, 'min_y': 145, 'max_x': 299, 'max_y': 259},
			{'length': 61179, 'min_x': 0, 'min_y': 0, 'max_x': 299, 'max_y': 299}
		], key=lambda x: (x["length"], x["min_x"], x["min_y"], x["max_x"], x["max_y"]))
		segment_properties = sorted([
			_calculate_segment_properties(segment) for segment in segments
		], key=lambda x: (x["length"], x["min_x"], x["min_y"], x["max_x"], x["max_y"]))
		self.assertEqual(segment_properties, known_segments)
