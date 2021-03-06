#Dependencies
import numpy as np
import pandas as pd
from keras.models import Sequential
from keras.layers import Dense
from keras.utils import normalize, np_utils
from keras.wrappers.scikit_learn import KerasClassifier
from sklearn.model_selection import train_test_split,cross_val_score,KFold
from sklearn.preprocessing import LabelEncoder
from sklearn.pipeline import Pipeline

#Load Dataset
data = pd.read_csv("data/Tar-Print-Data-wFall-woutWater.csv",index_col=0)
x_train = data.iloc[:,:9].values
y_train = data.iloc[:,9:10].values

# encode class values as integers
encoder_train = LabelEncoder()
y_train = y_train.ravel()
encoder_train.fit(y_train)
encoded_train_y = encoder_train.transform(y_train)

# convert integers to dummy variables (i.e. one hot encoded)
binary_train_y = np_utils.to_categorical(encoded_train_y)

### MODEL DEFINITION AND PROPERTIES
# define the keras model
model = Sequential()
model.add(Dense(180, input_dim=9, activation='relu'))
model.add(Dense(180, activation='relu'))
model.add(Dense(6, activation='softmax'))

x_train = normalize(x_train, axis=1)  # scales data between 0 and 1

model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

# fit the keras model on the dataset
model.fit(x_train, binary_train_y, epochs=500, batch_size=15)
model.save('Models/wFall-woutWater-Models/Model-7/ML-Model.model')
