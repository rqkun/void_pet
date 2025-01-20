import requests
import json
import lzma

def get_manifest():
    """API request to get export manifest."""
    request_ref = "https://origin.warframe.com/PublicExport/index_en.txt.lzma"
    request_object = requests.get(request_ref)
    try:
        decompressed_data = lzma.decompress(request_object.content)
        manifest_list = decompressed_data.decode("utf-8", errors='ignore')
        for item in manifest_list.split("\r\n"):
            if 'ExportManifest' in item:
                return item
        return ""
    except lzma.LZMAError as e:
        raise ValueError(f"Failed to decompress the LZMA file: {e}")
    
if __name__ == "__main__":

    file = get_manifest()
    # URL of the JSON file
    url = f"http://content.warframe.com/PublicExport/Manifest/{file}"

    # File to save the JSON data
    output_file = "./config/manifest.json"

    try:
        # Fetch the data from the URL
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for HTTP issues
        
        # Parse the JSON data
        data = response.json()
        
        # Save the JSON data to a file
        with open(output_file, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4)
        
        print(f"JSON data successfully saved to {output_file}")
    except requests.exceptions.RequestException as e:
        print(f"An error occurred while fetching the JSON: {e}")
    except json.JSONDecodeError:
        print("Failed to decode JSON from the response.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")