import os
import subprocess
import getpass



# Function to update and upgrade system packages
def update_system():
    print("OK, first lets get your Machine updated...")
    subprocess.run(['sudo', 'apt', 'update'])
    subprocess.run(['sudo', 'apt', 'upgrade', '-y'])
    print("Step 1: Done!")

# Function to create or update the trusted IP file
def create_trusted_ip_file():
    trusted_ip_directory = "JumpBoxOne"
    trusted_ip_file = "trusted_ip.txt"
    trusted_ip_path = os.path.join(trusted_ip_directory, trusted_ip_file)
    
    # Check if the trusted IP file exists
    if os.path.exists(trusted_ip_path):
        # File already exists; do nothing
        print(f"Step 0: Trusted IP file '{trusted_ip_file}' already exists.")
    else:
        # File does not exist; create it
        print(f"Step 0: Creating trusted IP file '{trusted_ip_file}'...")
        with open(trusted_ip_path, 'w') as ip_file:
            ip_file.write("# Trusted IP Addresses and Subnets\n")
            ip_file.write("# Format: Enter one trusted IP address or subnet per line\n")
            ip_file.write("# Examples:\n")
            ip_file.write("#   192.168.1.100\n")
            ip_file.write("#   10.0.0.0/24\n")
        print(f"Step 0: Done! '{trusted_ip_file}' created.")
    
    # Add or update format directions
    with open(trusted_ip_path, 'a') as ip_file:
        ip_file.write("\n# Additional Format Directions:\n")
        ip_file.write("# - Enter each IP address or subnet on a separate line.\n")
        ip_file.write("# - Use the format 'IP_ADDRESS' or 'IP_ADDRESS/SUBNET_MASK'.\n")
        ip_file.write("# - Comments (lines starting with '#') are allowed.\n")

# Function to secure SSH configuration
def secure_ssh():
    print("SSH is a common attack surface, lets remove that. Nope, no password logins here...")
    # Disable password-based authentication
    with open('/etc/ssh/sshd_config', 'a') as ssh_config:
        ssh_config.write("\nPasswordAuthentication no\n")
        ssh_config.write("PermitRootLogin no\n")
    # Restart SSH service
    subprocess.run(['sudo', 'systemctl', 'restart', 'ssh'])
    print("Step 2: Done!")

# Function to set up firewall rules
def configure_firewall():
    print("Step 3: Configuring firewall rules...")
    
    # Define the directory and filename for the trusted IP file
    trusted_ip_directory = "JumpBoxOne"
    trusted_ip_file = "trusted_ip.txt"
    
    # Construct the full path to the trusted IP file
    trusted_ip_path = os.path.join(trusted_ip_directory, trusted_ip_file)
    
    # Check if the trusted IP file exists
    if os.path.exists(trusted_ip_path):
        # Read trusted IP addresses from the file
        with open(trusted_ip_path, 'r') as ip_file:
            trusted_ips = [line.strip() for line in ip_file.readlines() if line.strip()]  # Read non-empty lines
    
        # Create rules to allow SSH from trusted IP addresses on port 8019
        for ip in trusted_ips:
            subprocess.run(['sudo', 'ufw', 'allow', 'from', ip, 'to', 'any', 'port', '8019'])
        
        # Delete existing SSH rules for port 22
        subprocess.run(['sudo', 'ufw', 'delete', 'allow', '22'])
        
        # Change SSH port to 8019
        subprocess.run(['sudo', 'sed', '-i', 's/^Port 22$/Port 8019/', '/etc/ssh/sshd_config'])
        
        # Restart SSH service
        #subprocess.run(['sudo', 'systemctl', 'restart', 'ssh'])
        
        # Enable the firewall
        subprocess.run(['sudo', 'ufw', 'enable'])
        
        print("Step 3: Done! Firewall rules configured based on trusted IP addresses. SSH port changed to 8019.")
    else:
        print("Step 3: Error - Trusted IP file not found.")


# Function to generate an SSH key pair for the current user
def generate_ssh_key():
    # Get the current user's username
    current_user = getpass.getuser()
    
    print(f"Step 1: Generating SSH key pair for user {current_user}...")
    
    # Define the path where the SSH key pair will be saved
    ssh_key_dir = f"/home/{current_user}/.ssh"
    ssh_key_path = f"{ssh_key_dir}/id_rsa"
    
    # Check if the .ssh directory exists, and if not, create it
    if not os.path.exists(ssh_key_dir):
        os.makedirs(ssh_key_dir)
    
    # Generate the SSH key pair without a passphrase (you can add one if needed)
    subprocess.run(['ssh-keygen', '-t', 'rsa', '-b', '2048', '-f', ssh_key_path, '-N', ''])
    
    print(f"Step 1: SSH key pair for user {current_user} generated and saved to {ssh_key_path}.")
    print("Step 2: Please provide the following public key to install on remote servers for authentication:")
    
    # Read and print the user's public key
    with open(f"{ssh_key_path}.pub", 'r') as public_key_file:
        public_key = public_key_file.read()
        print(public_key)

    # Notify the user about the upcoming SSH service restart
    print("Step 3: Important Notice!")
    print("The SSH service will be restarted to apply changes, and your current SSH session will be disconnected.")
    print("Make sure you have your SSH private key and take note of the new SSH port.")
    print("You will need to reconnect using the following information:")
    print(f"- SSH private key: {ssh_key_path}")
    print(f"- New SSH port: 8019 (or the port specified in the script)")
    print("To install the public key on a remote server:")
    print("1. Copy the public key text above.")
    print("2. Log in to the remote server as the desired user.")
    print("3. Append the public key to the ~/.ssh/authorized_keys file of the remote user.")
    
    # Pause for user acknowledgment
    input("Press Enter to acknowledge and continue...")

# The script can continue to the next function after user acknowledgment

# Function to implement centralized logging
def configure_logging():
    print("Step 4: Configuring centralized logging...")
    # Install rsyslog for centralized logging
    subprocess.run(['sudo', 'apt', 'install', '-y', 'rsyslog'])
    # Configure rsyslog to forward logs to a remote SIEM system
    with open('/etc/rsyslog.d/50-default.conf', 'a') as rsyslog_config:
        rsyslog_config.write("\n*.* @siem_server_ip:514\n")
    # Restart rsyslog
    subprocess.run(['sudo', 'systemctl', 'restart', 'rsyslog'])
    print("Step 4: Done!")

# Function to restrict user privileges
def restrict_user_privileges():
    print("Step 5: Restricting user privileges...")
    # Implement RBAC or use 'sudo' to control user permissions
    # Example: Create a new user and grant sudo access
    subprocess.run(['sudo', 'useradd', '-m', 'new_user'])
    subprocess.run(['sudo', 'usermod', '-aG', 'sudo', 'new_user'])
    print("Step 5: Done!")

# Function to disable unnecessary services
def disable_unnecessary_services():
    print("Step 6: Disabling unnecessary services...")
    # List and disable unnecessary services
    services_to_disable = ['service1', 'service2', 'service3']
    for service in services_to_disable:
        subprocess.run(['sudo', 'systemctl', 'disable', service])
    print("Step 6: Done!")

# Function to perform regular backups
def perform_backups():
    print("Step 7: Performing regular backups... (to be implemented as needed)")
    # Implement a backup strategy using tools like 'rsync' or 'backup software'
    # Schedule backups and test restoration procedures
    print("Step 7: Done!")

if __name__ == "__main__":
    # Step 1: Update and upgrade system packages
    update_system()

# Call the function to create or update the trusted IP file
    create_trusted_ip_file()

# Call the function to generate an SSH key for the current user
    generate_ssh_key()

    # Step 2: Secure SSH configuration
    secure_ssh()

    # Step 3: Configure firewall rules
    configure_firewall()

    # Step 4: Configure centralized logging
    configure_logging()

    # Step 5: Restrict user privileges
    restrict_user_privileges()

    # Step 6: Disable unnecessary services
    disable_unnecessary_services()

    # Step 7: Perform regular backups (to be implemented as needed)
    perform_backups()

    print("All steps completed successfully!")
