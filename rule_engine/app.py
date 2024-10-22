from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from utils import validate_user_attributes
from models import db, Rule
from rules import create_rule, combine_rules, evaluate_rule
import logging

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///rules.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#db = SQLAlchemy(app)
db.init_app(app)
migrate = Migrate(app, db)

with app.app_context():
    db.create_all()

@app.errorhandler(Exception)
def handle_exception(e):
    app.logger.error(f"Unhandled Exception: {str(e)}")  # Log the error
    return jsonify({"error": "Internal Server Error", "details": str(e)}), 500


class Rule(db.Model):
    __tablename__ = 'rule'  # Optional, can help avoid conflicts
    id = db.Column(db.Integer, primary_key=True)
    rule_string = db.Column(db.String, nullable=False)

    __table_args__ = {'extend_existing': True}

@app.route('/rules', methods=['GET'])
def get_rules():
    rules = Rule.query.all()  # Fetch all rules from the database
    return jsonify([{'id': rule.id, 'rule_string': rule.rule_string} for rule in rules]), 200

def evaluate_rule(user_data, conditions):
    age = user_data.get('age')
    
    # Ensure age is a number and handle evaluation logic
    if conditions == "age > 18":
        if isinstance(age, (int, float)):  # Check if age is numeric
            return {"result": "User is eligible" if age > 18 else "User is not eligible"}
        else:
            raise ValueError("Age must be a number.")
    # Additional conditions can be added here
    return {"result": "No valid condition matched."}

@app.route('/create_rule', methods=['POST'])
def create_rule_endpoint():
    data = request.json
    new_rule = Rule(name=data['name'], conditions=data['conditions'])
    db.session.add(new_rule)
    db.session.commit()
    try:
        rule_string = request.json.get('rule_string')
        if not rule_string:
            return jsonify({"error": "Rule string is required."}), 400
        
        # Validate rule string format (basic validation)
        if ">" not in rule_string and "<" not in rule_string:
            return jsonify({"error": "Invalid rule string."}), 400

        new_rule = Rule(rule_string=rule_string)
        db.session.add(new_rule)
        db.session.commit()
        return jsonify({"message": "Rule created", "id": new_rule.id}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/', methods=['GET'])
def test():
    return "Test Endpoint is working!"

@app.route('/combine_rules', methods=['POST'])
def combine_rules_endpoint():
    try:
        rules = request.json.get('rules')
        if not rules:
            return jsonify({"error": "Rules are required."}), 400

        combined_ast = combine_rules(rules)
        return jsonify({"combined_ast": combined_ast}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/evaluate_rule', methods=['POST'])
def evaluate_rule():
    user_data = request.json
    app.logger.info(f"Received user data: {user_data}")  # Log the input data

    # Check if Rule ID and user data are provided
    rule_id = user_data.get("rule_id")
    if not rule_id or not user_data:
        return jsonify({"error": "Rule ID and user data are required."}), 400

    # Fetch the rule from the database using the Rule ID
    rule = Rule.query.get(rule_id)
    if not rule:
        return jsonify({"error": "Rule not found."}), 404

    try:
        # Evaluate the rule using the user attributes
        result = evaluate_rule(user_data, rule.conditions)
        return jsonify(result)
    except Exception as e:
        app.logger.error(f"Error during rule evaluation: {str(e)}")  # Log the error
        return jsonify({"error": "Internal Server Error", "details": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
