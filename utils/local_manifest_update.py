import re
import requests
import json
import lzma

import urllib

def get_manifest():
    """ Getting manifest files from the zip file.

    Raises:
        ValueError: lzma failed to decompress the index zip file.

    Returns:
        List: A list of export.json and their hash position.
    """
    request_ref = "https://origin.warframe.com/PublicExport/index_en.txt.lzma"
    request_object = requests.get(request_ref)
    try:
        decompressed_data = lzma.decompress(request_object.content)
        manifest_list = decompressed_data.decode("utf-8", errors='ignore')
        # for item in manifest_list.split("\r\n"):
        #     write_manifest(item)
        return manifest_list.split("\r\n")
    except lzma.LZMAError as e:
        raise ValueError(f"Failed to decompress the LZMA file: {e}")

def write_manifest(file):
    """ Save a json file.

    Args:
        file (json): export data from the Warframe's PublicExport endpoint.
    """
    try:
        # Fetch the data from the URL
        encoded_name = urllib.parse.quote(file, safe="")
        url = f"http://content.warframe.com/PublicExport/Manifest/{encoded_name}"
        
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for HTTP issues

        # Clean the JSON string to remove invalid control characters
        cleaned_json = re.sub(r'[\x00-\x1f\x7f]', '', response.text)

        # Parse the JSON data
        data = json.loads(cleaned_json)
        if ".json" in file:
            file = file.split(".json")[0] + ".json"
        
        # Save the JSON data to a file
        output_path = f"./config/data/{file}"
        with open(output_path, "w", encoding="utf-8") as output_file:
            json.dump(data, output_file, indent=4)
        
        print(f"JSON data successfully saved to {file}")
    except requests.exceptions.RequestException as e:
        print(f"An error occurred while fetching the JSON: {e}")
    except json.JSONDecodeError:
        print("Failed to decode JSON from the response.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":

    file_list = get_manifest()
    for item in file_list:
        item = item.replace(" ","")
        write_manifest(item)
    