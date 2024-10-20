# rule_engine application

## Description
The Rule Engine Application is a flexible tool designed to evaluate user eligibility based on various attributes such as age, department, income, and spending. It allows users to create rules using logical expressions and assess whether specific user attributes meet those conditions. The rule engine supports the dynamic creation, combination, and evaluation of rules.

### Prerequisites
Before we begin, we should have the following installed on our system:

1. **Python 3.x**: Download it from [python.org](https://www.python.org/downloads/).
2. **pip**: This is the package installer for Python.

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
**Create a Rule**
  from rules import create_rule

# Create a new rule
rule = create_rule("age > 18 and income < 50000")

**Evaluate a Rule**
from rules import evaluate_rule

# Define user attributes
user_attributes = {
    'age': 20,
    'income': 30000,
    'department': 'Finance',
    'spend': 1000
}

# Evaluate the rule
result = evaluate_rule(user_attributes)

print("Eligibility:", result)  # Output: Eligibility: True or False

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
  

## Security Measures:
**Input Validation** : The application performs validation on user inputs to prevent invalid data entry.
**Data Protection** : Sensitive information is handled securely, and proper authentication should be considered if this application is used in a web environment.

## Performance Optimizations:
**Efficient Rule Evaluation** : The rule engine is optimized for quick evaluations by using efficient algorithms to parse and assess rules against user attributes.
**Caching** : Frequently evaluated rules can be cached to improve performance during repeated assessments.



