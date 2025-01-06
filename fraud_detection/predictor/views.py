import joblib
import json

from tensorflow.keras.models import load_model
from django.shortcuts import render
from geopy.geocoders import Nominatim
from datetime import datetime

from django.shortcuts import render
from .forms import TransactionForm
# Load the trained model
model = load_model(r'C:\Users\abdes\Desktop\MIAAD\S3\DL\Fraud_detaction\fraud_detection\predictor\models\6features_fraud_detection_model.h5')

# Load the scaler and encoders
scaler = joblib.load(r'C:\Users\abdes\Desktop\MIAAD\S3\DL\Fraud_detaction\fraud_detection\predictor\models\6scaler.pkl')
encoders = joblib.load(r'C:\Users\abdes\Desktop\MIAAD\S3\DL\Fraud_detaction\fraud_detection\predictor\models\6label_encoders.pkl')
# GeoPy setup for address resolution
geolocator = Nominatim(user_agent="fraud_detection",  timeout=10)


def home(request):
    return render(request, r'C:\Users\abdes\Desktop\MIAAD\S3\DL\Fraud_detaction\fraud_detection\predictor\templates\predictor\home.html')


def predict_fraud(request):
    with open(r'C:\Users\abdes\Desktop\MIAAD\S3\DL\Fraud_detaction\fraud_detection\predictor\JSON\choices.json') as f:  # Adjust path to your JSON file
        city_pop_json = json.load(f)
    if request.method == 'POST':
        entered_features = request.POST.dict()  # Or however you extract the input

        form = TransactionForm(request.POST)
        if form.is_valid():
            # Extract form data
            raw_data = form.cleaned_data

            # Convert DateTime with timezone to UNIX time
            raw_data['unix_time'] = int(datetime.strptime(
                str(raw_data['unix_time']),
                '%Y-%m-%d %H:%M:%S%z'
            ).timestamp())


            # # Get holder's latitude and longitude from street address
            # holder_address = f"{raw_data['street']}, {raw_data['city']}, {raw_data['state']}, {raw_data['zip']}"
            # holder_location = geolocator.geocode(holder_address)
            # raw_data['lat'] = holder_location.latitude if holder_location else 0
            # raw_data['long'] = holder_location.longitude if holder_location else 0
            #
            # # Get merchant's latitude and longitude
            # merchant_address = f"{raw_data['merchant']}, {raw_data['city']}, {raw_data['state']}"
            # merchant_location = geolocator.geocode(merchant_address)
            # raw_data['merch_lat'] = merchant_location.latitude if merchant_location else 0
            # raw_data['merch_long'] = merchant_location.longitude if merchant_location else 0

            # Encode categorical features
            for col, encoder in encoders.items():
                if col in raw_data:
                    try:
                        raw_data[col] = encoder.transform([raw_data[col]])[0]
                    except ValueError:
                        raw_data[col] = -1  # Default value for unseen categories

            # Arrange data in the correct feature order
            feature_order = [
                'category',  'amt', 'gender', 'city', 'unix_time','age',
                # 'street', 'state', 'zip', 'lat', 'long', 'merch_lat', 'merch_long', 'merch_age'

            ]
            input_data = [raw_data[feature] for feature in feature_order]

            # Scale the data
            input_data_scaled = scaler.transform([input_data])

            # Make prediction
            prediction = model.predict(input_data_scaled)
            fraud_probability = prediction[0][0]
            is_fraud = fraud_probability > 0.005

            # Render the result
            return render(request, r'C:\Users\abdes\Desktop\MIAAD\S3\DL\Fraud_detaction\fraud_detection\predictor\templates\predictor\result.html', {
                'is_fraud': is_fraud,
                'fraud_probability': fraud_probability,
                'entered_features': entered_features,
            })
    else:
        form = TransactionForm()

    return render(request, r'C:\Users\abdes\Desktop\MIAAD\S3\DL\Fraud_detaction\fraud_detection\predictor\templates\predictor\form.html', {'form': form, 'city_pop_json': city_pop_json})

