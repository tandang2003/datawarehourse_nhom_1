# Function to flatten nested JSON
def flatten_json(y):
    """Flatten a nested JSON object."""
    out = {}

    def flatten(x, name=''):
        # If the value is a dictionary, recurse into it
        if isinstance(x, dict):
            for a in x:
                flatten(x[a], name + a + '_')
        # If the value is a list, recurse into each item
        elif isinstance(x, list):
            for i, a in enumerate(x):
                flatten(a, name + str(i) + '_')
        else:
            out[name[:-1]] = x  # Remove trailing underscore

    flatten(y)