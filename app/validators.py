def validate_user (data, partial = False):
    errors = []
    if 'name' not in data or not str(data.get('name', '')).strip():
        errors.append ("Name is required and cannot be blank")
    elif len(str(data['name']).strip()) > 100:
        errors.append ("Name must be 100 characters or fewer")

    if not partial or 'email' in data:
        email = data.get('email', '')
        if not email or '@' not in str (email) or '.' not in str(email).split ('@')[-1]:
            errors.append ("A valid email is required")
    if not partial or 'age' in data:
        if 'age' not in data:
            errors.append ("Age is required")
        else:
            try:
                age = int(data['age'])
                if age < 1 or age >120:
                    errors.append ("Age must be between 1 and 120")
            except (ValueError, TypeError):
                errors.append("Age must be a valid integer")

    return errors

def validate_post (data, partial = False):
    errors = []
    if not partial or 'title' in data:
        if 'title' not in data or not str (data.get('title', '')):
            errors.append ("Title is required and cannot be blank")
        elif len(str(data['title'].strip())) > 200:
            errors.append ("Title must be 200 charcaters or fewer")
    
    

    if not partial or 'body' in data:
        if 'body' not in data or not str (data.get('body', '')):
            errors.append ("Body must not be empty")
        elif len(str(data['body'].strip())) > 200:
            errors.append ("Body must be 200 characters or fewer")
    
    
    if not partial or 'user_id' in data:
        if 'user_id' not in data:
            errors.append ("user_id is required")
        else:
            try:
                user_id = int(data['user_id'])
                if user_id < 1:
                    errors.append ("Invalid user id")
            except:
                errors.append ("User id must be a valid integer")
    return errors