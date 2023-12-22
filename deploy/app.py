from flask import Flask, jsonify, request
from pynasapower.get_data import query_power
from pynasapower.geometry import point
import datetime
import os
import pandas as pd
import tensorflow as tf
from datetime import datetime, timedelta

app = Flask(__name__)

# Set the working directory to the script's directory
os.chdir(os.path.dirname(os.path.abspath(__file__)))



def get_solar_radiation_data(latitude, longitude, start_date, end_date):
    # Create the 'data' folder if it doesn't exist
    data_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')
    if not os.path.exists(data_folder):
        os.makedirs(data_folder)
    
    location = point(longitude, latitude, "EPSG:4326")
    
    # Use an absolute path for the output folder
    output_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')

    data = query_power(
        location,
        start_date,
        end_date,
        path=output_folder,
        to_file=True,
        community="re",
        parameters=["CLRSKY_SFC_SW_DWN"],
        temporal_api="daily",
        spatial_api="point",
        format="csv"
    )

    return data

def download_and_extract_dataset(csv_file_path):
    df = pd.read_csv(csv_file_path, sep=',', header=0)
    df['datetime'] = pd.to_datetime(df['DY'].astype(str) + '/' + df['MO'].astype(str) + '/' + df['YEAR'].astype(str), format='%d/%m/%Y')
    df.set_index('datetime', inplace=True)
    df = df[['CLRSKY_SFC_SW_DWN']]
    window_size = 30
    df_filtered_smoothed = df.rolling(window=window_size, min_periods=1).mean()
    df_filtered_smoothed.columns = ['CLRSKY_SFC_SW_DWN_smoothed']
    df_result = pd.concat([df, df_filtered_smoothed], axis=1)
    df_final = df_result[['CLRSKY_SFC_SW_DWN', 'CLRSKY_SFC_SW_DWN_smoothed']]

    N_FEATURES = df_final.shape[1]
    data = df_final.values
    # data_normalized = normalize_series(data, data.min(axis=0), data.max(axis=0))
    return data, N_FEATURES

def normalize_series(data, min, max):
    data = data - min
    data = data / max
    return data

def windowed_dataset(series, batch_size, n_past=365, n_future=365, shift=1):
    dataset = tf.data.Dataset.from_tensor_slices(series)
    dataset = dataset.window(size=n_past + n_future, shift=shift, drop_remainder=True)
    dataset = dataset.flat_map(lambda window: window.batch(n_past + n_future))
    dataset = dataset.map(lambda window: (window[:n_past], window[n_past:]))
    dataset = dataset.batch(batch_size).prefetch(1)
    return dataset

def prepare_for_future_prediction(trained_model, series, n_past):
    n_future = 365
    n_features = series.shape[1]
    future_data = series[-n_past:].reshape((1, n_past, n_features))
    future_predictions = trained_model.predict(future_data)
    return future_predictions

def load_model(model_path):
    # Load the pre-trained model
    trained_model = tf.keras.models.load_model(model_path)
    return trained_model

def solution_C5(model_path):
    # Specify the path to your data folder
    data_folder_path = './data'

    # Get a list of files in the data folder
    files_in_data_folder = os.listdir(data_folder_path)

    # Get CSV files from the list
    csv_files = [file for file in files_in_data_folder if file.endswith('.csv')]

    if not csv_files:
        raise FileNotFoundError("No CSV file found in the data folder.")

    # Take the first CSV file, you can modify this based on your requirements
    csv_file_path = os.path.join(data_folder_path, csv_files[0])

    data, N_FEATURES = download_and_extract_dataset(csv_file_path)

    BATCH_SIZE = 32
    N_PAST = 365
    N_FUTURE = 730
    SHIFT = 1

    # Load the pre-trained model
    trained_model = load_model(model_path)

    # Prepare for future prediction
    future_predictions = prepare_for_future_prediction(trained_model, data, N_PAST)

    return trained_model, future_predictions

@app.route('/')
def home():
    return 'Hello, World!'

@app.route('/get_data_and_predict', methods=['POST'])
def get_data_and_predict():
    try:
        # Get JSON data from the request
        data = request.get_json()

        # Extract data from JSON
        latitude = data.get('latitude')
        longitude = data.get('longitude')
        start_date = datetime(1984, 1, 1)
        end_date = datetime(2023, 6, 30)

        # Get solar radiation data
        solar_data = get_solar_radiation_data(latitude, longitude, start_date, end_date)

        # Convert the DataFrame to a dictionary
        solar_data_dict = solar_data.to_dict(orient='records')

        # Specify the path for the model file
        model_path = 'static/model_C5.h5'

        # Load the pre-trained model
        trained_model, future_predictions = solution_C5(model_path)
        formatted_predictions = {'Date_Prediction': []}
        future_predictions_list = future_predictions[0, :, 0].tolist()

        # Format the predictions with dates
        start_date_predictions = datetime(2023, 7, 1)
        date_list = [start_date_predictions + timedelta(days=i) for i in range(future_predictions.shape[1])]


        # Combine dates and predictions into a single list of dictionaries
        for i in range(len(date_list)):
            date_str = str(date_list[i].date())
            prediction_value = future_predictions_list[i]
            formatted_predictions['Date_Prediction'].append({'date': date_str, 'prediction': prediction_value})

        return jsonify(formatted_predictions)

    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)
