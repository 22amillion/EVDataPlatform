import pymongo
import hashlib
import csv

# MongoDB connection information
mongo_uri = "mongodb://localhost:27017"
database_name_prefix = "Electric_Vehicles"
collection_name_prefix = "dataCleaned"

# User authentication information
username = input("Please input your username: ")
password = input("Please input your password: ")

# User authentication function
def authenticate(username, password):
    # Implement user authentication logic here
    # For example, you can query the username and hashed password from the database and compare
    # Here we assume there is only one hardcoded username and password
    valid_username = "admin"
    valid_password = "Dsci-551"

    if username == valid_username and hashlib.sha256(password.encode()).hexdigest() == hashlib.sha256(valid_password.encode()).hexdigest():
        return True
    else:
        return False

# Add data from CSV file
def add_data_from_csv(client, csv_file_path):
    try:
        with open(csv_file_path, 'r') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            for row in csv_reader:
                data = {key: value for key, value in row.items()}
                year = int(data['Year'])
                cutoff_year = 2020

                if year < cutoff_year:
                    database_name = f"{database_name_prefix}_before_{cutoff_year}"
                    collection_name = f"{collection_name_prefix}"
                else:
                    database_name = f"{database_name_prefix}_after_{cutoff_year}"
                    collection_name = f"{collection_name_prefix}"

                db = client[database_name]
                collection = db[collection_name]

                collection.insert_one(data)

            print(f"Data from {csv_file_path} added successfully to the databases.")
    except FileNotFoundError:
        print(f"CSV file not found: {csv_file_path}")

# Add data
def add_data(client):
    while True:
        choice = input("Please choose your option (1.add single data 2.add data from CSV file 3.back to main menu): ")
        if choice == "1":
            data = get_single_data_from_user()
            if data is not None:
                save_data_to_database(client, data)
            else:
                break
        elif choice == "2":
            csv_file_path = input("Please enter the path of the CSV file: ")
            add_data_from_csv(client, csv_file_path)
        elif choice == "3":
            break
        else:
            print("Invalid option, Please try again.")

# Delete data
def delete_data(client):
    while True:
        query = get_query_from_user()
        if query is None:
            break

        before_collection = client[f"{database_name_prefix}_before_2020"][collection_name_prefix]
        after_collection = client[f"{database_name_prefix}_after_2020"][collection_name_prefix]

        before_result = before_collection.delete_many(query)
        after_result = after_collection.delete_many(query)

        print(f"Deleted {before_result.deleted_count} records from {database_name_prefix}_before_2020.{collection_name_prefix}")
        print(f"Deleted {after_result.deleted_count} records from {database_name_prefix}_after_2020.{collection_name_prefix}")

        choice = input("Do you want to delete more data? (y/n): ")
        if choice.lower() != "y":
            break

# Modify data
def modify_data(client):
    while True:
        query = get_query_from_user()
        if query is None:
            break

        update = get_update_from_user()
        if update is None:
            break

        before_collection = client[f"{database_name_prefix}_before_2020"][collection_name_prefix]
        after_collection = client[f"{database_name_prefix}_after_2020"][collection_name_prefix]

        before_result = before_collection.update_many(query, update)
        after_result = after_collection.update_many(query, update)

        print(f"Updated {before_result.modified_count} records in {database_name_prefix}_before_2020.{collection_name_prefix}")
        print(f"Updated {after_result.modified_count} records in {database_name_prefix}_after_2020.{collection_name_prefix}")

        choice = input("Do you want to modify more data? (y/n): ")
        if choice.lower() != "y":
            break

# Query data
def query_data(client):
    while True:
        query = get_query_from_user()
        if query is None:
            break

        before_collection = client[f"{database_name_prefix}_before_2020"][collection_name_prefix]
        after_collection = client[f"{database_name_prefix}_after_2020"][collection_name_prefix]

        before_result = list(before_collection.find(query))
        after_result = list(after_collection.find(query))

        print(f"Query results from {database_name_prefix}_before_2020.{collection_name_prefix}:")
        for data in before_result:
            print(data)

        print(f"\nQuery results from {database_name_prefix}_after_2020.{collection_name_prefix}:")
        for data in after_result:
            print(data)

        choice = input("Do you want to query more data? (y/n): ")
        if choice.lower() != "y":
            break

# Get single data from user
def get_single_data_from_user():
    try:
        VIN = input("Please enter the VIN: ")
        County = input("Please enter the County: ")
        City = input("Please enter the City: ")
        State = input("Please enter the State: ")
        Postal_Code = input("Please enter the Postal Code: ")
        Year = int(input("Please enter the Year: "))
        Make = input("Please enter the Make: ")
        Model = input("Please enter the Model: ")
        Type = input("Please enter the Type: ")
        Eligibility = input("Please enter the Eligibility: ")
        Range = int(input("Please enter the Range: "))
        MSRP = int(input("Please enter the MSRP: "))
        longitude = float(input("Please enter the longitude: "))
        latitude = float(input("Please enter the latitude: "))

        data = {
            "VIN": VIN,
            "County": County,
            "City": City,
            "State": State,
            "Postal Code": Postal_Code,
            "Year": Year,
            "Make": Make,
            "Model": Model,
            "Type": Type,
            "Eligibility": Eligibility,
            "Range": Range,
            "MSRP": MSRP,
            "longitude": longitude,
            "latitude": latitude
        }

        return data
    except ValueError:
        print("An exception occurred. Please ensure the input data types are correct.")
        return None


# Get query from user
def get_query_from_user():
    field = input("Please enter the field to query (e.g., 'VIN', 'Year', 'Make') or 'back' to return to the previous menu: ")
    if field.lower() == "back":
        return None

    value = input(f"Please enter the value for {field}: ")

    query = {field: value}
    return query

# Get update operation from user
def get_update_from_user():
    field = input("Please enter the field to update (e.g., 'MSRP', 'Range') or 'back' to return to the previous menu: ")
    if field.lower() == "back":
        return None

    new_value = input(f"Please enter the new value for {field}: ")

    update = {"$set": {field: new_value}}
    return update

# Save data to database
def save_data_to_database(client, data):
    year = data['Year']
    cutoff_year = 2020

    if year < cutoff_year:
        database_name = f"{database_name_prefix}_before_{cutoff_year}"
        collection_name = f"{collection_name_prefix}"
    else:
        database_name = f"{database_name_prefix}_after_{cutoff_year}"
        collection_name = f"{collection_name_prefix}"

    db = client[database_name]
    collection = db[collection_name]

    collection.insert_one(data)
    print(f"Data added successfully to {database_name}.{collection_name}")


# Authenticate username and password
if authenticate(username, password):
    client = pymongo.MongoClient(mongo_uri)

    # Data operations
    while True:
        operation = input("Please choose your operation(1.add data 2.delete data 3.update data 4.query data 5.exit): ")
        if operation == "1":
            add_data(client)
        elif operation == "2":
            delete_data(client)
        elif operation == "3":
            modify_data(client)
        elif operation == "4":
            query_data(client)
        elif operation == "5":
            break
        else:
            print("Invalid operation, Please try again.")