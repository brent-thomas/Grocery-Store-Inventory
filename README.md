# Grocery Inventory Management System

## Overview
The Grocery Inventory Management System is a Python-based application designed for managing grocery product inventories. It provides functionalities such as viewing product details, adding new products, analyzing inventory data, and backing up inventory information. This application is ideal for small to medium-sized grocery stores looking to digitize their inventory management process.

## Features
- **View Product Details**: Browse through product details including name, price, quantity, update date, and associated brand.
- **Add New Products**: Easily add new products to the inventory with their respective details.
- **Inventory Analysis**: Perform an analysis to identify the most and least expensive products and the brand with the most inventory.
- **Backup Database**: Create backups of the inventory data in CSV format, ensuring data safety and portability.

## How to Use
1. **Start the Application**: Run the application to initialize the database and load initial data.
2. **Navigate through Menu**: Use the main menu to navigate to different functionalities:
   - `V`: View Product Details
   - `N`: Add a New Product
   - `A`: View Inventory Analysis
   - `B`: Backup Database
   - `X`: Exit the Application
3. **Follow Prompts**: Each functionality provides prompts to guide you through the process. Enter the requested information or make a selection as needed.
4. **View or Update Data**: View product details, add new products, or get insights from the inventory analysis.
5. **Backup Your Data**: Regularly backup your database to CSV files for safekeeping.

## Technical Details
- Built with Python.
- Uses SQLAlchemy for database interactions.
- Leverages CSV for data backup and restoration.
- Customizable and extendable for additional features.

## Dependencies
- SQLAlchemy
- Python's CSV module
