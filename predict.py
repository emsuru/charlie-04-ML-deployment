import pandas as pd
import json
import joblib
from preprocessing.data_preprocessor import DataPreprocessor
import logging

logging.basicConfig(level=logging.INFO)

def load_preprocessor(preprocessor_path):
    """Load the saved preprocessor object."""
    return joblib.load(preprocessor_path)

def load_model(model_path):
    """Load the saved model."""
    return joblib.load(model_path)

# def clean_newdata(data_path):
#     """Clean the new data using the DataPreprocessor class."""
#     # df = pd.read_csv(data_path)

#     # Read the JSON file instead of a CSV file
#     with open(data_path, 'r') as file:
#         data = json.load(file)
#     df = pd.DataFrame(data)

#     preprocessor = DataPreprocessor(df)
#     preprocessor.clean_drop().clean_impute().encode_state_building().encode_epc()
#     cleaned_df = preprocessor.df
#     #save the cleaned data to a csv file
#     # cleaned_df.to_csv('input_data/cleaned_newdata.csv', index=False)

#     return cleaned_df

def clean_newdata(data):
    """
    Clean the new data using the DataPreprocessor class.
    This version of the function accepts a dictionary directly.

    Args:
    - data (dict): The data to be cleaned, in dictionary format.

    Returns:
    - DataFrame: The cleaned data as a pandas DataFrame.
    """
    # Assuming 'data' is a dictionary representing a single property,
    # we convert it into a DataFrame. If 'data' is expected to represent
    # multiple properties, it should already be a list of dictionaries,
    # and this line would not need to change.
    df = pd.DataFrame([data])  # Convert the dictionary to a DataFrame

    # Initialize the DataPreprocessor with the DataFrame
    preprocessor = DataPreprocessor(df)
    # Apply the cleaning and preprocessing methods as defined in your DataPreprocessor class
    preprocessor.clean_drop().clean_impute().encode_state_building().encode_epc()
    # Retrieve the cleaned DataFrame
    cleaned_df = preprocessor.df
    # #save the cleaned data to a json file
    # cleaned_df.to_json('input_data/cleaned_newdata.json', orient='records')
    return cleaned_df

def preprocess_newdata(cleaned_df, preprocessor_paths):
    """Preprocess the new data using the loaded preprocessor objects."""
    new_df = cleaned_df.copy()

    # Load preprocessing objects
    ohe = joblib.load(preprocessor_paths['onehotencoder'])
    ohe.set_params(handle_unknown='ignore')  # Ensure it ignores unknown categories (an issue I encountered during testing the API)
    num_imputer = joblib.load(preprocessor_paths['num_imputer'])
    columns_to_keep = joblib.load(preprocessor_paths['columns_to_keep'])

    # Check if the target variable 'price' is in the dataframe and drop it if found
    if 'price' in new_df.columns:
        new_df.drop('price', axis=1, inplace=True)
        print("'price' column found in the dataset. It has been dropped for prediction.")

    # Apply preprocessing transformations
    # categorical encoding
    cat_cols = new_df.select_dtypes(include=['object', 'category']).columns
    new_df_encoded = ohe.transform(new_df[cat_cols])
    new_df_encoded_df = pd.DataFrame(new_df_encoded.toarray(), columns=ohe.get_feature_names_out(cat_cols), index=new_df.index)
    new_df = new_df.drop(columns=cat_cols).join(new_df_encoded_df)

    #save the preprocessed data to a csv file
    new_df.to_csv('input_data/preprocessed_categ_encoding_newdata.csv', index=False)

    # feature selection based on correlation (this comes from preprocess_feat_select
    # and ensures the new data has the same columns as the model was trained on, filling missing columns with zeros
    new_df = new_df.reindex(columns=columns_to_keep, fill_value=0)

    #numerical imputation
    numeric_cols = new_df.select_dtypes(include=['int64', 'float64']).columns
    new_df[numeric_cols] = num_imputer.transform(new_df[numeric_cols])
    logging.info(f"Preprocessed new data: {new_df.head()}")
    return new_df

def predict(model, X):
    """Make predictions using the preprocessed data and the loaded model."""
    return model.predict(X)

# DEAR USER 1/3: update the 'output_path' to save your predictions with your desired file name


def save_predictions(predictions, output_path='output_data/predictions_ninel'):
    """Save the predictions to both CSV and JSON files with prices rounded to 2 decimal points."""
    df = pd.DataFrame(predictions, columns=['PredictedPrice'])
    df['PredictedPrice'] = df['PredictedPrice'].round(2)  # Round to 2 decimal points

    # Save to CSV
    csv_output_path = f"{output_path}.csv"
    df.to_csv(csv_output_path, index=False)
    print(f"Predictions for Random Forest saved to {csv_output_path}")

    # Save to JSON
    json_output_path = f"{output_path}.json"
    df.to_json(json_output_path, orient='records')
    print(f"Predictions for Random Forest saved to {json_output_path}")

    # DEAR USER 2/3: update the 'new_data_path' to match the name of your new data

if __name__ == "__main__":
    # 1. Load and clean the new data (using clean & encode methods from the DataPreprocessor class)

    # new_data_path = 'input_data/newdata_ninel.csv' # if newdata is csv
    new_data_path = 'input_data/newdata_ninel.json' # if newdata is json
    cleaned_new_data = clean_newdata(new_data_path)

    # 2. Load the preprocessing objects (that were saved during training, when running Preprocessor)
    preprocessor_paths = {
        'onehotencoder': 'preprocessing/onehotencoder.pkl',
        'num_imputer': 'preprocessing/num_imputer.pkl',
        'columns_to_keep': 'preprocessing/columns_to_keep.pkl'
    }
    preprocessed_new_data = preprocess_newdata(cleaned_new_data, preprocessor_paths)

    # DEAR USER 3/3: update the 'model_path' with the saved model you want to use for your predictions

    # 3. Load the model (that was saved during training, when running any model in models/ directory, e.g. RandomForest)
    model_path = 'saved_models/random_forest_model.pkl'
    model = load_model(model_path)

    # 4. Make & save predictions
    predictions = predict(model, preprocessed_new_data)
    save_predictions(predictions)
