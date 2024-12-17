# Related Libraries
import pandas as pd
import numpy as np
from urllib.parse import urlparse
import socket
import tldextract

# Handling Features Missing Values Modules

class FeaturesMissingHandler:
    # Class to Handling Missing Values
    def __init__(self,df,remove_missing= True,col_rem_val = None):
        '''
        Instantiate the class
        Parameter:
            df  : dataframe to handle
            remove_missing  : hyperparameter if you want to handle the missing values by removing it
            col_rem_val     : choose columns from df to get remove_missing
        
        '''
        self.df = df
        self.handled_col = col_rem_val 
        if remove_missing:
            self.remove_missing_values()
        change_type(self.df,'URL','str')
        self.handling_missing_values()

    # Handling missing values by removing it
    def remove_missing_values(self):
        for col in self.handled_col:
            self.df = remove_by_idx(self.df,col)

    # Handling missing values 
    def handling_missing_values(self):
        self.df['Domain'] = self.df['Domain'].apply(lambda x: extract_domain(x))
        self.df['DomainLength'] = self.df['Domain'].apply(lambda x: domain_length(x))
        self.df['URLLength']= self.df['URL'].apply(lambda x: url_length(x))
        self.df['IsDomainIP'] = self.df['URL'].apply(lambda x: is_domain_ip(x) )
        self.df['IsHTTPS'] = self.df['URL'].apply(lambda x: isHttps(x))
        self.df['NoOfSubDomain'] = self.df['URL'].apply(lambda x: count_subdomains(x))
        self.df['TLD'] = self.df['URL'].apply(lambda x: extract_tld(x))


    
    
# Functions to handling Missing Values
def change_type(df, col, new_type):
    """
    Change the type of a specified column while handling missing values.
    input:
        df  : dataframe
        col : column name to remove
        new_type    : the new dtype
    output :
        df  : with newest dtypes for each columns
    """
    if col not in df.columns:
        raise ValueError(f"Column '{col}' does not exist in the DataFrame")
    try:
        df[col] = df[col].astype(new_type, errors='ignore')  # Keep errors=ignore to handle NaNs properly
    except Exception as e:
        print(f"Error converting column '{col}' to {new_type}: {e}")
    return df

def remove_by_idx(df,col):
    """
    Function to removes row by index of a certain column

    input:
        df  : dataframe
        col : str
        idx : Index
    output  : dataframe without dropped index
    """
    drop_idx = df[df[col].isna()].index
    df = df.drop(index=drop_idx)

    return df

def is_domain_ip(url):
    '''
    Function to distinct whether the url is using IP Address or domain
    input:
        url : str
    output:
        boolean : True jika URL merupakan IP Address, False jika URL bukan IP Address
    '''
    domain = extract_domain(url)
    if pd.isna(domain):
        return False
    try:
        domain = domain.split(":")[0]  
        socket.inet_aton(domain)  
        return True
    except socket.error:
        return False  

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
    print(f'extracted : {extracted} \n')
    print(f'extracted domain : {extracted.domain} \n')
    return extracted.domain

    

def extract_tld(url):
    '''
    Function to extract Top Level Domain of the URL
    input:
        URL : str
    output:
        tld : str
    '''
    if pd.isna(url):
        return np.nan
    extracted = tldextract.extract(url)
    return extracted.suffix


def isHttps(url):
    '''
    Function to check whether the url using HTPPS or not
    input:
        URL : str
    output:
        Boolean : True jika url menggunakan HTTPS, False jika url tidak menggunakan HTTPS
    
    '''
    if isinstance(url,str):
        return url.lower().startswith('https://')
    return False

def count_subdomains(url):
    '''
    Function to count subdomain that domain has
    input:
        domain  : str
    output:
        count_subdomain : int
    '''
    extracted = tldextract.extract(url)
    subdomain = extracted.subdomain
    
    if subdomain:
        count_subdomains = len(subdomain.split('.'))
    else:
        count_subdomains = 0
    return count_subdomains


def url_length(url):
    if pd.isna(url):
        return 0
    else:
        return len(url)

def domain_length(domain):
    if pd.isna(domain):
        return 0
    else:
        return len(domain)    
    

# Handling Outliers
