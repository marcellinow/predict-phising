import pandas as pd
import numpy as np
import re
import urllib.parse
from unidecode import unidecode
import Levenshtein
import socket
import tldextract

class FeaturesManipulation:
    def __init__(self,df):
        '''
        Instantiate the class
        Parameter:
            df  : dataframe to handle
        
        '''
        self.df = df

        def features_manipulation(self):
            self.df['TLDMajorLegit'] = self.df['TLD']


def extract_domain(url):
    '''
    Function to extract domain from url
    input:
        URL : str
    output:
        domain : str
    '''
    if pd.isna(url):
        return np.nan
    extracted = tldextract.extract(url)
    # print(f'extracted : {extracted} \n')
    # print(f'extracted domain : {extracted.domain} \n')
    return extracted.domain

def get_tld_counts(df,tld,label='label'):
    '''
    Function to count how much the phising (label == 0) certain tld
    input:
        df  : df
        tld : str
        label   : 'label'
    output:
        count_0 : how much the label 0
        count_1 : how much the label 1
    '''
    count_0 = len(df[(df['TLD'] == tld) & (df[label] == 0)])
    count_1 = len(df[(df['TLD'] == tld) & (df[label] == 1)])
    return count_0, count_1

def column_major_legit(df,column,label='label'):
    '''
    Function to check the majority of a certain column is legit or phising (based on amount of label).
    If amount of label 0 > amount of label 1, then the column is majority phising
    input:
        df  : dataframe
        column  : column name (only accept one column)
        label:  'label'
    output:
        column  : with value 1 (majority legit), 0 (majority phising)
    '''
    if len(column) > 1:
        raise ValueError("Only one column name should be provided")
    df.groupby(column)[label].value_counts().unstack(fill_value=0)
    col_counts = df.groupby(column)[label].value_counts().unstack(fill_value=0)
    col_name = f'{column}MajorityLegit'
    col_counts[col_name] = col_counts[0] > col_counts[1]
    col_counts[col_name] = col_counts['TLDMajoritylegitimate'].map({True: 0, False: 1})
    df = df.merge(col_counts[[col_name]],on=column,how='left')
    return df

def has_obfuscation(df,url):
    '''
    Function to check whether the URL contains obfuscated method inside of it
    input:
        df  : dataframe
        url : str
    output:
        boolean : whether the url has obfuscation or not, 1: True it does have an obfsucation, 0: False it doesn't have an obfiscaton
    '''

    decoded_url = urllib.parse.unquote(url) # buat ngecek si urlnya ada pen-encode-an
    if decoded_url != url:
        return True
    
    normalized_url = unidecode(url)

    if normalized_url != url:
        return True
    
    if len(url) > 100:
        return True
    
    if re.search(r'\b[a-fA-F0-9]{32}\b|\b[a-fA-F0-9]{40}\b', url): # pake hashing atau ngga
        return True
    
    if count_subdomains(url) > 3:
        return True
    

    # Algorithm to find a major legit domain based on the tld counts
    legit_domains = []
    for tld in df['TLD'].unique():
        count_0, count_1 = get_tld_counts(df,tld)
        if count_0 > count_1:
            domains_tld = df[df['TLD'] == tld]['Domain'].tolist()
            legit_domains.extend(domains_tld)
    domain = extract_domain(url)
    if domain in legit_domains:
        return False
    return True

def count_subdomains(url):
    '''
    Function to count the number of subdomains in a URL
    Args:
        url (str): The URL to evaluate
    Returns:
        int: The count of subdomains
    '''
    
    domain = urlparse(url).hostname  
    if domain:
        parts = domain.split('.')
        
        return max(0, len(parts) - 2)
    return 0  