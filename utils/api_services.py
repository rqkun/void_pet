from io import BytesIO
import lzma
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
    

def decompress_lzma(data):
    results = []
    while True:
        decomp = lzma.LZMADecompressor(lzma.FORMAT_AUTO, None, None)
        try:
            res = decomp.decompress(data)
        except lzma.LZMAError:
            if results:
                break  # Leftover data is not a valid LZMA/XZ stream; ignore it.
            else:
                raise  # Error on the first iteration; bail out.
        results.append(res)
        data = decomp.unused_data
        if not data:
            break
        if not decomp.eof:
            raise lzma.LZMAError("Compressed data ended before the end-of-stream marker was reached")
    return b"".join(results)
import streamlit as st
@st.cache_data(ttl="30d",show_spinner=False)
def get_manifest():
    """API request to get export manifest."""
    request_ref = "https://origin.warframe.com/PublicExport/index_en.txt.lzma"
    request_object = requests.get(request_ref)
    raise_detailed_error(request_object)
    try:
        decompressed_data = lzma.decompress(request_object.content)
        decompressed_data = decompress_lzma(request_object.content)
        manifest_list = decompressed_data.decode("utf-8")
        for item in manifest_list.split("\r\n"):
            if 'ExportManifest' in item:
                return item
        return None # backup
    except lzma.LZMAError as e:
        raise ValueError(f"Failed to decompress the LZMA file: {e}")