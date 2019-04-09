
def split_string_at_char(string, char):
    """
    Splits a given string at the given char and returns both ends
    :param string: String that is supposed to be splitted
    :param char: The char that triggers the split
    :return: (string before the char, string after the char)
    """
    index = string.find(char)
    return string[:index], string[index + 1:]
