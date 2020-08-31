from bs4 import BeautifulSoup as Bs4


def get_roster_info(year, team_name, page_source):
    """获取Roster数据"""
    soup = Bs4(page_source, 'lxml')
    table = soup('table', id='roster')[0]
    t_body = table.select('tbody')[0]
    tr_list = t_body.select('tr')
    data_con = []
    for tr in tr_list:
        line_data = [year, team_name]
        th_text = tr.select('th')[0].text
        if th_text != '':
            line_data.append(th_text)
        else:
            line_data.append('无')

        td_list = tr.select('td')
        for td in td_list:
            td_text = td.text
            if td_text != '':
                line_data.append(td_text)
            else:
                line_data.append('无')
        data_con.append(line_data)
        print(line_data, len(line_data))
    return data_con


def get_table_info(year, team_name, table_id, page_source):
    soup = Bs4(page_source, 'lxml')
    try:
        table = soup('table', id=table_id)[0]
        t_body = table.select('tbody')[0]
        tr_list = t_body.select('tr')
    except:
        return []

    data_con = []
    for tr in tr_list:
        line_data = [year, team_name]
        # th
        try:
            th_text = tr.select('th')[0].text
            if th_text != '':
                line_data.append(th_text)
            else:
                line_data.append('无')
        except Exception as e:
            print(e)
        # td
        try:
            td_list = tr.select('td')
            for td in td_list:
                td_text = td.text
                if td_text != '':
                    line_data.append(td_text)
                else:
                    line_data.append('无')
        except Exception as e:
            print(e)
        data_con.append(line_data)
        print(table_id, line_data, len(line_data))
    return data_con
