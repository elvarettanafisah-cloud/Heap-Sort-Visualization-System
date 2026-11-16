from Heap import generate_array, heapify, build_max_heap

def heap_sort(array):
  n=len(array)

  #step 1. build_max_heap from the array (read and run function from part 1)
  build_max_heap(array)

  #step 2. Extract the element one by one
  # LOOPING: from last element (n-1) down to the second element (index 1)
  for i in range(n - 1, 0, -1):

    #step 3. SWAPPING: current largest element (array[0]) w/ the last element of the heap (array[i])
    array[0], array[i] = array[i], array[0]

    #step 4. CALL (heapify) on the reduced heap (size i)
    # to restore the Max-Heap property on the remaining elements
    heapify(array, i, 0)
  return array
