"""
Regex Data Extraction Program
Extracts emails, URLs, phone numbers, times, and hashtags from text.
"""

import re

#REGEX PATTERNS

EMAIL_PATTERN = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
URL_PATTERN = r'https?://[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}[/\w.-]*'
PHONE_PATTERN = r'\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}'
TIME_PATTERN = r'\d{1,2}:\d{2}\s?(?:AM|PM|am|pm)?'
HASHTAG_PATTERN = r'#[A-Za-z0-9_]+'

# VALIDATION FUNCTIONS

def is_valid_email(email):
    """
    Check if email looks reasonable.
    Rules:
    - Not too long (max 100 chars)
    - Has exactly one @
    - Domain has a dot
    """
    if len(email) > 100:
        return False
    if email.count('@') != 1:
        return False
    parts = email.split('@')
    if '.' not in parts[1]:  # Domain must have a dot
        return False
    return True


def is_valid_url(url):
    """
    Check if URL looks reasonable.
    Rules:
    - Not too long (max 200 chars)
    - Starts with http:// or https://
    """
    if len(url) > 200:
        return False
    if not url.startswith(('http://', 'https://')):
        return False
    return True


def is_valid_phone(phone):
    """
    Check if phone number has correct length.
    Rules:
    - Must have exactly 10 digits (US format)
    """
    # Remove all non-digit characters
    digits = re.sub(r'\D', '', phone)
    # US phone numbers have 10 digits
    return len(digits) == 10


def is_valid_time(time_str):
    """
    Check if time makes sense.
    Rules:
    - Hours: 0-23 (24-hour) or 1-12 (12-hour with AM/PM)
    - Minutes: 0-59
    """
    # Remove spaces and convert to uppercase for easier checking
    time_clean = time_str.replace(' ', '').upper()
    
    # Split by colon
    parts = time_clean.split(':')
    if len(parts) != 2:
        return False
    
    try:
        hours = int(parts[0])
        # Get minutes (might have AM/PM attached)
        minutes_str = parts[1].replace('AM', '').replace('PM', '')
        minutes = int(minutes_str)
    except ValueError:
        return False
    
    # Check minutes (always 0-59)
    if minutes < 0 or minutes > 59:
        return False
    
    # Check hours
    if 'AM' in time_clean or 'PM' in time_clean:
        # 12-hour format: 1-12
        if hours < 1 or hours > 12:
            return False
    else:
        # 24-hour format: 0-23
        if hours < 0 or hours > 23:
            return False
    
    return True


def is_valid_hashtag(hashtag):
    """
    Check if hashtag is reasonable.
    Rules:
    - Length: 2-50 characters (including #)
    - Not all numbers
    """
    if len(hashtag) < 2 or len(hashtag) > 50:
        return False
    # Remove # and check content
    content = hashtag[1:]
    # Can't be all digits
    if content.isdigit():
        return False
    return True

#EXTRACTION FUNCTION
def extract_data(text):
    """
    Extract all data types from text.
    
    Returns a dictionary with:
    - Valid items for each data type
    - Count of rejected items
    """
    results = {
        'emails': [],
        'urls': [],
        'phones': [],
        'times': [],
        'hashtags': []
    }
    
    rejected = {
        'emails': 0,
        'urls': 0,
        'phones': 0,
        'times': 0,
        'hashtags': 0
    }
    
    # Extract emails
    print("Searching for emails...")
    for match in re.findall(EMAIL_PATTERN, text):
        if is_valid_email(match):
            results['emails'].append(match)
        else:
            rejected['emails'] += 1
    
    # Extract URLs
    print("Searching for URLs...")
    for match in re.findall(URL_PATTERN, text):
        if is_valid_url(match):
            results['urls'].append(match)
        else:
            rejected['urls'] += 1
    
    # Extract phone numbers
    print("Searching for phone numbers...")
    for match in re.findall(PHONE_PATTERN, text):
        if is_valid_phone(match):
            results['phones'].append(match)
        else:
            rejected['phones'] += 1
    
    # Extract times
    print("Searching for times...")
    for match in re.findall(TIME_PATTERN, text):
        if is_valid_time(match):
            results['times'].append(match)
        else:
            rejected['times'] += 1
    
    # Extract hashtags
    print("Searching for hashtags...")
    for match in re.findall(HASHTAG_PATTERN, text):
        if is_valid_hashtag(match):
            results['hashtags'].append(match)
        else:
            rejected['hashtags'] += 1
    
    # Remove duplicates from each list
    for key in results:
        results[key] = list(dict.fromkeys(results[key]))
    
    return results, rejected

# DISPLAY FUNCTION

def display_results(results, rejected):
    """
    Print results in a nice format.
    """
    print("\n" + "." * 60)
    print("EXTRACTION RESULTS")
    print("." * 60 + "\n")
    
    # Display emails
    print(f"EMAILS: {len(results['emails'])} found ({rejected['emails']} rejected)")
    if results['emails']:
        for i, email in enumerate(results['emails'], 1):
            print(f"   {i}. {email}")
    else:
        print("   (none found)")
    print()
    
    # Display URLs
    print(f"URLs: {len(results['urls'])} found ({rejected['urls']} rejected)")
    if results['urls']:
        for i, url in enumerate(results['urls'], 1):
            print(f"   {i}. {url}")
    else:
        print("   (none found)")
    print()
    
    # Display phone numbers
    print(f"PHONE NUMBERS: {len(results['phones'])} found ({rejected['phones']} rejected)")
    if results['phones']:
        for i, phone in enumerate(results['phones'], 1):
            print(f"   {i}. {phone}")
    else:
        print("   (none found)")
    print()
    
    # Display times
    print(f"TIMES: {len(results['times'])} found ({rejected['times']} rejected)")
    if results['times']:
        for i, time in enumerate(results['times'], 1):
            print(f"   {i}. {time}")
    else:
        print("   (none found)")
    print()
    
    # Display hashtags
    print(f"HASHTAGS: {len(results['hashtags'])} found ({rejected['hashtags']} rejected)")
    if results['hashtags']:
        for i, hashtag in enumerate(results['hashtags'], 1):
            print(f"   {i}. {hashtag}")
    else:
        print("   (none found)")
    print()
    
    # Summary
    print("." * 60)
    print("SUMMARY")
    print("." * 60)
    total_valid = sum(len(v) for v in results.values())
    total_rejected = sum(rejected.values())
    print(f"Total valid items: {total_valid}")
    print(f"Total rejected items: {total_rejected}")
    print("." * 60)


#MAIN PROGRAM

def main():
    """
    Main function - runs the entire program.
    """
    print("\n" + "." * 60)
    print("REGEX DATA EXTRACTION PROGRAM")
    print("." * 60 + "\n")
    
    # Try to read from file
    filename = 'input.txt'
    
    try:
        with open(filename, 'r') as file:
            text = file.read()
        print(f"Loaded text from '{filename}'\n")
        
    except FileNotFoundError:
        # Use default sample if file not found
        print(f"'{filename}' not found. Using default sample text.\n")
        text = """
            Hi everyone!

            Meeting scheduled for 2:30 PM tomorrow or 14:30 on Thursday.
            Alternative times: 9:00 AM, 11:45 AM, 3:15 PM

            Contact Information:
            - John Smith: john.smith@example.com, (555) 123-4567
            - Sarah Jones: sarah@company.co.uk, 555-987-6543
            - Mike Davis: mike.davis@testmail.org, 555.111.2222

            Resources:
            https://www.example.com/meeting
            https://docs.google.com/presentation
            http://company-site.org/resources

            Social Media:
            #TechConference2024 #Innovation #Python #DataScience

            Invalid Examples (should be rejected)
            Bad email: notanemail@
            Bad phone: 123-456 (too short)
            Bad time: 25:99
            Bad hashtag: #123 (only numbers)
        """
    
    # Show input text
    print("Input Text:")
    print("." * 60)
    print(text)
    print("." * 60 + "\n")
    
    # Extract data
    print("Starting extraction...\n")
    results, rejected = extract_data(text)
    print("\nExtraction complete!\n")
    
    # Display results
    display_results(results, rejected)
    
    print("\nProgram finished successfully!")

# RUN
if __name__ == "__main__":
    main()