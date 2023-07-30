from bs4 import BeautifulSoup 
from datetime import datetime
import itertools
import argparse
import requests
import calendar
import glob
import re
import os

def get_date_month_year(date_raw):
    
    '''Takes string describing date and formats it as a day, month, year
    args:
        date_raw(str): String with a date in "DD<space>Month as string<space>YYYY" format.
    returns:
        day(int): Day in DD format. 
        month(str) The month as a string, first letter uppercase. 
        year(int): Year in YYYY format
    '''
    # Get months of the year as strings
    # Modified from https://stackoverflow.com/questions/66790398/how-to-generate-month-names-as-list-in-python
    months = calendar.month_name[1:]
    # Format months for regrex 
    re_months = '|'.join(months)
    # Modified from: https://stackoverflow.com/questions/35413746/regex-to-match-date-like-month-name-day-comma-and-year
    # DD<space>Month as string<space>YYYY
    date_pattern = "(\d{1,2})\s+(%s)\s+(\d{4})"%(re_months)
    date, month_name, year = re.findall(date_pattern, date_raw)[0]
    month = datetime.strptime(month_name,'%B').month
    return date, month, year


def clean_text(text):
    # Remove citations
    text = re.sub("\[\d+\]","", text)
    # Remove \n and \t and replace with just a space. 
    text = re.sub("\s+", " ", text)
    # Remove anything not language or typical punctuation. 
    text = re.sub("[^a-zA-Z\d\s?!:,.;\"\'\-\/]", "",  text)
    return text

def get_clean_references(raw_refs_list):

    refs = []
    for raw_ref in raw_refs_list:
        raw_ref_text = raw_ref.get_text()
        ref = clean_text(raw_ref_text)
        refs.append(ref)
    return "\n".join(refs)

def get_clean_paragraphs(paragraphs):
    all_paragraphs = []
    for paragraph in paragraphs:
        paragraph = paragraph.get_text()
        paragraph = clean_text(paragraph)
        all_paragraphs.append(paragraph)
    # Each paragraph separated by exactly one newline character.
    article = "\n".join(all_paragraphs)
    return article

parser = argparse.ArgumentParser(
                    description='This program will convert raw HTML to cleaned text from a wikipedia article and references.'
    )
parser.add_argument('--input_dir')      
parser.add_argument('--output_dir')
args = parser.parse_args()

html_files = sorted(glob.glob(os.path.join(args.input_dir, "*.html")))
if not os.path.exists(args.output_dir): os.mkdir(args.output_dir)
    
for html_file in html_files:
    with open(html_file, 'r') as f:
        response = f.read()

    raw = BeautifulSoup(response, 'html.parser')
    # Get field describing last modification
    date_raw = raw.find("li", {"id": "footer-info-lastmod"}).get_text()
    d, m, y = get_date_month_year(date_raw)

    article_title = raw.title.get_text()

    raw_paragraph_list = raw.find_all('p')
    article_body = get_clean_paragraphs(raw_paragraph_list)


    raw_refs_list = raw.find("ol", {"class": "references"}).find_all("li")
    refs = get_clean_references(raw_refs_list)
    
    output_file_temp = "{}_{}_{}_{}".format(article_title, y, m, d)
    output_file_article_body = "article_{}.txt".format(output_file_temp)
    output_file_refs = "refs_{}.txt".format(output_file_temp)

    with open(os.path.join(args.output_dir,output_file_article_body), "w") as f:
        f.write(article_body)

    with open(os.path.join(args.output_dir, output_file_refs), "w") as f:
        f.write(refs)