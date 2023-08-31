import os
import subprocess

def install_elastic_keyring():
    # Download and install the Public Signing Key
    keyring_url = "https://artifacts.elastic.co/GPG-KEY-elasticsearch"
    keyring_path = "/usr/share/keyrings/elastic-keyring.gpg"
    
    try:
        subprocess.run(["wget", "-qO", "-", keyring_url], stdout=subprocess.PIPE)
        subprocess.run(["sudo", "gpg", "--dearmor", "-o", keyring_path], check=True)
        print("Elasticsearch Public Signing Key installed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")

def install_apt_transport_https():
    try:
        # Install the apt-transport-https package
        subprocess.run(["sudo", "apt-get", "install", "-y", "apt-transport-https"], check=True)
        print("apt-transport-https package installed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")

def configure_elastic_repository():
    # Define the repository definition
    repo_definition = (
        "deb [signed-by=/usr/share/keyrings/elastic-keyring.gpg] "
        "https://artifacts.elastic.co/packages/8.x/apt stable main"
    )
    
    try:
        # Save the repository definition to /etc/apt/sources.list.d/elastic-8.x.list
        with open("/etc/apt/sources.list.d/elastic-8.x.list", "w") as repo_file:
            repo_file.write(repo_definition)
        
        print("Elasticsearch repository definition saved successfully.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    # Step 1: Install the Elastic Public Signing Key
    install_elastic_keyring()

    # Step 2: Install the apt-transport-https package
    install_apt_transport_https()

    # Step 3: Configure the Elasticsearch repository
    configure_elastic_repository()

    # Step 4: Update the package repository
    try:
        subprocess.run(["sudo", "apt-get", "update"], check=True)
        print("Package repository updated successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")

    # Step 5: Install Logstash
    try:
        subprocess.run(["sudo", "apt-get", "install", "-y", "logstash"], check=True)
        print("Logstash installed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
