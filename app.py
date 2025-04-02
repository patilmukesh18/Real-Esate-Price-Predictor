from flask import Flask, render_template, request
import pandas as pd
import pickle

# Initialize Flask app
app = Flask(__name__)

# Load the trained model pipeline (make sure to save your model as 'model.pkl')
with open('model.pkl', 'rb') as model_file:
    model_pipeline = pickle.load(model_file)

# Define the prediction function
def predict_amount(user_input):
    # Convert the user input into a DataFrame to match the model's input format
    user_input_df = pd.DataFrame([user_input])

    # Make prediction using the trained model pipeline
    predicted_amount = model_pipeline.predict(user_input_df)
    return predicted_amount[0]

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Get the user input from the form
        user_input = {
            'Transaction Type': request.form['transaction_type'],
            'Registration type': request.form['registration_type'],
            'Area': request.form['area'],
            'Property Type': request.form['property_type'],
            'Property Sub Type': request.form['property_sub_type'],
            'Property Size (sq.m)': float(request.form['property_size']),
            'Bedrooms': int(request.form['bedrooms']),
            'Parking': request.form['parking'],
            'Nearest Metro': request.form['nearest_metro'],
            'Nearest Mall': request.form['nearest_mall'],
            'Nearest Landmark': request.form['nearest_landmark']
        }

        # Get prediction
        predicted_amount = predict_amount(user_input)

        # Render the result on the same page
        return render_template('index.html', predicted_amount=round(predicted_amount,2))

    # If the request is GET, just show the form
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
