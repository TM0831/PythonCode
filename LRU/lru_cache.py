"""
Version: Python3.7
Author: OniOn
Site: http://www.cnblogs.com/TM0831/
Time: 2020/7/8 18:08
"""


# Node of the list
class Node:
    def __init__(self, val):
        self.val = val
        self.prev = None
        self.next = None

    def __str__(self):
        return "The value is " + str(self.val)


# Double Linked List
class DoubleList:
    def __init__(self):
        self.head = None
        self.tail = None

    def is_empty(self):
        """
        returns true if the list is empty, false otherwise
        :return:
        """
        return self.head is None

    def append(self, value):
        """
        append element after the list
        :param value: the value of node
        :return:
        """
        node = Node(value)
        if self.is_empty():
            self.head = node
            self.tail = node
            return
        cur = self.head
        # find the tail of the list
        while cur.next:
            cur = cur.next
        cur.next = node
        node.prev = cur
        self.tail = node

    def remove(self, value):
        """
        if value in the list, remove the element
        :param value: the value of node
        :return:
        """
        if self.is_empty():
            return
        cur = self.head
        while cur:
            if cur.val == value:
                if len(self) == 1:
                    # when the list has only one node
                    self.head, self.tail = None, None
                else:
                    if cur == self.head:
                        self.head = cur.next
                    elif cur == self.tail:
                        self.tail = cur.prev
                    else:
                        cur.prev.next = cur.next
                return
            else:
                cur = cur.next

    def traverse(self):
        """
        iterate through the list
        :return:
        """
        cur = self.head
        index = 1
        while cur:
            print("Index: {}".format(index) + cur)
            cur = cur.next
            index += 1

    def __len__(self):
        count = 0
        cur = self.head
        while cur:
            count += 1
            cur = cur.next
        return count

    def __str__(self):
        cur = self.head
        ret = ""
        while cur:
            ret += str(cur.val) + "->" if cur.next else str(cur.val)
            cur = cur.next
        return ret


# LRU Cache
class LRU:
    def __init__(self, size):
        self.size = size
        self._list = DoubleList()
        self._cache = dict()

    def _set_recent(self, node):
        """
        set the node to most recently used
        :param node: node
        :return:
        """
        # when the node is the tail of the list
        if node == self._list.tail:
            return
        cur = self._list.head
        while cur:
            # remove the node from the list
            if cur == node:
                if cur == self._list.head:
                    self._list.head = cur.next
                else:
                    prev = cur.prev
                    prev.next = cur.next
            if cur.next:
                cur = cur.next
            else:
                break
        # set node to the tail of the list
        cur.next = node
        node.next = None
        node.prev = cur
        self._list.tail = node

    def get(self, key):
        """
        get value of the key
        :param key: key
        :return:
        """
        node = self._cache.get(key, None)
        if not node:
            return
        self._set_recent(node)
        return node.val

    def put(self, key, value):
        """
        set value of the key and add to the cache
        :param key: key
        :param value: value
        :return:
        """
        node = self._cache.get(key, None)
        if not node:
            if len(self._list) < self.size:
                self._list.append(value)
            else:
                # when the quantity reaches the maximum, delete the head node
                name = None
                for k, v in self._cache.items():
                    if v == self._list.head:
                        name = k
                if name:
                    del self._cache[name]
                self._list.head = self._list.head.next
                self._list.append(value)
        else:
            self._set_recent(node)
            self._list.tail.val = value
        # add to cache
        self._cache[key] = self._list.tail

    def show(self):
        """
        show data of the list
        :return:
        """
        return "The list is: {}".format(self._list)


if __name__ == '__main__':
    lru = LRU(8)
    for i in range(10):
        lru.put(str(i), i)
    print(lru.show())
    for i in range(10):
        if i % 3 == 0:
            print("Get {}: {}".format(i, lru.get(str(i))))
    print(lru.show())
    lru.put("2", 22)
    lru.put("4", 44)
    lru.put("6", 66)
    print(lru.show())
