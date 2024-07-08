from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from OpenAssistant import OpenAssistant
import csv
from tqdm import tqdm

def read_vocabulary_codes(csv_file_path):
    vocabulary_codes = []
    with open(csv_file_path, mode='r', newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for row in reader:
            if len(row) >= 3:
                vocabulary = row[0]
                code = row[1]
                vocabulary_codes.append((vocabulary, code))
    return vocabulary_codes

def add_classification_column(input_csv_file, output_csv_file, classifications):
    with open(input_csv_file, mode='r', newline='') as csvfile:
        reader = list(csv.reader(csvfile, delimiter=','))
        
        # Add the classification column header
        if reader:
            reader[0].append('classification')
        
        # Add the classification values to each row
        for i, row in enumerate(reader[1:]):
            if i < len(classifications):
                row.append(classifications[i])
            else:
                row.append('')  # If classifications list is shorter than the number of rows

    with open(output_csv_file, mode='w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=',')
        writer.writerows(reader)

codes = read_vocabulary_codes("./CodesWithPPIPotential.csv")

# Initialize the Chrome driver
driver = webdriver.Chrome()  # or specify the path like: webdriver.Chrome('/path/to/chromedriver')
results = []
for vocab, code in tqdm(codes[1:]):
    try:
        # URL of the website
        url = f"https://athena.ohdsi.org/search-terms/terms?vocabulary={vocab}&page=1&pageSize=15&query=49436004"
        print(url)

        # Open the website
        driver.get(url)
        time.sleep(3)

        # Locate the first element link
        first_element = driver.find_element(By.CLASS_NAME, "ac-table__cell.at-search-results__name-td").find_element(By.CLASS_NAME, "ac-link.ac-table-cell-link")

        # Get the link
        first_element_link = first_element.get_attribute("href")

        # Open the webpage
        driver.get(first_element_link)

        # Wait for the page to fully load
        time.sleep(3)  # Adjust the sleep time if necessary

        # Extract data from tbody
        tbody = driver.find_element(By.TAG_NAME, 'tbody')
        rows = tbody.find_elements(By.TAG_NAME, 'tr')
        tbody_data = []
        for row in rows:
            cols = row.find_elements(By.TAG_NAME, 'td')
            cols = [ele.text.strip() for ele in cols]
            tbody_data.append(cols)

        # Extract data from span
        spans = driver.find_elements(By.TAG_NAME, 'span')
        span_data = [span.text.strip() for span in spans if span.text.strip()]

        # Format and print the extracted data
        table = f"{'Relationship':<40} {'attribute Name':<40} {'attribute ID':<15} {'Vocabulary':<15}" + "\n" + "="*110
        for item in tbody_data:
            table += f"\n{item[0]:<40} {item[1]:<40} {item[2]:<15} {item[3]:<15}"

        # Extract data from spans within "ac-panel" elements
        panel = driver.find_element(By.CLASS_NAME, 'ac-panel__content')
        spans = panel.find_elements(By.TAG_NAME, 'span')
        spans_text = [span.text.strip() for span in spans]
        spans_text = " ".join([x.replace("\n", " ") for x in spans_text if x != ""])

        print(table)

        assistant = OpenAssistant(model="llama3")
        results.append(assistant.classify_code(table))
        break
    except Exception as e:
        print(e)
        results.append(None)
        
    
# Close the driver
driver.quit()
add_classification_column("./CodesWithPPIPotential.csv", "./classified.csv", results)