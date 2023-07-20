import dataclasses
import gspread
from oauth2client.service_account import ServiceAccountCredentials

@dataclasses.dataclass
class SearchGroup:
    name: str
    last_update: str
    chat_id: str
    link: str


@dataclasses.dataclass
class SearchResult:
    chat_id: str
    from_group: str
    name: str
    surname: str
    username: str
    phone: str
    message_time: str
    message_text: str



scope = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('google.json', scope)
search_group_page_id = 541067323
keywords_page_id = 391680335
search_result_page_id = 221888722

def get_chats() -> list[SearchGroup]:
    client = gspread.authorize(creds)
    sheet = client.open('ЧАТ').get_worksheet_by_id(search_group_page_id)
    values = sheet.get_all_values()[1::]
    resp = []
    for v in values:
        resp.append(SearchGroup(name=v[3], last_update=v[1], chat_id=v[2], link=v[0]))
    return resp


def get_keywords() -> list[str]:
    client = gspread.authorize(creds)
    sheet = client.open('ЧАТ').get_worksheet_by_id(keywords_page_id)
    values = sheet.get_all_values()
    resp = []
    for v in values:
        resp.append(v[0])
    return resp


def write_result(result: SearchResult):
    print(result)
    client = gspread.authorize(creds)
    sheet = client.open('ЧАТ').get_worksheet_by_id(search_result_page_id)
    sheet.append_row([result.chat_id, result.from_group, result.name, result.surname,
                     result.username, result.phone, result.message_time, result.message_text])


def update_group_info(group: SearchGroup):
    client = gspread.authorize(creds)
    sheet = client.open('ЧАТ').get_worksheet_by_id(search_group_page_id)
    values = sheet.get_all_values()
    for row in range(len(values)):
        if values[row][0] == group.link:
            sheet.update_cell(row + 1, 2, group.last_update)
            sheet.update_cell(row + 1, 3, group.chat_id)
            sheet.update_cell(row + 1, 4, group.name)
            break
