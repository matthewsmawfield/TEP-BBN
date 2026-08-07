import urllib.request
from pathlib import Path

def download_models():
    script_dir = Path(__file__).parent
    project_root = script_dir.parent.parent
    dest_dir = project_root / 'data' / 'literature_components'
    dest_dir.mkdir(parents=True, exist_ok=True)
    
    models = ['model_3a.26', 'model_5a.26', 'model_6a.26']
    base_url = "https://raw.githubusercontent.com/ezavarygin/q1009p2956/master/vpfit/"
    
    for m in models:
        model_dir = m.replace('.26', '')
        url = f"{base_url}{model_dir}/{m}"
        dest_path = dest_dir / m
        print(f"Downloading {m} from {url}...")
        try:
            urllib.request.urlretrieve(url, dest_path)
            print(f"Saved to {dest_path}")
        except Exception as e:
            print(f"Failed to download {m}: {e}")

if __name__ == '__main__':
    download_models()
