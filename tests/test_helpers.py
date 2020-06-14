

def assert_in_error_msg(text: str, e, compare_lowercase: bool = True):
    """

    :param text: Text to search for. Regex not supported.
    :param e: Error Message
    :param compare_lowercase: If true, both the search text and the error message will be converted
    to lowercase before searching.
    :return:
    """
    error_msg: str = e.value.args[0]
    if compare_lowercase:
        error_msg = error_msg.lower()
        text = text.lower()
    assert text in error_msg
