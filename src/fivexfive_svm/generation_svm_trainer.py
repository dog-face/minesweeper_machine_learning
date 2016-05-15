from sklearn.svm import SVC
import numpy
import pickle
import sys

print("Loading data...", end=" ")
sys.stdout.flush()
train_data = pickle.load(open("../data/generation_train_data.pickle", "rb"))
train_keys = pickle.load(open("../data/generation_train_keys.pickle", "rb"))

validate_data = pickle.load(open("../data/generation_validate_data.pickle", "rb"))
validate_keys = pickle.load(open("../data/generation_validate_keys.pickle", "rb"))
print("Done. ")

print("Vectorizing boards...", end=" ")
sys.stdout.flush()
vector_train_data = []
vector_validate_data = []
for board in train_data:
    #print(board)
    vector_board = board.reshape(25)
    vector_train_data.append(vector_board)
for board in validate_data:
    vector_board = board.reshape(25)
    vector_validate_data.append(vector_board)
print("Done. ")
#print(vector_data[0])

print("Fitting classifier...", end=" ")
sys.stdout.flush()
classifier = SVC(C=25, kernel='rbf', gamma=1/1000, probability=True)
classifier.fit(vector_train_data, train_keys)
print("Done. ")

print("Dumping to src/data/generation_svm_classifier.pickle...", end=" ")
sys.stdout.flush()
pickle.dump(classifier, open("../data/generation_svm_classifier.pickle", "wb"))
print("Done. ")

print("Checking validation error...", end=" ")
sys.stdout.flush()
errors = 0
for i, board in enumerate(vector_validate_data):
    board = board.reshape(1, -1)
    prediction = classifier.predict(board)
    if prediction != validate_keys[i]:
        #print(validate_data[i])
        #print(validate_keys[i])
        errors += 1
print("Done. Validation error is " + str(errors) + "/" + str(len(validate_data)) + " or " + str(100 * errors/len(validate_data)) + "%")

print("ALL DONE. ")
