import requests

# URLs for the files
deploy_url = 'https://raw.githubusercontent.com/chuanqi305/MobileNet-SSD/master/deploy.prototxt'
caffemodel_url = 'https://github.com/chuanqi305/MobileNet-SSD/blob/master/mobilenet_iter_73000.caffemodel?raw=true'

# Local paths where you want to save the files
deploy_file_path = 'deploy.prototxt'
caffemodel_file_path = 'mobilenet_iter_73000.caffemodel'

def download_file(url, file_path):
    """Download a file from the given URL and save it to the specified path."""
    response = requests.get(url)
    if response.status_code == 200:
        with open(file_path, 'wb') as f:
            f.write(response.content)
        print(f"Downloaded: {file_path}")
    else:
        print(f"Failed to download {file_path}")

# Download the files
download_file(deploy_url, deploy_file_path)
download_file(caffemodel_url, caffemodel_file_path)
