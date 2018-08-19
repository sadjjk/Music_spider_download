# -*- coding: utf-8 -*-
# @Author: kjjdas
# @Date:   2018-08-19 15:21:36
# @Last Modified time: 2018-08-19 18:06:22
import requests
import urllib
import json
import os 


def get_song_list(keyword):
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36'
    }
    keyword = urllib.parse.quote(keyword)
    url = 'https://c.y.qq.com/soso/fcgi-bin/client_search_cp?aggr=1&cr=1&p=1&n=20&w=%s' % keyword
    response = requests.get(url, headers=headers).text.encode(
        'gbk', 'ignore').decode('gbk').split('callback')[-1].strip('()')
    response = json.loads(response)
    return response['data']['song']


def print_info(songs):
    for num, song in enumerate(songs):
        songname = song['songname']
        singer_length = len(song['singer'])
        singers = []
        for i in range(singer_length):
            singers.append(song['singer'][i]['name'])
        singers = ('/').join(singers)
        media_mid = song['media_mid']
        album_name = song['albumname']
        time = song['interval']
        m, s = divmod(time, 60)
        time = "%02d:%02d" % (m, s)
        print(num,'歌曲名字：',songname,'作者：' ,singers, '专辑：',album_name, '时长：',time)

def get_mp3_url(songs,num):
    media_mid = songs['list'][num]['media_mid']
    url_1 = 'https://c.y.qq.com/base/fcgi-bin/fcg_music_express_mobile3.fcg?g_tk=5381&cid=205361747&songmid=%s&filename=C400%s.m4a&guid=6800588318' % (media_mid,media_mid)
    response = requests.get(url_1).json()
    vkey= response['data']['items'][0]['vkey']
    if vkey:
        url_2 = 'http://dl.stream.qqmusic.qq.com/C400%s.m4a?vkey=%s&guid=6800588318&uin=0&fromtag=66' % (media_mid,vkey)
        return url_2
    return None

def download_mp3(url,filename):
    abspath = os.path.abspath('.')  # 获取绝对路径
    os.chdir(abspath)
    response = requests.get(url).content
    path = os.path.join(abspath,filename)
    with open(filename + '.m4a', 'wb') as f:
        f.write(response)
        print('下载完毕,可以在%s   路径下查看' % path + '.mp3') 



def run():
    while  True:
        name = input('请输入你要下载的歌曲：')
        songs = get_song_list(name)
        if songs['totalnum'] == 0 : 
            print('没有搜到此歌曲，请换个关键字')
        else:
            print_info(songs['list'])
            num = input('请输入需要下载的歌曲，输入左边对应数字即可')
            url = get_mp3_url(songs,int(num))
            if not url :
                print('歌曲已下架 找不到下载地址 下载失败')
            else:
                songname = songs['list'][int(num)]['songname']
                download_mp3(url, songname)

            flag = input('如需继续可以按任意键进行搜歌，否则按0结束程序')
            if flag == '0':
                break



def main():
    run()

if __name__ == '__main__':
    main()