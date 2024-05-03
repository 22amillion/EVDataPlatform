# Electric Vehicle Data Platform

## What's This All About?

Welcome to the electric vehicle (EV) data platform! Our platform explores the complexities of managing, analyzing, and visualizing EV data. Designed with care by a team of tech experts, data pros, and environmental enthusiasts, we're here to make sense of the numbers and trends that define the electric vehicle landscape.

## Architecture Design

![Architecture Design](static/images/design.png)

## Key Features

### MongoDB for Data Management

- **Why MongoDB?** It is scalable, powerful, and good at handling large amounts of data, making it our chosen database for storing and organizing EV data.
- **Smart Data Storage**: Unique identifiers are assigned to each record via a hash function, optimizing data retrieval and storage efficiency.

### Real-Time Data Processing with Spark DataFrame

- **Fast Data Processing**: Using Spark DataFrame, we transform and analyze data in real-time, quickly extracting valuable features.
- **Efficient Computations**: Thanks to Spark's distributed nature, we process vast datasets efficiently, ensuring timely analytics.

### Interactive Web Application

- **Dual Interfaces**: Tailored experiences for both casual users and database managers.
- **Lookup Page**: Explore and interact with EV data through advanced search and aggregation tools.
- **Visualization Page**: Engage with data through interactive visualizations that make trends easy to understand.
- **Database Manager’s Interface**: Direct database interactions via a Python-powered backend for precise control over data operations.

## Wrapping Up

By integrating technologies such as PySpark, Flask, MongoDB, and JavaScript, our platform serves as a powerful tool for stakeholders across the EV spectrum.

### Thank You!

We appreciate your interest in our project. Your feedback and contributions are welcome as we continue to refine and expand our platform.