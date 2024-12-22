import pandas as pd
import numpy as np
import re
import urllib
from urllib.parse import urlparse
from unidecode import unidecode
import tldextract

class FeaturesManipulation:
    def __init__(self,df):
        '''
        Instantiate the class
        Parameter:
            df  : dataframe to handle
        
        '''
        self.df = df
        self.features_manipulation()
    def features_manipulation(self):
        self.df = column_major_legit(self.df, 'TLD', merge=True)
        legit_domains = column_major_legit(self.df, 'Domain',merge=False)
        self.df['HasObfuscation'] = self.df['URL'].apply(lambda x: has_obfuscation(x,legit_domains=legit_domains))

def extract_domain(url):
    '''
    Function to extract domain from url
    input:
        URL : str
    output:
        domain : str
    '''
    # print(f"extract domain\n")
    if pd.isna(url):
        return np.nan
    extracted = tldextract.extract(url)
    # print(f'extracted : {extracted} \n')
    # print(f'extracted domain : {extracted.domain} \n')
    return extracted.domain

def get_tld_counts(df, tld, label='label'):
    '''
    Function to count how much the phishing (label == 0) certain TLD
    input:
        df  : DataFrame
        tld : str
        label : str
    output:
        count_0 : int
        count_1 : int
    '''
    if 'TLD' not in df.columns or label not in df.columns:
        raise ValueError("DataFrame must contain 'TLD' and '{}' columns".format(label))

    tld_counts = df[df['TLD'] == tld][label].value_counts()
    count_0 = tld_counts.get(0, 0)
    count_1 = tld_counts.get(1, 0)
    
    return count_0, count_1

def column_major_legit(df, column, label='label', merge=False):
    '''
    Function to check the majority of a certain column is legit or phishing (based on amount of label).
    If amount of label 0 > amount of label 1, then the column is majority phishing.
    input:
        df     : dataframe
        column : column name (only accept one column)
        label  : label column name
        merge  : boolean, if True, merge the result back to the original dataframe
    output:
        If merge is False, return list of columns name with majority legitimate link.
        If merge is True, return the original dataframe with the new column added.
    '''
    if column not in df.columns or label not in df.columns:
        raise ValueError(f"DataFrame must contain '{column}' and '{label}' columns")
    
    # print("entering algorithm to find majority legitimate columns")
    col_counts = df.groupby(column)[label].value_counts().unstack(fill_value=0)
    col_name = f'{column}MajorityLegit'
    col_counts[col_name] = col_counts[0] < col_counts[1]
    col_counts[col_name] = col_counts[col_name].map({True: 0, False: 1})
    # print("DONE\n")
    
    if merge:
        df = df.merge(col_counts[[col_name]], on=column, how='left')
        return df
    else:
        return col_counts[col_counts[col_name] == 0].index.to_list()

def has_obfuscation(url, legit_domains):
    '''
    Function to check whether the URL contains obfuscated method inside of it
    input:
        url : str
        legit_domains : list of legitimate domains
    output:
        boolean : whether the url has obfuscation or not, 1: True it does have an obfuscation, 0: False it doesn't have an obfuscation
    '''
    decoded_url = urllib.parse.unquote(url)
    if decoded_url != url:
        return True

    normalized_url = unidecode(url)
    if normalized_url != url:
        return True

    if len(url) > 100:
        return True

    if re.search(r'\b[a-fA-F0-9]{32}\b|\b[a-fA-F0-9]{40}\b', url):
        return True

    if count_subdomains(url) > 3:
        return True

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