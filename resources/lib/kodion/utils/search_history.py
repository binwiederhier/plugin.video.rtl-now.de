import hashlib

from storage import Storage

class SearchHistory(Storage):
    def __init__(self, filename, max_items=10):
        Storage.__init__(self, filename, max_item_count=max_items)
        pass

    def __del__(self):
        Storage.__del__(self)
        pass

    def is_empty(self):
        return self._is_empty()

    def list(self):
        result = []

        keys = self._get_ids(oldest_first=False)
        for key in keys:
            item = self._get(key)
            result.append(item[0])
            pass

        return result

    def clear(self):
        self._clear()
        pass

    def _make_id(self, search_text):
        m = hashlib.md5()
        m.update(search_text.encode('utf-8'))
        return m.hexdigest()

    def remove(self, search_text):
        self._remove(self._make_id(search_text))
        pass

    def update(self, search_text):
        self._set(self._make_id(search_text), search_text)
        pass

    pass