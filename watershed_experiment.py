from datetime import datetime

from PIL import Image

from imagehash import watershed_hash


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
    print(result.matches(result2, hamming_cutoff=10))
    print(result.matches(result2, bit_error_rate=0.25))
    print("Done")
