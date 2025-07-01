# Python Generators Project

This project demonstrates various uses of Python generators for database operations.

## Files

1. `seed.py` - Sets up the MySQL database and populates it with sample data
2. `0-stream_users.py` - Streams users one by one from the database
3. `1-batch_processing.py` - Processes users in batches and filters by age
4. `2-lazy_paginate.py` - Implements lazy pagination of user data
5. `4-stream_ages.py` - Calculates average age using memory-efficient generators

## Requirements

- Python 3.x
- MySQL server
- mysql-connector-python package

## Setup

1. Run `seed.py` to create and populate the database
2. Execute the other scripts to see the generators in action
