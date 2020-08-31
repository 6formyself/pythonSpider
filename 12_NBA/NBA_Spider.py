import requests
from bs4 import BeautifulSoup as Bs4
import xlrd
import xlutils.copy
from NBA import data_tool
from selenium import webdriver

head = {'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1'}
head_url = 'https://www.basketball-reference.com/'


def write_team_info():
    """将所有队伍信息写入文件"""
    file = open('links.txt')
    link_con = file.readlines()
    team_file = open('team.txt', 'a')
    for link in link_con:
        year = int(link[-10: -6])
        year_url = link[0:-1]
        # 获取队伍名称和队伍链接
        team_data = get_team_name_url(year, year_url)
        for team_item in team_data:
            # [2020, 'Toil', '/Toil/dad']
            year = team_item[0]
            team_link = team_item[2]
            team_name = team_item[1]
            team_file.write(str(year) + head_url + str(team_link) + str(team_name) + '\n')
    team_file.close()
    file.close()


def get_team_name_url(year, url):
    """ 获取给定年份的队伍数据和链接[ 2020, 'Toil', '/Toil/dad'] """
    html = requests.get(url, headers=head)
    html.encoding = 'utf-8'
    soup = Bs4(html.text, 'lxml')
    data_con = []
    # 获取每个赛季的球队信息与链接
    global tr_E
    global table_E
    try:
        table_E = soup('table', id='divs_standings_E')[0]
    except Exception as e:
        table_E = soup('table', id='divs_standings_')[0]
    tr_E = table_E.select('.full_table')
    for item in tr_E:
        th = item.select('th')[0]
        team_a = th.select('a')[0]
        team_name = team_a.string
        team_href = team_a.get('href')
        data_con.append([year, team_name, team_href])
        print(year, team_name, team_href)
    try:
        table_W = soup('table', id='divs_standings_W')[0]
        tr_W = table_W.select('.full_table')
        for item in tr_W:
            th = item.select('th')[0]
            team_a = th.select('a')[0]
            team_name = team_a.string
            team_href = team_a.get('href')
            data_con.append([year, team_name, team_href])
            print(year, team_name, team_href)
    except Exception as e:
        print(e)
    return data_con


def write_to_xlsx():
    # 读取年份链接
    file = open('links.txt')
    link_con = file.readlines()
    # 打开excel表格
    tar_work_book = xlrd.open_workbook(r'data_2000-2005.xlsx')
    work_book = xlutils.copy.copy(tar_work_book)
    roster_rows = per_game_rows = 516
    for link in link_con:
        year = int(link[-10: -6])
        year_url = link[0:-1]
        # 获取队伍名称和队伍链接
        team_data = get_team_name_url(year, year_url)
        for team_item in team_data:
            # [2020, 'Toil', '/Toil/dad']
            year = team_item[0]
            team_name = team_item[1]
            team_page_source = requests.get('https://www.basketball-reference.com' + team_item[2], headers=head)
            team_page_source.encoding = 'utf-8'
            # Roster数据
            try:
                roster_data = data_tool.get_roster_info(year, team_name, team_page_source.text)
                roster_sheet = work_book.get_sheet(0)
                for staff_item in roster_data:
                    # [2020, 'TOR', '9', 'Wesley Matthews', 'SG', '6-4', '220', 'October 14, 1986', 'us', '10', 'Marquette']
                    for index in range(0, len(staff_item)):
                        roster_sheet.write(roster_rows, index, staff_item[index])
                    roster_rows = roster_rows + 1
            except Exception as e:
                print(e)
            # PerGame
            # per_game_data = data_tool.get_per_game_info(year, team_name, team_page_source.text)
            # per_game_sheet = work_book.get_sheet(1)
            # for per_game_item in per_game_data:
            #     for index in range(0, len(per_game_item)):
            #         per_game_sheet.write(per_game_rows, index, per_game_item[index])
            #     per_game_rows = per_game_rows + 1
    work_book.save('data_2000-2005.xlsx')
    file.close()


if __name__ == '__main__':
    # 浏览器
    driver = webdriver.Chrome()
    # 读取年份链接
    file = open('team.txt')
    lines = file.readlines()
    # 打开excel表格
    tar_work_book = xlrd.open_workbook(r'data_2016-2020.xlsx')
    work_book = xlutils.copy.copy(tar_work_book)
    # 所有列表的名称
    table_id = ['roster', 'per_game', 'per_poss', 'advanced', 'adj-shooting', 'shooting', 'pbp', 'playoffs_per_game',
                'playoffs_per_poss', 'playoffs_advanced', 'playoffs_shooting', 'playoffs_pbp', 'salaries2']
    rows = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    for line in lines:
        year = int(line[0:4])
        team_url = line[4:60]
        team_name = line[60:-1]
        print(line)
        try:
            driver.get(team_url)
            for i in range(0, 13):
                table_data = data_tool.get_table_info(year, team_name, table_id[i], driver.page_source)
                sheet = work_book.get_sheet(i)
                for data_item in table_data:
                    for index in range(0, len(data_item)):
                        sheet.write(rows[i], index, data_item[index])
                    rows[i] = rows[i] + 1
        except Exception as e:
            print(e)
            work_book.save('data_2016-2020.xlsx')
    work_book.save('data_2016-2020.xlsx')
    file.close()

