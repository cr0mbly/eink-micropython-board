

def convert_fields_query_params(path, query_parameters):
    """
    :param path: path of the current url
    :param query_parameters: dict containing query keys and values
    :return: built query url
    """
    return path + '?' + '&'.join('%s=%s' % (key, value) for key, value in query_parameters.items())



