from io import BytesIO
import requests

def raise_detailed_error(request_object):
    """ Get details on http errors.

    Args:
        request_object (json): Json response data.

    Raises:
        requests.exceptions.HTTPError: HTTP error
    """
    try:
        request_object.raise_for_status()
    except requests.exceptions.HTTPError as error:
        raise requests.exceptions.HTTPError(error, request_object.text)
    except requests.exceptions.Timeout as error:
        raise requests.exceptions.Timeout("The request timed out")
    except requests.exceptions.ConnectionError as erro:
        raise requests.exceptions.ConnectionError(error, request_object.text)


def get_image(path) -> bytes:
    """ Getting image for json path to bytes.

    Args:
        path (str): Url of an item.

    Returns:
        bytes: Image bytes.
    """
    try:
        request_object = requests.get(path)
        raise_detailed_error(request_object)
        return BytesIO(request_object.content)
    except requests.exceptions.HTTPError as err:
        return None

    