from datetime import datetime
from django import template

register = template.Library()

L2L_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


@register.filter
def l2l_dt(value):
    dt_obj = None

    # The goal here is to take a variable type input and get it into one type so that it can be reformated
    if isinstance(value, str):
        try:
            dt_obj = datetime.fromisoformat(value)
        except ValueError:
            # The string is not in a recognized ISO format
            return f"bad string input: '{value}' is not a valid ISO format"
        except Exception as e:
            # Catch other potential unexpected errors during parsing
            return f"unexpected error processing string '{value}': {e}"
    elif isinstance(value, datetime):
        dt_obj = value
    else:
        return (
            f"bad input type: expected string or datetime, got {type(value).__name__}"
        )

    if dt_obj:
        try:
            return dt_obj.strftime(L2L_DATE_FORMAT)
        except Exception as e:
            return f"error formatting datetime object: {e}"

    # This path should ideally not be reached if the logic above is complete
    return "processing failed to produce a datetime object"
