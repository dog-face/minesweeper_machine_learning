import numpy
import pickle
import sys

λ_value = 2**-3### set λ here ###



#training function
def pegasos_train(data, spamOrHam, λ):
    #Initialize w to be all 0 weight vector.
    weightVector = numpy.zeros(len(wordVector), dtype=numpy.int)#weight vector
    t = 0
    k = 0 #number of mistakes, starting at 0
    totalHingeLoss = 0
    f_of_wt = []
    for iterations in range(1, 21):
        hingeLoss = 0
        k_local = 0 #number of mistakes per pass. Needed because we stop when we make a full pass with no mistakes.
        for i, x_t in enumerate(data):
            t = t+1
            η = 1/(t * λ) # stepsize
            prediction = numpy.dot(weightVector, x_t)
            if (spamOrHam[i] * prediction) < 1:
                hingeLoss += 1 - (spamOrHam[i] * prediction)
                weightVector = numpy.add((1 - (η * λ)) * weightVector, η * numpy.dot(spamOrHam[i], x_t)) #adjust weights.
            else:
                weightVector = (1 - (η * λ)) * weightVector
            if spamOrHam[i] * prediction < 0:
                k_local += 1 #note the error
        hingeLoss = hingeLoss/len(data) #divide by size of dataset
        totalHingeLoss += hingeLoss
        w_norm_sq = weightVector.dot(weightVector)
        f_of_wt.append((λ/2)*w_norm_sq + hingeLoss)
        k += k_local # update total number of errors
        print("iteration " + str(iterations) + " done. errors: " + str(k_local))
        if k_local == 0:
            print("Full pass with no errors. ")
            break #break condition: no errors this pass
    return weightVector, k, totalHingeLoss, f_of_wt

def pegasos_test(w, data, spamOrHam):
    print("testing")
    k = 0 #errors
    for i, x_t in enumerate(data):
        prediction = numpy.dot(w, x_t)
        if prediction == 0: #prediction of 0 is no good.
            k += 1
        if (spamOrHam[i] * prediction) < 0: #signs don't match => incorrect prediction
            k += 1


    return (k/len(data) * 100)

def findSupportVectors(w, data):
    suppVecs = []
    for i, x_t in enumerate(data):
        if spamOrHam[i] * numpy.dot(w, x_t) < 1:
            suppVecs.append(i)
    return suppVecs

#Time-Saving: Once we have trained a vector, we save it to disk. Then we can load it rather than retraining in the future.
userInput = input("load pre-trained classification vector from disk? (y/n) ")

if userInput == 'y':
    stdPreTrainedVectorFile = open("../data/stdPreTrainedVector", "rb")
    stdWeightVector = pickle.load(stdPreTrainedVectorFile)
else:
    stdWeightVector, k, totalHingeLoss, f_of_wt = pegasos_train(trainingVectors, spamOrHam, λ_value)
    print("Training done.")
    avgHingeLoss = totalHingeLoss/20
    print("average hinge loss over all iterations: " + str(avgHingeLoss))
    print("average training error over all iterations: " + str(k/(len(trainingVectors) * 20)))

    stdPreTrainedVector = open("../data/stdPreTrainedVector", "wb")
    pickle.dump(stdWeightVector, stdPreTrainedVector)

    supportVectors = findSupportVectors(stdWeightVector, trainingVectors)
    #print("support Vectors = " + str(supportVectors))
    #print(len(supportVectors))

#Testing Classification Vector
percent_wrong = pegasos_test(stdWeightVector, trainingVectors, spamOrHam)
print("pegasos test on training data: " + str(percent_wrong) + "% wrong")

percent_wrong = pegasos_test(stdWeightVector, validationVectors, spamOrHam_validation)
print("pegasos test on validation data: " + str(percent_wrong) + "% wrong")

percent_wrong = pegasos_test(stdWeightVector, testVectors, spamOrHam_test)
print("pegasos test on final test data: " + str(percent_wrong) + "% wrong")
