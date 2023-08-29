

```


       dP                               888888ba                     .88888.                    
       88                               88    `8b                   d8'   `8b                   
       88 dP    dP 88d8b.d8b. 88d888b. a88aaaa8P' .d8888b. dP.  .dP 88     88 88d888b. .d8888b. 
       88 88    88 88'`88'`88 88'  `88  88   `8b. 88'  `88  `8bd8'  88     88 88'  `88 88ooood8 
88.  .d8P 88.  .88 88  88  88 88.  .88  88    .88 88.  .88  .d88b.  Y8.   .8P 88    88 88.  ... 
 `Y8888'  `88888P' dP  dP  dP 88Y888P'  88888888P `88888P' dP'  `dP  `8888P'  dP    dP `88888P' 
                              88                                                                
                              dP                                                                

```
# JumpBoxOne

JumpBoxOne is a versatile utility for configuring and securing your server, with a focus on enhancing security, managing firewall rules, and simplifying log forwarding. This README provides an overview of the program, its features, and how to use it effectively.

## Table of Contents
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Configuration](#configuration)
- [Elastic Stack Integration](#elastic-stack-integration)
- [Contributing](#contributing)
- [License](#license)

## Features

JumpBoxOne offers the following key features:

- **Firewall Configuration:** Easily configure firewall rules to control network traffic and enhance security.
- **Log Forwarding:** Configure centralized log forwarding using rsyslog to a remote SIEM system.
- **The Elastic Stack(Kibana, logstash, & elasticsearch) 
- **The SSH port will be changed to port 8019 and only use generated keys
- **Package Installation:** Automatically check and install required system and Python packages.
- **Customizable:** Add or remove Python packages, modify firewall rules, and tailor the program to your needs.
- **Security:** Enhance your server's security by customizing firewall rules and ensuring essential packages are installed.
- **User-Friendly:** Designed with user interaction in mind, with prompts and informative messages.

## Installation

To install JumpBoxOne, follow these steps:

1. Clone the repository to your server:

   ```shell
   git clone https://github.com/iamplaga/JumpBoxOne.git
   ```

2. Change to the program directory:

   ```shell
   cd JumpBoxOne
   ```

3. Run the program:

   ```shell
   python jumpboxone.py
   ```

JumpBoxOne will guide you through the installation process and any necessary configurations.
****NOTE**** SSH Will disconnect at the end of the installation when the port changes from default port 22 to port 8019
## Usage

JumpBoxOne is designed to be user-friendly. 
Simply run the program and follow the on-screen prompts to configure your server's firewall rules, set up log forwarding, ensure essential packages are installed, and more.

Example usage:

```shell
python jumpboxone.py
```

Follow the prompts and instructions provided by the program.

## Configuration

JumpBoxOne allows for various configurations to suit your needs:

- **Custom Firewall Rules FOR Trusted IP Addresses & Subnets:** Edit the firewall configuration in `JumpBoxOne/trusted_ip.txt`.
- **Additional Python Packages:** Modify the `required_python_packages` list in `JumpBoxOne/software_installer.py`.
- **Log Forwarding Configuration:** Edit the `rsyslog` configuration in `JumpBoxOne/software_installer.py`.

## Elastic Stack Integration

JumpBoxOne seamlessly integrates with the Elastic Stack to provide advanced log analysis and visualization. Here's how to set it up:

1. **Elasticsearch, Logstash, and Kibana:** Install and configure the Elastic Stack on your server as per your requirements. Ensure that Elasticsearch, Logstash, and Kibana are up and running.

2. **Firewall Rules:** Configure firewall rules to allow communication between your server and the Elastic Stack components.
3. Common ports to open include 9200 (Elasticsearch), 5044 (Logstash), and 5601 (Kibana). Adjust these ports as needed.

4. **Log Forwarding:** Configure Logstash to accept incoming logs from your server. Update Logstash configuration files to specify input and output plugins according to your log forwarding requirements.

5. **JumpBoxOne Configuration:** Customize JumpBoxOne's `rsyslog` configuration to forward logs to Logstash or the appropriate input endpoint of your Logstash setup.

6. **Security:** Ensure that only necessary ports are open for communication with the Elastic Stack and other services. JumpBoxOne helps you control firewall rules effectively.

## Contributing

Contributions to JumpBoxOne are welcome! If you have suggestions, bug reports, or feature requests, please open an issue on the [GitHub repository](https://github.com/yourusername/JumpBoxOne).

## License

This project is licensed under the [MIT](LICENSE).
```

In this extended README, we've added a section on Elastic Stack Integration, which explains how to set up and configure the Elastic Stack for log analysis and visualization. It also emphasizes security by mentioning the need to control firewall rules effectively. 
