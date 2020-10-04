from datetime import datetime

import numpy
from PIL import Image, ImageFilter

import imagehash


def find_region(pixels, segmented_pixels, segment_threshold_ratio, segmentation_img_size, from_highest=True):
    in_region = set()
    not_in_region = set()
    highest = numpy.unravel_index(numpy.nanargmax(pixels, axis=None), pixels.shape)
    lowest = numpy.unravel_index(numpy.nanargmin(pixels, axis=None), pixels.shape)
    peak = pixels[highest]
    trough = pixels[lowest]
    if from_highest:
        threshold = (peak - ((peak - trough) * segment_threshold_ratio))
        in_region.add(highest)
    else:
        threshold = (trough + ((peak - trough) * segment_threshold_ratio))
        in_region.add(lowest)
    new_pixels = in_region.copy()
    while True:
        try_next = set()
        # Find surrounding pixels
        for pixel in new_pixels:
            x, y = pixel
            new_pixels = []
            if x > 0:
                new_pixels.append((x - 1, y))
            if x < segmentation_img_size - 1:
                new_pixels.append((x + 1, y))
            if y > 0:
                new_pixels.append((x, y - 1))
            if y < segmentation_img_size - 1:
                new_pixels.append((x, y + 1))
            try_next.update(new_pixels)
        try_next -= in_region
        try_next -= not_in_region
        try_next -= segmented_pixels
        if not try_next:
            break
        # Check those
        if from_highest:
            upper, lower = peak, threshold
        else:
            upper, lower = threshold, trough
        new_pixels = set()
        for pixel in try_next:
            if upper > pixels[pixel] > lower:
                in_region.add(pixel)
                new_pixels.add(pixel)
            else:
                not_in_region.add(pixel)
    return in_region


def watershed_hash(image):
    # Define some tunable params
    segmentation_img_size = 300
    gaussian_blur = 2
    median_filter = 3
    segment_threshold_ratio = 0.3
    segmentation_required = 0.5
    min_segment_size = 100
    hash_func = imagehash.dhash

    orig_image = image.copy()
    orig_w, orig_h = orig_image.size
    # Convert to gray scale and resize
    image = image.convert("L").resize((segmentation_img_size, segmentation_img_size), Image.ANTIALIAS)
    # Add filters
    image = image.filter(ImageFilter.GaussianBlur(gaussian_blur)).filter(ImageFilter.MedianFilter(median_filter))
    pixels = numpy.array(image).astype(numpy.float32)

    segments = []
    already_segmented = set()
    while len(already_segmented) < segmentation_img_size * segmentation_img_size * segmentation_required:
        segment = find_region(pixels, already_segmented, segment_threshold_ratio, segmentation_img_size, True)
        # Apply segment
        if len(segment) > min_segment_size:
            segments.append(segment)
        for pix in segment:
            pixels[pix] = numpy.NaN
        already_segmented.update(segment)
        segment = find_region(pixels, already_segmented, segment_threshold_ratio, segmentation_img_size, False)
        # Apply segment
        if len(segment) > min_segment_size:
            segments.append(segment)
        for pix in segment:
            pixels[pix] = numpy.NaN
        already_segmented.update(segment)

    # Create bounding box for each segment
    hashes = []
    for segment in segments:
        scale_w = 1  # orig_w / segmentation_img_size
        scale_h = 1  # orig_h / segmentation_img_size
        min_y = min(coord[0] for coord in segment) * scale_h
        min_x = min(coord[1] for coord in segment) * scale_w
        max_y = (max(coord[0] for coord in segment)+1) * scale_h
        max_x = (max(coord[1] for coord in segment)+1) * scale_w
        # Compute robust hash for each bounding box
        bounding_box = image.crop((min_x, min_y, max_x, max_y))
        hashes.append(hash_func(bounding_box))
        # Show bounding box
        #show_segments(image, segment)
        #bounding_box.show()

    return imagehash.CropResistantHash(hashes)


def show_segments(image, segment):
    im_segment = image.copy()
    for pix in segment:
        im_segment.putpixel(pix[::-1], 255)
    im_segment.show()


if __name__ == "__main__":
    start_time = datetime.now()
    img = Image.open("alpacabread_Lorg.png")
    result = watershed_hash(img)
    print(datetime.now() - start_time)

    start_time = datetime.now()
    img2 = Image.open("alpacabread_Lorg-crop.png")
    result2 = watershed_hash(img2)
    print(datetime.now() - start_time)
    print(result)
    print(result2)
    print(result == result2)
    print(result.matches(result2, 10))
    print("Done")
