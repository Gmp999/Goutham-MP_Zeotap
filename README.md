
# Rule Engine with AST

This project is a web-based application that allows users to create, combine, and evaluate rules using Abstract Syntax Trees (AST). The project includes a Python-based backend API and a frontend user interface for interacting with the rule engine.

## Features

- **Create Rules:** Define rules using an AST-based parser and send them to the backend.
- **Combine Rules:** Combine multiple rules into a single rule on the backend.
- **Evaluate Rules:** Submit data to evaluate against the defined rules and get results.

## Technologies Used

### Backend:
- **Python** with `AST` module for parsing and evaluating rules.
- **FastAPI** for creating the RESTful API.

### Frontend:
- **HTML/CSS/JavaScript** for user interaction.
- **Fetch API** for sending requests to the backend.

## Files

### Backend:
- **main.py**: The main Python file containing the FastAPI app and endpoints for rule creation, combination, and evaluation.
- **rule_engine.py**: Contains the core logic for parsing rules using Python's `ast` module and evaluating them.

### Frontend:
- **app.js**: Contains JavaScript functions to handle user input and make API requests to the backend for rule creation, combination, and evaluation【8†source】.
- **style.css**: Styles the frontend user interface, including forms, buttons, and output areas【9†source】.

## Setup Instructions

### Prerequisites:
- Python 3.x
- FastAPI
- Uvicorn
- JavaScript-enabled browser

### Step 1: Install Dependencies
Run the following command to install required Python packages:

```bash
pip install fastapi uvicorn
```

### Step 2: Start the Backend Server
Run the following command to start the FastAPI server:

```bash
uvicorn main:app --reload
```

This will start the server at `http://127.0.0.1:8000`.

### Step 3: Open the Frontend
Open the `index.html` file in your browser to interact with the rule engine.

## Usage

1. **Create Rule:** Enter a rule in the input field and click "Create Rule". This will send a POST request to the backend to create the rule.
2. **Combine Rules:** Click "Combine Rules" to merge all existing rules into one.
3. **Evaluate Rule:** Enter JSON data to evaluate it against the defined rules and see the result.

## Example

1. **Rule:** `x > 10`
2. **Data:** `{ "x": 15 }`
3. **Evaluation Result:** `true`

## Styles
The frontend is styled using a clean and minimal design with form elements, buttons, and an output section. The background uses a gradient effect for a modern look【9†source】.

## License

This project is open-source and available under the MIT License.
```

This `README.md` file explains your project's structure, setup instructions, and usage, helping others understand and run the rule engine system.
