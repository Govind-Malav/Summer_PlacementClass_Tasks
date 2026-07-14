class Matrix:
    def __init__(self, matrix):
        self.matrix = matrix
    def add(self, other):
        result = []
        for i in range(len(self.matrix)):
            row = []
            for j in range(len(self.matrix[0])):
                row.append(self.matrix[i][j] + other.matrix[i][j])
            result.append(row)
        return result
    def multiply(self, other):
        result = []
        for i in range(len(self.matrix)):
            row = []
            for j in range(len(other.matrix[0])):
                total = 0
                for k in range(len(other.matrix)):
                    total = total + self.matrix[i][k] * other.matrix[k][j]
                row.append(total)
            result.append(row)
        return result
