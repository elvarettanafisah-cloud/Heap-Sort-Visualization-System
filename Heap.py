import random


def generate_array(size, minimum=1, maximum=100):
    array = []

    for _ in range(size):
        number = random.randint(minimum, maximum)
        array.append(number)
    return array

def heapify(array, n, i):
    largest = i

    left = 2 * i + 1
    right = 2 * i + 2

    if left < n and array[left] > array[largest]:
        largest = left
    if right < n and array[right] > array[largest]:
        largest = right

    #If the current node not the largest, swap
    if largest != i:
        array[i], array[largest] = array[largest], array[i]
        #Recursively call heapify on the affect subtree
        heapify(array, n, largest)


def build_max_heap(array):
    n = len(array)

    # Start from the last non-leaf node and go up to the root (index 0)
    # n // 2 - 1 is the index of the last parent node
    for i in range(n // 2 - 1, -1, -1):
        heapify(array, n, i)


def verify_max_heap(array):
    n = len(array)
    for i in range(n):
        left = 2 * i + 1
        right = 2 * i + 2

        # If a left child exists and the parent is smaller than the child, it's NOT a Max-Heap
        if left < n and array[i] < array[left]:
            return False
        # If a right child exists and the parent is smaller than the child, it's NOT a Max-Heap
        if right < n and array[i] < array[right]:
            return False
        # If all checks pass, the array is a valid Max-Heap

    return True
