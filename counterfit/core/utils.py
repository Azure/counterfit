# Utility functions should live here so can be used across codebase...

def parse_special_string_w_eval(input_str):
    # This function accepts input string and returns list of elements
    if len(input_str) < 2:
        return '{input_str} must be of at least of length 2'
    if input_str[0] == '`' and input_str[-1] == '`':
        return eval(input_str[1:-1])
    else:
        return '{input_str} should be prefixed and suffixed with special character "`"'
