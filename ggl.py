import gspread
import gdown
from oauth2client.service_account import ServiceAccountCredentials


def download_pdf(link):
    url = f'https://drive.google.com/uc?id={link.split("/d/")[1].split("/")[0]}'
    output = 'description.pdf'
    gdown.download(url, output, quiet=False)


config_page_id = 9111257


def read_table():
    scope = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name('google.json', scope)
    client = gspread.authorize(creds)
    sheet = client.open('ЧАТ').get_worksheet_by_id(config_page_id)
    pdf_link = sheet.cell(3, 3).value
    pipeline_id = sheet.cell(4, 3).value
    return pdf_link, pipeline_id
