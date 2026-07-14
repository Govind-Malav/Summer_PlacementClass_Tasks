def add_three_dimensional(data1, data2):
    result = []
    for i in range(len(data1)):
        layer = []
        for j in range(len(data1[i])):
            row = []
            for k in range(len(data1[i][j])):
                row.append(data1[i][j][k] + data2[i][j][k])
            layer.append(row)
        result.append(layer)
    return result
