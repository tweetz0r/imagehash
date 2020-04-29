ImageHash
===========

A image hashing library written in Python. ImageHash supports:

* average hashing (`aHash`_)
* perception hashing (`pHash`_)
* difference hashing (`dHash`_)
* wavelet hashing (`wHash`_)
* color hash (colorhash)

|Travis|_ |Coveralls|_

Rationale
---------
Why can we not use md5, sha-1, etc.?

Unfortunately, we cannot use cryptographic hashing algorithms in our implementation. Due to the nature of cryptographic hashing algorithms, very tiny changes in the input file will result in a substantially different hash. In the case of image fingerprinting, we actually want our similar inputs to have similar output hashes as well.

Requirements
-------------
Based on PIL/Pillow Image, numpy and scipy.fftpack (for pHash)
Easy installation through `pypi`_.

Basic usage
------------
::

	>>> from PIL import Image
	>>> import imagehash
	>>> hash = imagehash.average_hash(Image.open('test.png'))
	>>> print(hash)
	d879f8f89b1bbf
	>>> otherhash = imagehash.average_hash(Image.open('other.bmp'))
	>>> print(otherhash)
	ffff3720200ffff
	>>> print(hash == otherhash)
	False
	>>> print(hash - otherhash)
	36

The demo script **find_similar_images** illustrates how to find similar images in a directory.

Source hosted at github: https://github.com/JohannesBuchner/imagehash

.. _aHash: http://www.hackerfactor.com/blog/index.php?/archives/432-Looks-Like-It.html
.. _pHash: http://www.hackerfactor.com/blog/index.php?/archives/432-Looks-Like-It.html
.. _dHash: http://www.hackerfactor.com/blog/index.php?/archives/529-Kind-of-Like-That.html
.. _wHash: https://fullstackml.com/2016/07/02/wavelet-image-hash-in-python/
.. _pypi: https://pypi.python.org/pypi/ImageHash


Example results
-----------------

To help evaluate how different hashes behave, below are a few hashes applied
to two datasets.

The first dataset is a **collection of 7441 free icons on github** (see examples/github-urls.txt).
The pages show groups of images with the same hash (the hashing method sees them as the same).

* `phash hashsize=8 clusters <https://johannesbuchner.github.io/imagehash/art3.html>`_
* `dhash hashsize=8 clusters <https://johannesbuchner.github.io/imagehash/art4.html>`_
* `whash-haar hashsize=8 clusters <https://johannesbuchner.github.io/imagehash/art5.html>`_
* `whash-db4 hashsize=8 clusters <https://johannesbuchner.github.io/imagehash/art6.html>`_
* `colorhash binbits=3 clusters <https://johannesbuchner.github.io/imagehash/art7.html>`_
* `average_hash hashsize=8 clusters <https://johannesbuchner.github.io/imagehash/art2.html>`_
* `z-transform+phash hashsize=8 clusters <https://johannesbuchner.github.io/imagehash/art9.html>`_
* `z-transform+dhash hashsize=8 clusters <https://johannesbuchner.github.io/imagehash/art10.html>`_
* `z-transform+whash-haar hashsize=8 clusters <https://johannesbuchner.github.io/imagehash/art11.html>`_
* `z-transform+whash-db4 hashsize=8 clusters <https://johannesbuchner.github.io/imagehash/art12.html>`_
* `z-transform+average_hash hashsize=8 clusters <https://johannesbuchner.github.io/imagehash/art8.html>`_

The first dataset is a **collection of 109259 art pieces** from parismuseescollections.paris.fr/en/recherche/image-libre/.
The pages show groups of images with the same hash (the hashing method sees them as the same).

* `phash hashsize:8 clusters <https://johannesbuchner.github.io/imagehash/index3.html>`_
* `dhash hashsize:8 clusters <https://johannesbuchner.github.io/imagehash/index4.html>`_
* `whash-haar hashsize:8 clusters <https://johannesbuchner.github.io/imagehash/index5.html>`_
* `whash-db4 hashsize:8 clusters <https://johannesbuchner.github.io/imagehash/index6.html>`_
* `colorhash binbits:3 clusters <https://johannesbuchner.github.io/imagehash/index7.html>`_
* `average_hash hashsize:8 clusters <https://johannesbuchner.github.io/imagehash/index2.html>`_
* `z-transform+phash hashsize:8 clusters <https://johannesbuchner.github.io/imagehash/index9.html>`_
* `z-transform+dhash hashsize:8 clusters <https://johannesbuchner.github.io/imagehash/index10.html>`_
* `z-transform+whash-haar hashsize:8 clusters <https://johannesbuchner.github.io/imagehash/index11.html>`_
* `z-transform+whash-db4 hashsize:8 clusters <https://johannesbuchner.github.io/imagehash/index12.html>`_
* `z-transform+average_hash hashsize:8 clusters <https://johannesbuchner.github.io/imagehash/index8.html>`_

You may want to adjust the hashsize or require some manhattan distance (hash1 - hash2 < threshold).

Changelog
----------

* 4.1: add examples and colorhash

* 4.0: Changed binary to hex implementation, because the previous one was broken for various hash sizes. This change breaks compatibility to previously stored hashes; to convert them from the old encoding, use the "old_hex_to_hash" function.

* 3.5: image data handling speed-up

* 3.2: whash now also handles smaller-than-hash images

* 3.0: dhash had a bug: It computed pixel differences vertically, not horizontally.
       I modified it to follow `dHash`_. The old function is available as dhash_vertical.

* 2.0: added whash

* 1.0: initial ahash, dhash, phash implementations.


.. |Travis| image:: https://travis-ci.org/JohannesBuchner/imagehash.svg?branch=master
.. _Travis: https://travis-ci.org/JohannesBuchner/imagehash

.. |Coveralls| image:: https://coveralls.io/repos/github/JohannesBuchner/imagehash/badge.svg
.. _Coveralls: https://coveralls.io/github/JohannesBuchner/imagehash
