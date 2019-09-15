import logging

log = logging.getLogger(__name__)


def chop(val, values):
    """ Prosaic binary search
        int val : search value
        int values[] : ordered list of values
        int return index of value else -1 if not found
    """
    start = 0
    end = len(values) - 1

    try:
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
    except Exception as error:
        log.exception(error)
