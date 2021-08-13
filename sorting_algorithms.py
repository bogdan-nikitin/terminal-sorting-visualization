# Quick sort
def quick_sort(array, left=0, right=-1):
    if right < 0:
        right = len(array) - 1
    if left < right:
        support = _partition(array, left, right)
        quick_sort(array, left, support)
        quick_sort(array, support + 1, right)


def _partition(array, left, right):
    support_element = array[(left + right) // 2]
    while left <= right:
        while array[left] < support_element:
            left += 1
        while array[right] > support_element:
            right -= 1
        if left >= right:
            break
        array[left], array[right] = array[right], array[left]
        left += 1
        right -= 1
    return right


# Merge sort
def _merge(arr, left, mid, end):
    right = mid + 1

    # If the direct merge is already sorted
    if arr[mid] <= arr[right]:
        return

    # Two pointers to maintain start
    # of both arrays to merge
    while left <= mid and right <= end:

        # If element 1 is in right place
        if arr[left] <= arr[right]:
            left += 1
        else:
            value = arr[right]
            index = right

            # Shift all the elements between element 1
            # element 2, right by 1.
            while index != left:
                arr[index] = arr[index - 1]
                index -= 1

            arr[left] = value

            # Update all the pointers
            left += 1
            mid += 1
            right += 1


def merge_sort(arr, left=0, right=None):
    if right is None:
        right = len(arr) - 1
    if left < right:
        # Same as (l + r) / 2, but avoids overflow
        # for large l and r
        m = left + (right - left) // 2

        # Sort first and second halves
        merge_sort(arr, left, m)
        merge_sort(arr, m + 1, right)

        _merge(arr, left, m, right)


# Bubble sort
def bubble_sort(array):
    length = len(array)
    for i in range(length - 1):
        for j in range(length - i - 1):
            if array[j] > array[j + 1]:
                array[j], array[j + 1] = array[j + 1], array[j]


# Cocktail shaker sort
def cocktail_shaker_sort(array):
    left = 0
    right = len(array) - 1

    while left <= right:
        for i in range(left, right, +1):
            if array[i] > array[i + 1]:
                array[i], array[i + 1] = array[i + 1], array[i]
        right -= 1

        for i in range(right, left, -1):
            if array[i - 1] > array[i]:
                array[i], array[i - 1] = array[i - 1], array[i]
        left += 1


# Radix sort
def _counting_sort(array, place):
    size = len(array)
    output = [0] * size
    count = [0] * 10

    # Calculate count of elements
    for i in range(0, size):
        index = array[i] // place
        count[index % 10] += 1

    # Calculate cumulative count
    for i in range(1, 10):
        count[i] += count[i - 1]

    # Place the elements in sorted order
    i = size - 1
    while i >= 0:
        index = array[i] // place
        output[count[index % 10] - 1] = array[i]
        count[index % 10] -= 1
        i -= 1

    for i in range(0, size):
        array[i] = output[i]


# Main function to implement radix sort
def radix_sort(array):
    # Get maximum element
    max_element = max(array)

    # Apply counting sort to sort elements based on place value.
    place = 1
    while max_element // place > 0:
        _counting_sort(array, place)
        place *= 10


SORTING_ALGORITHMS = {
    'quicksort': quick_sort,
    'bubble_sort': bubble_sort,
    'merge_sort': merge_sort,
    'cocktail_shaker_sort': cocktail_shaker_sort,
    'radix_sort': radix_sort
}
