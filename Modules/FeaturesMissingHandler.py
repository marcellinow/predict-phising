# Libraries to handle missing values on the dataset link phising features

# Related Libraries
import pandas as pd
import numpy as np
import re

from unidecode import unidecode
from urllib.parse import urlparse
import socket
import tldextract

# Handling Features Missing Values Modules

class FeaturesMissingHandler:
    # Class to Handling Missing Values
    def __init__(self,df):
        '''
        Instantiate the class
        Parameter:
            df  : dataframe to handle
            
        '''
        self.df = df
        
        # Handling missing values by removing the missing values from the rows (default is URL)
        # if remove_missing:
        # Extract element url related properly
        self.url_handler()
        self.df['Domain'] = self.df['URL'].apply(lambda x: extract_domain(x))
        self.df['TLD'] = self.df['URL'].apply(lambda x: extract_tld(x))
        # Handling missing values by fixing it
        self.handling_missing_values()
        self.features_engineering()


    def url_handler(self):
        # Hitung URL yang paling sering muncul (modus)
        most_common_url = self.df['URL'].mode()[0] if not self.df['URL'].isna().all() else ''
        
        # Iterasi melalui setiap baris untuk memeriksa URL dan Domain
        self.df['URL'] = self.df.apply(
            lambda row: row['Domain'] if pd.isna(row['URL']) and pd.notna(row['Domain']) else
                        most_common_url if pd.isna(row['URL']) and pd.isna(row['Domain']) else row['URL'],
            axis=1
        )
        return self.df



        
    # Handling missing values 
    def handling_missing_values(self):

        self.df['DomainLength'] = self.df['Domain'].apply(lambda x: domain_length(x))
        self.df['URLLength']= self.df['URL'].apply(lambda x: url_length(x))
        self.df['IsDomainIP'] = self.df['URL'].apply(lambda x: is_domain_ip(x) )
        self.df['IsHTTPS'] = self.df['URL'].apply(lambda x: isHttps(x))
        self.df['NoOfSubDomain'] = self.df['URL'].apply(lambda x: count_subdomains(x))
        self.df['CharContinuationRate'] = self.df['URL'].apply(char_continuation_rate)
        self.df['TLDLength'] = self.df['TLD'].apply(lambda x: tld_length(x))
        self.df['NoOfLettersInURL'] = self.df['URL'].apply(count_letters)
        self.df['LetterRatioInURL'] = self.df['URL'].apply(calc_letter_ratio)
        self.df['NoOfDigitsInURL'] = self.df['URL'].apply(count_digits)
        self.df['DigitRatioInURL'] = self.df['URL'].apply(calc_digit_ratio)
        self.df['NoOfEqualsInURL'] = self.df['URL'].apply(count_equals)
        self.df['NoOfQMarkInURL'] = self.df['URL'].apply(count_qmark)
        self.df['NoOfAmpersandInURL'] = self.df['URL'].apply(count_ampersand)
        self.df['NoOfOtherSpecialCharsInURL'] = self.df['URL'].apply(count_special_chars)
        self.df['SpecialCharRatioInURL'] = self.df['URL'].apply(calc_spacial_char_ratio)
        self.df['HasTitle'] = self.df['Title'].apply(hastitle)
    def features_engineering(self):# Feature Engineering
        self.df['WebComplexity'] = web_complexity(self.df)
        self.df['RefLinksCount'] = ref_links_count(self.df)
        self.df['LinkMatchScore'] = link_match_score(self.df)
        self.df['HasFinanceTransaction'] = financial_transaction(self.df)


        

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
    # print(f'extracted : {extracted} \n')
    # print(f'extracted domain : {extracted.domain} \n')
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



def url_length(url):
    if pd.isna(url):
        return 0
    else:
        return len(url)
def tld_length(tld):
    if pd.isna(tld):
        return 0
    else:
        return len(tld)
def domain_length(domain):
    if pd.isna(domain):
        return 0
    else:
        return len(domain)    

def char_continuation_rate(url):
    '''
    Function to count rate of char continuation of url
    input:
        url : str
    output:
        char_contination_rate   : float
    '''
    if not isinstance(url, str):  
        return 0  
    
    cleaned_url = re.sub(r'[^a-zA-Z0-9]', '', url)
    
    continuation_count = 0

    for i in range(1, len(cleaned_url)):
        if cleaned_url[i] == cleaned_url[i - 1]: 
            continuation_count += 1    

    char_continuation_rate = continuation_count / len(cleaned_url) if len(cleaned_url) > 0 else 0
    
    return char_continuation_rate



'''
Function to extract related information based on current column:
- NoOfLettersInURL
- LetterRatioInURL
- NoOfDigitsInURL
- DigitRatioInURL
- NoOfEqualsInURL
- OfOFQMarkInURL
- NoOFAmpersandInURL
- NoOfOtherSpecialCharsInURL
- SpecialCharRatioInURL
'''
def count_letters(url):
    if isinstance(url, str):  # Pastikan URL adalah string
        return len(re.findall(r'[a-zA-Z]', url))  # Menghitung jumlah huruf
    return 0  # Jika bukan string, return 0

def count_digits(url):
    if isinstance(url, str):  # Pastikan URL adalah string
        return len(re.findall(r'\d', url))  # Menghitung jumlah digit
    return 0  # Jika bukan string, return 0

def count_equals(url):
    if isinstance(url, str):  # Pastikan URL adalah string
        return url.count('=')  # Menghitung jumlah '='
    return 0  # Jika bukan string, return 0

def count_qmark(url):
    if isinstance(url, str):  # Pastikan URL adalah string
        return url.count('?')  # Menghitung jumlah '?'
    return 0  # Jika bukan string, return 0

def count_ampersand(url):
    if isinstance(url, str):  # Pastikan URL adalah string
        return url.count('&')  # Menghitung jumlah '&'
    return 0  # Jika bukan string, return 0

def count_special_chars(url):
    if isinstance(url, str):  # Pastikan URL adalah string
        special_chars = re.findall(r'[^a-zA-Z0-9\s]', url)  # Menghitung karakter selain alphanumeric dan spasi
        return len(special_chars)
    return 0  # Jika bukan string, return 0

def calc_spacial_char_ratio(url):
    if isinstance(url, str):  # Pastikan URL adalah string
        special_count = count_special_chars(url)
        return special_count / len(url) if len(url) > 0 else 0  # Rasio karakter khusus terhadap panjang URL
    return 0  # Jika bukan string, return 0

# Fungsi untuk menghitung rasio huruf dan angka
def calc_letter_ratio(url):
    if isinstance(url, str):  # Pastikan URL adalah string
        letter_count = count_letters(url)
        return letter_count / len(url) if len(url) > 0 else 0  # Rasio huruf terhadap panjang URL
    return 0  # Jika bukan string, return 0

def calc_digit_ratio(url):
    if isinstance(url, str):  # Pastikan URL adalah string
        digit_count = count_digits(url)
        return digit_count / len(url) if len(url) > 0 else 0  # Rasio angka terhadap panjang URL
    return 0  # Jika bukan string, return 0


def hastitle(title):
    if pd.isna(title):
        return 0
    return 1
# Features Engineer Function

def web_complexity(df):
    df['NoOfImage'] = df['NoOfImage'].fillna(0)
    df['NoOfCSS'] = df['NoOfCSS'].fillna(0)
    df['NoOfJS'] = df['NoOfJS'].fillna(0)
    return df['NoOfImage'] + df['NoOfCSS'] + df['NoOfJS']

def ref_links_count(df):
    df['NoOfSelfRef'] = df['NoOfSelfRef'].fillna(0)
    df['NoOfEmptyRef'] = df['NoOfEmptyRef'].fillna(0)
    df['NoOfExternalRef'] = df['NoOfExternalRef'].fillna(0)
    
    return df['NoOfSelfRef'] + df['NoOfEmptyRef'] + df['NoOfExternalRef']

def link_match_score(df):
    df['DomainTitleMatchScore'] = df['DomainTitleMatchScore'].fillna(0)
    df['URLTitleMatchScore'] = df['URLTitleMatchScore'].fillna(0)
    return (df['DomainTitleMatchScore'] + df['URLTitleMatchScore'])/2

def financial_transaction(df):
    df['Bank'] = df['Bank'].fillna(0)
    df['Pay'] = df['Pay'].fillna(0)
    df['Crypto'] = df['Crypto'].fillna(0)
    return df[['Bank', 'Pay', 'Crypto']].max(axis=1)