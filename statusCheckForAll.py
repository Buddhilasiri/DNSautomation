import pandas as pd
import requests
import concurrent.futures

# File paths (update these for your local machine)
file1 = "SiteStatusCheck/################.csv"
file2 = "SiteStatusCheck//################.csv"

# Function to extract the domain name
def extract_domain(entry):
    if isinstance(entry, str):
        return entry.split()[0].rstrip('.')  # Extract the first part & remove trailing period
    return None

# Function to check if a domain is actually working via HTTP(S)
def check_http_status(domain):
    for scheme in ["http", "https"]:  # Try both HTTP and HTTPS
        url = f"{scheme}://{domain}"
        try:
            response = requests.get(url, timeout=5, allow_redirects=True)
            if response.status_code == 200:
                return "Working"  # If either HTTP or HTTPS works, it's "Working"
        except requests.RequestException:
            continue  # Try the next scheme if this one fails
    return "Not Working"

# Load CSV files
df1 = pd.read_csv(file1)
df2 = pd.read_csv(file2)

# Extract unique domain names
df1["Cleaned_Domain"] = df1[df1.columns[0]].apply(extract_domain)
df2["Cleaned_Domain"] = df2[df2.columns[0]].apply(extract_domain)

unique_domains_1 = df1["Cleaned_Domain"].dropna().unique()
unique_domains_2 = df2["Cleaned_Domain"].dropna().unique()

# Use multithreading to speed up HTTP checks
def check_domains_multithreaded(domains):
    results = {}
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        future_to_domain = {executor.submit(check_http_status, domain): domain for domain in domains}
        for future in concurrent.futures.as_completed(future_to_domain):
            domain = future_to_domain[future]
            try:
                results[domain] = future.result()
            except Exception:
                results[domain] = "Not Working"
    return results

# Run HTTP(S) checks in parallel
df1_results = pd.DataFrame({"Domain": unique_domains_1})
df1_results["Status"] = df1_results["Domain"].map(check_domains_multithreaded(unique_domains_1))

df2_results = pd.DataFrame({"Domain": unique_domains_2})
df2_results["Status"] = df2_results["Domain"].map(check_domains_multithreaded(unique_domains_2))

# Save results to an Excel file
output_file = "domain_http_https_check_results.xlsx"
with pd.ExcelWriter(output_file, engine="openpyxl") as writer:
    df1_results.to_excel(writer, sheet_name="################.", index=False)
    df2_results.to_excel(writer, sheet_name="################.", index=False)

print(f"Results saved to: {output_file}")
