###########################################
# Suppress matplotlib user warnings
# Necessary for newer version of matplotlib
import warnings

warnings.filterwarnings("ignore", category=UserWarning, module="matplotlib")
#
# Display inline matplotlib plots with IPython
from IPython import get_ipython

get_ipython().run_line_magic('matplotlib', 'inline')
###########################################

import numpy as np
import pandas as pd
import matplotlib as matplot
import matplotlib.pyplot as plt



def filter_data(data, condition):
    """
    Remove elements that do not match the condition provided.
    Takes a data list as input and returns a filtered list.
    Conditions should be a list of strings of the following format:
      '<field> <op> <value>'
    where the following operations are valid: >, <, >=, <=, ==, !=

    Example: ["Team == 'CHI'", 'Age < 18']
    """

    field, op, value = condition.split(" ")

    # convert value into number or strip excess quotes if string
    try:
        value = float(value)
    except:
        value = value.strip("\'\"")

    # get booleans for filtering
    if op == ">":
        matches = data[field] > value
    elif op == "<":
        matches = data[field] < value
    elif op == ">=":
        matches = data[field] >= value
    elif op == "<=":
        matches = data[field] <= value
    elif op == "==":
        matches = data[field] == value
    elif op == "!=":
        matches = data[field] != value
    else:  # catch invalid operation codes
        raise Exception("Invalid comparison operator. Only >, <, >=, <=, ==, != allowed.")

    # filter data and outcomes
    data = data[matches].reset_index(drop=True)
    return data


def playoff_stats(data, outcomes, key, filters=[]):
    """
    Print out selected statistics regarding survival, given a feature of
    interest and any number of filters (including no filters)
    """

    # Check that the key exists
    if key not in data.columns.values:
        print "'{}' is not a feature of the Player_Stats data. Did you spell something wrong?".format(key)
        return False

    # Return the function before visualizing if 'Cabin' or 'Ticket'
    # is selected: too many unique categories to display
    if (key == 'Birthdate' or key == 'College' or key == 'Team'):
        print "'{}' has too many unique categories to display! Try a different feature.".format(key)
        return False

    # Merge data and outcomes into single dataframe
    all_data = pd.concat([data, outcomes], axis=1)

    # Apply filters to data
    for condition in filters:
        all_data = filter_data(all_data, condition)

    # Create outcomes DataFrame
    all_data = all_data[[key, 'Playoffs']]

    # Create plotting figure
    plt.figure(figsize=(8, 6))

    # 'Categorical' features
    if (key == 'Birth_Place' or key == 'POS'):

        # Set the various categories
        if (key == 'Birth_Place'):
            values = ['us', 'ru', 'fr', 'it', 'il', 'ca', 'au', 'nz', 'gb', 'ba', 'br', 'de', 'ch', 'hr', 'tr', 'ng',
                      'do', 'jm', 'pr', 'si', 'gr', 'gf', 'sn', 've', 'es', 'mx', 'cm', 'pl', 'ht', 'cg', 'vi', 'be',
                      'NULL']

        if (key == 'POS'):
            values = ['PG', 'PF', 'C', 'SG', 'SF']

        # Create DataFrame containing categories and count of each
        frame = pd.DataFrame(index=np.arange(len(values)), columns=(key, 'Playoffs', 'No_Playoffs'))
        for i, value in enumerate(values):
            frame.loc[i] = [value, \
                            len(all_data[(all_data['Playoffs'] == 1) & (all_data[key] == value)]), \
                            len(all_data[(all_data['Playoffs'] == 0) & (all_data[key] == value)])]

        # Set the width of each bar
        bar_width = 0.4

        # Display each category's survival rates
        for i in np.arange(len(frame)):
            noplay_bar = plt.bar(i - bar_width, frame.loc[i]['No_Playoffs'], width=bar_width, color='r')
            play_bar = plt.bar(i, frame.loc[i]['Playoffs'], width=bar_width, color='g')

            plt.xticks(np.arange(len(frame)), values)
            plt.legend((noplay_bar[0], play_bar[0]), ('Did not make playoffs', 'Playoffs'), framealpha=0.8)

    # 'Numerical' features
    else:

        # Remove NaN values from Age data
        all_data = all_data[~np.isnan(all_data[key])]

        # Divide the range of data into bins and count survival rates
        min_value = all_data[key].min()
        max_value = all_data[key].max()
        value_range = max_value - min_value

        # Creating bins for numerical values
        if (key == 'Games Played'):
            bins = np.arange(0, all_data['Games Played'].max() + 10, 10)

        if (key == 'MIN'):
            bins = np.arange(0, all_data['MIN'].max() + 20, 20)

        if (key == 'PTS'):
            bins = np.arange(0, all_data['PTS'].max() + 20, 20)

        if (key == 'FG%'):
            bins = np.arange(0, all_data['FG%'].max() + 10, 10)

        if (key == '3P%'):
            bins = np.arange(0, all_data['3P%'].max() + 10, 10)

        if (key == 'FT%'):
            bins = np.arange(0, all_data['FT%'].max() + 10, 10)

        if (key == 'REB'):
            bins = np.arange(0, all_data['REB'].max() + 20, 20)

        if (key == 'AST'):
            bins = np.arange(0, all_data['AST'].max() + 10, 10)

        if (key == 'STL'):
            bins = np.arange(0, all_data['STL'].max() + 10, 10)

        if (key == 'BLK'):
            bins = np.arange(0, all_data['BLK'].max() + 10, 10)

        if (key == 'TOV'):
            bins = np.arange(0, all_data['TOV'].max() + 10, 10)

        if (key == 'PF'):
            bins = np.arange(0, all_data['PF'].max() + 10, 10)

        if (key == 'EFF'):
            bins = np.arange(0, all_data['EFF'].max() + 20, 20)

        if (key == 'AST/TOV'):
            bins = np.arange(0, all_data['AST/TOV'].max() + 10, 10)

        if (key == 'STL/TOV'):
            bins = np.arange(0, all_data['STL/TOV'].max() + 10, 10)

        if (key == 'Age'):
            bins = np.arange(0, all_data['Age'].max() + 10, 10)

        if (key == 'Experience'):
            bins = np.arange(0, all_data['Experience'].max() + 10, 10)

        if (key == 'Height'):
            bins = np.arange(0, all_data['Height'].max() + 10, 10)

        if (key == 'Weight'):
            bins = np.arange(0, all_data['Weight'].max() + 10, 10)

        # Overlay each bin's survival rates
        nonsurv_vals = all_data[all_data['Playoffs'] == 0][key].reset_index(drop=True)
        surv_vals = all_data[all_data['Playoffs'] == 1][key].reset_index(drop=True)
        plt.hist(nonsurv_vals, bins=bins, alpha=0.6,
                 color='red', label='Did not make playoffs')
        plt.hist(surv_vals, bins=bins, alpha=0.6,
                 color='green', label='Made playoffs')

        # Add legend to plot
        plt.xlim(0, bins.max())
        plt.legend(framealpha=0.8)


    # Common attributes for plot formatting
    plt.xlabel(key)
    plt.ylabel('Number of Players')
    plt.title('Player Playoff Statistics With \'%s\' Feature' % (key))
    plt.show()

    # Report number of passengers with missing values
    if sum(pd.isnull(all_data[key])):
        nan_outcomes = all_data[pd.isnull(all_data[key])]['Playoffs']
        print "Players with missing '{}' values: {} ({} Made playoffs, {} Did not make playoffs)".format( \
            key, len(nan_outcomes), sum(nan_outcomes == 1), sum(nan_outcomes == 0))