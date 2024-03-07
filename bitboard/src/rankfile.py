# Converts an (x, y) location to chess rank-file notation
# Ex: to_rank_file(0, 1) = A2

def to_rank_file(x, y):
    return_string = ""
    return_string += chr(x + 65)
    return_string += str(y + 1)
    return return_string
