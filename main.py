import csv
import time
from typing import List, Tuple

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from tqdm import tqdm

from OpenAssistant import OpenAssistant

privacy_accepted = False

def read_vocabulary_codes(csv_file_path: str) -> List[Tuple[str, str]]:
    """
    Read vocabulary codes from a CSV file.

    Args:
        csv_file_path (str): Path to the CSV file containing vocabulary codes.

    Returns:
        List[Tuple[str, str]]: A list of tuples containing (vocabulary, code).
    """
    vocabulary_codes = []
    with open(csv_file_path, mode='r', newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # Skip header row
        for row in reader:
            if len(row) >= 2:
                vocabulary, code = row[:2]
                vocabulary_codes.append((vocabulary, code))
    return vocabulary_codes

def add_classification_column(input_csv_file: str, output_csv_file: str, classifications: List[str]):
    """
    Add a classification column to the input CSV file and write to a new output file.

    Args:
        input_csv_file (str): Path to the input CSV file.
        output_csv_file (str): Path to the output CSV file.
        classifications (List[str]): List of classifications to add.
    """
    with open(input_csv_file, mode='r', newline='', encoding='utf-8') as infile, \
         open(output_csv_file, mode='w', newline='', encoding='utf-8') as outfile:
        reader = csv.reader(infile)
        writer = csv.writer(outfile)

        header = next(reader)
        writer.writerow(header + ['classification'])

        for row, classification in zip(reader, classifications):
            writer.writerow(row + [classification])

def scrape_athena_data(vocab: str, code: str, driver: webdriver.Chrome) -> Tuple[str, str]:
    """
    Scrape data from the Athena website for a given vocabulary and code.

    Args:
        vocab (str): Vocabulary name.
        code (str): Code to search for.
        driver (webdriver.Chrome): Selenium WebDriver instance.

    Returns:
        Tuple[str, str]: A tuple containing the formatted table and span text.
    """
    global privacy_accepted
    url = f"https://athena.ohdsi.org/search-terms/terms?vocabulary={vocab}&page=1&pageSize=15&query={code}"
    driver.get(url)

    # Check for and accept privacy agreement if present
    if not privacy_accepted:
        agree_button = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Accept')]"))
        )
        agree_button.click()
        print(f"Clicked Accept button")
        privacy_accepted = True

    try:
        # Wait for the first element to be clickable
        first_element = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "ac-table__cell.at-search-results__name-td"))
        )
        first_element_link = first_element.find_element(By.CLASS_NAME, "ac-link.ac-table-cell-link").get_attribute("href")

        driver.get(first_element_link)
        time.sleep(3)

        # Extract data from tbody
        tbody = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'tbody')))
        rows = tbody.find_elements(By.TAG_NAME, 'tr')
        tbody_data = [
            [ele.text.strip() for ele in row.find_elements(By.TAG_NAME, 'td')]
            for row in rows
        ]

        # Format the extracted data
        table = f"{'Relationship':<40} {'Attribute Name':<40} {'Attribute ID':<15} {'Vocabulary':<15}\n" + "="*110
        for item in tbody_data:
            table += f"\n{item[0]:<40} {item[1]:<40} {item[2]:<15} {item[3]:<15}"

        # Extract data from spans within "ac-panel" elements
        panel = driver.find_element(By.CLASS_NAME, 'ac-panel__content')
        spans = panel.find_elements(By.TAG_NAME, 'span')
        spans_text = " ".join([span.text.strip().replace("\n", " ") for span in spans if span.text.strip()])

        return table, spans_text
    except (NoSuchElementException, TimeoutException) as e:
        print(f"Error scraping data for {vocab} {code}: {e}")
        return "", ""

def main():
    codes = read_vocabulary_codes("./CodesWithPPIPotential.csv")
    
    driver = webdriver.Chrome()  # Make sure to have chromedriver in PATH or specify the path
    assistant = OpenAssistant(model="llama3")
    results = []

    try:
        for vocab, code in tqdm(codes, desc="Processing codes"):
            try:
                table, spans_text = scrape_athena_data(vocab, code, driver)
                if table and spans_text:
                    print(table)
                    print(spans_text)
                    
                    classification = assistant.classify_code(table)
                    results.append(classification)
                else:
                    print(f"No data found for {vocab} {code}")
                    results.append(None)
            except Exception as e:
                print(f"Error processing {vocab} {code}: {e}")
                results.append(None)
    finally:
        driver.quit()

    add_classification_column("./CodesWithPPIPotential.csv", "./classified.csv", results)

if __name__ == "__main__":
    main()