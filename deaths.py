# Files
from __future__ import division
import secrets
from sheets import update_sheet
from library import get_reports, get_table

# Libraries
import requests
import datetime as dt
import gspread
import time

# Google Sheets
from oauth2client.service_account import ServiceAccountCredentials
from apiclient.discovery import build
from httplib2 import Http

scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
credentials = ServiceAccountCredentials.from_json_keyfile_name(secrets.google_json_file, scope)
gc = gspread.authorize(credentials)
service = build('sheets', 'v4', http=credentials.authorize(Http()))

wb = gc.open_by_key(secrets.google_sheet_id)
wks = wb.worksheet('add_deaths')

def get_deaths(reports):
  deaths = []
  for report in reports:
    r_json = get_table(report, 'deaths', None)
    for death in r_json['entries']:
      sources = death['damage']['sources']
      if len(sources) > 0:
        source = sources[0]['name']
        dmg_type = sources[0]['type']
        if dmg_type == 'Boss':
          kind = 'Boss'
        elif dmg_type == 'NPC':
          kind = 'Trash'
        else:
          kind = 'Friendly'
      else:
        source = 'Divine Intervention'
        kind = 'Friendly'
      new_row = [
          report['date'],
          str(report['id'], 'utf-8'),
          str(report['title'], 'utf-8'),
          death['name'],
          source,
          kind,
          1
      ]
      deaths.append(new_row)

  return deaths

def main():
  reports = get_reports(secrets.raid_id, secrets.c_date)
  print('Reports retrieved')
  deaths = get_deaths(reports)
  print('Deaths retrieved')
  update_sheet(wks, deaths)
  print('Worksheet updated')

if __name__ == '__main__':
  main()
