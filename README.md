# CyberScope

CyberScope is a Python-based graphical user interface (GUI) application designed to assist in various cybersecurity reconnaissance and testing tasks. Built with `tkinter`, it integrates popular open-source security tools like Sublist3r, Dalfox, SQLMap, and Nmap, providing a centralized and user-friendly interface for common security checks.

## Features

* **Subdomain Enumeration:** Discover subdomains for a given domain using Sublist3r.
* **XSS (Cross-Site Scripting) Check:** Scan URLs for XSS vulnerabilities using Dalfox.
* **SQL Injection Check:** Test URLs for SQL injection vulnerabilities using SQLMap.
* **Network Scanning:** Perform basic port scanning on a target host or IP address using Nmap.
* **User-Friendly Interface:** Intuitive neon-style GUI for easy interaction.
* **Input Validation:** Basic validation for domains, URLs, and IP addresses to prevent common errors.

## Installation and Setup

### Prerequisites

Before running CyberScope, you need to have the following tools installed and accessible on your system:

* **Python 3.x:** Download and install from [python.org](https://www.python.org/downloads/).
* **Git:** Download and install from [git-scm.com](https://git-scm.com/downloads/).
* **Sublist3r:**
    * Install via pip: `pip install sublist3r`
    * *Note: Ensure the path to `sublist3r.py` in `cyberScope.py` matches your installation (e.g., `C:\\Users\\nzd\\AppData\\Roaming\\Python\\Python312\\site-packages\\sublist3r.py`).*
* **Dalfox:**
    * Follow installation instructions from the official Dalfox GitHub repository: [https://github.com/dalfox/dalfox](https://github.com/dalfox/dalfox)
    * *Note: Update the `dalfox_path` variable in `cyberScope.py` to point to your `dalfox.exe` executable.*
* **SQLMap:**
    * Clone the SQLMap repository: `git clone --depth 1 https://github.com/sqlmapproject/sqlmap.git sqlmap-master`
    * *Note: Update the `sqlmap_path` variable in `cyberScope.py` to point to your `sqlmap.py` script.*
* **Nmap:**
    * Download and install from the official Nmap website: [https://nmap.org/download.html](https://nmap.org/download.html)
    * *Note: Update the `nmap_path` variable in `cyberScope.py` to point to your `nmap.exe` executable.*

### Project Setup

1.  **Clone the Repository:**
    ```bash
    git clone [https://github.com/schwarz-cloud/cyberScope.git](https://github.com/schwarz-cloud/cyberScope.git)
    cd cyberScope
    ```
2.  **Install Python Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
    This will install `sublist3r` if not already present.

3.  **Adjust Tool Paths:**
    **Crucially, you must open `cyberScope.py` and update the following variables to match the exact paths where you installed Dalfox, SQLMap, and Nmap on *your* system:**

    ```python
    sublist3r_path = 'C:\\Users\\nzd\\AppData\\Roaming\\Python\\Python312\\site-packages\\sublist3r.py' # Update if different
    dalfox_path = "C:\\Users\\nzd\\go\\bin\\dalfox.exe" # <-- **MUST UPDATE THIS PATH**
    sqlmap_path = "C:\\Users\\nzd\\OneDrive\\Desktop\\ecc201 project\\sqlmap-master\\sqlmap.py" # <-- **MUST UPDATE THIS PATH**
    nmap_path = 'C:\\Users\\nzd\\Nmap\\nmap.exe' # <-- **MUST UPDATE THIS PATH**
    ```

## Usage

To run the CyberScope application:

```bash
python cyberScope.py
