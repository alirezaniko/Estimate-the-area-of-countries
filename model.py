import sqlite3
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt

def load_data():
    conn = sqlite3.connect('countries.db')
    query = 'SELECT population, area FROM countries'
    df = pd.read_sql(query, conn)
    conn.close()
    return df

def prepare_data(df):
    X = df['population'].values.reshape(-1, 1)  
    y = df['area'].values  
    return X, y

def build_model(X, y):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = LinearRegression()
    model.fit(X_train, y_train)
    
    y_pred = model.predict(X_test)
    
    mse = mean_squared_error(y_test, y_pred)
    print(f"Mean Squared Error: {mse}")
    
    plt.scatter(X_test, y_test, color='blue', label='Actual')
    plt.scatter(X_test, y_pred, color='red', label='Predicted')
    plt.xlabel('Population')
    plt.ylabel('Area')
    plt.title('Actual vs Predicted Area')
    plt.legend()
    plt.show()

    return model

def predict_area(model, population):
    predicted_area = model.predict([[population]])
    return predicted_area[0]

def main():
    df = load_data()
    X, y = prepare_data(df)
    model = build_model(X, y)
    
    population = 5000000
    predicted_area = predict_area(model, population)
    print(f"Predicted area for a country with population {population}: {predicted_area:.2f} km²")

if __name__ == "__main__":
    main()
