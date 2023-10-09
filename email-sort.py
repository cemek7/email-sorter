from validate_email_address import validate_email
import smtplib

# Function to get the email domain from an email address
def get_email_domain(email):
    return email.split('@')[-1]

# Function to check if an email is live and active using SMTP
def check_email_live(email):
    domain = email.split('@')[-1]

    try:
        server = smtplib.SMTP(domain)
        server.ehlo()
        response_code, _ = server.verify(email)
        server.quit()

        if response_code == 250:
            return True
        else:
            return False
    except Exception as e:
        print(f"Error: {e}")
        return False

# Function to sort emails based on their domain and validate their status
def sort_and_validate_emails(input_file_path):
    email_data = {}

    try:
        with open(input_file_path, 'r') as file:
            total_emails = sum(1 for line in file)
            file.seek(0)
            processed_count = 0

            for line in file:
                email = line.strip()
                domain = get_email_domain(email).lower()

                is_valid_format = validate_email(email)

                if is_valid_format:
                    is_live = check_email_live(email)

                    if is_live:
                        if domain not in email_data:
                            email_data[domain] = []
                        email_data[domain].append(email)
                        with open(f'{domain}_emails.txt', 'a') as domain_file:
                            domain_file.write(email + '\n')

                processed_count += 1
                print(f"Processed: {processed_count}/{total_emails} ({processed_count/total_emails*100:.2f}%)", end='\r')

    except Exception as e:
        print(f"Error: {e}")

    print("\nProcessing complete.")

if __name__ == "__main__":
    input_file_path = input("Enter the path to the input text file: ")
    sort_and_validate_emails(input_file_path)
