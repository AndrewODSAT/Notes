dataArray = list(range(5, 16))
for i in range(1, 11):
    currentData = dataArray[i]
    position = i
    while (position > 0 and dataArray[position-1]>currentData):
        dataArray[position] = dataArray[x]
        position -= 1

    dataArray[position] = currentData
