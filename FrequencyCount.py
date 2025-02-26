def frequency(freq):
    freq = {}
    for i in a:
        if i in freq:
            freq[i] +=1
        if i == " ":
                continue
        else:
            freq[i] = 1
    return freq
a="my name is saloni"
print(frequency(a))