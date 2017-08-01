import json 

def encode_data(data_tuple):
    string_tuple = tuple( str(data) for data in data_tuple )
    json_tuple = json.dumps(string_tuple)
    encoded_tuple = json_tuple.encode()

    return encoded_tuple

