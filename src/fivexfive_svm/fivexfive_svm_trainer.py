from sklearn.svm import SVC
import numpy
import pickle
import sys

print("Loading data...", end=" ")
sys.stdout.flush()
data = pickle.load(open("../data/5x5_blocks_data.pickle", "rb"))
keys = pickle.load(open("../data/5x5_blocks_keys.pickle", "rb"))
print("Done. ")

print("Vectorizing boards...", end=" ")
sys.stdout.flush()
vector_data = []
for board in data:
    vector_board = board.reshape(25)
    vector_data.append(vector_board)
print("Done. ")
#print(vector_data[0])

print("Fitting classifier...", end=" ")
sys.stdout.flush()
classifier = SVC(C=1.0, kernel='rbf', degree=3, probability=True)
classifier.fit(vector_data, keys)
print("Done. ")

print("Dumping to src/data/5x5_trained_svm_classifier.pickle...", end=" ")
sys.stdout.flush()
pickle.dump(classifier, open("../data/5x5_trained_svm_classifier.pickle", "wb"))
print("Done. ")

print("ALL DONE. ")