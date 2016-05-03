import numpy
import pickle
import random
from sklearn.svm import SVC
import sys

print("Loading data...", end=" ")
sys.stdout.flush()
new_data = pickle.load(open("../data/new_data.pickle", "rb"))
new_keys = pickle.load(open("../data/new_keys.pickle", "rb"))

new_validate_data = []
new_validate_keys = []
for i in range(0, int(len(new_data)/5)):
    index = random.randint(0, len(new_data)-1)
    new_validate_data.append(new_data.pop(index))
    new_validate_keys.append(new_keys.pop(index))
print("Done. ")

print(str(len(new_data)) + " data points.")

print("Vectorizing boards...", end=" ")
sys.stdout.flush()
vector_train_data = []
vector_validate_data = []
for board in new_data:
    #print(board)
    vector_board = board.reshape(25)
    vector_train_data.append(vector_board)
for board in new_validate_data:
    vector_board = board.reshape(25)
    vector_validate_data.append(vector_board)
print("Done. ")

print("Fitting classifier...", end=" ")
sys.stdout.flush()
classifier = SVC(C=25, kernel='rbf', gamma=1/1000, probability=True)
classifier.fit(vector_train_data, new_keys)
print("Done. ")

print("Dumping to src/data/5x5_new_classifier.pickle...", end=" ")
sys.stdout.flush()
pickle.dump(classifier, open("../data/5x5_new_classifier.pickle", "wb"))
print("Done. ")

print("Checking validation error...", end=" ")
sys.stdout.flush()
errors = 0
for i, board in enumerate(vector_validate_data):
    board = board.reshape(1, -1)
    prediction = classifier.predict(board)
    #if prediction[0] != 1:
        #print("#####")
    if prediction != new_validate_keys[i]:
        errors += 1
print("Done. Validation error is " + str(errors) + "/" + str(len(new_validate_data)) + " or " + str(100 * errors/len(new_validate_data)) + "%")

print("ALL DONE. ")
