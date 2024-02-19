# Use Pandas for data cleaning and feature extraction.
# Train a simple model predicting the quantity of products sold based on factors such as price, day of the week, and month.
# Integrate the model with the /predict endpoint.

import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import joblib



# Load your dataset
data = pd.read_excel('online_retail_II.xlsx')

# Invoice                object
# StockCode              object
# Description            object
# Quantity                int64
# InvoiceDate    datetime64[ns]
# Price                 float64
# Customer ID           float64
# Country                object
# dtype: object

#Preprocess and feature extraction
data['invoice_date'] = pd.to_datetime(data['InvoiceDate'])
data['day_of_week'] = data['invoice_date'].dt.dayofweek
data['month'] = data['invoice_date'].dt.month
X = data[['Price', 'day_of_week', 'month']]
y = data['Quantity']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Fit model
model = RandomForestRegressor()
model.fit(X_train, y_train)

# After training the model, Evaluate its performance with test data, which helps understand its prediction accuracy. 
y_pred = model.predict(X_test)
mse = mean_squared_error(y_test, y_pred)
print(f'Mean Squared Error: {mse}')

# then save the model for later use:
joblib.dump(model, 'model.joblib')
