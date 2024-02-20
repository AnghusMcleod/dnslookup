
Certainly, my apologies for the confusion. Here's the entire README in a single markdown block:

markdown
Copy code
# dnslookup

**dnslookup** is a lightweight tool that allows you to perform DNS queries through a simple RESTful API. It is designed to be flexible, allowing you to specify the DNS entry, timeout, and DNS server as part of the query parameters.

## Features

- DNS queries for both IP addresses and Fully Qualified Domain Names (FQDNs).
- Specify timeout and DNS server in the query for flexibility.
- Secure API access with an API key.
- Docker support for easy deployment.

## Usage

### Running Locally

1. Install the required dependencies:

   ```bash
   pip install -r requirements.txt
Set environment variables:

API_KEY: Your secret API key for authentication.
DEFAULT_DNS_SERVER: Default DNS server (optional, default is '8.8.8.8').
Run the application:

bash
Copy code
python dnslookup.py
Running with Docker
Build the Docker image:

bash
Copy code
docker build -t dnslookup .
Run the Docker container, specifying your API key and other optional parameters:

bash
Copy code
docker run -p 5000:5000 -e API_KEY=<your_api_key> -e DEFAULT_DNS_SERVER=<your_default_dns_server> dnslookup
API Endpoints
GET /query-dns/{dns_entry}

Perform a DNS query for the specified dns_entry.

Query Parameters:

api_key: Your API key (required).
timeout: Timeout for the DNS query in seconds (optional, default is 5 seconds).
dns_server: DNS server to use for the query (optional, default is '8.8.8.8').
Example:

bash
Copy code
curl -X GET "http://localhost:5000/query-dns/example.com?api_key=<your_api_key>&timeout=3&dns_server=8.8.4.4"
License
This project is licensed under the MIT License - see the LICENSE file for details.

sql
Copy code

Feel free to copy and paste this block directly into your GitHub repository's README.



