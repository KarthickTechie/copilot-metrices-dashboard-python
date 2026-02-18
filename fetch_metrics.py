import os
import requests
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configuration
GITHUB_TOKEN = os.getenv("YOUR_GITHUB_TOKEN")
ORG_NAME = "sysarc-svn"  # Replace with your organization name if different
API_URL = f"https://api.github.com/orgs/{ORG_NAME}/copilot/metrics/reports/organization-28-day/latest"

def fetch_copilot_metrics():
    """
    Fetch GitHub Copilot metrics from the API and save to local JSON file.
    """
    print("🔍 Fetching GitHub Copilot metrics...")
    
    # Set up headers
    headers = {
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28"
    }
    
    try:
        # Make API request to get download links
        print(f"📡 Requesting metrics from: {API_URL}")
        response = requests.get(API_URL, headers=headers)
        response.raise_for_status()
        
        data = response.json()
        print(f"✅ Successfully retrieved report metadata")
        print(f"📅 Report period: {data['report_start_day']} to {data['report_end_day']}")
        
        # Get the download link
        download_links = data.get("download_links", [])
        if not download_links:
            print("❌ No download links found in response")
            return False
        
        download_url = download_links[0]
        print(f"📥 Downloading metrics data from Azure...")
        
        # Download the actual metrics data
        metrics_response = requests.get(download_url)
        metrics_response.raise_for_status()
        
        metrics_data = metrics_response.json()
        
        # Save to local file
        output_file = "copilot_metrices.json"
        with open(output_file, "w") as f:
            json.dump(metrics_data, f, indent=2)
        
        print(f"✅ Successfully saved metrics to {output_file}")
        print(f"📊 Total days in report: {len(metrics_data.get('day_totals', []))}")
        
        return True
        
    except requests.exceptions.HTTPError as e:
        print(f"❌ HTTP Error: {e}")
        if e.response.status_code == 401:
            print("💡 Check your GitHub token in .env file")
        elif e.response.status_code == 403:
            print("💡 Token may lack required permissions or no org access")
        elif e.response.status_code == 404:
            print("💡 Organization not found or no Copilot subscription")
        return False
        
    except requests.exceptions.RequestException as e:
        print(f"❌ Request Error: {e}")
        return False
        
    except json.JSONDecodeError as e:
        print(f"❌ JSON Decode Error: {e}")
        return False
        
    except Exception as e:
        print(f"❌ Unexpected Error: {e}")
        return False

if __name__ == "__main__":
    if not GITHUB_TOKEN:
        print("❌ Error: YOUR_GITHUB_TOKEN not found in .env file")
        print("💡 Please create a .env file with YOUR_GITHUB_TOKEN=your_token_here")
    else:
        success = fetch_copilot_metrics()
        if success:
            print("\n🎉 Metrics fetch completed successfully!")
            print("💡 You can now run: streamlit run app.py")
        else:
            print("\n❌ Failed to fetch metrics. Please check the errors above.")
