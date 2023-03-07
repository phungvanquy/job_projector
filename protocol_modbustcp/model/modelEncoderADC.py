import numpy as np
import os
# import matplotlib.pyplot as plt
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression
import pandas as pd
poly = PolynomialFeatures(degree=3, include_bias=False)

# Training dataset
dataFilePath = os.path.join(os.path.dirname(__file__), './data.csv')
data = pd.read_csv(dataFilePath, sep=",")
encoder_val  = data['ADCvalue'].astype(int).to_numpy() 
angle_val = data['angle'].astype(int).to_numpy()

# #=======================================================================
# # Create model to convert ADC value to Angle value
x = encoder_val
y = angle_val
poly_features_ADC = poly.fit_transform(x.reshape(-1, 1))    # Add Polynimial Features from x to dataset
reg_ADCToAngle_model = LinearRegression()                   # Create LinearRegression Model
reg_ADCToAngle_model.fit(poly_features_ADC, y)              # Train model! Then can see model.coef_, model.intercept_
print("model.intercept_", reg_ADCToAngle_model.intercept_)
print("model.coef_", reg_ADCToAngle_model.coef_)


# #=======================================================================
# # Create model to convert Angle value to ADC value
# x = angle_val
# y = encoder_val
# poly_features_angle = poly.fit_transform(x.reshape(-1, 1))  # Add Polynimial Features from x to dataset
# reg_angleToADC_model = LinearRegression()                   # Create LinearRegression Model
# reg_angleToADC_model.fit(poly_features_angle, y)            # Train model! Then can see model.coef_, model.intercept_
# print("model.intercept_", reg_angleToADC_model.intercept_)
# print("model.coef_", reg_angleToADC_model.coef_)




# With received model we can convert ADC to angle or vice versa
def angleToADC(angle):
    if angle > 180:
        angle = angle - 360
    valueToPredict = poly.transform(np.array([angle]).reshape(-1,1))
    result = reg_angleToADC_model.predict(valueToPredict)[0]
    return round(result)
    
def ADCtoAngle(ADCvalue):
    valueToPredict = poly.transform(np.array([ADCvalue]).reshape(-1,1))
    result = reg_ADCToAngle_model.predict(valueToPredict)[0]
    return round(result)


#=======================================================================
# Graphic show
# plt.figure(figsize=(10,6))
# plt.scatter(x, y)
# yhat = reg_angleToADC_model.predict(poly.transform(np.array(x).reshape(-1,1)))
# print(angleToADC(0))
# plt.scatter(x, yhat)
# plt.show()

