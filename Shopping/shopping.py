import csv
import sys

from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from time import strptime
TEST_SIZE = 0.4


def main():
    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python shopping.py data")

    # Load data from spreadsheet and split into train and test sets
    evidence, labels = load_data(sys.argv[1])
    X_train, X_test, y_train, y_test = train_test_split(
        evidence, labels, test_size=TEST_SIZE
    )

    # Train model and make predictions
    model = train_model(X_train, y_train)
    predictions = model.predict(X_test)
    sensitivity, specificity = evaluate(y_test, predictions)

    # Print results
    print(f"Correct: {(y_test == predictions).sum()}")
    print(f"Incorrect: {(y_test != predictions).sum()}")
    print(f"True Positive Rate: {100 * sensitivity:.2f}%")
    print(f"True Negative Rate: {100 * specificity:.2f}%")


def load_data(filename):
    """
     Load shopping data from a CSV file `filename` and convert into a list of
     evidence lists and a list of labels. Return a tuple (evidence, labels).

     evidence should be a list of lists, where each list contains the
     following values, in order:
         - Administrative, an integer
         - Administrative_Duration, a floating point number
         - Informational, an integer
         - Informational_Duration, a floating point number
         - ProductRelated, an integer
         - ProductRelated_Duration, a floating point number
         - BounceRates, a floating point number
         - ExitRates, a floating point number
         - PageValues, a floating point number
         - SpecialDay, a floating point number
         - Month, an index from 0 (January) to 11 (December)
         - OperatingSystems, an integer
         - Browser, an integer
         - Region, an integer
         - TrafficType, an integer
         - VisitorType, an integer 0 (not returning) or 1 (returning)
         - Weekend, an integer 0 (if false) or 1 (if true)

     labels should be the corresponding list of labels, where each label
     is 1 if Revenue is true, and 0 otherwise.
     """

    #Dictionary made to get corresponding number for month.
    months = {
        'Jan': 0, 'Feb': 1, 'Mar': 2, 'Apr': 3, 'May': 4, 'June': 5, 'Jul': 6, 'Aug': 7, 'Sep': 8,
        'Oct': 9, 'Nov': 10, 'Dec': 11
    }

    #Creates 2 different lists to hold what needs to be returned.
    evidence = []
    labels = []

    #Opens file and goes to contents.
    with open(filename) as f:
        reader = csv.reader(f)
        next(reader)

        #Appends a list containing the correct number or boolean with in the right data type.
        for person in reader:
            evidence.append(
                [(int(person[0])),
                (float(person[1])),
                (int(person[2])),
                (float(person[3])),
                (int(person[4])),
                (float(person[5])),
                (float(person[6])),
                (float(person[7])),
                (float(person[8])),
                (float(person[9])),
                (int(months[person[10]])),
                (int(person[11])),
                (int(person[12])),
                (int(person[13])),
                (int(person[14])),
                (0 if person[15] == 'New_Visitor' else 1),
                (0 if person[16] == 'FALSE' else 1)])

            #Add true/false depending on if person bought.
            labels.append(person[17])

        return evidence, labels


def train_model(evidence, labels):
    """
    Given a list of evidence lists and a list of labels, return a
    fitted k-nearest neighbor model (k=1) trained on the data.
    """

    #Makes a KNeighborsClassifier model with the evidence and labels we input from test set and returns it.
    model = KNeighborsClassifier(n_neighbors=1)
    model.fit(evidence, labels)

    return model


def evaluate(labels, predictions):
    """
    Given a list of actual labels and a list of predicted labels,
    return a tuple (sensitivity, specificty).

    Assume each label is either a 1 (positive) or 0 (negative).

    `sensitivity` should be a floating-point value from 0 to 1
    representing the "true positive rate": the proportion of
    actual positive labels that were accurately identified.

    `specificity` should be a floating-point value from 0 to 1
    representing the "true negative rate": the proportion of
    actual negative labels that were accurately identified.
    """

    #Counts how many correct TRUEs and FALSEs respectively.
    yes = 0
    no = 0

    #Checks to see if it matches and if it does it'll add to the count.
    for i in range(len(labels)):
        if labels[i] == predictions[i] and labels[i] == 'TRUE':
            yes += 1
        if labels[i] == predictions[i] and labels[i] == 'FALSE':
            no += 1

    #Sensitivity and specificity are calculated then returned.
    sensitivity = yes / labels.count('TRUE')
    specificity = no / labels.count('FALSE')

    return sensitivity, specificity


if __name__ == "__main__":
    main()
