# utils.py
def validate_user_attributes(attributes):
    required_keys = ['age', 'department', 'income', 'spend']
    
    # Check if all required keys are present
    if not all(key in attributes for key in required_keys):
        return False

    # Validate that income and spend are numbers
    if not isinstance(attributes['income'], (int, float)):
        raise ValueError("income should be a number")
    if not isinstance(attributes['spend'], (int, float)):
        raise ValueError("spend should be a number")
    
    return True
