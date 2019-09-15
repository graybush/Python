def chop(val, values):
    start = 0
    end = len(values) - 1

    ret = -1
    while(start <= end):
        index = (start + end) // 2
        if (values[index] == val):
            ret = index
            break
        if (values[index] > val):
            end = index - 1
        else:
            start = index + 1

    return ret
