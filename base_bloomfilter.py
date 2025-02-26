from math import ceil, log
import bitarray
import hashlib


class BloomFilter:
    def __init__(self, expected_items, false_positive_rate):
        self.size = ceil((-expected_items * log(false_positive_rate)) / (log(2) ** 2))
        self.hash_count = ceil((self.size / expected_items) * log(2))
        self.bit_array = bitarray.bitarray(self.size)
        self.bit_array.setall(0)

    def _hashes(self, item):
        hash1 = int(hashlib.md5(item.encode()).hexdigest(), 16)
        hash2 = int(hashlib.sha1(item.encode()).hexdigest(), 16)
        return [(hash1 + i * hash2) % self.size for i in range(self.hash_count)]

    def add(self, item):
        for hash_val in self._hashes(item):
            self.bit_array[hash_val] = 1

    def check(self, item):
        return all(self.bit_array[hash_val] for hash_val in self._hashes(item))
