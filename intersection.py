# some_dict={'zope':'zzz','python':'program'}
# another_dict={'python':'program','pearl':'ship'}
# print("Intersection of keys:", set(some_dict.keys()) & set(another_dict.keys()))

# the_new_list=[1,2,3,4,5,6]
# the_new_list=[x+23 for x in the_new_list if x>5]
# print(the_new_list)

# you want to keep a limited history of the last few items seen during iteration or during some other kind of processing ,

def search(lines,pattern,history=5):
    prevlines=deque(maxlen=history)
    for line in lines:
        if pattern in line:
            yield line,prevlines
        prevlines.append(line)