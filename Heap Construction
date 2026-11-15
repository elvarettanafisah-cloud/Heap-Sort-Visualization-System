import random


def generate_array(size, minimum=1, maximum=100):
    #create an empty list to store the numbers
    array = []
    #loop 'size' times to generate random numbers
    for _ in range(size):
        #pick a random integer between min and max
        number = random.randint(minimum, maximum)
        #add a number to array
        array.append(number)
    #return the completed array
    return array


def heapify(array, n, i):
    #the current node (i) is the largest
    largest = i
    #calculate the index of the left child
    left = 2 * i + 1
    #calculate the index of the right child
    right = 2 * i + 2
    #if the left greater than the current largest, update largest
    if left < n and array[left] > array[largest]:
        largest = left
    #if the right greater than the current largest, update largest
    if right < n and array[right] > array[largest]:
        largest = right

    #if the current node not the largest, swap
    if largest != i:
        #swap w/ the largest child
        array[i], array[largest] = array[largest], array[i]
        #recursively call heapify on the affect subtree
        heapify(array, n, largest)


def build_max_heap(array):
    #get the length of the array
    n = len(array)

    # Start from the last non-leaf node and go up to the root (index 0)
    # n // 2 - 1 is the index of the last parent node
    for i in range(n // 2 - 1, -1, -1):
        # Call heapify for each node to build the Max-Heap
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
