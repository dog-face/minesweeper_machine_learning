import pickle
import sys
import numpy

#Shows validation error of Generation and Gameplay based classifiers on a validation set of data from both types combined.


def vectorize(data_pt):
    return data_pt.reshape(25).reshape(1, -1)

def get_top_bottom(support_vectors, alphas):
    blank1, top_10_indices = numpy.where(alphas == numpy.max(alphas))
    blank2, bottom_10_indices = numpy.where(alphas == numpy.min(alphas))
    top_10_vals = []
    for index in top_10_indices:
        top_10_vals.append(support_vectors[index])
    bottom_10_vals = []
    for index in bottom_10_indices:
        bottom_10_vals.append(support_vectors[index])
    return top_10_vals, bottom_10_vals, top_10_indices, bottom_10_indices

generation_validation_set_data = pickle.load(open("../data/generation_validate_data.pickle", "rb"))
generation_validation_set_keys = pickle.load(open("../data/generation_validate_keys.pickle", "rb"))

gameplay_data = pickle.load(open("../data/gameplay_data.pickle", "rb"))
gameplay_keys = pickle.load(open("../data/gameplay_keys.pickle", "rb"))

gameplay_validation_set_data = gameplay_data[0:10000]
gameplay_validation_set_keys = gameplay_keys[0:10000]

combined_validation_set_data = gameplay_validation_set_data + generation_validation_set_data
combined_validation_set_keys = gameplay_validation_set_keys + generation_validation_set_keys

gameplay_classifier = pickle.load(open("../data/gameplay_svm_classifier.pickle", "rb"))
generation_classifier = pickle.load(open("../data/generation_svm_classifier.pickle", "rb"))

#gameplay supp vecs and params
gameplay_support_vectors = gameplay_classifier.support_vectors_

print("Gameplay classifier support vectors: " + str(len(gameplay_support_vectors)) + " support vectors")
print(gameplay_support_vectors)

gameplay_alphas = gameplay_classifier.dual_coef_
print("Gameplay classifier support vector weights: \n" + str(gameplay_alphas))

print("Top and bottom support vectors: ")
print(get_top_bottom(gameplay_support_vectors, gameplay_alphas))

#Generation supp vecs and params
generation_support_vectors = generation_classifier.support_vectors_

print("Generation classifier support vectors: " + str(len(generation_support_vectors)) + " support vectors")
print(generation_support_vectors)

generation_alphas = generation_classifier.dual_coef_
print("Generation classifier support vector weights: \n" + str(generation_alphas))

print("Top and bottom support vectors: ")
print(get_top_bottom(generation_support_vectors, generation_alphas))

#gameplay validation error
print("Calculating validation error for gameplay classifier... ", end="")
sys.stdout.flush()
errors = 0
for i, data_pt in enumerate(combined_validation_set_data):
    prediction = gameplay_classifier.predict(vectorize(data_pt))
    if prediction != combined_validation_set_keys[i]:
        errors += 1
print("Done. ")
print("Gameplay validation error: " + str(100 * errors/len(combined_validation_set_data)) + "%")

#generation validation error
print("Calculating validation error for generation classifier... ", end="")
sys.stdout.flush()
errors = 0
for i, data_pt in enumerate(combined_validation_set_data):
    prediction = generation_classifier.predict(vectorize(data_pt))
    if prediction != combined_validation_set_keys[i]:
        errors += 1
print("Done. ")
print("Generation validation error: " + str(100 * errors/len(combined_validation_set_data)) + "%")

