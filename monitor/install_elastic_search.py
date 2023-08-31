import os
import subprocess
import getpass


''' 1ST Install this program 1st, STACK HAS TO BE
 in order so do not rearrange the calls'''


def install_elasticsearch(version="8.9.1"):
    # Download Elasticsearch Debian package and its SHA512 checksum
    package_url = f"https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-{version}-amd64.deb"
    checksum_url = f"{package_url}.sha512"
    package_filename = f"elasticsearch-{version}-amd64.deb"

    try:
        # Download the package and checksum files
        subprocess.run(["wget", package_url])
        subprocess.run(["wget", checksum_url])
        
        # Verify the checksum
        subprocess.run(["shasum", "-a", "512", "-c", f"{package_filename}.sha512"], check=True)
        
        # Install Elasticsearch using dpkg
        subprocess.run(["sudo", "dpkg", "-i", package_filename], check=True)
        
        print(f"Elasticsearch {version} installed successfully.")
        
        # Inform the user to save important information
        print("IMPORTANT: Please save any passwords or keys provided during Elasticsearch installation.")
        print("You will be asked to enter this information if you chose to add this password to your PATH for ease of use.")
        input("Press Enter to continue...")  # Wait for user confirmation
        
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
    finally:
        # Clean up downloaded files
        subprocess.run(["rm", package_filename, f"{package_filename}.sha512"])




if __name__ == "__main__":
    # Step 1: Install Elasticsearch
    install_elasticsearch()

   
