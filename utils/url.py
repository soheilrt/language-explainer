def normalize(url: str) -> str:
    """
    removes // from url
    :param url: string
    :return: string
    """
    return url.replace('//', 'https://')
