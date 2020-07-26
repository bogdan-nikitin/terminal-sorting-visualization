def qsort(array, left=0, right=-1):
    if right < 0:
        right = len(array) - 1
    if left < right:
        support = partition(array, left, right)
        qsort(array, left, support)
        qsort(array, support + 1, right)


def partition(array, left, right):
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


def bubble_sort(array):
    length = len(array)
    for i in range(length - 1):
        for j in range(length - i - 1):
            if array[j] > array[j + 1]:
                array[j], array[j + 1] = array[j + 1], array[j]


SORTING_ALGORITHMS = {
    'quicksort': qsort,
    'bubble sort': bubble_sort
}
