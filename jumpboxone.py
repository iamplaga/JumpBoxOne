import os
import subprocess
import getpass
from software_installer import install_package
import sys
from software_check import Install_Check

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
    trusted_ip_directory = "JumpBoxOne"
    trusted_ip_file = "trusted_ip.txt"
    trusted_ip_path = os.path.join(trusted_ip_directory, trusted_ip_file)
    
    # Check if the trusted IP file exists
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
   
    # Define the path where the JumpBoxOne folder will be located
    jumpbox_dir = f"/home/{getpass.getuser()}/JumpBoxOne"
    
    print(f"All files will be located in the folder: {jumpbox_dir}")
   
    # Add or update format directions
    with open(trusted_ip_path, 'a') as ip_file:
        ip_file.write("\n# Additional Format Directions:\n")
        ip_file.write("# - Enter each IP address or subnet on a separate line.\n")
        ip_file.write("# - Use the format 'IP_ADDRESS' or 'IP_ADDRESS/SUBNET_MASK'.\n")
        ip_file.write("# - Comments (lines starting with '#') are allowed.\n")


    # Get the user's IP address8888888888888888888888888
    user_ip = subprocess.check_output(['curl', 'ifconfig.me']).decode('utf-8').strip()


    # Append the user's IP address to the trusted IP file
    with open(trusted_ip_path, 'a') as ip_file:
        ip_file.write(user_ip + '\n')

    # Optionally, you can print a message to confirm the addition
    print(f"User's IP address ({user_ip}) added to trusted IP file.")

# Function to secure SSH configuration
def secure_ssh():
    print("SSH is a common attack surface, lets remove that. Nope, no password logins here...")
    # Disable password-based authentication
    with open('/etc/ssh/sshd_config', 'a') as ssh_config:
        ssh_config.write("\nPasswordAuthentication no\n")
        ssh_config.write("PermitRootLogin no\n")
    # Restart SSH service ********************************************
    #subprocess.run(['sudo', 'systemctl', 'restart', 'ssh'])
    print(" Done!")

# Function to set up firewall rules
def configure_firewall():
    #global trusted_ip_directory, trusted_ip_file, ssh_port
    
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
        subprocess.run(['sudo', 'ufw', 'allow', '5601', '8019'])
        
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

def configure_log_forwarding():
    print("Configure log forwarding to a **External** SIEM system? (yes/no): ")
    user_choice = input().strip().lower()

    if user_choice == 'yes':
        print("Configuring log forwarding...")
        print("Record the following information to configure the SIEM on your external server properly.")
        # Prompt the user for the SIEM server IP and port
        siem_server_ip = input("Enter the SIEM server IP: ")
        siem_server_port = input("Enter the SIEM server port (e.g., 514): ")
        
        # Write the SIEM server and port to the rsyslog configuration
        with open('/etc/rsyslog.d/50-default.conf', 'a') as rsyslog_config:
            rsyslog_config.write(f"\n*.* @ {siem_server_ip}:{siem_server_port}\n")
        
        # Restart the rsyslog service
        subprocess.run(['sudo', 'systemctl', 'restart', 'rsyslog'])
        
        print(f"Log forwarding to {siem_server_ip}:{siem_server_port} configured.")
    elif user_choice == 'no':
        print("Log forwarding configuration skipped.")
        print("I will configure your logs to forwarded to the Elastic Stack on the local host")
    else:
        print("Invalid choice. Log forwarding configuration skipped.")


def check_if_elasticsearch_installed():
    try:
        # Use subprocess to run a command that checks if the elasticsearch executable is in the PATH
        subprocess.check_output(['elasticsearch', '--version'], stderr=subprocess.STDOUT, text=True)
        return True
    except subprocess.CalledProcessError as e:
        # The command will raise an exception if elasticsearch is not found
        return False

def configure_logging():
    print("Configuring centralized logging...")
    
    # Check if Elasticsearch is installed
    elasticsearch_installed = check_if_elasticsearch_installed()
    
    # Install rsyslog for centralized logging
    subprocess.run(['sudo', 'apt', 'install', '-y', 'rsyslog'])
    
    if elasticsearch_installed:
        # Configure rsyslog to forward logs to Elasticsearch (modify this as needed)
        elastic_stack_ip = "localhost"  # Change as per your Elasticsearch setup
        elastic_stack_port = "9200"     # Change as per your Elasticsearch setup
    
        with open('/etc/rsyslog.d/50-default.conf', 'a') as rsyslog_config:
            rsyslog_config.write(f"\n*.* @ {elastic_stack_ip}:{elastic_stack_port}\n")
        
        print("Centralized logging configured to forward logs to Elasticsearch.")
    else:
        print("Elasticsearch is not installed. Rsyslog installed without log forwarding.")
        print("You can manually configure log forwarding to Elasticsearch later.")
    
    # Restart rsyslog
    subprocess.run(['sudo', 'systemctl', 'restart', 'rsyslog'])
    
    print("Done!")




# Function to restrict user privileges
def restrict_user_privileges():
    print(" Restricting user privileges...")
    # Implement RBAC or use 'sudo' to control user permissions
    # Example: Create a new user and grant sudo access
    subprocess.run(['sudo', 'useradd', '-m', 'new_user'])
    subprocess.run(['sudo', 'usermod', '-aG', 'sudo', 'new_user'])
    print(" Done!")

# Function to disable unnecessary services
def disable_unnecessary_services():
    print(" Disabling unnecessary services...")
    # List and disable unnecessary services
    services_to_disable = ['service1', 'service2', 'service3']
    for service in services_to_disable:
        subprocess.run(['sudo', 'systemctl', 'disable', service])
    print(" Done!")

# Function to perform regular backups
def perform_backups():
    print("Performing regular backups... (to be implemented as needed)")
    # Implement a backup strategy using tools like 'rsync' or 'backup software'
    # Schedule backups and test restoration procedures
    print("Done!")


def install_software_prompt():
    print("Do you want to install Elastic Stack (Elasticsearch, Logstash, Kibana)?")
    user_input = input("Enter 'yes' to install or 'no' to skip: ").strip().lower()

    if user_input == 'yes':
        install_package('elasticsearch')
        install_package('logstash')
        install_package('kibana')
        print("Elastic Stack components installed successfully.")
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

def display_ascii_header():
    ascii_header = """ 
       dP                               888888ba                     .88888.                    
       88                               88    `8b                   d8'   `8b                   
       88 dP    dP 88d8b.d8b. 88d888b. a88aaaa8P' .d8888b. dP.  .dP 88     88 88d888b. .d8888b. 
       88 88    88 88'`88'`88 88'  `88  88   `8b. 88'  `88  `8bd8'  88     88 88'  `88 88ooood8 
88.  .d8P 88.  .88 88  88  88 88.  .88  88    .88 88.  .88  .d88b.  Y8.   .8P 88    88 88.  ... 
 `Y8888'  `88888P' dP  dP  dP 88Y888P'  88888888P `88888P' dP'  `dP  `8888P'  dP    dP `88888P' 
                              88                                                                
                              dP                                                                
"""
    print(ascii_header)



# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

if __name__ == "__main__":
    # "Update and upgrade system packages
    
    
    display_ascii_header()
    
    update_system()

   # This will check & ask for all critical packages that may need to be installed 
    Install_Check()

# Call the function to create or update the trusted IP file
    create_trusted_ip_file()

# Call the function to generate an SSH key for the current user
    generate_ssh_key()

    #  Secure SSH configuration
    secure_ssh()

    # Call the function to allow access to the specified port
    allow_loopback_access(port)

    install_software_prompt()    

    #  Configure centralized logging
    configure_logging()

    #  Restrict user privileges
    restrict_user_privileges()

    #  Disable unnecessary services
    disable_unnecessary_services()

    # Perform regular backups (to be implemented as needed)
    perform_backups()

     # Configure firewall rules
    configure_firewall()
    print("All steps completed successfully!")
    display_ascii_header()