import asyncio  # 异步I/O
import os  # 系统操作
import time  # 时间操作
from typing import Optional
from urllib.parse import urlencode, quote  # URL编码
import yaml  # 配置文件

# 基础爬虫客户端和抖音API端点
from scraper.base import BaseScraper
from scraper.douyin.web.endpoints import DouyinAPIEndpoints
# 抖音接口数据请求模型
from scraper.douyin.web.models import (
    AwemeDetail, TrendingList, HomeFeed, RecommendFeed, RelatedAweme,
    PostCommentsReply, LiveRoomRanking, PostComments,
    UserProfile, UserCollection, UserLike, UserLive,
    UserLive2, UserMix, UserPost
)
# 抖音应用的工具类
from scraper.douyin.web.utils import (AwemeIdFetcher,  # Aweme ID获取
                                       BogusManager,  # XBogus管理
                                       SecUserIdFetcher,  # 安全用户ID获取
                                       TokenManager,  # 令牌管理
                                       VerifyFpManager,  # 验证管理
                                       WebCastIdFetcher,  # 直播ID获取
                                       extract_valid_urls  # URL提取
                                       )

# 配置文件路径
path = os.path.abspath(os.path.dirname(__file__))

# 读取配置文件
with open(f"{path}/config.yaml", "r", encoding="utf-8") as f:
    config = yaml.safe_load(f)


class DouyinWebScraper:

    # 从配置文件中获取抖音的请求头
    async def get_douyin_headers(self):
        douyin_config = config["TokenManager"]["douyin"]
        kwargs = {
            "headers": {
                "Accept-Language": douyin_config["headers"]["Accept-Language"],
                "User-Agent": douyin_config["headers"]["User-Agent"],
                "Referer": douyin_config["headers"]["Referer"],
                "Cookie": douyin_config["headers"]["Cookie"],
            },
            "proxies": {"http://": douyin_config["proxies"]["http"], "https://": douyin_config["proxies"]["https"]},
        }
        return kwargs


    async def fetch_aweme_detail(self, params: AwemeDetail):
        kwargs = await self.get_douyin_headers()
        base_scraper = BaseScraper(proxies=kwargs["proxies"], scraper_headers=kwargs["headers"])
        async with base_scraper as scraper:
            endpoint = BogusManager.ab_model_2_endpoint(DouyinAPIEndpoints.AWEME_DETAIL, params.model_dump())
            response = await scraper.fetch_get_json(endpoint)
        return response


    async def fetch_trending_list(self, params: TrendingList):
        kwargs = await self.get_douyin_headers()
        base_scraper = BaseScraper(proxies=kwargs["proxies"], scraper_headers=kwargs["headers"])
        async with base_scraper as scraper:
            endpoint = BogusManager.ab_model_2_endpoint(DouyinAPIEndpoints.DOUYIN_TRENDING_LIST, params.model_dump())
            response = await scraper.fetch_get_json(endpoint)
        return response


    async def fetch_home_feed(self, params: HomeFeed):
        kwargs = await self.get_douyin_headers()
        base_scraper = BaseScraper(proxies=kwargs["proxies"], scraper_headers=kwargs["headers"])
        async with base_scraper as scraper:
            endpoint = BogusManager.ab_model_2_endpoint(DouyinAPIEndpoints.HOME_FEED, params.model_dump())
            response = await scraper.fetch_post_json(endpoint) # fetch POST/GET sẽ phụ thuộc vào method gọi API từ phía Douyin
        return response
    

    async def fetch_recommend_feed(self, params: RecommendFeed):
        kwargs = await self.get_douyin_headers()
        base_scraper = BaseScraper(proxies=kwargs["proxies"], scraper_headers=kwargs["headers"])
        async with base_scraper as scraper:
            endpoint = BogusManager.ab_model_2_endpoint(DouyinAPIEndpoints.RECOMMEND_FEED, params.model_dump())
            response = await scraper.fetch_get_json(endpoint)
        return response
    

    async def fetch_related_aweme(self, params: RelatedAweme):
        kwargs = await self.get_douyin_headers()
        base_scraper = BaseScraper(proxies=kwargs["proxies"], scraper_headers=kwargs["headers"])
        async with base_scraper as scraper:
            endpoint = BogusManager.ab_model_2_endpoint(DouyinAPIEndpoints.RELATED_AWEME, params.model_dump())
            response = await scraper.fetch_get_json(endpoint)
        return response

    # 获取用户发布作品数据
    async def fetch_user_post_videos(self, sec_user_id: str, max_cursor: int, count: int):
        kwargs = await self.get_douyin_headers()
        base_scraper = BaseScraper(proxies=kwargs["proxies"], scraper_headers=kwargs["headers"])
        async with base_scraper as scraper:
            params = UserPost(sec_user_id=sec_user_id, max_cursor=max_cursor, count=count)
            # endpoint = BogusManager.xb_model_2_endpoint(
            #     DouyinAPIEndpoints.USER_POST, params.dict(), kwargs["headers"]["User-Agent"]
            # )
            # response = await scraper.fetch_get_json(endpoint)

            # 生成一个用户发布作品数据的带有a_bogus加密参数的Endpoint
            params_dict = params.dict()
            params_dict["msToken"] = ''
            a_bogus = BogusManager.ab_model_2_endpoint(params_dict, kwargs["headers"]["User-Agent"])
            endpoint = f"{DouyinAPIEndpoints.USER_POST}?{urlencode(params_dict)}&a_bogus={a_bogus}"

            response = await scraper.fetch_get_json(endpoint)
        return response

    # 获取用户喜欢作品数据
    async def fetch_user_like_videos(self, sec_user_id: str, max_cursor: int, count: int):
        kwargs = await self.get_douyin_headers()
        base_scraper = BaseScraper(proxies=kwargs["proxies"], scraper_headers=kwargs["headers"])
        async with base_scraper as scraper:
            params = UserLike(sec_user_id=sec_user_id, max_cursor=max_cursor, count=count)
            # endpoint = BogusManager.xb_model_2_endpoint(
            #     DouyinAPIEndpoints.USER_FAVORITE_A, params.dict(), kwargs["headers"]["User-Agent"]
            # )
            # response = await scraper.fetch_get_json(endpoint)

            params_dict = params.dict()
            params_dict["msToken"] = ''
            a_bogus = BogusManager.ab_model_2_endpoint(params_dict, kwargs["headers"]["User-Agent"])
            endpoint = f"{DouyinAPIEndpoints.USER_FAVORITE_A}?{urlencode(params_dict)}&a_bogus={a_bogus}"

            response = await scraper.fetch_get_json(endpoint)
        return response

    # 获取用户收藏作品数据（用户提供自己的Cookie）
    async def fetch_user_collection_videos(self, cookie: str, cursor: int = 0, count: int = 20):
        kwargs = await self.get_douyin_headers()
        kwargs["headers"]["Cookie"] = cookie
        base_scraper = BaseScraper(proxies=kwargs["proxies"], scraper_headers=kwargs["headers"])
        async with base_scraper as scraper:
            params = UserCollection(cursor=cursor, count=count)
            endpoint = BogusManager.xb_model_2_endpoint(
                DouyinAPIEndpoints.USER_COLLECTION, params.dict(), kwargs["headers"]["User-Agent"]
            )
            response = await scraper.fetch_post_json(endpoint)
        return response

    # 获取用户合辑作品数据
    async def fetch_user_mix_videos(self, mix_id: str, cursor: int = 0, count: int = 20):
        kwargs = await self.get_douyin_headers()
        base_scraper = BaseScraper(proxies=kwargs["proxies"], scraper_headers=kwargs["headers"])
        async with base_scraper as scraper:
            params = UserMix(mix_id=mix_id, cursor=cursor, count=count)
            endpoint = BogusManager.xb_model_2_endpoint(
                DouyinAPIEndpoints.MIX_AWEME, params.dict(), kwargs["headers"]["User-Agent"]
            )
            response = await scraper.fetch_get_json(endpoint)
        return response

    # 获取用户直播流数据
    async def fetch_user_live_videos(self, webcast_id: str, room_id_str=""):
        kwargs = await self.get_douyin_headers()
        base_scraper = BaseScraper(proxies=kwargs["proxies"], scraper_headers=kwargs["headers"])
        async with base_scraper as scraper:
            params = UserLive(web_rid=webcast_id, room_id_str=room_id_str)
            endpoint = BogusManager.xb_model_2_endpoint(
                DouyinAPIEndpoints.LIVE_INFO, params.dict(), kwargs["headers"]["User-Agent"]
            )
            response = await scraper.fetch_get_json(endpoint)
        return response

    # 获取指定用户的直播流数据
    async def fetch_user_live_videos_by_room_id(self, room_id: str):
        kwargs = await self.get_douyin_headers()
        base_scraper = BaseScraper(proxies=kwargs["proxies"], scraper_headers=kwargs["headers"])
        async with base_scraper as scraper:
            params = UserLive2(room_id=room_id)
            endpoint = BogusManager.xb_model_2_endpoint(
                DouyinAPIEndpoints.LIVE_INFO_ROOM_ID, params.dict(), kwargs["headers"]["User-Agent"]
            )
            response = await scraper.fetch_get_json(endpoint)
        return response

    # 获取直播间送礼用户排行榜
    async def fetch_live_gift_ranking(self, room_id: str, rank_type: int = 30):
        kwargs = await self.get_douyin_headers()
        base_scraper = BaseScraper(proxies=kwargs["proxies"], scraper_headers=kwargs["headers"])
        async with base_scraper as scraper:
            params = LiveRoomRanking(room_id=room_id, rank_type=rank_type)
            endpoint = BogusManager.xb_model_2_endpoint(
                DouyinAPIEndpoints.LIVE_GIFT_RANK, params.dict(), kwargs["headers"]["User-Agent"]
            )
            response = await scraper.fetch_get_json(endpoint)
        return response

    # 获取指定用户的信息
    async def handler_user_profile(self, sec_user_id: str):
        kwargs = await self.get_douyin_headers()
        base_scraper = BaseScraper(proxies=kwargs["proxies"], scraper_headers=kwargs["headers"])
        async with base_scraper as scraper:
            params = UserProfile(sec_user_id=sec_user_id)
            endpoint = BogusManager.xb_model_2_endpoint(
                DouyinAPIEndpoints.USER_DETAIL, params.dict(), kwargs["headers"]["User-Agent"]
            )
            response = await scraper.fetch_get_json(endpoint)
        return response

    # 获取指定视频的评论数据
    async def fetch_video_comments(self, aweme_id: str, cursor: int = 0, count: int = 20):
        kwargs = await self.get_douyin_headers()
        base_scraper = BaseScraper(proxies=kwargs["proxies"], scraper_headers=kwargs["headers"])
        async with base_scraper as scraper:
            params = PostComments(aweme_id=aweme_id, cursor=cursor, count=count)
            endpoint = BogusManager.xb_model_2_endpoint(
                DouyinAPIEndpoints.POST_COMMENT, params.dict(), kwargs["headers"]["User-Agent"]
            )
            response = await scraper.fetch_get_json(endpoint)
        return response

    # 获取指定视频的评论回复数据
    async def fetch_video_comments_reply(self, item_id: str, comment_id: str, cursor: int = 0, count: int = 20):
        kwargs = await self.get_douyin_headers()
        base_scraper = BaseScraper(proxies=kwargs["proxies"], scraper_headers=kwargs["headers"])
        async with base_scraper as scraper:
            params = PostCommentsReply(item_id=item_id, comment_id=comment_id, cursor=cursor, count=count)
            endpoint = BogusManager.xb_model_2_endpoint(
                DouyinAPIEndpoints.POST_COMMENT_REPLY, params.dict(), kwargs["headers"]["User-Agent"]
            )
            response = await scraper.fetch_get_json(endpoint)
        return response

    # 生成真实msToken
    async def gen_real_msToken(self, ):
        result = {
            "msToken": TokenManager().gen_real_msToken()
        }
        return result

    # 生成ttwid
    async def gen_ttwid(self, ):
        result = {
            "ttwid": TokenManager().gen_ttwid()
        }
        return result

    # 生成verify_fp
    async def gen_verify_fp(self, ):
        result = {
            "verify_fp": VerifyFpManager.gen_verify_fp()
        }
        return result

    # 生成s_v_web_id
    async def gen_s_v_web_id(self, ):
        result = {
            "s_v_web_id": VerifyFpManager.gen_s_v_web_id()
        }
        return result

    # 使用接口地址生成Xb参数
    async def get_x_bogus(self, url: str, user_agent: str):
        url = BogusManager.xb_str_2_endpoint(url, user_agent)
        result = {
            "url": url,
            "x_bogus": url.split("&X-Bogus=")[1],
            "user_agent": user_agent
        }
        return result

    # 使用接口地址生成Ab参数
    async def get_a_bogus(self, url: str, user_agent: str):
        endpoint = url.split("?")[0]
        # 将URL参数转换为dict
        params = dict([i.split("=") for i in url.split("?")[1].split("&")])
        # 去除URL中的msToken参数
        params["msToken"] = ""
        a_bogus = BogusManager.ab_model_2_endpoint(params, user_agent)
        result = {
            "url": f"{endpoint}?{urlencode(params)}&a_bogus={a_bogus}",
            "a_bogus": a_bogus,
            "user_agent": user_agent
        }
        return result

    # 提取单个用户id
    async def get_sec_user_id(self, url: str):
        return await SecUserIdFetcher.get_sec_user_id(url)

    # 提取列表用户id
    async def get_all_sec_user_id(self, urls: list):
        # 提取有效URL
        urls = extract_valid_urls(urls)

        # 对于URL列表
        return await SecUserIdFetcher.get_all_sec_user_id(urls)

    # 提取单个作品id
    async def get_aweme_id(self, url: str):
        return await AwemeIdFetcher.get_aweme_id(url)

    # 提取列表作品id
    async def get_all_aweme_id(self, urls: list):
        # 提取有效URL
        urls = extract_valid_urls(urls)

        # 对于URL列表
        return await AwemeIdFetcher.get_all_aweme_id(urls)

    # 提取单个直播间号
    async def get_webcast_id(self, url: str):
        return await WebCastIdFetcher.get_webcast_id(url)

    # 提取列表直播间号
    async def get_all_webcast_id(self, urls: list):
        # 提取有效URL
        urls = extract_valid_urls(urls)

        # 对于URL列表
        return await WebCastIdFetcher.get_all_webcast_id(urls)

    async def main(self):
        # aweme_id = "7372484719365098803"
        # result = await self.fetch_one_video(aweme_id)
        # print(result)
        pass


if __name__ == "__main__":
    # 初始化
    DouyinWebScraper = DouyinWebScraper()

    # 开始时间
    start = time.time()

    asyncio.run(DouyinWebScraper.main())

    # 结束时间
    end = time.time()
    print(f"耗时：{end - start}")
