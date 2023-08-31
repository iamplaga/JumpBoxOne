import os
import subprocess

def install_kibana(version="8.9.1"):
    try:
        # Download Kibana Debian package and its SHA512 checksum
        package_url = f"https://artifacts.elastic.co/downloads/kibana/kibana-{version}-amd64.deb"
        checksum_url = f"{package_url}.sha512"
        package_filename = f"kibana-{version}-amd64.deb"

        # Create the ElasticStackBox directory if it doesn't exist
        elasticstack_box_dir = os.path.join(os.getcwd(), "JumpBoxOne", "ElasticStackBox")
        os.makedirs(elasticstack_box_dir, exist_ok=True)

        # Download the package and checksum files
        subprocess.run(["wget", package_url])
        subprocess.run(["wget", checksum_url])

        # Verify the checksum
        subprocess.run(["shasum", "-a", "512", "-c", f"{package_filename}.sha512"], check=True)

        # Install Kibana using dpkg
        subprocess.run(["sudo", "dpkg", "-i", package_filename], check=True)

        # Save Kibana configuration to kibanabox.txt
        kibana_config = f"Kibana version: {version}\n"
        kibana_config += f"Kibana installation path: /usr/share/kibana\n"
        kibana_config += f"Kibana configuration file: /etc/kibana/kibana.yml\n"
        
        kibanabox_file_path = os.path.join(elasticstack_box_dir, "kibanabox.txt")
        with open(kibanabox_file_path, 'w') as kibanabox_file:
            kibanabox_file.write(kibana_config)

        print(f"Kibana {version} installed successfully.")
        print(f"Kibana configuration saved to {kibanabox_file_path}")
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
    finally:
        # Clean up downloaded files
        subprocess.run(["rm", package_filename, f"{package_filename}.sha512"])

if __name__ == "__main__":
    install_kibana()
