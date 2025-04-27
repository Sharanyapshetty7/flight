import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
import pickle

# Load dataset
data = pd.read_csv('Clean_Dataset.csv')

# ✅ Drop the unnecessary 'Unnamed: 0' column if you want
data = data.drop(columns=['Unnamed: 0'])

# ✅ Define input (X) and output (y)
X = data.drop('price', axis=1)
y = data['price']

# ✅ For simplicity, let's use only numeric features
# (You can improve later by encoding categorical variables)
X = X.select_dtypes(include=['int64', 'float64'])

# Split into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train the model
model = RandomForestRegressor()
model.fit(X_train, y_train)

# Save the model to a file
with open('flight_price_model.pkl', 'wb') as file:
    pickle.dump(model, file)

print("✅ Model trained and saved successfully!")
