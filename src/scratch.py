from itertools import islice

fed_tax = [(0, 55867, 0.15),
           (55867, 111733, 0.205),
           (111733, 173205, 0.26),
           (173205, 246752, 0.29),
           (246752, float('inf'), 0.33)]

prov_tax = [(0, 51446, 0.0505),
            (51446, 102894, 0.0915),
            (102894, 150000, 0.1116),
            (150000, 220000, 0.1216),
            (220000, float('inf'), 0.1316)]


fed = [(x[0], x[1]) for x in fed_tax]
prov = [(x[0], x[1]) for x in prov_tax]

brackets = fed + prov
brackets = sorted(list(set([x for item in brackets for x in item])))
brackets


# def chunk(arr_range, arr_size):
#     arr_range = iter(arr_range)
#     return iter(lambda: tuple(islice(arr_range, arr_size)), ())
#
# list(chunk(brackets, 2))

lst = brackets
n = 2
all_brackets = [lst[i:i + n] for i in range(0, len(lst))]
if len(all_brackets[-1]) == 1:
    all_brackets = all_brackets[:-1]



