# tests/test_rules.py
import pytest
from app import app, db, Rule

@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        # Create the database and the tables before each test
        with app.app_context():
            db.create_all()
        yield client
        # Drop the database after each test
        with app.app_context():
            db.drop_all()

def test_create_rule(client):
    response = client.post('/api/rules', json={
        "name": "Test Rule",
        "conditions": "age > 18"
    })
    assert response.status_code == 200
    assert response.json["message"] == "Rule created successfully"

    # Check if the rule is actually created in the database
    rule = Rule.query.first()
    assert rule is not None
    assert rule.name == "Test Rule"
    assert rule.conditions == "age > 18"

def test_evaluate_rule_valid(client):
    # Create a rule first
    client.post('/api/rules', json={
        "name": "Age Rule",
        "conditions": "age > 18"
    })

    # Test evaluation with valid attributes
    response = client.post('/api/evaluate', json={
        "age": 25,
        "department": "Sales",
        "income": 50000,
        "spend": 2000
    })
    assert response.status_code == 200
    assert response.json["result"] == "Rule evaluated successfully"
    assert response.json["attributes"] == {
        "age": 25,
        "department": "Sales",
        "income": 50000,
        "spend": 2000
    }

def test_evaluate_rule_invalid(client):
    # Create a rule first
    client.post('/api/rules', json={
        "name": "Age Rule",
        "conditions": "age > 18"
    })

    # Test evaluation with missing attributes
    response = client.post('/api/evaluate', json={
        "age": 25,
        "department": "Sales"
        # Missing 'income' and 'spend'
    })
    assert response.status_code == 400
    assert response.json["error"] == "Invalid attributes"

def test_evaluate_rule_invalid_data_type(client):
    # Create a rule first
    client.post('/api/rules', json={
        "name": "Age Rule",
        "conditions": "age > 18"
    })

    # Test evaluation with invalid data types
    response = client.post('/api/evaluate', json={
        "age": "twenty-five",  # Invalid data type
        "department": "Sales",
        "income": "fifty thousand",  # Invalid data type
        "spend": 2000
    })
    assert response.status_code == 400
    assert response.json["error"] == "income should be a number" or response.json["error"] == "spend should be a number"
