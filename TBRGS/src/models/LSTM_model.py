# Seerch in the LSTM model for specific time forecasting
import numpy as np
import pandas as pd
import joblib
import tensorflow as tf
# import keras.models as load_model 
from datetime import datetime, timedelta
from sklearn.preprocessing import MinMaxScaler

from .utils import generating_sequences, replace_outliers_iqr

print("Initialized Libraries...")
print("Tensorflow version:", tf.__version__)

def lstm_prediction_engine(data_set, site_id, target_time):
    model_path = f"TBRGS/src/models/LSTM_model/models/lstm_model_site_{site_id}.keras"
    scaler_path = f"TBRGS/src/models/LSTM_model/scalers/scaler_site_{site_id}.save"
    
    target_time = pd.to_datetime(target_time)
    target_time = pd.to_datetime(target_time.strftime("2006-11-%d %H:%M"), format="%Y-%m-%d %H:%M")
    # target_time = target_time.strftime("%d %H:%M")
    # target_time = pd.to_datetime(target_time)
    
    # Calculate number of 15-min steps from last known timestamp
    last_known_time = data_set["timestamp"].max()
    last_known_time = pd.to_datetime(last_known_time)
    
    
    # last_known_time = datetime.strptime(last_known_time, "%Y-%m-%d %H:%M")
    
    delta = target_time - last_known_time
    
    print("Last known time:", last_known_time)
    print("Target time:", target_time)
    
    # Convert time delta to 15-min steps
    num_steps = int(delta.total_seconds() // (15 * 60))
    print(f"⏩ Predicting {num_steps} steps forward (from {last_known_time} to {target_time})...")
    
    try:
        print('Loading model and scaler...')
        # Load the model
        model = tf.keras.models.load_model(model_path)
        # Load the scaler
        scaler = joblib.load(scaler_path)
    except Exception as e:
      print('Model and scaler failed to load. Please check the path and try again.')
      print('Path to model:', model_path)
      print('Path to scaler:', scaler_path)
      print("❌ An error occurred:", e)
      return 1
    
    try:
        print('Loading data...')
        # Load the dataset
        replace_outliers_iqr(data_set, 'volume')
    except Exception as e:
        print('Data loading failed. Please check the path and try again.')
        print("❌ An error occurred:", e)
        return 2  

    try:
        print("Preprocessing data...")
        data_set['volume'] = scaler.fit_transform(data_set[['volume']])
    except Exception as e:
        print('Data preprocessing failed. Please check the path and try again.')
        print("❌ An error occurred:", e)
        return 3 
    
    try:
        print('Generating sequences...')
        # Generate sequences
        x = np.array(data_set['volume'][-96:]).reshape(-1, 96, 1)
        print('Shape of x:', x.shape)
    except Exception as e:
      print('Sequence generation failed. Please check the data and try again.')
      print("❌ An error occurred:", e)
      return 4
  
    print('Sequences generated successfully.')
    
    predictions_scaled = []
    current_input = x.copy()
    
    try:
        # Make predictions
        print('Making predictions...')
        for i in range(num_steps):
            current_input = current_input[-96:].reshape(1, 96, 1)
            # Predict the next time step
            next_step = model.predict(current_input, verbose=0)[0][0]
            # if not np.isfinite(next_step):
            #     print(f"🚨 Invalid prediction at step {i}: {next_step}")
            #     break 
            # print(i, end='\n')
            predictions_scaled.append(next_step)
            current_input = np.append(current_input[:, 1:, :], [[[next_step]]], axis=1)
            
        try:
            print('Inverse transforming predictions...')
            # print(predictions_scaled)
            # Inverse transform the predictions
            predicted_volumes = scaler.inverse_transform(np.array(predictions_scaled).reshape(-1, 1))
            predicted_value = predicted_volumes[-1][0]
        except Exception as e:
            print('Inverse transformation failed. Please check the scaler and try again.')
            print("❌ An error occurred:", e)
            exit()
            return 6
        
        print('Predictions made successfully.')
    except Exception as e:
        print('Prediction failed. Please check the model and data.')
        print("❌ An error occurred:", e)
        return 5

    return predicted_value

def LSTM_prediction(site_id, input_time):
    site_id = site_id
    input_time = input_time
    # Load the dataset
    data = pd.read_csv(f"TBRGS/data/processed/processed_dataset.csv")
    data_set = data[data['site_id'] == int(site_id)].sort_values("timestamp")
    predictions = lstm_prediction_engine(data_set, site_id, input_time)
    return predictions