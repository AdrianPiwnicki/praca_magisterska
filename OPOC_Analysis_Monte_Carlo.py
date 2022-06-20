import numpy as np
from matplotlib import pyplot as plt

from One_Plus_One_Continous import One_Plus_One_Continous

histogram = []
ekstrema = []

for i in range(10000):
    pokolenia, ekstremum = One_Plus_One_Continous(0)
    histogram.append(pokolenia)
    ekstrema.append(ekstremum)

unique_histogram = np.unique(histogram)
histogram_result = []
for i in unique_histogram:
    histogram_result.append(histogram.count(i))
probability = (max(histogram_result)/10000) * 100

plt.figure(2)
plt.title("Najczęściej ekstremum znajdowało w " + str(unique_histogram[histogram_result.index(max(histogram_result))]) +" pokoleniu")
plt.suptitle("Prawdopodobieństwo wynosi: " + str(round(probability,2)) +"%")
plt.bar(unique_histogram, histogram_result)
plt.xlabel('Pokolenia')
plt.ylabel('Ilość')
plt.savefig('histograms/one_plus_one_c_histogram.png')
plt.show()
