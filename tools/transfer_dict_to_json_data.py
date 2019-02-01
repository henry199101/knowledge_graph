def transfer_dict_to_json_data(a_dict, readable):
    import json

    indent = 8 if readable else 0

    return json.dumps(a_dict, sort_keys=True, indent=indent, separators=(',', ':'), ensure_ascii=False)
    '''
    >>> d
    {'a': 1}
    >>> import json
    >>> r = json.dumps(d)
    >>> r
    '{"a": 1}'
    >>> type(r)
    <class 'str'>
    '''
