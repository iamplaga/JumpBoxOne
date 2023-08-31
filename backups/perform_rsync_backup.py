import subprocess

def perform_rsync_backup():
    print("Welcome to the Rsync Backup Wizard by Hattori Hanzo!")
    
    # Prompt the user for the backup destination path
    backup_path = input("Enter the destination path where you want to store the backup: ").strip()
    
    sources = []
    
    while True:
        print("\nAdd files or directories to your backup.")
        print("Press Enter to finish adding sources or type 'skip' to skip the backup.")
        
        source = input("Enter the path of the file or directory to add: ").strip()
        
        if not source:
            break  # Finish adding sources
        
        if source.lower() == 'skip':
            print("Backup skipped.")
            return
        
        if not source:
            print("Source path cannot be empty. Please provide a valid path or 'skip' to skip the backup.")
        else:
            sources.append(source)

    if not sources:
        print("No sources provided. Backup skipped.")
        return

    try:
        # Create the rsync command
        rsync_command = ["rsync", "-av", "--progress"]

        for source in sources:
            rsync_command.append(source)

        rsync_command.append(backup_path)

        # Run the rsync command
        subprocess.run(rsync_command, check=True)

        print("Backup completed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    perform_rsync_backup()

