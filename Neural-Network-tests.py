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
data = pd.read_csv("data/Tar-Print-Data-wFall.csv",index_col=0)
all_x = data.iloc[:,:9].values
all_y = data.iloc[:,9:10].values
x_train, x_test, y_train, y_test = train_test_split(all_x, all_y, test_size=0.2)

# encode class values as integers
encoder_train = LabelEncoder()
encoder_test = LabelEncoder()
y_train = y_train.ravel()
y_test = y_test.ravel()
encoder_train.fit(y_train)
encoder_test.fit(y_test)
encoded_train_y = encoder_train.transform(y_train)
encoded_test_y = encoder_test.transform(y_test)

# convert integers to dummy variables (i.e. one hot encoded)
binary_train_y = np_utils.to_categorical(encoded_train_y)
binary_test_y = np_utils.to_categorical(encoded_test_y)

# define the keras model
model = Sequential()
model.add(Dense(100, input_dim=9, activation='relu'))
model.add(Dense(100, activation='relu'))
model.add(Dense(7, activation='softmax'))

x_train = normalize(x_train, axis=1)  # scales data between 0 and 1
x_test = normalize(x_test, axis=1)  # scales data between 0 and 1

model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

# fit the keras model on the dataset
print(x_train.shape)
print(binary_train_y.shape)

model.fit(x_train, binary_train_y, epochs=150, batch_size=15)
model.save('Tar-Print-Model-3-All-Labels.model')
# evaluate the keras model
#_, accuracy = model.evaluate(x_test, binary_test_y)
#print('Accuracy: %.2f' % (accuracy*100))