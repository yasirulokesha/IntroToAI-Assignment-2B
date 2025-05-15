# Seerch in the LSTM model for specific time forecasting
import numpy as np
import pandas as pd
import joblib
import tensorflow as tf
# import keras.models as load_model 
from datetime import datetime, timedelta
from sklearn.preprocessing import MinMaxScaler

from utils import generating_sequences, replace_outliers_iqr

print("Initialized Libraries...")
print("Tensorflow version:", tf.__version__)

def LSTM_model(data_set, site_id, target_time):
    model_path = f"TBRGS/models/LSTM_model/models/lstm_model_site_{site_id}.keras"
    scaler_path = f"TBRGS/models/LSTM_model/scalers/scaler_site_{site_id}.save"
    
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

if __name__ == "__main__":
    # Example usage
    site_id = '970'
    input_time = '2006-11-02 00:00'
    data = pd.read_csv(f"TBRGS/data/processed/processed_dataset.csv")
    data_set = data[data['site_id'] == int(site_id)].sort_values("timestamp")
    predictions = LSTM_model(data_set, site_id, input_time)
    print(predictions)
    
    
# # -------------------------------
# # STEP 2.1: Let user input target datetime
# # -------------------------------
# # Example input: "2006-11-10 08:15"
# target_datetime_str = input("🔢 Enter target datetime (e.g., 2006-11-10 08:15): ")
# target_datetime = pd.to_datetime(target_datetime_str)

# # Calculate number of 15-min steps from last known timestamp
# last_known_time = df_site["timestamp"].max()
# delta = target_datetime - last_known_time

# if delta.total_seconds() <= 0:
#     print("⚠️ Cannot predict: target time must be in the future beyond last known data.")
#     exit()

# # Convert time delta to 15-min steps
# num_steps = int(delta.total_seconds() // (15 * 60))
# print(f"⏩ Predicting {num_steps} steps forward (from {last_known_time} to {target_datetime})...")

# # -------------------------------
# # STEP 3: Predict next N time steps
# # -------------------------------
# predictions_scaled = []
# current_input = last_sequence.copy()

# for _ in range(num_steps):
#     next_step = model.predict(current_input, verbose=0)[0][0]
#     predictions_scaled.append(next_step)
#     current_input = np.append(current_input[:, 1:, :], [[[next_step]]], axis=1)

# # -------------------------------
# # STEP 4: Inverse transform and get target prediction
# # -------------------------------
# predicted_volumes = scaler.inverse_transform(np.array(predictions_scaled).reshape(-1, 1))
# predicted_value = predicted_volumes[-1][0]

# print(f"\n📍 Predicted volume at {target_datetime}: {predicted_value:.2f} vehicles")


# Replace outliers using IQR
# replace_outliers_iqr(final_dataset, 'volume')

# for id in sites:
#     # Load the model and scaler
#     model = load_model(f"../models/LSTM_model/models/lstm_model_site_{id}.keras")
#     scaler = joblib.load(f"../models/LSTM_model/scalers/scaler_site_{id}.save")
#     print(f"\n🚦 Loading model and scaler for site {id}...")
    
#     # Filter data for this site
#     site_data = final_dataset[final_dataset['site_id'] == id].sort_values("timestamp")
    
#     site_data['volume'] = scaler.transform(site_data[['volume']])
    
#     # Predictions for the next time step
#     last_site_data = np.array(site_data['volume'][-96:]).reshape(-1, 96, 1)
   
#     # Make predictions on the test set
#     last_test_site_data = np.array(site_data['volume'][:97])
    
#     testX, testY = generating_sequences(last_test_site_data)
    
#     testX = testX.reshape(-1, 96, 1)
    
#     # Make predictions on the test set
#     y_pred = model.predict(testX)

#     # Reverse scaling if necessary
#     y_test_actual = scaler.inverse_transform(testY.reshape(-1, 1))
#     y_pred_actual = scaler.inverse_transform(y_pred)

#     smape = 100 * abs(y_pred_actual - y_test_actual) / ((abs(y_pred_actual) + abs(y_test_actual)) / 2)
#     accuracy = 100 - smape
#     accuracy = np.mean(accuracy)
#     print(f"Accuracy: {accuracy:.2f}%")
    
#     pred_scaled = model.predict(last_site_data)
#     pred_volume = scaler.inverse_transform(pred_scaled)[0][0]

#     # print(f"Predicted volume for the next time step: {pred_volume:.2f}")
#     # print(pred_scaled)
#     print(pred_volume)