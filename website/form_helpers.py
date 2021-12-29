from datetime import datetime

def _get_form_value(value):
    if value is None:
        return None

    return None if value.strip() == "" else value.strip()


def form_value_to_string(value):
    return _get_form_value(value)


def form_value_to_int(value):
    temp_value = _get_form_value(value)

    try:
        temp_value = int(temp_value)
    except:
        temp_value = None

    return temp_value


def form_value_to_float(value):
    temp_value = _get_form_value(value)

    try:
        temp_value = float(temp_value)
    except:
        temp_value = None

    return temp_value

def form_value_to_bool(value):
    temp_value = _get_form_value(value)

    try:
        temp_value = bool(temp_value)
    except:
        temp_value = None

    return temp_value

def form_value_to_datetime(value):
    temp_value = _get_form_value(value)

    try:
        temp_value = datetime.fromisoformat(temp_value)
    except:
        temp_value = None

    return temp_value
