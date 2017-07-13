import pandas as pd

def accuracy_score(truth, predictions):
    """ Returns accuracy score for input truth and predictions """

    # Ensure that the number of predictions matches the number of outcomes
    if len(truth) == len(predictions):

        # Calculate and return the accuracy as a percent
        return "Predictions have an accuracy of {:.2f}%.".format((truth == predictions).mean() * 100)
    else:
        return "Number of predictions does not match number of outcomes!"

def predictions0(data):
    """ Model with no features """

    predictions = []
    for _, player in data.iterrows():

        #Predict player making the playoffs
        predictions.append(0)

    return pd.Series(predictions)