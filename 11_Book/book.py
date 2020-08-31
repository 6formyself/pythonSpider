import requests
from bs4 import BeautifulSoup as Bs4

url = 'https://www.aladin.co.kr/m/msearch.aspx?SearchTarget=All&KeyWord=%EA%B9%80%ED%83%9C%EC%84%B1+&KeyRecentPublish=0&OutStock=0&ViewType=Detail&SortOrder=11&CustReviewCount=0&CustReviewRank=0&KeyFullWord=%EA%B9%80%ED%83%9C%EC%84%B1+&KeyLastWord=%EA%B9%80%ED%83%9C%EC%84%B1+&CategorySearch=&MViewType=&page={}'
headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    'Cookie': 'CheckSameSite=IsValidSameSiteSet; AladdinUser=UID=-588926833&SID=PAecxrhMNCwmxRT9YMcVMg%3d%3d; AladdinSession=UID=-588926833&SID=PAecxrhMNCwmxRT9YMcVMg%3d%3d; AladdinUS=pMptdrkpjqMraohMigMqGg%3d%3d&USA=0; AUAZ3A43579=1598412374753201163%7C2%7C1598412374753201163%7C1%7C1598412374727VZ24U; _ga=GA1.3.850652152.1598412375; _gid=GA1.3.1204923044.1598412375; _TRK_AUIDA_13987=b180304be6f2038f021530ed7b7f13c9:1; _TRK_ASID_13987=6cbf80777ae0246042b616c0bffd0f92; _BS_GUUID=WFSgrWUorSml85Vcx82R4LosDLJGtIWqoOGQLAed; divGoodsEventBottomLayerCount=2; refererURL=https://www.aladin.co.kr/m/msearch.aspx?SearchTarget=All&KeyWord=%EA%B9%80%ED%83%9C%EC%84%B1+&KeyRecentPublish=0&OutStock=0&ViewType=Detail&SortOrder=11&CustReviewCount=0&CustReviewRank=0&KeyFullWord=%EA%B9%80%ED%83%9C%EC%84%B1+&KeyLastWord=%EA%B9%80%ED%83%9C%EC%84%B1+&CategorySearch=&MViewType=&page=1; ASAZ3A43579=1598412374753201163%7C1598414250745251218%7C1598412374753201163%7C1598414250745251218%7Cbookmark; ARAZ3A43579=httpswwwaladincokrmmsearchaspxSearchTargetAllKeyWordEAB980ED839CEC84B1+KeyRecentPublish0OutStock0ViewTypeDetailSortOrder11CustReviewCount0CustReviewRank0KeyFullWordEAB980ED839CEC84B1+KeyLastWordEAB980ED839CEC84B1+CategorySearchMViewTypepage1httpswwwaladincokrmmsearchaspxSearchTargetAllKeyWordEAB980ED839CEC84B1+KeyRecentPublish0OutStock0ViewTypeDetailSortOrder11CustReviewCount0CustReviewRank0KeyFullWordEAB980ED839CEC84B1+KeyLastWordEAB980ED839CEC84B1+CategorySearchMViewTypePriceFilterMaxpage2',
    'Host': 'www.aladin.co.kr',
    'Referer': 'https://www.aladin.co.kr/m/msearch.aspx?SearchTarget=All&KeyWord=%EA%B9%80%ED%83%9C%EC%84%B1+&KeyRecentPublish=0&OutStock=0&ViewType=Detail&SortOrder=11&CustReviewCount=0&CustReviewRank=0&KeyFullWord=%EA%B9%80%ED%83%9C%EC%84%B1+&KeyLastWord=%EA%B9%80%ED%83%9C%EC%84%B1+&CategorySearch=&MViewType=&PriceFilterMax=&page=2',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-User': '?1',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36'
}


def get_struct_data(page_url):
    res = requests.get(page_url, headers=headers)
    soup = Bs4(res.text, 'lxml')
    f = open('book.txt', 'a', encoding='utf-8')
    # print(res.text)
    div_list = soup('div', attrs={'class': 'browse_list_box'})
    for div in div_list:
        li = div.select('li')
        f.writelines(li[0].stripped_strings)
        f.write('\n')
        f.writelines(li[1].stripped_strings)
        f.write('\n')
        f.writelines(li[2].stripped_strings)
        f.write('\n')
        f.writelines(li[3].stripped_strings)
        f.write('\n\n')


if __name__ == '__main__':
    for i in range(6, 13):
        get_struct_data(url.format(str(i)))
