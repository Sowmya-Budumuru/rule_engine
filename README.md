# rule_engine application

## Description
The Rule Engine Application is a flexible tool designed to evaluate user eligibility based on various attributes such as age, department, income, and spending. It allows users to create rules using logical expressions and assess whether specific user attributes meet those conditions. The rule engine supports the dynamic creation, combination, and evaluation of rules.

## Project Structure:
The project structure is organized as follows:

rule-engine-app/  
├── app.py             # Main entry point for the application  
├── models.py          # Database models and ORM configuration  
├── rules.py           # Rule processing logic  
├── config.py          # Configuration settings for the application  
├── templates/         # HTML templates for the UI  
├── static/            # Static files (CSS, JavaScript)  
├── requirements.txt   # List of dependencies  
├── README.md          # Project documentation  
└── .env               # Environment variables (not included in version control)  

## Prerequisites
Before we begin, we should have the following installed on our system:

1. **Python 3.x**: Download it from [python.org](https://www.python.org/downloads/).
2. **pip**: This is the package installer for Python.
3. SQLite (included with Python by default)
4. pip for managing Python packages
5. Basic understanding of Flask and SQLAlchemy

## Features
- **Rule Creation** : Define rules using logical expressions (e.g., "age > 18 and income < 50000").
- **Attribute Evaluation** : Evaluate user attributes against defined rules to determine eligibility.
- **Customizable Logic** : Create rules based on different criteria, enhancing flexibility for various use cases.
- **Error Handling** : Basic error handling for invalid input or rule syntax errors.

## Folder Structure and Files
rule_engine/
    **app.py** : Main Flask application file.      
    **models.py** : Defines the database schema and models.  
    **rules.py** : Contains functions for creating and evaluating rules.

## Rule Engine Functionality
    **create_rule(rule_string)** : Parses a rule string and generates an AST.
    **combine_rules(rules)** : Combines multiple rules into a single AST.
    **evaluate_rule(json_data)** : Evaluates the combined rule against the provided data.

# Usage:
## Rule Creation : 
**Define a Rule** : Rules are created with conditional expressions based on user attributes such as age, department, income, and spend.

Rule Format:

Rules are represented using a JSON-like structure.  
The rule logic uses operators like ==, >, <, AND, OR, etc.  

Example rule:  
{
    "condition": "AND",    
    "rules": [
        {
            "field": "age",
            "operator": ">",
            "value": 30
        },
        {
            "field": "income",
            "operator": ">=",
            "value": 50000
        }
    ]
}

## Evaluating a Rule
To evaluate a rule, pass the user attributes to the evaluation endpoint. The rule engine will parse the AST representation of the rule and determine if the user meets the conditions.

Example:

{
    "age": 35,
    "department": "Engineering",
    "income": 60000,
    "spend": 15000
}

## Using the API
**API Endpoints** :   
**Create Rule** :  
URL: /api/rules   
Method: POST  
Description: Creates a new rule.  
Request Body: JSON object with rule definition.  

**Get All Rules**:  
URL: /api/rules  
Method: GET  
Description: Retrieves all existing rules.  

**Evaluate Rule**:  
URL: /api/rules/evaluate  
Method: POST  
Description: Evaluates a rule against the given user attributes.  
Request Body: JSON object with user attributes. 

**Delete Rule** :  
URL: /api/rules/<rule_id>  
Method: DELETE  
Description: Deletes a specific rule by ID.  

## Extending the Application
**Adding New Conditions** : To support additional fields or conditions, update the rule parsing logic in rules.py to include the new operators and fields.

**Improving the UI** : The UI templates can be enhanced using modern front-end libraries such as React or Vue.js for a more interactive user experience.

## Database Setup: SQLite
The rule engine application uses SQLite, a lightweight, file-based relational database system. SQLite is well-suited for development and testing environments due to its simplicity and ease of setup. The database is stored in a single file (rules.db), making it easy to manage and transport. SQLite is ideal for smaller projects or embedded applications where a full-fledged database server like PostgreSQL might not be necessary. For larger-scale production environments, switching to a more robust database system would be advisable.

## Testing:
  Verified individual rule creation and AST representation.
  Combined rules to ensure the AST reflects the combined logic.
  Evaluated rules using various sample data scenarios.

## Running the application:
  **Install dependencies** : pip install -r requirements.txt
  **Set up the database** : SQLALCHEMY_DATABASE_URI = 'sqlite:///rules.db'
  **Run migrations** : flask db upgrade
  **Start the Flask development server** : flask run  {#output: * Running on http://127.0.0.1:5000}

## Deployment  
**Docker** : Use a Dockerfile to containerize the application for easy deployment.  
**Cloud Services** : Deploy using services like AWS, Google Cloud, or Azure.  
**Web Server Configuration** : Use Nginx or Apache as a reverse proxy with Gunicorn for production deployment.  
  

## Security Measures:  
**Input Validation** : The application performs validation on user inputs to prevent invalid data entry.  
**Data Protection** : Sensitive information is handled securely, and proper authentication should be considered if this application is used in a web environment.  

## Performance Optimizations:
**Efficient Rule Evaluation** : The rule engine is optimized for quick evaluations by using efficient algorithms to parse and assess rules against user attributes.  
**Caching** : Frequently evaluated rules can be cached to improve performance during repeated assessments.



