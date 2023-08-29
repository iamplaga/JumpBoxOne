import subprocess

def check_system_packages(packages):
    missing_packages = []
    for package in packages:
        try:
            subprocess.check_output([package, "--version"])
        except subprocess.CalledProcessError:
            missing_packages.append(package)
    return missing_packages

def install_system_packages(packages):
    for package in packages:
        subprocess.run(["sudo", "apt", "install", "-y", package])

def check_python_packages(packages):
    missing_packages = []
    for package in packages:
        try:
            __import__(package)
        except ImportError:
            missing_packages.append(package)
    return missing_packages

def install_python_packages(packages):
    for package in packages:
        subprocess.run(["pip", "install", package])

def Install_Check():
    required_system_packages = ["ufw", "curl", "rsyslog"]
    missing_system_packages = check_system_packages(required_system_packages)

    if missing_system_packages:
        print("The following required system packages are missing:")
        for package in missing_system_packages:
            print(f"- {package}")
        install_input = input("Do you want to install the missing system packages? (yes/no): ").strip().lower()
        if install_input == "yes":
            install_system_packages(missing_system_packages)
        else:
            print("Please install the missing system packages manually.")
    else:
        print("All required system packages are installed.")

    required_python_packages = ["requests", "other_python_package"]
   
    # Ask the user if they want to add additional Python packages
    add_packages_input = input("Do you want to add additional Python packages to the installation list? (yes/no): ").strip().lower()
    
    if add_packages_input == "yes":
        additional_python_packages = input("Enter additional Python packages separated by spaces: ").split()
        required_python_packages.extend(additional_python_packages)
    else:
        print("No additional packages will be added.")

    missing_python_packages = check_python_packages(required_python_packages)
    
    if missing_python_packages:
        print("The following required Python packages are missing:")
        for package in missing_python_packages:
            print(f"- {package}")
        install_input = input("Do you want to install the missing Python packages? (yes/no): ").strip().lower()
        if install_input == "yes":
            install_python_packages(missing_python_packages)
        else:
            print("Please install the missing Python packages manually.")
    else:
        print("All required Python packages are installed.")

if __name__ == "__main__":
   Install_Check()
