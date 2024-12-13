# Related Libraries
import pandas as pd
import numpy as np
from urllib.parse import urlparse
import socket
import tldextract

# Handling Features Missing Values Modules

class FeaturesMissingHandler:
    # Class to Handling Missing Values
    def __init__(self,df):
        self.df = df


# Functions to handling Missing Values

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
    else:
        parsed = urlparse(url)
        domain =  parsed.netloc
        if domain.startswith('www.'):
            domain = domain[:4]
        return domain
    

def extract_tld(url):
    '''
    Function to extract Top Level Domain of the URL
    input:
        URL : str
    output:
        tld : str
    '''
    if pd.isna(url):
        return url
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

def count_subdomains(domain):
    '''
    Function to count subdomain that domain has
    input:
        domain  : str
    output:
        count_subdomain : int
    '''
    extracted = tldextract.extract(domain)
    return len(extracted.subdomain.split('.')) if extracted.subdomain else 0


    
    