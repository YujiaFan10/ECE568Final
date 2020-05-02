import numpy as np
from os import listdir
import csv
import math

def baysian_curve_fitting(time, price, test_val):
    M = 4
    beta = 12
    alpha = 0.1

    # Calculate 𝜑T(x)
    a = [[math.pow(test_val, i) for i in range(M + 1)]]
    matrix_a = np.matrix(a)

    # Calculate alpha * I
    I = [[0 for _ in range(M + 1)] for _ in range(M + 1)]
    for i in range(M + 1):
        I[i][i] = alpha
    matrix_I = np.matrix(I)

    # Calculate sum-𝜑(xn)
    b = [[0] for _ in range(M + 1)]
    for j in range(len(time) - 1):
        for i in range(M + 1):
            b[i][0] += math.pow(time[j], i)
    matrix_b = np.matrix(b)

    # Calculate Matrix S
    matrix_S_1 = matrix_b * matrix_a * beta + matrix_I
    matrix_S = np.linalg.inv(matrix_S_1)

    # Calculate sum-[𝜑(xn)*tn]
    c = [[0] for _ in range(M + 1)]
    for i in range(len(time) - 1):
        for j in range(M + 1):
            c[j][0] += (math.pow(time[i], j) * price[i])
    matrix_c = np.matrix(c)

    # Calculate mean
    mean_matrix = matrix_a * matrix_S * matrix_c * beta
    mean = mean_matrix.item(0)

    # Calculate 𝜑(x)
    d = [[0] for _ in range(M + 1)]
    for i in range(M + 1):
        d[i][0] = math.pow(test_val, i)
    matrix_d = np.matrix(d)

    # Calculate variance
    variance = math.sqrt((matrix_a * matrix_S * matrix_d)[0][0] + (1 / beta))


    print("Predicted Val   : {:.4f}".format(mean))
    print("Actual Val      : {:.4f}".format(price[-1]))
    print("Range Prediction : [{:.4f}, {:.4f}]".format(mean - 3 * variance, mean + 3 * variance))
    print("Absolute Error  : {:.4f}".format(abs(price[-1] - mean)))
    print("Relative Error  : {:.4f}%".format(abs(price[-1] - mean) / price[-1] * 100))

def find_csv(path):
    return [f for f in listdir(path) if f.split('.')[-1] == "csv"]

def read_csv(path, name):
    file = open(path + name, "r")
    reader = csv.reader(file)
    time, price = [], []
    date = 0
    for entry in reader:
        if date > 0 and date <31:
            # Encode the date into integer from 1 ~ 30
            # skip the 1st row: titles of columns
            time.append(date)
            price.append(float(entry[1]))


        date += 1
    file.close()

    return time, price

if __name__ == "__main__":
    csv_path = "/Users/xiaoliu/PycharmProjects/BaysianCurveFitting/"
    files = find_csv(csv_path)
    for f in files:
        print(("-" * 5 + f.split(".")[0] + " Summary" + "-" * 20)[:40])
        time, price = read_csv(csv_path, f)
        baysian_curve_fitting(time, price, time[-1])
        print("-" * 20, end = "\n\n\n")
