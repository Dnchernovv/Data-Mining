import scrapy
import scrapy
from scrapy.http import HtmlResponse
import re
import json
from urllib.parse import urlencode
from copy import deepcopy
from instaparser.items import Subscriber_Item
from instaparser.items import User_Item
from instaparser.items import Subcriptions_Item

class InstaSpider(scrapy.Spider):
    name = 'insta_2'
    allowed_domains = ['instagram.com']
    start_urls = ['https://instagram.com/']
    inst_login_link = 'https://www.instagram.com/accounts/login/ajax/'
    inst_login = ''
    inst_password = ''
    parse_user = ['niikkkii___','m108mm','lnktmv']
    posts_hash = '02e14f6a7812a876f7d133c9555b1151'
    subscribers_hash = '5aefa9893005572d237da5068082d8d5'
    subscriptions_hash = '3dec7e2c57367ef3da3d987d89f9dbc8'
    graphql_url = 'https://www.instagram.com/graphql/query/?'


    def parse(self, response):
        csrf = self.fetch_csrf_token(response.text)
        yield scrapy.FormRequest(
            self.inst_login_link,
            method='POST',
            callback=self.login,
            formdata={'username': self.inst_login,
                        'enc_password': self.inst_password},
            headers={'X-CSRFToken': csrf}
            )



    def fetch_csrf_token(self, text):
            matched = re.search('\"csrf_token\":\"\\w+\"', text).group()
            return matched.split(':').pop().replace(r'"', '')

    def fetch_user_id(self, text, username):
        matched = re.search(
            '{\"id\":\"\\d+\",\"username\":\"%s\"}' % username, text
        ).group()
        return json.loads(matched).get('id')

    def login(self, response: HtmlResponse):
        j_body = response.json()
        if j_body.get('authenticated'):
            for user in self.parse_user:
                yield response.follow(
                    f'/{user}',
                    callback = self.user_data_parse,
                    cb_kwargs= {'username': user}
                )
            # если нужно собрать данные с более чем одной страницы необходимо обратить на это
            # внимание в рамках cb_kwargs

    def user_data_parse(self,response:HtmlResponse, username):
        user_id = self.fetch_user_id(response.text, username)
        variables = {'id':user_id, 'first':12}
        url_posts = f'{self.graphql_url}query_hash={self.posts_hash}&{urlencode(variables)}'
        url_subbs = f'{self.graphql_url}query_hash={self.subscribers_hash}&{urlencode(variables)}'
        url_subscr = f'{self.graphql_url}query_hash={self.subscriptions_hash}&{urlencode(variables)}'
        yield response.follow(url_posts,
                             callback= self.user_posts_parse,
                              cb_kwargs={'username':username, 'user_id':user_id, 'variables': deepcopy(variables)})

        yield response.follow(url_subbs,
                          callback=self.user_subsribers_parse,
                          cb_kwargs={'username': username, 'user_id': user_id, 'variables': deepcopy(variables)})

        yield response.follow(url_subscr,
                          callback=self.user_subscriptions_parse,
                          cb_kwargs={'username': username, 'user_id': user_id, 'variables': deepcopy(variables)})

    def user_posts_parse(self, response:HtmlResponse, username, user_id, variables):
        print()
        j_data = response.json()
        page_info = j_data.get('data').get('user').get('edge_owner_to_timeline_media').get('page_info')
        if page_info.get('has_next_page'):
            variables['after'] = page_info.get('end_cursor')
            url_posts = f'{self.graphql_url}query_hash={self.posts_hash}&{urlencode(variables)}'
            yield response.follow(url_posts,
                                  callback=self.user_posts_parse,
                                  cb_kwargs={'username': username, 'user_id': user_id,
                                             'variables': deepcopy(variables)})
        posts = j_data.get('data').get('user').get('edge_owner_to_timeline_media').get('edges')
        # перебором значений в данном словаре, где содержатся данные пользователя, мы получаем необходимые
        # значения
        for post in posts:
            item = User_Item(
                user_id = user_id,
                photo = post.get('node').get('display_url'),
                likes = post.get('node').get('edge_media_preview_like').get('count'),
            )
            yield item

    def user_subsribers_parse(self, response: HtmlResponse, username, user_id, variables):
        j_data = response.json()
        page_info = j_data.get('data').get('user').get('edge_followed_by').get('page_info')
        if page_info.get('has_next_page'):
            variables['after'] = page_info.get('end_cursor')
            url_subbs = f'{self.graphql_url}query_hash={self.subscribers_hash}&{urlencode(variables)}'
            yield response.follow(url_subbs,
                          callback=self.user_subsribers_parse,
                          cb_kwargs={'username': username, 'user_id': user_id, 'variables': deepcopy(variables)})
        users = j_data.get('data').get('user').get('edge_followed_by').get('edges')
        for user in users:
            item = Subscriber_Item(
                user_id = user_id,
                subscriber_id = user.get('node').get('id'),
                subscriber_name = user.get('node').get('username'),
                subscriber_pic = user.get('node').get('profile_pic_url'))
            yield item

    def user_subscriptions_parse(self, response: HtmlResponse,username, user_id, variables):
        j_data = response.json()
        page_info = j_data.get('data').get('user').get('edge_follow').get('page_info')
        if page_info.get('has_next_page'):
            variables['after'] = page_info.get('end_cursor')
            url_subscr = f'{self.graphql_url}query_hash={self.subscriptions_hash}&{urlencode(variables)}'
            yield response.follow(url_subscr,
                          callback=self.user_subscriptions_parse,
                          cb_kwargs={'username': username, 'user_id': user_id, 'variables': deepcopy(variables)})
        users = j_data.get('data').get('user').get('edge_follow').get('edges')
        for user in users:
            item = Subcriptions_Item(
                user_id = user_id,
                subscription_id = user.get('node').get('id'),
                subscription_name = user.get('node').get('username'),
                subscription_pic = user.get('node').get('profile_pic_url'))
            yield item
        # собрать у нескольких пользователей информацию о всех подписчиках и обо всех подписках пользователя
        # как к этому подойти можно пронаблюдать с 1:58
        # при этом необходимо будет разделить методы сбора данных о подписках и подписчиках
        # список пользователей необходимо взять > 2


