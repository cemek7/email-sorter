import dns.resolver
import validate_email
import os

# List of supported email providers
providers = {
    'office365': ['outlook.com', 'office365.com'],
    'gmail': ['gmail.com'],
    'yahoo': ['yahoo.com'],
    'godaddy': ['godaddy.com'],
    'rackspace': ['rackspace.com'],
    'qq': ['qq.com'],
    'netease': ['163.com', '126.com'],
    'networksolutions': ['networksolutions.com'],
    '263': ['263.net'],
    'aliyun': ['aliyun.com'],
    'namecheap': ['namecheap.com'],
    '1and1': ['1and1.com'],
    'mimecast': ['mimecast.com'],
    'hinet': ['hinet.net'],
    'synaq': ['synaq.com'],
    'mweb': ['mweb.co.za'],
    'chinaemail': ['chinaemail.cn'],
    'zmail': ['zmail300.cn'],
    'yizhigher': ['yizhigher.com'],
    'coremail': ['coremail.cn']
    # Add more providers if needed
}

# Function to get the email domain from an email address
def get_email_domain(email):
    return email.split('@')[-1]

# Function to check the MX record of a domain
def check_mx_record(domain):
    try:
        mx_records = dns.resolver.resolve(domain, 'MX')
        return str(mx_records[0].exchange)
    except dns.resolver.NoAnswer:
        return None
    except dns.resolver.NXDOMAIN:
        return None
    except dns.exception.DNSException as e:
        print(f"DNS Resolution Error for domain {domain}: {str(e)}")
        with open('dns_resolution_errors.txt', 'a') as error_file:
            error_file.write(f"DNS Resolution Error for domain {domain}: {str(e)}\n")
        return None

# Function to sort emails based on their domain's MX record and validate their status
def sort_and_validate_emails(input_file_path):
    sorted_emails = {provider: [] for provider in providers}

    with open(input_file_path, 'r') as file:
        total_emails = sum(1 for line in file)  # Count the total number of email addresses
        file.seek(0)  # Reset file pointer to the beginning
        processed_count = 0  # Counter for processed emails

        for line in file:
            email = line.strip()
            domain = get_email_domain(email).lower()  # Convert the domain to lowercase
            mx_record = check_mx_record(domain)

            if mx_record:
                for provider, domains in providers.items():
                    if domain in domains:
                        is_valid = validate_email.validate_email(email)
                        if is_valid:
                            sorted_emails[provider].append(email)
                            # Write the email to its respective file immediately
                            with open(f'{provider}_emails.txt', 'a') as provider_file:
                                provider_file.write(email + '\n')
                        break

            processed_count += 1
            print(f"Processed: {processed_count}/{total_emails} ({processed_count/total_emails*100:.2f}%)", end='\r')

    print("\nProcessing complete.")
    return sorted_emails

if __name__ == "__main__":
    input_file_path = input("Enter the path to the input text file: ")
    sorted_emails = sort_and_validate_emails(input_file_path)
