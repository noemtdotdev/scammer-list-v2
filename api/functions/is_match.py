def is_match(scammer, arguments):
    for key, value in scammer.items():
        if isinstance(value, str) and arguments.lower() in value.lower():
            return True
        elif isinstance(value, list):
            if any(isinstance(item, str) and arguments.lower() in item.lower() for item in value):
                return True
    return False