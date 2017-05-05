"""
MAP Abstract Data Type
Map() Create a new, empty map. It returns an empty map collection.
put(key,val) Add a new key-value pair to the map. If the key is already in the map then replace the old value with the new value.
get(key) Given a key, return the value stored in the map or None otherwise.
del Delete the key-value pair from the map using a statement of the form del map[key].
len() Return the number of key-value pairs stored in the map.
in Return True for a statement of the form key in map, if the given key is in the map, False otherwise.
"""
from unittest import TestCase


class HashTable(object):
    _empty = object()
    _deleted = object()

    def __init__(self, size=11):
        self.size = size
        self._keys = [self._empty] * size  # keys
        self._values = [self._empty] * size  # values

    def put(self, key, value):
        initial_hash = hash_ = self.hash(key)

        while True:
            if self._keys[hash_] is self._empty or self._keys[hash_] is self._deleted:
                # can assign to hash_ index
                self._keys[hash_] = key
                self._values[hash_] = value
                return
            elif self._keys[hash_] == key:
                # key already exists here, assign over
                self._keys[hash_] = key
                self._values[hash_] = value
                return

            hash_ = self.rehash(hash_)

            if initial_hash == hash_:
                # table is full
                raise ValueError("Table is full")

    def get(self, key):
        initial_hash = hash_ = self.hash(key)
        while True:
            if self._keys[hash_] is self._empty:
                # That key was never assigned
                return None
            elif self._keys[hash_] == key:
                # key found
                return self._values[hash_]

            hash_ = self.rehash(hash_)
            if initial_hash == hash_:
                # table is full and wrapped around
                return None

    def del_(self, key):
        initial_hash = hash_ = self.hash(key)
        while True:
            if self._keys[hash_] is self._empty:
                # That key was never assigned
                return None
            elif self._keys[hash_] == key:
                # key found, assign with deleted sentinel
                self._keys[hash_] = self._deleted
                self._values[hash_] = self._deleted
                return

            hash_ = self.rehash(hash_)
            if initial_hash == hash_:
                # table is full and wrapped around
                return None

    def hash(self, key):
        return key % self.size

    def rehash(self, old_hash):
        """
        linear probing
        """
        return (old_hash + 1) % self.size

    def __getitem__(self, key):
        return self.get(key)

    def __setitem__(self, key, value):
        self.put(key, value)


class TestHashTable(TestCase):
    def test_one_entry(self):
        m = HashTable(10)
        m.put(1, '1')
        self.assertEqual('1', m.get(1))

    def test_add_entry_bigger_than_table_size(self):
        m = HashTable(10)
        m.put(11, '1')
        self.assertEqual('1', m.get(11))

    def test_get_none_if_key_missing_and_hash_collision(self):
        m = HashTable(10)
        m.put(1, '1')
        self.assertEqual(None, m.get(11))

    def test_two_entries_with_same_hash(self):
        m = HashTable(10)
        m.put(1, '1')
        m.put(11, '11')
        self.assertEqual('1', m.get(1))
        self.assertEqual('11', m.get(11))

    def test_get_on_full_table_does_halts(self):
        # and does not search forever
        m = HashTable(10)
        for i in range(10, 20):
            m.put(i, i)
        self.assertEqual(None, m.get(1))

    def test_delete_key(self):
        m = HashTable(10)
        m.put(1, 1)
        m.del_(1)
        self.assertEqual(None, m.get(1))

    def test_delete_key_and_reassign(self):
        m = HashTable(10)
        m.put(1, 1)
        m.del_(1)
        m.put(1, 2)
        self.assertEqual(2, m.get(1))

    def test_assigning_to_full_table_throws_error(self):
        m = HashTable(3)
        m.put(1, 1)
        m.put(2, 2)
        m.put(3, 3)
        with self.assertRaises(ValueError):
            m.put(4, 4)
