from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Index


db = SQLAlchemy()

class Rule(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    conditions = db.Column(db.Text, nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "conditions": self.conditions
        }

    def __repr__(self):
        return f'<Rule {self.id}: {self.rule_string}>'

#Index('idx_rule_status', rule.status)