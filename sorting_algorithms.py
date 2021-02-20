def qsort(array, left=0, right=-1):
    if right < 0:
        right = len(array) - 1
    if left < right:
        support = _partition(array, left, right)
        qsort(array, left, support)
        qsort(array, support + 1, right)


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


def bubble_sort(array):
    length = len(array)
    for i in range(length - 1):
        for j in range(length - i - 1):
            if array[j] > array[j + 1]:
                array[j], array[j + 1] = array[j + 1], array[j]


SORTING_ALGORITHMS = {
    'quicksort': qsort,
    'bubble_sort': bubble_sort,
    'merge_sort': merge_sort
}
