#!/usr/bin/env python3
"""
Batch Uploader to the Macquarie University Research Data Repository 
"""

__author__ = "Gerry Devine"
__version__ = "0.1.0"
__license__ = "MIT"


import sys
import numpy as np
import requests
import getpass
import pandas as pd


# Set Base URL 
BASE_URL = "https://api.figsh.com/v2"


def read_records_file(records_file):
    """ Read and return a dataframe from a supplied metadata csv file
    
    """
    if records_file.endswith('.csv'):
        df = pd.read_csv(records_file)
    else: 
        sys.exit('File extension is not recognised')

    return df


def verify_metadata(df):
    """ Verify that the supplied metadata file is valid 

    """
    # Check that mandatory column headings are present
    col_headings = df.columns.values
    requireds = ['Title', 'Authors', 'Categories', 'Item type', 'Keywords', 'Description', 'License', 'Data Sensitivity', 'RDR Project ID']
    result =  all(elem in col_headings for elem in requireds)
    if not result:
        print('Error: You must supply all mandatory column headings')
        sys.exit()


    # Check that values exist for each of the mandatory fields
    for index, row in df.iterrows():
        if row['Title'] == '' or row['Title'] is None or row['Title'] is np.NaN:
            print(f"Title is missing on row {index+1}")
            sys.exit()
        if row['Authors'] == '' or row['Authors'] is None or row['Authors'] is np.NaN:
            print(f"Authors is missing on row {index+1}")
            sys.exit()
        if row['Categories'] == '' or row['Categories'] is None or row['Categories'] is np.NaN:
            print(f"Categories is missing on row {index+1}")
            sys.exit()
        if row['Item type'] == '' or row['Item type'] is None or row['Item type'] is np.NaN:
            print(f"Item type is missing on row {index+1}")
            sys.exit()
        if row['Keywords'] == '' or row['Keywords'] is None or row['Keywords'] is np.NaN:
            print(f"Keywords is missing on row {index+1}")
            sys.exit()
        if row['Description'] == '' or row['Description'] is None or row['Description'] is np.NAN:
            print(f"Description is missing on row {index+1}")
            sys.exit()
        if row['License'] == '' or row['License'] is None or row['License'] is np.NAN:
            print(f"License is missing on row {index+1}")
            sys.exit()
        if row['Data Sensitivity'] == '' or row['Data Sensitivity'] is None or row['Data Sensitivity'] is np.NAN:
            print(f"Data Sensitivity is missing on row {index+1}")
            sys.exit()
        if row['RDR Project ID'] == '' or row['RDR Project ID'] is None or row['RDR Project ID'] is np.NAN:
            print(f"RDR Project ID is missing on row {index+1}")
            sys.exit()
    

def get_token():
    """ Request User RDR API token and return as a header

    """
    token = getpass.getpass('Paste in your RDR API token and press Enter:')
    return {'Authorization': 'token ' + token}


def get_authors(authors):
    structured_authors = []
    
    split_authors = authors.split(';')
    for author in split_authors:
        new_author = {}
        new_author['name']=author
        structured_authors.append(new_author)

    return structured_authors  


def get_categories(categories):
    structured_categories = []
    
    split_categories = categories.split(';')
    for category in split_categories:
        structured_categories.append(int(category))

    return structured_categories  


def get_keywords(keywords):
    structured_keywords = []
    
    split_keywords = keywords.split(';')
    for keyword in split_keywords:
        structured_keywords.append(keyword)

    return structured_keywords  


def get_references(references):
    structured_references = []
    
    split_references = references.split(';')
    for reference in split_references:
        structured_references.append(reference)

    return structured_references  

def get_qalogs(qalogs):
    structured_qalogs = []
    
    split_qalogs = qalogs.split(';')
    for qalog in split_qalogs:
        structured_qalogs.append(qalog)

    return structured_qalogs  


def build_data_object(record):
    # Clean for empty cells (ignoring mandatory fields picked up in validation)
    # Resource Title
    if record['Resource Title'] is np.NAN:
        cleaned_resource_title = ''
    else: 
        cleaned_resource_title = record['Resource Title']
    # Resource DOI
    if record['Resource DOI'] is np.NAN:
        cleaned_resource_doi = ''
    else: 
        cleaned_resource_doi = record['Resource DOI']
    # FAIR Self Assessment Rating
    if record['FAIR Self Assessment Rating'] is np.NAN:
        cleaned_fair_self_assessment_rating = ''
    else: 
        cleaned_fair_self_assessment_rating = record['FAIR Self Assessment Rating']
    # FAIR Self Assessment Summary
    if record['FAIR Self Assessment Summary'] is np.NAN:
        cleaned_fair_self_assessment_summary = ''
    else: 
        cleaned_fair_self_assessment_summary = record['FAIR Self Assessment Summary']
    # Research Project ID
    cleaned_research_project_id = str(record['Research Project ID'])
  
    # Get structured list of authors
    structured_authors = get_authors(record['Authors'])

    # Get structured list of authors
    structured_keywords = get_keywords(record['Keywords'])

    # Get structured list of references
    structured_references = get_references(record['References'])

    # Get structured list of categories
    structured_categories = get_categories(record['Categories'])

    # Get structured list of Q/A Logs
    structured_qalogs = get_qalogs(record['Q/A Log'])

    return {
        "title": record['Title'],
        "description": record['Description'],
        "funding": record['Funding'],
        "authors":structured_authors,
        "keywords":structured_keywords,
        "references":structured_references,
        "categories":structured_categories,
        "resource_doi": cleaned_resource_doi,
        "resource_title": cleaned_resource_title,
        "custom_fields": {
            "Research Project ID": cleaned_research_project_id,
            "Q/A Log": structured_qalogs,
            "Research Project URL": record['Research Project URL'],
            "Data Sensitivity": [record['Data Sensitivity']],
            "FAIR Self Assessment Rating": [cleaned_fair_self_assessment_rating],
            "FAIR Self Assessment Summary": cleaned_fair_self_assessment_summary,
        },
        "defined_type": record['Item type'],
        "license": record['License'],
    }


def upload_record(data, headers, rdr_project_id):
    """ Upload a supplied record to the research data repository
    
    """
    request_url = f"https://api.figsh.com/v2/account/projects/{rdr_project_id}/articles"
    response = requests.post(request_url, headers=headers, json=data)

    return response.json()


def main():
    """ Main function 
    
    """
    # Read metadata excel or csv file into dataframe
    records_file = sys.argv[1]

    df = read_records_file(records_file)

    # Verify that the supplied records file record contents are valid
    verify_metadata(df)

    # Get auth token
    headers = get_token()

    # Iterate over each record row and upload record to the RDR
    for index, record in df.iterrows():
        data = build_data_object(record)
        # Pull out the RDR project ID to populate the URL
        rdr_project_id = record['RDR Project ID']
        # Upload the record to the RDR
        uploaded_record = upload_record(data, headers, rdr_project_id)
        print(uploaded_record)

    print('')
    print('Complete!')


if __name__ == "__main__":
    """ This is executed when run from the command line 
    
    """
    # Check that a file was supplied
    if len(sys.argv) != 2:
        print('Error: You need to supply a .csv file')
        sys.exit()

    main()