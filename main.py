from bson import ObjectId
from flask import Flask, jsonify, send_from_directory, redirect, url_for, render_template, request, json
from pymongo import MongoClient
from flask_bootstrap import Bootstrap

app = Flask(__name__)
Bootstrap(app)
mongo_uri = "mongodb://localhost:27017"

def serialize_data(data):
    for document in data:

        if '_id' in document:
            document['_id'] = str(document['_id'])
    return data


def get_data_from_mongodb(database_name, collection_name):
    client = MongoClient(mongo_uri)
    db = client[database_name]
    collection = db[collection_name]
    data = list(collection.find({}))

    serialized_data = serialize_data(data)
    return serialized_data

def get_filtered_data_from_db(db_name, collection_name, query):
    client = MongoClient(mongo_uri)
    db = client[db_name]
    collection = db[collection_name]
    return list(collection.find(query, {'_id': 0}))

def get_visualization_data():
    client = MongoClient(mongo_uri)

    # Connect to the before 2020 database and retrieve data
    db_before_2020 = client["Electric_Vehicles_before_2020"]
    collection_before_2020 = db_before_2020["dataCleaned"]
    pipeline_before_2020 = [
        {"$group": {"_id": {"Year": "$Year", "Make": "$Make"}, "count": {"$sum": 1}}}
    ]
    data_before_2020 = list(collection_before_2020.aggregate(pipeline_before_2020))

    db_after_2020 = client["Electric_Vehicles_after_2020"]
    collection_after_2020 = db_after_2020["dataCleaned"]
    pipeline_after_2020 = [
        {"$group": {"_id": {"Year": "$Year", "Make": "$Make"}, "count": {"$sum": 1}}}
    ]
    data_after_2020 = list(collection_after_2020.aggregate(pipeline_after_2020))

    visualization_data = data_before_2020 + data_after_2020

    return visualization_data

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/<path:path>')
def static_file(path):
    return send_from_directory('static', path)

@app.route('/search')
def search():
    return render_template('search.html')

@app.route('/visualization', methods=['GET'])
def visualization():
    data_before_2020 = get_data_from_mongodb("Electric_Vehicles_before_2020", "dataCleaned")
    data_after_2020 = get_data_from_mongodb("Electric_Vehicles_after_2020", "dataCleaned")
    
    return render_template('visualization.html', data_before_2020=json.dumps(data_before_2020), data_after_2020=json.dumps(data_after_2020))

@app.route('/data_before_2020', methods=['GET'])
def get_data_before_2020():
    data = get_data_from_mongodb("Electric_Vehicles_before_2020", "dataCleaned")
    return jsonify(data)

@app.route('/data_after_2020', methods=['GET'])
def get_data_after_2020():
    data = get_data_from_mongodb("Electric_Vehicles_after_2020", "dataCleaned")  
    data = get_data_from_mongodb("Electric_Vehicles_after_2020", "dataCleaned")  
    return jsonify(data)

@app.route('/filter_data', methods=['GET'])
def filter_data():
    query = {}

    year = request.args.get('year')
    make = request.args.get('make')
    state = request.args.get('state')
    county = request.args.get('county')
    if year:
        query['Year'] = {'$in': [int(y) for y in year.split(',')]}
    if make:
        query['Make'] = {'$in': make.split(',')}
    if state:
        query['State'] = state
    if county:  
        query['County'] = county

    data_before_2020 = get_filtered_data_from_db("Electric_Vehicles_before_2020", "dataCleaned", query)
    data_after_2020 = get_filtered_data_from_db("Electric_Vehicles_after_2020", "dataCleaned", query)

    combined_data = data_before_2020 + data_after_2020

    return jsonify(combined_data)

#####################
@app.route('/get-visualization-data', methods=['GET'])
def get_grouped_visualization_data():
    data_before_2020 = get_data_from_mongodb("Electric_Vehicles_before_2020", "dataCleaned")
    data_after_2020 = get_data_from_mongodb("Electric_Vehicles_after_2020", "dataCleaned")

    # Combine the data
    combined_data = data_before_2020 + data_after_2020

    # Group the data by year and make
    grouped_data = {}
    for item in combined_data:
        year = item['Year']
        make = item['Make']
        count = 1  # Assuming each item represents one vehicle

        if year not in grouped_data:
            grouped_data[year] = {}

        if make not in grouped_data[year]:
            grouped_data[year][make] = 0

        grouped_data[year][make] += count

    return jsonify(grouped_data)

@app.route('/get-yearly-bev-phev-data', methods=['GET'])
def get_yearly_bev_phev_data():
    data = []

    for year in range(2010, 2025):
        db_before = MongoClient(mongo_uri)["Electric_Vehicles_before_2020"]
        db_after = MongoClient(mongo_uri)["Electric_Vehicles_after_2020"]
        collection_before = db_before["dataCleaned"]
        collection_after = db_after["dataCleaned"]

        bev_count_before = collection_before.count_documents({"Year": year, "Type": "Battery Electric Vehicle (BEV)"})
        phev_count_before = collection_before.count_documents({"Year": year, "Type": "Plug-in Hybrid Electric Vehicle (PHEV)"})
        bev_count_after = collection_after.count_documents({"Year": year, "Type": "Battery Electric Vehicle (BEV)"})
        phev_count_after = collection_after.count_documents({"Year": year, "Type": "Plug-in Hybrid Electric Vehicle (PHEV)"})

        bev_count = bev_count_before + bev_count_after
        phev_count = phev_count_before + phev_count_after

        data.append({"year": year, "BEV": bev_count, "PHEV": phev_count})

    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)