# -*- coding:utf-8 -*-

from mitmproxy import ctx
import json

def response(flow):
    """
    爬取简书发现页面的推荐内容，包括文章标题、作者、ID、喜欢数、评论数、获赏数、阅读量等
    :param flow:
    :return:
    """
    url = 'https://s0.jianshuapi.com/'
    url_ = 'https://s0.jianshuapi.com/v3/trending/now3?'
    if flow.request.url.startswith(url):
        if flow.request.url.startswith(url_):
            text = flow.response.text  # 获取响应
            data = json.loads(text)
            info = ctx.log.info

            # 获取文章信息列表
            for i in range(len(data)):
                title = data[i].get('object').get('data').get('title')
                id = data[i].get('object').get('data').get('user').get('id')
                author = data[i].get('object').get('data').get('user').get('nickname')
                likes_count = data[i].get('object').get('data').get('likes_count')
                comments_count = data[i].get('object').get('data').get('comments_count')
                total_rewards_count = data[i].get('object').get('data').get('total_rewards_count')
                views_count = data[i].get('object').get('data').get('views_count')

                # 显示获取的信息
                info('总数据' + str(len(data)))
                info('文章标题：' + title)
                info('作者：' + author)
                info('ID：' + str(id))
                info('喜欢：' + str(likes_count))
                info('评论：' + str(comments_count))
                info('赞赏：' + str(total_rewards_count))
                info('阅读量：' + str(views_count))
                info('-'*80)

                # 存储至数据库
                data_ = {
                    'title': title,
                    'id': id,
                    'author': author,
                    'likes': likes_count,
                    'comments': comments_count,
                    'rewards': total_rewards_count,
                    'views': views_count,
                }
                with open('./result/jianshu.json', 'a', encoding='utf-8') as f:
                    f.write(json.dumps(data_, indent=2, ensure_ascii=False))
                    f.write(', \n')




