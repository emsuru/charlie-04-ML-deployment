import pandas as pd
import json

def csv_to_json(csv_path, json_path):
    """Convert a CSV file to a JSON file."""
    # Read the CSV file using pandas
    df = pd.read_csv(csv_path)

    # Convert the DataFrame to a JSON string and save to a file
    # Update: Remove `lines=True` to ensure the JSON is formatted as an array of objects
    df.to_json(json_path, orient='records')

    print(f"CSV file {csv_path} has been converted to JSON and saved as {json_path}")

csv_path = 'input_data/newdata_ninel.csv'
json_path = 'input_data/newdata_ninel_2.json'

csv_to_json(csv_path, json_path)



# def csv_to_json_columns(csv_path, json_path):
#     """Convert CSV file columns, their data types, and unique values (where applicable) to a JSON file."""

#     df = pd.read_csv(csv_path)

#     # Extract column names, their data types, and unique values where applicable
#     columns_info = {}
#     for column in df.columns:
#         # Infer data type of column, convert pandas dtype to general type
#         dtype = str(df[column].dtype)
#         if "int" in dtype:
#             dtype = "int"
#         elif "float" in dtype:
#             dtype = "float"
#         elif "bool" in dtype:
#             dtype = "bool"
#         else:
#             dtype = "str"  # Default to string for other types

#         # Initialize column info with data type
#         column_info = {'type': dtype}

#         # For certain data types or based on the number of unique values, add unique values to the column info
#         if dtype in ["bool", "str"] and df[column].nunique() <= 10:  # Adjust the threshold as needed
#             unique_values = df[column].dropna().unique().tolist()
#             # Convert numpy types to Python types for JSON serialization
#             unique_values = [val.item() if hasattr(val, 'item') else val for val in unique_values]
#             column_info['unique_values'] = unique_values

#         columns_info[column] = column_info

#     # Prepare a dictionary with a key that describes the content, e.g., 'columns', and the columns info as its value
#     columns_dict = {'columns': columns_info}

#     # Convert the dictionary to JSON format and save to a file
#     with open(json_path, 'w') as json_file:
#         json.dump(columns_dict, json_file, indent=4)

#     print(f"JSON file with column names, types, and unique values saved to {json_path}")

# # Example usage
# csv_path = 'input_data/newdata_ninel.csv'  # Update this path to your CSV file path
# json_path = 'input_data/columns_types_unique.json'  # Update this path to your desired JSON file path
# csv_to_json_columns(csv_path, json_path)


# --- ONLY GET COLUMN NAMES & TYPES ---

# def csv_to_json_columns(csv_path, json_path):
#     """Convert CSV file columns and their data types to a JSON file."""

#     df = pd.read_csv(csv_path)

#     # Extract column names and their data types
#     columns_info = {}
#     for column in df.columns:
#         # Infer data type of column, convert pandas dtype to general type
#         dtype = str(df[column].dtype)
#         if "int" in dtype:
#             dtype = "int"
#         elif "float" in dtype:
#             dtype = "float"
#         elif "bool" in dtype:
#             dtype = "bool"
#         else:
#             dtype = "str"  # Default to string for other types

#         columns_info[column] = dtype

#     # Prepare a dictionary with a key that describes the content, e.g., 'columns', and the columns info as its value
#     columns_dict = {'columns': columns_info}

#     # Convert the dictionary to JSON format and save to a file
#     with open(json_path, 'w') as json_file:
#         json.dump(columns_dict, json_file, indent=4)

#     print(f"JSON file with column names and types saved to {json_path}")

# Run
# csv_path = 'input_data/newdata_ninel.csv'  # Update this path to your CSV file path
# json_path = 'input_data/columns_types.json'  # Update this path to your desired JSON file path
# csv_to_json_columns(csv_path, json_path)


# -- ONLY GET COLUMNS NAMES --
# def csv_to_json_columns(csv_path, json_path):
#     """Convert CSV file columns to a JSON file."""
#     # Read the CSV file
#     df = pd.read_csv(csv_path)

#     # Extract column names and convert to list
#     columns_list = df.columns.tolist()

#     # Prepare a dictionary with a key that describes the content, e.g., 'columns', and the list of columns as its value
#     columns_dict = {'columns': columns_list}

#     # Convert the dictionary to JSON format and save to a file
#     with open(json_path, 'w') as json_file:
#         pd.json.dump(columns_dict, json_file, indent=4)

#     print(f"JSON file with column names saved to {json_path}")

# # RUN
# csv_path = 'input_data/newdata_ninel.csv'  # Update this path to your CSV file path
# json_path = 'output_data/columns.json'  # Update this path to your desired JSON file path
# csv_to_json_columns(csv_path, json_path)
