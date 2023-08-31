import os
import subprocess
import getpass
import sys


from monitor import install_elastic_search
from monitor import install_kibana
from monitor import install_logstash
from monitor import store_elastic_pass
from artwork import display_status
from artwork import display_ascii_header
from backups import perform_rsync_backup
def check_sudo():
    # Check if the script is running with sudo (root) privileges
    if os.geteuid() != 0:
        print("This program requires administrative privileges. Please run it with sudo.")
        sys.exit(1)

# Define the port for which you want to allow access (e.g., 5601 for Kibana)
port = "5601"

# Define the directory and filename for the trusted IP file
trusted_ip_directory = "JumpBoxOne"
trusted_ip_file = "trusted_ip.txt"

 # Construct the full path to the trusted IP file
trusted_ip_path = os.path.join(trusted_ip_directory, trusted_ip_file)

# Define the SSH port
ssh_port = "8019"

# Function to update and upgrade system packages
def update_system():
    print("OK, first lets get your Machine updated...")
    subprocess.run(['sudo', 'apt', 'update'])
    subprocess.run(['sudo', 'apt', 'upgrade', '-y'])
    print( "Done!")

# Function to create or update the trusted IP file
def create_trusted_ip_file():
    # Determine the absolute path of the script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Construct the full path to the 'trusted_ip.txt' file within the 'JumpBoxOne' directory
    trusted_ip_directory = os.path.join(script_dir, "JumpBoxOne")
    trusted_ip_file = "trusted_ip.txt"
    trusted_ip_path = os.path.join(trusted_ip_directory, trusted_ip_file)
    
    # Check if the trusted IP directory exists
    if not os.path.exists(trusted_ip_directory):
        # Directory does not exist; create it
        os.makedirs(trusted_ip_directory)

    # Check if the 'trusted_ip.txt' file exists
    if os.path.exists(trusted_ip_path):
        # File already exists; do nothing
        print(f"Trusted IP file '{trusted_ip_file}' already exists.")
    else:
        # File does not exist; create it
        print(f"Creating trusted IP file '{trusted_ip_file}'...")
        with open(trusted_ip_path, 'w') as ip_file:
            ip_file.write("# Trusted IP Addresses and Subnets\n")
            ip_file.write("# Format: Enter one trusted IP address or subnet per line\n")
            ip_file.write("# Examples:\n")
            ip_file.write("#   192.168.1.100\n")
            ip_file.write("#   10.0.0.0/24\n")
        print(f"Done! '{trusted_ip_file}' created.")

    # Get the user's IP address using 'curl' (ifconfig.me)
    try:
        user_ip = subprocess.check_output(['curl', 'ifconfig.me']).decode('utf-8').strip()
        
        # Append the user's IP address to the trusted IP file
        with open(trusted_ip_path, 'a') as ip_file:
            ip_file.write(f"User's IP address: {user_ip}\n")

        # Optionally, you can print a message to confirm the addition
        print(f"User's IP address ({user_ip}) added to trusted IP file.")
    except subprocess.CalledProcessError as e:
        # Handle any errors that may occur when fetching the user's IP address
        print("Failed to fetch the user's IP address. The IP address will not be added to the trusted IP file.")

# Function to secure SSH configuration
def secure_ssh():
    print("SSH is a common attack surface, lets remove that. Nope, no password logins here...")
    # Disable password-based authentication
    with open('/etc/ssh/sshd_config', 'a') as ssh_config:
        ssh_config.write("\nPasswordAuthentication no\n")
        ssh_config.write("PermitRootLogin no\n")
    # Restart SSH service ********************************************
    subprocess.run(['sudo', 'systemctl', 'restart', 'ssh'])
    print(" Done!")

# Function to set up firewall rules
def configure_firewall():
   
    
    print("Configuring firewall rules...")
    
    # Check if the trusted IP file exists
    if os.path.exists(trusted_ip_path):
        # Read trusted IP addresses from the file
        with open(trusted_ip_path, 'r') as ip_file:
            trusted_ips = [line.strip() for line in ip_file.readlines() if line.strip()]  # Read non-empty lines
    
        # Create rules to allow SSH from localhost and trusted IP addresses on port ssh_port
        allowed_ips = ["127.0.0.1"] + trusted_ips
        for ip in allowed_ips:
            subprocess.run(['sudo', 'ufw', 'allow', 'from', ip, 'to', 'any', 'port', ssh_port])
            print(f"Access to port {ssh_port} allowed from {ip}.")
        # Delete existing SSH rules for port 22
        subprocess.run(['sudo', 'ufw', 'delete', 'allow', '22'])
        
        # Change SSH port to ssh_port
        subprocess.run(['sudo', 'sed', '-i', f's/^Port 22$/Port {ssh_port}/', '/etc/ssh/sshd_config'])
        
        # Restart SSH service ********************************* Restart here to avoid disconect until insall completes
        subprocess.run(['sudo', 'systemctl', 'restart', 'ssh'])
        
        # Enable the firewall
        subprocess.run(['sudo', 'ufw', 'enable'])
        
        # Allow communication with necessary programs (add more rules as needed)
        # Example: Allow incoming traffic to port 1234
        subprocess.run(['sudo', 'ufw', 'allow', '5601', '8019', '9200', '5044'])
        
        print("Done! Firewall rules configured based on trusted IP addresses. SSH port changed to", ssh_port)
    else:
        print("Error - Trusted IP file not found.")


# Function to generate an SSH key pair for the current user
def generate_ssh_key():
    # Get the current user's username
    current_user = getpass.getuser()
    
    print(f"Generating SSH key pair for user {current_user}...")
    
    # Define the path where the SSH key pair will be saved
    ssh_key_dir = f"/home/{current_user}/.ssh"
    ssh_key_path = f"{ssh_key_dir}/id_rsa"
    
    # Check if the .ssh directory exists, and if not, create it
    if not os.path.exists(ssh_key_dir):
        os.makedirs(ssh_key_dir)
    
    # Generate the SSH key pair without a passphrase (you can add one if needed)
    subprocess.run(['ssh-keygen', '-t', 'rsa', '-b', '2048', '-f', ssh_key_path, '-N', ''])
    
    print(f"SSH key pair for user {current_user} generated and saved to {ssh_key_path}.")
    print(" Please provide the following public key to install on remote servers for authentication:")
    
    # Read and print the user's public key
    with open(f"{ssh_key_path}.pub", 'r') as public_key_file:
        public_key = public_key_file.read()
        print(public_key)

    # Notify the user about the upcoming SSH service restart****************************************
    print("Important Notice!")
    print("The SSH service will be restarted to apply changes, and your current SSH session will be disconnected.")
    print("Make sure you have your SSH private key and take note of the new SSH port.")
    print("You will need to reconnect using the following information:")
    print(f"- SSH private key: {ssh_key_path}")
    print(f"- New SSH port: 8019 (or the port specified in the script)")
    print("To install the public key on a remote server:")
    print("1. Copy the public key text above.")
    print("2. Log in to the remote server as the desired user.")
    print("3. Append the public key to the ~/.ssh/authorized_keys file of the remote user.")
    
    # Make sure to ask for user acknowledgment***************************************
    input("Press Enter to acknowledge and continue...")

# The script can continue to the next function after user acknowledgment




def check_if_rsyslog_installed():
    try:
        # Use subprocess to run a command that checks if rsyslog is in the PATH
        subprocess.check_output(['rsyslogd', '-v'], stderr=subprocess.STDOUT)
        return True
    except subprocess.CalledProcessError as e:
        # The command will raise an exception if something goes wrong other than FileNotFoundError
        return False
    except FileNotFoundError:
        # This will catch the case where 'rsyslog' is not installed
        return False


def install_rsyslog():
    print("Configuring centralized logging...")
    if not check_if_rsyslog_installed():
        print("Rsyslog is not installed. Installing now...")
        # Install rsyslog
        subprocess.run(['sudo', 'add-apt-repository', 'ppa:adiscon/v8-stable'])
        subprocess.run(['sudo', 'apt-get', 'update'])
        subprocess.run(['sudo', 'apt-get', 'install', 'rsyslog'])
        subprocess.run(['sudo', 'systemctl', 'enable', 'rsyslog'])
        # Restart rsyslog
        subprocess.run(['sudo', 'systemctl', 'restart', 'rsyslog'])
    else:
        print("Rsyslog is already installed.")
        print("Skipping rsyslog installation.")
    
    print("Done!")

    
    

# Function to perform regular backups
def perform_backups():
    print("Using Rsync to secure your data")
    perform_rsync_backup()
    print("Done!")


def install_elk_stack():
    print("Do you want to install Elastic Stack (Elasticsearch, Logstash, Kibana)?")
    user_input = input("Enter 'yes' to install or 'no' to skip: ").strip().lower()

    if user_input == 'yes':
        install_elastic_search()
        print("Elastic Search installation complete, We will now add the password provided to your path")
        store_elastic_pass()
        display_status()
        print("Kibana installation will now begin.")
        install_kibana()
        print("Kibana installation is complete ")
        display_status()
        install_logstash()
        print("Logstash installation is complete.")
        print("ELK Stack components installed successfully.")
        display_status()
    elif user_input == 'no':
        print("Elastic Stack installation skipped.")
    else:
        print("Invalid input. Please enter 'yes' or 'no'.")

       # Function to add a rule to allow access to the loopback interface on the specified port
def allow_loopback_access(port):
    try:
        # Add a rule to allow access from the loopback interface (localhost)
        subprocess.run(['sudo', 'ufw', 'allow', 'in', 'on', 'lo', 'to', 'any', 'port', port])
        print(f"Access to port {port} from localhost allowed.")
    except Exception as e:
        print(f"Error: {str(e)}")





# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$


    
def main(): 
    
   # Ascii Header 
    display_ascii_header()
   
   # Check if user has sudo
    check_sudo()
   
   # System update1
    update_system()
   
    #  Configure centralized logging
    install_rsyslog()
   
   
    #Call the function to create or update the trusted IP file
    create_trusted_ip_file()

    # Call the function to generate an SSH key for the current user
    generate_ssh_key()

 # Configure firewall rules
    configure_firewall()
    #  Secure SSH configuration
    secure_ssh()

    # Function to allow access to the specified port
    allow_loopback_access(port)
    
    # Option to install elk stack  
    install_elk_stack()    

    # Use Rsync to safe gaurd data
    perform_backups()

    
   
    print("All steps completed successfully!")
   
    display_status()
   
    display_ascii_header()

if __name__ == "__main__":
    main()