from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from models import db, Rule
from rules import create_rule, combine_rules, evaluate_rule

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///rules.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
migrate = Migrate(app, db)

with app.app_context():
    db.create_all()

class Rule(db.Model):
    __tablename__ = 'rule'  # Optional, can help avoid conflicts
    id = db.Column(db.Integer, primary_key=True)
    rule_string = db.Column(db.String, nullable=False)

    __table_args__ = {'extend_existing': True}

@app.route('/rules', methods=['GET'])
def get_rules():
    rules = Rule.query.all()  # Fetch all rules from the database
    return jsonify([{'id': rule.id, 'rule_string': rule.rule_string} for rule in rules]), 200

def evaluate_rule_logic(rule_string, user_data):
    # Basic example of evaluation logic
    if rule_string == "((age > 30 AND department = 'Sales'))":
        return user_data["age"] > 30 and user_data["department"] == 'Sales'
    
    return False  # Default return value for unhandled rules


@app.route('/create_rule', methods=['POST'])
def create_rule_endpoint():
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

@app.route('/test', methods=['GET'])
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
    try:
        rule_id = request.json.get('rule_id')
        user_data = request.json.get('data')

        if not rule_id or not user_data:
            return jsonify({"error": "Rule ID and user data are required."}), 400

        rule = Rule.query.get(rule_id)
        if not rule:
            return jsonify({"error": "Rule not found."}), 404

        # Call the evaluation logic with the rule and user data
        result = evaluate_rule_logic(rule.rule_string, user_data)

        return jsonify({"result": result}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
