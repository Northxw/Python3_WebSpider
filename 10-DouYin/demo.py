# -*- coding:utf-8 -*-

from mitmproxy import ctx
import json
import requests
import time
import os

def response(flow):
    """
    抓取抖音标题、APP视频链接、作者、抖音ID、发布时间、获赞数、评论和转发数等信息, 并将结果保存为JSON格式.
    :return: None
    """
    url = 'https://api.amemv.com/'   # 获取抖音短视频的URL接口
    url_ = 'https://aweme.snssdk.com/'
    if flow.request.url.startswith(url) or flow.request.url.startswith(url):
        text = flow.response.text   # 获取响应
        dyjson = json.loads(text)
        info = ctx.log.info

        # 获取视频列表
        aweme_list = dyjson.get('aweme_list')
        # 遍历列表，获取每个视频的相应数据
        for i in range(len(aweme_list)):
            # 视频标题
            title = aweme_list[i].get('share_info').get('share_title')
            # 视频链接
            videourl = aweme_list[i].get('video').get('play_addr').get('url_list')[0]
            # 保存视频
            res = requests.get(videourl, stream=True)
            # 规范文件命名
            _str = ['\\', '/', ':', '*', '?', '"', '<', '>', '|', '.', '..', '？']
            for _ in _str:
                if _ in title:
                    title.replace(_, '')
            # 判断文件路径是否存在
            save_dir = './video/'
            if not os.path.exists(save_dir):
                os.mkdir(save_dir)
            with open('{}/{}.mp4'.format(save_dir, title), 'wb') as f:
                f.write(res.content)

            # 作者名称
            nickname = aweme_list[i].get('author').get('nickname')
            # 抖音ID
            short_id = aweme_list[i].get('author').get('short_id')
            # 发布时间
            create_time = aweme_list[i].get('create_time')
            create_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(create_time))   # 格式化时间
            # 获赞、评论、转发数
            digg_count = aweme_list[i].get('statistics').get('digg_count')
            comment_count = aweme_list[i].get('statistics').get('comment_count')
            share_count = aweme_list[i].get('statistics').get('share_count')

            # 显示所有获取信息
            info("标题:" + title)
            info("URL：" + videourl)
            info("作者: " + nickname)
            info("ID: " + short_id)
            info("发布时间: " + create_time)
            info("获赞：" + str(digg_count))
            info("评论：" + str(comment_count))
            info("转发：" + str(share_count))
            info('-'*80)

            # 保存为json文件
            data = {
                'title': title,
                'url': videourl,
                'nickname': nickname,
                'douyin_id': short_id,
                'create_time': create_time,
                'diggs': digg_count,
                'commments': comment_count,
                'shares': share_count
            }
            with open('./douyin.json', 'a', encoding='utf-8') as f:
                f.write(json.dumps(data, indent=2, ensure_ascii=False))
                f.write(', \n')
