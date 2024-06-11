# FastAPI Vending Machine API

This is a simple FastAPI application that simulates a Vending Machine API.

## Running the Application

Follow these steps to run the application on your local machine:

1. **Install Python**: If you don't already have Python installed, download and install Python from [python.org](https://www.python.org/).

2. **Clone the Repository**: Clone this repository to your computer using Git:

   ```bash
   git clone https://github.com/HFenda/VendingMachineProject

3. **Navigate to the Project Directory**: Open a terminal and change your directory to the cloned repository:
   ```bash
    cd VendingMachineProject

4. **Install Dependencies**: Install project dependencies using Poetry:

   ```bash
   poetry install
5. **Run the Application**: Start the FastAPI application using Uvicorn:

   ```bash
   poetry run uvicorn main:app --reload
6. **Access the API**: Once the application is running, you can access the API at http://localhost:8000 in your web browser or through API testing tools like Postman.