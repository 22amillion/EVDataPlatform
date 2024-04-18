import os
import pandas as pd
import pymongo

def find_csv_file(directory):
    for file in os.listdir(directory):
        if file.endswith(".csv"):
            return os.path.join(directory, file)
    return None
<<<<<<< HEAD

def hash_year(year, cutoff_year):
    return 'before' if year < cutoff_year else 'after'

def upload_based_on_year(directory, collection_name_prefix, database_name_prefix, mongo_uri, cutoff_year=2020):
    csv_file_path = find_csv_file(directory)
    if not csv_file_path:
        print(f"No CSV file found in directory: {directory}")
        return

    df = pd.read_csv(csv_file_path)
    client = pymongo.MongoClient(mongo_uri)

    for index, row in df.iterrows():
        year = int(row['Year'])
        suffix = hash_year(year, cutoff_year)
        database_name = f"{database_name_prefix}_{suffix}_{cutoff_year}"
        collection_name = collection_name_prefix

        data = row.to_dict()
        db = client[database_name]
        collection = db[collection_name]
        collection.insert_one(data)
        print(f"Data uploaded successfully to {collection_name} in {database_name}.")

if __name__ == '__main__':
    mongo_uri = "mongodb://localhost:27017"  
    directory_path = "Electric_Vehicle_Population_Data_Cleaned"
    database_name_prefix = "Electric_Vehicles"
    collection_name_prefix = "dataCleaned"
    cutoff_year = 2020
=======

def upload_based_on_year(directory, collection_name_prefix, database_name_prefix, mongo_uri, cutoff_year):
    csv_file_path = find_csv_file(directory)
    if csv_file_path:
        df = pd.read_csv(csv_file_path)

        client = pymongo.MongoClient(mongo_uri)

        for index, row in df.iterrows():
            year = int(row['Year']) 

            if year < cutoff_year:
                database_name = f"{database_name_prefix}_before_{cutoff_year}"
                collection_name = f"{collection_name_prefix}"
            else:
                database_name = f"{database_name_prefix}_after_{cutoff_year}"
                collection_name = f"{collection_name_prefix}" 

            data = row.to_dict()

            db = client[database_name]
            collection = db[collection_name]

            collection.insert_one(data)
            print(f"Data uploaded successfully to {collection_name} in {database_name}.")
    else:
        print(f"No CSV file found in directory: {directory}")
if __name__ == '__main__':
    # MongoDB URI for local instance
    mongo_uri = "mongodb://localhost:27017"  
    directory_path = "Electric_Vehicle_Population_Data_Cleaned"  # 请替换为你的CSV文件目录

    database_name_prefix = "Electric_Vehicles"
    collection_name_prefix = "dataCleaned"


    cutoff_year = 2020


>>>>>>> feca63891d9923da81086a8978f8441a317e0629
    upload_based_on_year(directory_path, collection_name_prefix, database_name_prefix, mongo_uri, cutoff_year)
