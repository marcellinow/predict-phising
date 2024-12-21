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
            remove_missing  : hyperparameter if you want to handle the missing values by removing it
            col_rem_val     : choose columns from df to get remove_missing
        
        '''
        self.df = df
        
        self.handled_col = ['URL']  
        # Handling missing values by removing the missing values from the rows (default is URL)
        # if remove_missing:
        self.url_handler()
        self.df['Domain'] = self.df['Domain'].apply(lambda x: extract_domain(x))
        self.df['TLD'] = self.df['URL'].apply(lambda x: extract_tld(x))
        # Make sure the URL datatype is string
        # Extract element url related properly
        # Handling missing values by fixing it
        self.handling_missing_values()

    # Handling missing values by removing it
    def url_handler(self):
        for col in self.handled_col:
            self.df = remove_by_idx(self.df,col)
        change_type(self.df,'URL','str')

    # Handling missing values 
    def handling_missing_values(self):

        self.df['DomainLength'] = self.df['Domain'].apply(lambda x: domain_length(x))
        self.df['URLLength']= self.df['URL'].apply(lambda x: url_length(x))
        self.df['IsDomainIP'] = self.df['URL'].apply(lambda x: is_domain_ip(x) )
        self.df['IsHTTPS'] = self.df['URL'].apply(lambda x: isHttps(x))
        self.df['NoOfSubDomain'] = self.df['URL'].apply(lambda x: count_subdomains(x))
        self.df['CharContinuationRate'] = self.df['URL'].apply(char_continuation_rate)

        self.df['NoOfLettersInURL'] = self.df['URL'].apply(count_letters)
        self.df['LetterRatioInURL'] = self.df['URL'].apply(calc_letter_ratio)
        self.df['NoOfDigitsInURL'] = self.df['URL'].apply(count_digits)
        self.df['DigitRatioInURL'] = self.df['URL'].apply(calc_digit_ratio)
        self.df['NoOfEqualsInURL'] = self.df['URL'].apply(count_equals)
        self.df['NoOfQMarkInURL'] = self.df['URL'].apply(count_qmark)
        self.df['NoOfAmpersandInURL'] = self.df['URL'].apply(count_ampersand)
        self.df['NoOfOtherSpecialCharsInURL'] = self.df['URL'].apply(count_special_chars)
        self.df['SpecialCharRatioInURL'] = self.df['URL'].apply(calc_spacial_char_ratio)

        

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

'''
extract url elements stop here
'''



'''
Distinction


'''
# '''
# Fungsi sama tapi pake waktu aja biar gua tau 
# run lamanya di mana
# '''

# import pandas as pd
# import numpy as np
# import re
# import urllib.parse
# from unidecode import unidecode
# import Levenshtein
# import socket
# import tldextract
# import time

# class FeaturesMissingHandler:
#     def __init__(self, df):
#         self.df = df
#         self.handled_col = ['URL']
#         self.url_handler()
#         self.df['Domain'] = self.df['Domain'].apply(lambda x: extract_domain(x))
#         self.df['TLD'] = self.df['URL'].apply(lambda x: extract_tld(x))
#         self.handling_missing_values()

#     def url_handler(self):
#         print("Sedang mengerjakan fungsi url_handler")
#         start_time = time.time()
#         for col in self.handled_col:
#             self.df = remove_by_idx(self.df, col)
#         change_type(self.df, 'URL', 'str')
#         print(f"Fungsi url_handler selesai dalam {time.time() - start_time:.2f} detik")

#     def handling_missing_values(self):
#         print("Sedang mengerjakan fungsi handling_missing_values")
#         start_time = time.time()
#         self.df['DomainLength'] = self.df['Domain'].apply(lambda x: domain_length(x))
#         self.df['URLLength'] = self.df['URL'].apply(lambda x: url_length(x))
#         self.df['IsDomainIP'] = self.df['URL'].apply(lambda x: is_domain_ip(x))
#         self.df['IsHTTPS'] = self.df['URL'].apply(lambda x: isHttps(x))
#         self.df['NoOfSubDomain'] = self.df['URL'].apply(lambda x: count_subdomains(x))
#         self.df['CharContinuationRate'] = self.df['URL'].apply(char_continuation_rate)
#         self.df['NoOfLettersInURL'] = self.df['URL'].apply(count_letters)
#         self.df['LetterRatioInURL'] = self.df['URL'].apply(calc_letter_ratio)
#         self.df['NoOfDigitsInURL'] = self.df['URL'].apply(count_digits)
#         self.df['DigitRatioInURL'] = self.df['URL'].apply(calc_digit_ratio)
#         self.df['NoOfEqualsInURL'] = self.df['URL'].apply(count_equals)
#         self.df['NoOfQMarkInURL'] = self.df['URL'].apply(count_qmark)
#         self.df['NoOfAmpersandInURL'] = self.df['URL'].apply(count_ampersand)
#         self.df['NoOfOtherSpecialCharsInURL'] = self.df['URL'].apply(count_special_chars)
#         self.df['SpecialCharRatioInURL'] = self.df['URL'].apply(calc_spacial_char_ratio)
#         self.df['HasObfuscation'] = self.df['URL'].apply(lambda url: has_obfuscation(self.df, url))
#         print(f"Fungsi handling_missing_values selesai dalam {time.time() - start_time:.2f} detik")

# def change_type(df, col, new_type):
#     print(f"Sedang mengerjakan fungsi change_type untuk kolom {col}")
#     start_time = time.time()
#     if col not in df.columns:
#         raise ValueError(f"Column '{col}' does not exist in the DataFrame")
#     try:
#         df[col] = df[col].astype(new_type, errors='ignore')
#     except Exception as e:
#         print(f"Error converting column '{col}' to {new_type}: {e}")
#     print(f"Fungsi change_type selesai dalam {time.time() - start_time:.2f} detik")
#     return df

# def remove_by_idx(df, col):
#     print(f"Sedang mengerjakan fungsi remove_by_idx untuk kolom {col}")
#     start_time = time.time()
#     drop_idx = df[df[col].isna()].index
#     df = df.drop(index=drop_idx)
#     print(f"Fungsi remove_by_idx selesai dalam {time.time() - start_time:.2f} detik")
#     return df

# def is_domain_ip(url):
#     print("Sedang mengerjakan fungsi is_domain_ip")
#     start_time = time.time()
#     domain = extract_domain(url)
#     if pd.isna(domain):
#         return False
#     try:
#         domain = domain.split(":")[0]
#         socket.inet_aton(domain)
#         print(f"Fungsi is_domain_ip selesai dalam {time.time() - start_time:.2f} detik")
#         return True
#     except socket.error:
#         print(f"Fungsi is_domain_ip selesai dalam {time.time() - start_time:.2f} detik")
#         return False

# def extract_domain(url):
#     print("Sedang mengerjakan fungsi extract_domain")
#     start_time = time.time()
#     if pd.isna(url):
#         return np.nan
#     extracted = tldextract.extract(url)
#     print(f"Fungsi extract_domain selesai dalam {time.time() - start_time:.2f} detik")
#     return extracted.domain

# def extract_tld(url):
#     print("Sedang mengerjakan fungsi extract_tld")
#     start_time = time.time()
#     if pd.isna(url):
#         return np.nan
#     extracted = tldextract.extract(url)
#     print(f"Fungsi extract_tld selesai dalam {time.time() - start_time:.2f} detik")
#     return extracted.suffix

# def isHttps(url):
#     print("Sedang mengerjakan fungsi isHttps")
#     start_time = time.time()
#     if pd.isna(url):
#         return False
#     result = url.lower().startswith('https')
#     print(f"Fungsi isHttps selesai dalam {time.time() - start_time:.2f} detik")
#     return result

# def count_subdomains(url):
#     print("Sedang mengerjakan fungsi count_subdomains")
#     start_time = time.time()
#     if pd.isna(url):
#         return 0
#     extracted = tldextract.extract(url)
#     result = len(extracted.subdomain.split('.'))
#     print(f"Fungsi count_subdomains selesai dalam {time.time() - start_time:.2f} detik")
#     return result

# def url_length(url):
#     print("Sedang mengerjakan fungsi url_length")
#     start_time = time.time()
#     if pd.isna(url):
#         return 0
#     result = len(url)
#     print(f"Fungsi url_length selesai dalam {time.time() - start_time:.2f} detik")
#     return result

# def domain_length(domain):
#     print("Sedang mengerjakan fungsi domain_length")
#     start_time = time.time()
#     if pd.isna(domain):
#         return 0
#     result = len(domain)
#     print(f"Fungsi domain_length selesai dalam {time.time() - start_time:.2f} detik")
#     return result

# def char_continuation_rate(url):
#     if not isinstance(url, str):  
#         return 0 
    

#     cleaned_url = re.sub(r'[^a-zA-Z0-9]', '', url)
    
    
#     continuation_count = 0
    
    
#     for i in range(1, len(cleaned_url)):
#         if cleaned_url[i] == cleaned_url[i - 1]:
#             continuation_count += 1

#     char_continuation_rate = continuation_count / len(cleaned_url) if len(cleaned_url) > 0 else 0
    
#     return char_continuation_rate

# def count_letters(url):
#     print("Sedang mengerjakan fungsi count_letters")
#     start_time = time.time()
#     if isinstance(url, str):
#         result = len(re.findall(r'[a-zA-Z]', url))
#         print(f"Fungsi count_letters selesai dalam {time.time() - start_time:.2f} detik")
#         return result
#     print(f"Fungsi count_letters selesai dalam {time.time() - start_time:.2f} detik")
#     return 0

# def count_digits(url):
#     print("Sedang mengerjakan fungsi count_digits")
#     start_time = time.time()
#     if isinstance(url, str):
#         result = len(re.findall(r'\d', url))
#         print(f"Fungsi count_digits selesai dalam {time.time() - start_time:.2f} detik")
#         return result
#     print(f"Fungsi count_digits selesai dalam {time.time() - start_time:.2f} detik")
#     return 0

# def count_equals(url):
#     print("Sedang mengerjakan fungsi count_equals")
#     start_time = time.time()
#     if isinstance(url, str):
#         result = url.count('=')
#         print(f"Fungsi count_equals selesai dalam {time.time() - start_time:.2f} detik")
#         return result
#     print(f"Fungsi count_equals selesai dalam {time.time() - start_time:.2f} detik")
#     return 0

# def count_qmark(url):
#     print("Sedang mengerjakan fungsi count_qmark")
#     start_time = time.time()
#     if isinstance(url, str):
#         result = url.count('?')
#         print(f"Fungsi count_qmark selesai dalam {time.time() - start_time:.2f} detik")
#         return result
#     print(f"Fungsi count_qmark selesai dalam {time.time() - start_time:.2f} detik")
#     return 0

# def count_ampersand(url):
#     print("Sedang mengerjakan fungsi count_ampersand")
#     start_time = time.time()
#     if isinstance(url, str):
#         result = url.count('&')
#         print(f"Fungsi count_ampersand selesai dalam {time.time() - start_time:.2f} detik")
#         return result
#     print(f"Fungsi count_ampersand selesai dalam {time.time() - start_time:.2f} detik")
#     return 0

# def count_special_chars(url):
#     print("Sedang mengerjakan fungsi count_special_chars")
#     start_time = time.time()
#     if isinstance(url, str):
#         special_chars = re.findall(r'[^a-zA-Z0-9\s]', url)
#         result = len(special_chars)
#         print(f"Fungsi count_special_chars selesai dalam {time.time() - start_time:.2f} detik")
#         return result
#     print(f"Fungsi count_special_chars selesai dalam {time.time() - start_time:.2f} detik")
#     return 0

# def calc_spacial_char_ratio(url):
#     print("Sedang mengerjakan fungsi calc_spacial_char_ratio")
#     start_time = time.time()
#     if isinstance(url, str):
#         special_count = count_special_chars(url)
#         result = special_count / len(url) if len(url) > 0 else 0
#         print(f"Fungsi calc_spacial_char_ratio selesai dalam {time.time() - start_time:.2f} detik")
#         return result
#     print(f"Fungsi calc_spacial_char_ratio selesai dalam {time.time() - start_time:.2f} detik")
#     return 0

# def calc_letter_ratio(url):
#     print("Sedang mengerjakan fungsi calc_letter_ratio")
#     start_time = time.time()
#     if isinstance(url, str):
#         letter_count = count_letters(url)
#         result = letter_count / len(url) if len(url) > 0 else 0
#         print(f"Fungsi calc_letter_ratio selesai dalam {time.time() - start_time:.2f} detik")
#         return result
#     print(f"Fungsi calc_letter_ratio selesai dalam {time.time() - start_time:.2f} detik")
#     return 0

# def calc_digit_ratio(url):
#     print("Sedang mengerjakan fungsi calc_digit_ratio")
#     start_time = time.time()
#     if isinstance(url, str):
#         digit_count = count_digits(url)
#         result = digit_count / len(url) if len(url) > 0 else 0
#         print(f"Fungsi calc_digit_ratio selesai dalam {time.time() - start_time:.2f} detik")
#         return result
#     print(f"Fungsi calc_digit_ratio selesai dalam {time.time() - start_time:.2f} detik")
#     return 0

# def has_obfuscation(df, url):
#     print("Sedang mengerjakan fungsi has_obfuscation")
#     start_time = time.time()
#     decoded_url = urllib.parse.unquote(url)
#     if decoded_url != url:
#         print(f"Fungsi has_obfuscation selesai dalam {time.time() - start_time:.2f} detik")
#         return True

#     normalized_url = unidecode(url)
#     if normalized_url != url:
#         print(f"Fungsi has_obfuscation selesai dalam {time.time() - start_time:.2f} detik")
#         return True

#     if len(url) > 100:
#         print(f"Fungsi has_obfuscation selesai dalam {time.time() - start_time:.2f} detik")
#         return True

#     if re.search(r'\b[a-fA-F0-9]{32}\b|\b[a-fA-F0-9]{40}\b', url):
#         print(f"Fungsi has_obfuscation selesai dalam {time.time() - start_time:.2f} detik")
#         return True

#     if count_subdomains(url) > 3:
#         print(f"Fungsi has_obfuscation selesai dalam {time.time() - start_time:.2f} detik")
#         return True

#     print(f"Fungsi has_obfuscation selesai dalam {time.time() - start_time:.2f} detik")
#     return False