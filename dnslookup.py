# dnslookup.py
import re
import socket
import dns.resolver
import os
import hashlib
import secrets
from flask import Flask, request, jsonify

app = Flask(__name__)

# Default values for API key and DNS server
API_KEY = os.environ.get('API_KEY', secrets.token_urlsafe(32))
DEFAULT_DNS_SERVER = os.environ.get('DEFAULT_DNS_SERVER', '8.8.8.8')

# Function to hash an API key for validation
def hash_api_key(api_key):
    return hashlib.sha256(api_key.encode()).hexdigest()

# Function to check if an API key is valid
def is_valid_api_key(api_key):
    return hash_api_key(api_key) == hash_api_key(API_KEY)

# Function to check the validity of a DNS entry format (FQDN or IP)
def is_valid_dns_entry(dns_entry):
    if is_valid_ip(dns_entry):
        return True
    elif is_fqdn(dns_entry):
        return True
    else:
        return False

# Function to check if the provided value is a valid IP address
def is_valid_ip(value):
    try:
        socket.inet_aton(value)
        return True
    except socket.error:
        return False

# Function to check if the provided value is a valid FQDN
def is_fqdn(hostname):
    """
    https://en.wikipedia.org/wiki/Fully_qualified_domain_name
    """
    if not 1 < len(hostname) < 253:
        return False

    # Remove trailing dot
    if hostname[-1] == '.':
        hostname = hostname[0:-1]

    # Split hostname into a list of DNS labels
    labels = hostname.split('.')

    # Define pattern of DNS label
    # Can begin and end with a number or letter only
    # Can contain hyphens, a-z, A-Z, 0-9
    # 1 - 63 chars allowed
    fqdn = re.compile(r'^[a-z0-9]([a-z-0-9-]{0,61}[a-z0-9])?$', re.IGNORECASE)

    # Check that all labels match that pattern
    return all(fqdn.match(label) for label in labels)

# Function to check if the provided DNS server is a valid IP or FQDN
def is_valid_dns_server(dns_server):
    return is_valid_ip(dns_server) or is_fqdn(dns_server)

# Function to perform a DNS query
def query_dns(dns_entry, timeout, dns_server):
    try:
        # Initialize a DNS resolver
        resolver = dns.resolver.Resolver()
        resolver.nameservers = [dns_server]
        # Perform the DNS query
        response = resolver.query(dns_entry, lifetime=timeout)
        # Return the successful response with a 200 status code
        return {"status": "success", "message": "DNS query successful", "response": str(response)}, 200
    except dns.resolver.Timeout:
        # Return a timeout error with a 504 status code
        return {"status": "error", "message": "DNS query timed out"}, 504
    except dns.resolver.NXDOMAIN:
        # Return no content, indicating the record was not found
        return "", 204
    except dns.exception.DNSException as e:
        # Return a generic DNS error with a 503 status code
        return {"status": "error", "message": f"DNS query failed: {str(e)}"}, 503

# Route to handle DNS queries
@app.route('/query-dns/<dns_entry>', methods=['GET'])
def handle_dns_query(dns_entry):
    # Retrieve API key from the URL query parameter
    api_key = request.args.get('api_key')
    # Retrieve timeout and DNS server from query parameters with default values
    timeout = request.args.get('timeout', default=5, type=int)
    dns_server = request.args.get('dns_server', default=DEFAULT_DNS_SERVER, type=str)

    # Validate API key
    if not is_valid_api_key(api_key):
        return {"status": "error", "message": "Invalid API key"}, 401

    # Validate main query (DNS entry)
    if not is_valid_dns_entry(dns_entry):
        return {"status": "error", "message": "Invalid DNS entry format"}, 422

    # Validate DNS server format
    if not is_valid_dns_server(dns_server):
        return {"status": "error", "message": "Invalid DNS server format"}, 422

    try:
        # Perform the DNS query and return the result with the appropriate status code
        result, status_code = query_dns(dns_entry, timeout, dns_server)
        return jsonify(result), status_code
    except:
        # Return a generic error with a 503 status code if an unknown error occurs
        return {"status": "error", "message": "Unknown error occurred"}, 503

# Run the Flask application
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
