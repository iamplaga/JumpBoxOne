import os
import getpass
import platform

def configure_elasticsearch_password():
    # Ask the user if they want to set the Elasticsearch superuser password
    choice = input("Do you want to set a password for the Elasticsearch superuser? (y/n): ").strip().lower()

    if choice == 'y':
        # Generate a random password for the elastic superuser
        elastic_password = getpass.getpass(prompt="Enter a password for the elastic superuser: ")
        
        # Set the password as an environment variable for the current session
        os.environ["ELASTIC_PASSWORD"] = elastic_password
        
        print("Elasticsearch superuser password set for the current session.")
        print("Make sure to keep this password secure.")
        
        # Check if the user wants to persist the password
        persist_choice = input("Do you want to persist the password for future sessions? (y/n): ").strip().lower()
        
        if persist_choice == 'y':
            # Determine the user's shell configuration file
            shell_config_file = None
            if platform.system() == "Linux":
                # For Linux, assume the user is using Bash
                shell_config_file = os.path.expanduser("~/.bashrc")
            elif platform.system() == "Darwin":
                # For macOS, assume the user is using Bash
                shell_config_file = os.path.expanduser("~/.bash_profile")

            # Add the export statement to the shell configuration file
            if shell_config_file:
                with open(shell_config_file, "a") as config_file:
                    config_file.write(f'\nexport ELASTIC_PASSWORD="{elastic_password}"\n')

                print(f'Exported ELASTIC_PASSWORD to {shell_config_file}.')
                print("The password will be available in future shell sessions.")
        
    else:
        print("No password set for the Elasticsearch superuser. Moving on to the next step.")

if __name__ == "__main__":
    configure_elasticsearch_password()