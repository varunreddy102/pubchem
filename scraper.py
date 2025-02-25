import requests
import os
import time

def download_json(compound_id):
    """Download JSON data for a given compound ID from PubChem."""
    url = f"https://pubchem.ncbi.nlm.nih.gov/rest/pug_view/data/compound/{compound_id}/JSON/?response_type=save&response_basename=COMPOUND_CID_{compound_id}"
    
    save_dir = os.path.join(os.getcwd(), "data")  # Save in "data/" folder
    os.makedirs(save_dir, exist_ok=True)  # Ensure folder exists
    save_path = os.path.join(save_dir, f"COMPOUND_CID_{compound_id}.json")

    try:
        response = requests.get(url, timeout=10)

        if response.status_code == 200:
            with open(save_path, 'wb') as file:
                file.write(response.content)
            print(f"✅ Downloaded: {save_path}")
            return True
        elif response.status_code == 404:
            print(f"⚠️ Skipping CID {compound_id}, not found (404).")
            return True  # Skip to the next ID without retrying
        else:
            print(f"❌ Failed to download CID {compound_id}. HTTP Status Code: {response.status_code}")
            return False

    except requests.RequestException as e:
        print(f"❌ Request failed for CID {compound_id}: {e}")
        return False

def main():
    """Loop through compound IDs, retrying after failures."""
    start_cid = 60001
    end_cid = 100001  # Reduced for testing; increase as needed

    while start_cid < end_cid:
        success = download_json(start_cid)
        
        if success:
            start_cid += 1  # Move to the next ID only if successful
        else:
            print("⏳ Waiting for 1 minute before retrying...")
            time.sleep(120)  # Wait for 1 minute before retrying the same ID

if __name__ == "__main__":
    main()
