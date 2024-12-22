# Predict Phishing

A notebook-based project to predict phishing attempts through link analysis.

## 📂 Folder Structure

root
src:
  Doodle: doodles of notebook 
  Model: Scratch model -> knn.py and gnb.py
  Modules: Modules use in the features preprocessing and cleaning -> FeaturesManipulation.py, FeaturesMissingHandler, and legit_tld.txt
  Prediction: all csv file prediction by all models
  TemplNotebook: previous notebook from EDA -> notebook-TubesTemplate.ipynb, notebook-Tucil.ipynb, and Tucil2_18222114_18222115
  notebook-Tubes.ipynb
  test.csv
  train.csv
doc: Tubes2_DAI_36


## ⚠️ Important Notes

- **Accessible Folders/Files:**
  - `Modules/`
  - `Model/`
  - `Prediction/`
  - Main notebook: `notebook-Tubes.ipynb`

- **Use Only:**
  - `notebook-Tubes.ipynb` for running the predictions.

---

## 🚀 How to Start

### Pre-requisites

Ensure the following libraries are installed:
```python
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.stats import zscore
import re
import urllib
from urllib.parse import urlparse
from unidecode import unidecode
import tldextract
from sklearn.impute import KNNImputer, SimpleImputer
```

Steps
Open notebook-Tubes.ipynb in the root folder.
Execute the cells in the notebook.
Analyze the results generated from the phishing link predictions.


# Tabel Log Act

| Nama               | NIM       | Kontribusi                        |
|--------------------|-----------|------------------------------------|
| Jeremy Deandito    | 18222112  | Naive Bayes Scikit-Learn          |
| Nathaniel Liady    | 18222114  | Naive Bayes Scratch               |
| Gabriel Marcellino | 18222115  | Data Cleaning, Preprocessing, dan KNN Scratch |
| Nicolas Jeremy     | 18222135  | KNN Scikit-Learn                  |
