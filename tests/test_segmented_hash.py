from __future__ import (absolute_import, division, print_function)

import unittest
from datetime import datetime

import imagehash
from .utils import TestImageHash


class Test(TestImageHash):
    def setUp(self):
        self.image = self.get_data_image()

    def test_segmented_hash(self):
        original_hash = imagehash.segmented_hash(self.image)
        rotate_image = self.image.rotate(-1)
        small_rotate_hash = imagehash.segmented_hash(rotate_image)
        emsg = ('slightly rotated image should have '
                'similar hash {} {}'.format(original_hash, small_rotate_hash))
        self.assertTrue(original_hash.matches(small_rotate_hash), emsg)
        rotate_image = self.image.rotate(-90)
        large_rotate_hash = imagehash.segmented_hash(rotate_image)
        emsg = ('rotated image should have different '
                'hash {} {}'.format(original_hash, large_rotate_hash))
        self.assertFalse(original_hash.matches(large_rotate_hash), emsg)

        other_hashes = [small_rotate_hash, large_rotate_hash]
        self.assertEqual(
            original_hash.best_match(other_hashes),
            small_rotate_hash,
            "Hash of the slightly rotated image should be a better match than for the more heavily rotated image."
        )

    def test_segmented_hash__hash_func(self):
        segmented_ahash = imagehash.segmented_hash(self.image, imagehash.average_hash)
        segmented_dhash = imagehash.segmented_hash(self.image, imagehash.dhash)
        self.assertFalse(
            segmented_ahash.matches(segmented_dhash),
            "Segmented hash should not match when the underlying hashing method is not the same"
        )

    def test_segmented_hash__limit_segments(self):
        segmented_orig = imagehash.segmented_hash(self.image)
        segmented_limit = imagehash.segmented_hash(self.image, limit_segments=1)
        self.assertGreaterEqual(
            len(segmented_orig.segment_hashes), len(segmented_limit.segment_hashes),
            "Limit segments should mean there are fewer segments"
        )
        self.assertEqual(
            len(segmented_limit.segment_hashes), 1,
            "Limit segments should correctly limit the segment count"
        )

    def test_segmented_hash__segment_threshold(self):
        segmented_low_threshold = imagehash.segmented_hash(self.image, segment_threshold=20)
        segmented_high_threshold = imagehash.segmented_hash(self.image, segment_threshold=250)
        self.assertFalse(
            segmented_low_threshold.matches(segmented_high_threshold, region_cutoff=3),
            "Segmented hash should not match when segment threshold is changed"
        )

    def test_segmentation_image_size(self):
        start_time = datetime.now()
        imagehash.segmented_hash(self.image, segmentation_image_size=200)
        small_timed = datetime.now() - start_time

        start_time = datetime.now()
        imagehash.segmented_hash(self.image, segmentation_image_size=400)
        large_timed = datetime.now() - start_time

        self.assertGreater(large_timed, small_timed, "Hashing should take longer when the segmentation image is larger")


if __name__ == '__main__':
    unittest.main()
