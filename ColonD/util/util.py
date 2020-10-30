# Function to find nth occurence in a string.
def findnth(string, substring, occurence):
    val = -1
    for i in range(occurence):
        val = string.find(substring, val + 1)

    return val