from typing import Any, List, Optional
from pydantic import BaseModel, Field

from scraper.douyin.web.utils import TokenManager, VerifyFpManager


# Base Model
class BaseRequestModel(BaseModel):
    device_platform: str = "webapp"
    aid: str = "6383"
    channel: str = "channel_pc_web"
    pc_client_type: int = 1
    version_code: str = "190500"
    version_name: str = "19.5.0"
    cookie_enabled: str = "true"
    screen_width: int = 1920
    screen_height: int = 1080
    browser_language: str = "zh-CN"
    browser_platform: str = "Win32"
    browser_name: str = "Firefox"
    browser_version: str = "124.0"
    browser_online: str = "true"
    engine_name: str = "Gecko"
    engine_version: str = "122.0.0.0"
    os_name: str = "Windows"
    os_version: str = "10"
    cpu_core_num: int = 12
    device_memory: int = 8
    platform: str = "PC"
    msToken: str = TokenManager.gen_real_msToken()


class BaseLiveModel(BaseModel):
    aid: str = "6383"
    app_name: str = "douyin_web"
    live_id: int = 1
    device_platform: str = "web"
    language: str = "zh-CN"
    cookie_enabled: str = "true"
    screen_width: int = 1920
    screen_height: int = 1080
    browser_language: str = "zh-CN"
    browser_platform: str = "Win32"
    browser_name: str = "Edge"
    browser_version: str = "119.0.0.0"
    enter_source: Any = ""
    is_need_double_stream: str = "false"
    # msToken: str = TokenManager.gen_real_msToken()
    # _signature: str = ''


class BaseLiveModel2(BaseModel):
    verifyFp: str = VerifyFpManager.gen_verify_fp()
    type_id: str = "0"
    live_id: str = "1"
    sec_user_id: str = ""
    version_code: str = "99.99.99"
    app_id: str = "1128"
    msToken: str = TokenManager.gen_real_msToken()


class BaseLoginModel(BaseModel):
    service: str = "https://www.douyin.com"
    need_logo: str = "false"
    need_short_url: str = "true"
    device_platform: str = "web_app"
    aid: str = "6383"
    account_sdk_source: str = "sso"
    sdk_version: str = "2.2.7-beta.6"
    language: str = "zh"


class BaseHomeFeed(BaseRequestModel):
    module_id: int = 3003101 # Đây là mã định danh của module hoặc phần giao diện mà API sẽ lấy dữ liệu
    filterGids: str = "" # Danh sách các gid (group ID) cần lọc ra khỏi kết quả. Ex: "123,456,789"
    presented_ids: str = "" # Danh sách ID của các mục đã được hiển thị trước đó. Ex: "1001,1002,1003"
    refer_id: str = "" # ID tham chiếu, có thể là ID của nội dung hoặc người dùng liên quan đến yêu cầu API
    refer_type: int = 10 # Loại tham chiếu, mô tả loại dữ liệu hoặc ngữ cảnh mà refer_id thuộc về : video, người dùng, module
    install_time: int = 1729440337 # Thời gian cài đặt ứng dụng hoặc phiên bản hiện tại, tính bằng Unix timestamp
    use_lite_type: int = 0 # Chỉ định phiên bản ứng dụng, có thể là bản đầy đủ hay bản rút gọn (lite)
    pc_libra_divert: str = 'Mac' # Chỉ định hệ điều hành của máy tính hoặc thiết bị (như Mac hoặc Windows).
    update_version_code: int = 170400 # Mã phiên bản cập nhật của ứng dụng, dùng để xác định phiên bản ứng dụng hiện tại và có thể giúp API cung cấp các tính năng phù hợp với phiên bản này.


class BaseRecommendFeed(BaseRequestModel):
    tag_id: str = ""
    share_aweme_id: str = ""
    live_insert_type: str = ""
    video_type_select: int = 1
    globalwid: str = "7427889601202669082"
    pull_type: int = 1
    refresh_type: int = 1
    min_window: int = 0
    free_right: int = 0
    view_count: int = 0
    plug_block: int = 0
    ug_source: str = ""
    creative_id: str = ""
    pc_libra_divert: str = "Mac"


# Model
class AwemeDetail(BaseRequestModel):
    aweme_id: str = Field(example="7372484719365098803", description="")
    msToken : Optional[str] = ""


class TrendingList(BaseRequestModel):
    detail_list: int = 1
    source: int = 6
    main_billboard_count: int = 5
    downlink: int = 10
    webid: str = "7427889601202669082"
    round_trip_time: int = 100
    effective_type: str = '4g'
    fp: str = VerifyFpManager.gen_verify_fp()
    verifyFp: str = VerifyFpManager.gen_verify_fp()


class HomeFeed(BaseHomeFeed):
    count: int = Field(default=10, description="") # Số lượng mục hoặc kết quả mà API cần trả về
    refresh_index: Optional[int] = Field(default=1, description="") # Chỉ số làm mới hoặc số lần làm mới nội dung
    awemePcRecRawData: Optional[dict] = {"is_client": False} # {"from_gid":"7429563055903706409"}


class RecommendFeed(BaseRecommendFeed):
    count: int = Field(default=10, description="") # Số lượng mục hoặc kết quả mà API cần trả về
    refresh_index: Optional[int] = Field(default=1, description="") # Chỉ số làm mới hoặc số lần làm mới nội dung
    aweme_pc_rec_raw_data: Optional[dict] = {"is_client":False,"ff_danmaku_status":0,"danmaku_switch_status":0,"is_auto_play":0,"is_full_screen":0,"is_full_webscreen":0,"is_mute":1,"is_speed":1,"is_visible":1,"related_recommend":1} # "videoPrefer":{"fsn":["7428118166498266420","4139041310389464"],"like":[],"halfMin":["7428118166498266420","4139041310389464"],"min":["7428118166498266420","4139041310389464"]


class RelatedAweme(BaseRequestModel):
    aweme_id: str = Field(example="7372484719365098803", description="aweme_id liên quan")
    count: int = Field(default=15, description="")
    filterGids: str = Field(example="7372484719365098803, 7372484719365045806", description="Các aweme_id cần loại bỏ khi lấy danh sách")
    refresh_index: int = Field(default=1, description="")
    awemePcRecRawData: Optional[dict] = {"is_client": False}
    sub_channel_id: Optional[int] = Field(default=3, description="")
    update_version_code: Optional[int] = 170400
    pc_client_type: Optional[int] = 1
    pc_libra_divert: Optional[str] = "Mac"
    downlink: int = 10
    webid: str = "7427889601202669082"

# Sắp xếp toàn diện
# search_channel: aweme_general
# enable_history: 1
# keyword: gái xinh viet nam
# search_source: normal_search
# query_correct_type: 1
# is_filter_search: 0
# from_group_id: 
# offset: 0
# count: 10
# need_filter_settings: 1
# list_type: single


# Phát hành mới nhất
# search_channel: aweme_general
# enable_history: 1
# filter_selected: {"sort_type":"2","publish_time":"0", "filter_duration":"0-1"} 
                                            # publish_time = 0,1,7,180 (don vị : ngày)
                                            # filter_duration : "0-1", "1-5" "5-10000" (5-10000 là lớn hơn 5) (đơn vị phút)
# keyword: gái xinh viet nam
# search_source: tab_search (sử dụng khi có bộ lọc),
                # normal_search (tìm kiếm thông thường, k bộ lọc), 
                # switch_tab (), 
                # hot_search_board (tìm kiếm theo từ khoá, chủ đề hot, k bo lọc), 
                # recom_search (từ khoá gơi ý, k bo loc)
# query_correct_type: 1
# is_filter_search: 1
# from_group_id: 
# offset: 0
# count: 10
# need_filter_settings: 1
# list_type: single

# Nhieu luot thich
# search_channel: aweme_general
# enable_history: 1
# filter_selected: {"sort_type":"2","publish_time":"0"}
# keyword: gái xinh viet nam
# search_source: tab_search
# query_correct_type: 1
# is_filter_search: 1
# from_group_id: 
# offset: 0
# count: 10
# need_filter_settings: 1
# list_type: single / multi


# search_id: 20241027020554DF04B0D990FE0317CB43 sử dung để phân trang

class UserProfile(BaseRequestModel):
    sec_user_id: str


class UserPost(BaseRequestModel):
    max_cursor: int
    count: int
    sec_user_id: str


# 获取单个作品视频弹幕数据
class PostDanmaku(BaseRequestModel):
    item_id: str
    duration: int
    end_time: int
    start_time: int = 0


class UserLike(BaseRequestModel):
    max_cursor: int
    count: int
    sec_user_id: str


class UserCollection(BaseRequestModel):
    # POST
    cursor: int
    count: int


class UserCollects(BaseRequestModel):
    # GET
    cursor: int
    count: int


class UserCollectsVideo(BaseRequestModel):
    # GET
    cursor: int
    count: int
    collects_id: str


class UserMusicCollection(BaseRequestModel):
    # GET
    cursor: int
    count: int


class UserMix(BaseRequestModel):
    cursor: int
    count: int
    mix_id: str


class FriendFeed(BaseRequestModel):
    cursor: int = 0
    level: int = 1
    aweme_ids: str = ""
    room_ids: str = ""
    pull_type: int = 0
    address_book_access: int = 2
    gps_access: int = 2
    recent_gids: str = ""


class PostFeed(BaseRequestModel):
    count: int = 10
    tag_id: str = ""
    share_aweme_id: str = ""
    live_insert_type: str = ""
    refresh_index: int = 1
    video_type_select: int = 1
    aweme_pc_rec_raw_data: dict = {}  # {"is_client":false}
    globalwid: str = ""
    pull_type: str = ""
    min_window: str = ""
    free_right: str = ""
    ug_source: str = ""
    creative_id: str = ""


class FollowFeed(BaseRequestModel):
    cursor: int = 0
    level: int = 1
    count: int = 20
    pull_type: str = ""


class PostRelated(BaseRequestModel):
    aweme_id: str
    count: int = 20
    filterGids: str  # id,id,id
    awemePcRecRawData: dict = {}  # {"is_client":false}
    sub_channel_id: int = 3
    # Seo-Flag: int = 0


class PostComments(BaseRequestModel):
    aweme_id: str
    cursor: int = 0
    count: int = 20
    item_type: int = 0
    insert_ids: str = ""
    whale_cut_token: str = ""
    cut_version: int = 1
    rcFT: str = ""


class PostCommentsReply(BaseRequestModel):
    item_id: str
    comment_id: str
    cursor: int = 0
    count: int = 20
    item_type: int = 0


class PostLocate(BaseRequestModel):
    sec_user_id: str
    max_cursor: str  # last max_cursor
    locate_item_id: str = ""  # aweme_id
    locate_item_cursor: str
    locate_query: str = "true"
    count: int = 10
    publish_video_strategy_type: int = 2


class UserLive(BaseLiveModel):
    web_rid: str
    room_id_str: str


# 直播间送礼用户排行榜
class LiveRoomRanking(BaseRequestModel):
    webcast_sdk_version: int = 2450
    room_id: int
    # anchor_id: int
    # sec_anchor_id: str
    rank_type: int = 30


class UserLive2(BaseLiveModel2):
    room_id: str


class FollowUserLive(BaseRequestModel):
    scene: str = "aweme_pc_follow_top"


class SuggestWord(BaseRequestModel):
    query: str = ""
    count: int = 8
    business_id: str
    from_group_id: str
    rsp_source: str = ""
    penetrate_params: dict = {}


class LoginGetQr(BaseLoginModel):
    verifyFp: str = ""
    fp: str = ""
    # msToken: str = TokenManager.gen_real_msToken()


class LoginCheckQr(BaseLoginModel):
    token: str = ""
    verifyFp: str = ""
    fp: str = ""
    # msToken: str = TokenManager.gen_real_msToken()


class UserFollowing(BaseRequestModel):
    user_id: str = ""
    sec_user_id: str = ""
    offset: int = 0  # 相当于cursor
    min_time: int = 0
    max_time: int = 0
    count: int = 20
    # source_type = 1: 最近关注 需要指定max_time(s) 3: 最早关注 需要指定min_time(s) 4: 综合排序
    source_type: int = 4
    gps_access: int = 0
    address_book_access: int = 0
    is_top: int = 1


class UserFollower(BaseRequestModel):
    user_id: str
    sec_user_id: str
    offset: int = 0  # 相当于cursor 但只对source_type: = 2 有效，其他情况为 0 即可
    min_time: int = 0
    max_time: int = 0
    count: int = 20
    # source_type = 1: 最近关注 需要指定max_time(s) 2: 综合关注(意义不明)
    source_type: int = 1
    gps_access: int = 0
    address_book_access: int = 0
    is_top: int = 1


# 列表作品
class URL_List(BaseModel):
    urls: List[str] = [
        "https://test.example.com/xxxxx/",
        "https://test.example.com/yyyyy/",
        "https://test.example.com/zzzzz/"
    ]