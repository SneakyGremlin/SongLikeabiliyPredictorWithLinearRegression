import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split

pd.set_option("display.width", None)

original_data_frame = pd.read_excel("AliasedDataForAlgorithm.xlsx", sheet_name="data")


# utilising min-max normalisation. This is being done since the values are majorly around or above the median.
def normalise_response(original_data_frame):
    normalised_response = MinMaxScaler().fit_transform(original_data_frame[["Response"]])  # expects 2D array
    normalised_dataframe_precursor = pd.DataFrame(normalised_response, columns=["Response"])  # a numpy array parameter
    original_data_frame["Response"] = normalised_dataframe_precursor["Response"]  # reassignment of the operator


# utilising min-max normalisation. This is being done since the values are majorly around or above the median.
def normalise_intelligence(original_data_frame):
    normalised_intelligence = MinMaxScaler().fit_transform(original_data_frame[["Intelligence"]])
    normalised_dataframe_precursor = pd.DataFrame(normalised_intelligence, columns=["Intelligence"])
    original_data_frame["Intelligence"] = normalised_dataframe_precursor["Intelligence"]


# normalising all others for consistency whenever appropriate (if the variable has any bearing whatsoever)
# min-max

# filling in the missing values in Response with the mean of the responses. These are empty since I felt my
# interpretation of their input (ref "Response" section in README.md) would be unsatisfactory
def fill_na_in_response():
    global original_data_frame
    original_data_frame = original_data_frame.fillna({"Response": original_data_frame["Response"].mean()})


# normalising all non-categorical features
def normalise_features():
    global original_data_frame

    list_of_features_and_response = ['Participant', 'Age Demographic', 'Relationship Level',
                                     'Musical Aptitude', 'Musical Affinity', 'Sensibilities', 'Intelligence',
                                     'Sex', 'Multiple Exposure', 'Response']

    list_of_features_and_response.remove("Participant")
    list_of_features_and_response.remove("Age Demographic")
    list_of_features_and_response.remove("Sex")
    list_of_features_and_response.remove("Multiple Exposure")
    # all categorical features have been removed

    normalised_data = MinMaxScaler().fit_transform(original_data_frame[list_of_features_and_response])
    normalised_data_frame_precursor = pd.DataFrame(normalised_data, columns=['Relationship Level',
                                                                             'Musical Aptitude', 'Musical Affinity',
                                                                             'Sensibilities', 'Intelligence',
                                                                             'Response'])
    # print(normalised_data_frame_precursor.info())

    original_data_frame["Relationship Level"] = normalised_data_frame_precursor["Relationship Level"]
    original_data_frame["Musical Aptitude"] = normalised_data_frame_precursor["Musical Aptitude"]
    original_data_frame["Musical Affinity"] = normalised_data_frame_precursor["Musical Affinity"]
    original_data_frame["Sensibilities"] = normalised_data_frame_precursor["Sensibilities"]
    original_data_frame["Intelligence"] = normalised_data_frame_precursor["Intelligence"]
    original_data_frame["Response"] = normalised_data_frame_precursor["Response"]

    # print(original_data_frame.info())
    # print(original_data_frame.head(n=20))
    # NOTE TO SELF: I could have passed the categorical features as well... it should've worked... sigh...


# using non float/int variables with linear regression causes a ValueError. I am certain there is a way to
# include categorical features (or perhaps a different regression that allows it) so this is a stopgap.
# Male is 0, Female is 1
# X Y Z -> 0.33, 0.66, 0.99
def convert_categorical():
    global original_data_frame
    original_data_frame.loc[original_data_frame["Sex"] == "Male", ["Sex"]] = 0
    original_data_frame.loc[original_data_frame["Sex"] == "Female", ["Sex"]] = 1

    original_data_frame.loc[original_data_frame["Age Demographic"] == "GenX", ["Age Demographic"]] = 0.33
    original_data_frame.loc[original_data_frame["Age Demographic"] == "GenY", ["Age Demographic"]] = 0.66
    original_data_frame.loc[original_data_frame["Age Demographic"] == "GenZ", ["Age Demographic"]] = 0.99


# now we sample the data i.e. divide it into training and test sets.
# Note to self, THANK GOD PYTHON SUPPORTS MULTIPLE RETURN VALUES.
# NOTE: any "redundancy" you see here might be intentional (I like to revisit and tinker)
def sample_data():
    global original_data_frame
    list_of_features_and_response = ['Participant', 'Age Demographic', 'Relationship Level',
                                     'Musical Aptitude', 'Musical Affinity', 'Sensibilities', 'Intelligence',
                                     'Sex', 'Multiple Exposure', 'Response']

    response_df = original_data_frame[["Response"]]
    list_of_features_and_response.remove("Response")
    features_df = original_data_frame[list_of_features_and_response]
    list_of_features_and_response.append("Response")

    # from the exploration .py file it was discerned that "Age Demographic" is a salient feature
    #       ergo, I use stratified sampling based on the aforesaid.
    predictors_train, predictors_test, response_train, response_test = \
        train_test_split(features_df, response_df,
                         test_size=0.2,
                         random_state=9999,
                         stratify=features_df["Age Demographic"])
    # random state is used for testing purposes.

    # print(predictors_train["Age Demographic"].value_counts(normalize=True),
    #       predictors_test["Age Demographic"].value_counts(normalize=True))

    return original_data_frame, predictors_train, predictors_test, response_train, response_test


# function which will complete the preparation process
def prep_data():
    fill_na_in_response()
    normalise_features()
    convert_categorical()
    return sample_data()
