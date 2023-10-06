import validate_email
import os

# Function to get the email domain from an email address
def get_email_domain(email):
    return email.split('@')[-1]

# Function to sort emails based on their domain and validate their status
def sort_and_validate_emails(input_file_path):
    email_data = {}  # Dictionary to store emails grouped by domain

    with open(input_file_path, 'r') as file:
        total_emails = sum(1 for line in file)  # Count the total number of email addresses
        file.seek(0)  # Reset file pointer to the beginning
        processed_count = 0  # Counter for processed emails

        for line in file:
            email = line.strip()
            domain = get_email_domain(email).lower()  # Convert the domain to lowercase

            # Validate the email format
            is_valid = validate_email.validate_email(email)

            if is_valid:
                if domain not in email_data:
                    email_data[domain] = []
                email_data[domain].append(email)
                # Write the email to its respective file immediately
                with open(f'{domain}_emails.txt', 'a') as domain_file:
                    domain_file.write(email + '\n')

            processed_count += 1
            print(f"Processed: {processed_count}/{total_emails} ({processed_count/total_emails*100:.2f}%)", end='\r')

    print("\nProcessing complete.")

if __name__ == "__main__":
    input_file_path = input("Enter the path to the input text file: ")
    sort_and_validate_emails(input_file_path)
