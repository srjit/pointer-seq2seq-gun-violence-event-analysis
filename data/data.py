import pandas as pd

__author__ = "Sreejith Sreekumar"
__email__ = "sreekumar.s@husky.neu.edu"
__version__ = "0.0.1"

filename = "fatal_encounters.csv"
data = pd.read_csv(filename)

_input = data[["A brief description of the circumstances surrounding the death",\
                   "Date of injury resulting in death (month/day/year)", "Subject's name"]]


_input.rename(columns={"A brief description of the circumstances surrounding \
                       the death": "report",
                       "Subject's name": "Name"}, inplace=True)


_input["Year"] = _input["Date of injury resulting in death (month/day/year)"].\
                      apply(lambda x : int(x.split("/")[2]))

train_data = _input[_input['Year'] <= 2012]
test_data = _input[_input['Year'] > 2012]

train_data.to_csv("train.csv")
test_data.to_csv("validation.csv")




