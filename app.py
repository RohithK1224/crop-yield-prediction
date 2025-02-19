from flask import Flask, request, jsonify, render_template
import pickle
import numpy as np

# Initialize the Flask app
app = Flask(__name__)

# Load the trained model
model_file_path = 'crop_yield_model.pkl'  # Path to the saved model
with open(model_file_path, 'rb') as f:
    model = pickle.load(f)

@app.route('/')
def home():
    return render_template('index.html')  # Serves the frontend HTML file

@app.route('/predict', methods=['POST'])
@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        print("Received Input Data:", data)  # Debugging Step

        # Extract features from input JSON
        state = data.get('state')
        season = data.get('season')
        crop_year = int(data.get('crop_year'))
        crop = data.get('crop')
        area = float(data.get('area'))

        # Convert into DataFrame
        input_data = pd.DataFrame([[state, season, crop_year, crop, area]], 
                                  columns=['State', 'Season', 'Crop_Year', 'Crop', 'Area'])

        print("Formatted Input Data:", input_data)  # Debugging Step

        # Ensure transformation is applied
        transformed_input = preprocessor.transform(input_data)
        print("Transformed Input Shape:", transformed_input.shape)  # Debugging Step

        # Make prediction
        prediction = model.predict(transformed_input)

        return jsonify({'yield': prediction[0]})
    
    except Exception as e:
        return jsonify({'error': str(e)})


if __name__ == '__main__':
    app.run(debug=True)
