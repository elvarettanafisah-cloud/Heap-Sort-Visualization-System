import math
import time
import os
import random
import matplotlib.pyplot as plt
import networkx as nx

from Heap import generate_array, verify_max_heap


# Store each step of the sorting process
class HeapRecorder:
    def __init__(self):
        self.steps = []
        self.step_counter = 0

    def record(self, array, action, heap_size=None, highlight=None, phase=""):
        self.step_counter += 1

        self.steps.append({
            "step": self.step_counter,
            "phase": phase,
            "action": action,
            "array": array.copy(),
            "heap_size": heap_size if heap_size is not None else len(array),
            "highlight": highlight if highlight is not None else []
        })


# Display the array and mark the active heap and sorted elements
def array_bar(array, heap_size, highlight):
    output = []

    for i, value in enumerate(array):
        tag = "*" if i in highlight else " "
        state = "H" if i < heap_size else "S"
        output.append(f"{tag}{state}{value:>3}")

    return " ".join(output)


# Display the heap as a binary tree

def draw_heap_tree(array, heap_size, highlight):
    G = nx.Graph()

    for i in range(heap_size):
        G.add_node(i)

        left = 2 * i + 1
        right = 2 * i + 2

        if left < heap_size:
            G.add_edge(i, left)

        if right < heap_size:
            G.add_edge(i, right)

    # Position nodes according to their tree levels
    pos = {}
    levels = heap_size.bit_length()

    for i in range(heap_size):
        level = (i + 1).bit_length() - 1
        position = i - (2 ** level - 1)
        width = 2 ** level

        x = (position - (width - 1) / 2) / width
        y = -level
        pos[i] = (x, y)

    node_colors = [
        "orange" if i in highlight else "skyblue"
        for i in range(heap_size)
    ]

    nx.draw(
        G,
        pos,
        labels={i: array[i] for i in range(heap_size)},
        with_labels=True,
        node_color=node_colors,
        node_size=1000,
        font_size=12,
        font_weight="bold",
        edge_color="gray",
        width=2
    )


def visualize(steps, delay=0.4):
    if not steps:
        print("No visualization steps recorded.")
        return

    plt.ion()

    fig, ax = plt.subplots(figsize=(10, 6))

    for step in steps:
        ax.clear()

        heap_size = step["heap_size"]
        array = step["array"]
        highlight = step["highlight"]

        ax.set_title(
            f"Step {step['step']} | {step['phase'].upper()}\n"
            f"{step['action']}\n"
            f"Active Heap Size: {heap_size}",
            fontsize=12
        )

        draw_heap_tree(array, heap_size, highlight)

        ax.axis("off")
        plt.tight_layout()
        plt.pause(delay)

    plt.ioff()
    plt.show()

    print("\nFinal Sorted Array:", steps[-1]["array"])


# Heapify function that also records each swap
def recorded_heapify(array, n, i, recorder, phase):
    largest = i
    left = 2 * i + 1
    right = 2 * i + 2

    if left < n and array[left] > array[largest]:
        largest = left

    if right < n and array[right] > array[largest]:
        largest = right

    if largest != i:
        old_parent = array[i]
        old_child = array[largest]

        array[i], array[largest] = array[largest], array[i]

        recorder.record(
            array,
            f"Heapify Down: swapped {old_parent} and {old_child}",
            n,
            [i, largest],
            phase
        )

        recorded_heapify(array, n, largest, recorder, phase)


# Perform Heap Sort and record the intermediate states
def recorded_heap_sort(array, recorder):
    n = len(array)

    recorder.record(
        array,
        "Initial Array",
        n,
        phase="initial"
    )

    # Build the Max-Heap
    for i in range(n // 2 - 1, -1, -1):
        recorded_heapify(array, n, i, recorder, "build")

    recorder.record(
        array,
        "Max-Heap Construction Completed",
        n,
        phase="build"
    )

    # Move the largest element to the end one by one
    for i in range(n - 1, 0, -1):
        maximum = array[0]
        last_element = array[i]

        array[0], array[i] = array[i], array[0]

        recorder.record(
            array,
            f"Extract Maximum: {maximum}, swap with {last_element}",
            i,
            [0, i],
            "sort"
        )

        # Restore the Max-Heap property
        recorded_heapify(array, i, 0, recorder, "sort")

        recorder.record(
            array,
            f"Heap Restored: Active heap size = {i}",
            i,
            [i],
            "sort"
        )

    recorder.record(
        array,
        "Sorting Completed",
        0,
        phase="done"
    )

    return array

MAX_SIZE = 20
DEFAULT_SIZE = 10


def get_array_size():
    while True:
        try:
            size = int(input(
                f"Enter array size (1-{MAX_SIZE}): "
            ))

            if size < 1 or size > MAX_SIZE:
                print(
                    f"Error: Size must be between 1 and {MAX_SIZE}."
                )
                continue

            return size

        except ValueError:
            print("Error: Please enter a valid integer.") 


# Test the program and display the result
def run_demo(size=10, seed=10, delay=2):

    random.seed(seed)
    original = generate_array(size)
    print("Original Array:", original)

    data = original.copy()
    recorder = HeapRecorder()

    sorted_array = recorded_heap_sort(data, recorder)

    # Check whether the Max-Heap was built correctly
    build_steps = [
        step for step in recorder.steps
        if step["action"] == "Max-Heap Construction Completed"
    ]

    if build_steps:
        built_heap = build_steps[0]["array"]
        heap_valid = verify_max_heap(built_heap)

        print("\nMax-Heap Verified:", heap_valid)
        assert heap_valid, "Max-Heap construction failed!"

    # Check the final sorting result
    expected = sorted(original)

    print("\nExpected Result:", expected)
    print("Actual Result:", sorted_array)

    assert sorted_array == expected, "Sorting failed!"

    print("\nSorting Correctness: PASSED")
    print("Total Recorded Steps:", len(recorder.steps))

    visualize(recorder.steps, delay=delay)

    return sorted_array, recorder.steps


if __name__ == "__main__":
    size = 10

    choice = input(
        "Use default array size (10)? (y/n): "
    ).lower()

    if choice == "n":
        size = get_array_size()

    run_demo(size=size, seed=10, delay=2)
