---
title: '古法编程“行为艺术”'
date: 2026-11-09T02:29:17+08:00
slug: "handcrafted-programming-performance-art"
draft: false
author: "十布"
summary: "计划开发一个多平台聚合客户端，目前已支持学习通自动登录、课程列表获取、通知和群聊消息读取等。"
tags: ["编程", "开发"]
ShowToc: false
---

尊重自己的内心，重拾编程手艺hh。计划开发一个多平台聚合客户端。目前代码三百行左右，已实现自动登录学习通，获取课程列表、通知和群聊消息等。部分代码如下，后续在 GitHub 上继续更新：

```python
import base64
import json
import time
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup
from playwright.sync_api import Cookie, sync_playwright

import easemob_pb2 as pb2


@dataclass
class Channel:
    chat_id: str
    group_id: str
    sender_id: str
    recent_message: str


@dataclass
class ChannelMessage:
    group_id: str
    sender_id: str
    message: str
    attachment: dict[str, object] | None


@dataclass
class Course:
    clazz_id: str
    course_id: str
    cur_person_id: str
    course_name: str
    is_finished: bool


@dataclass
class Notice:
    notice_id: str
    title: str
    sender: str
    send_time: str
    content: str
    content_html: str


@dataclass
class ImCredentials:
    uid: int
    hx_token: str


class ChaoxingClient:
    def __init__(self, account: str, password: str) -> None:
        if not account or any(c < '0' or c > '9' for c in account):
            raise ValueError("账号必须由 0-9 数字组成")
        
        self.account = account
        self.password = password
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/157.0.0.0 Safari/537.36 Edg/157.0.0.0"
            )
        })

        self.auth_file = Path(__file__).parent / ".auth" / f"{account}.json"
        if self.auth_file.is_file():
            cookies = json.loads(self.auth_file.read_text(encoding="utf-8"))
        else:
            cookies = self._login(auto_save=True)
        self._load_cookies(cookies)

    def _login(self, auto_save: bool = True) -> list[Cookie]:
        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page()
            page.goto("https://fysso.chaoxing.com/oauthsso/fudan")
            page.locator("#login-username").fill(self.account)
            page.locator("#login-password").fill(self.password)
            page.get_by_role("button", name="登录", exact=True).click()

            page.wait_for_url("https://fudan.mooc.chaoxing.com/portal")
            page.goto("https://i.chaoxing.com")
            cookies = page.context.cookies()
            browser.close()

        if auto_save:
            self.auth_file.parent.mkdir(parents=True, exist_ok=True)
            self.auth_file.write_text(json.dumps(cookies), encoding="utf-8")
        return cookies

    def _load_cookies(self, cookies: list[Cookie]) -> None:
        self.session.cookies.clear()
        for cookie in cookies:
            if "name" not in cookie or "value" not in cookie:
                raise ValueError("无法加载 Cookie: 缺少 name 或 value 字段")

            expires = cookie.get("expires", -1)
            http_only = cookie.get("httpOnly", False)
            self.session.cookies.set(
                name=cookie["name"],
                value=cookie["value"],
                domain=cookie.get("domain", ""),
                path=cookie.get("path", "/"),
                secure=cookie.get("secure", False),
                expires=int(expires) if expires >= 0 else None,
                discard=expires < 0,
                rest={"HttpOnly": None} if http_only else {},
            )

    @staticmethod
    def _is_login_page(res: requests.Response) -> bool:
        target = urlparse(res.url)
        return (
            target.hostname == "passport2.chaoxing.com"
            and target.path.rstrip("/") == "/login"
        )

    def _request(self, method: str, url: str, **kwargs) -> requests.Response:
        kwargs.setdefault("timeout", 30)
        res = self.session.request(method, url, **kwargs)

        if self._is_login_page(res):
            self._load_cookies(self._login(auto_save=True))
            res = self.session.request(method, url, **kwargs)
            if self._is_login_page(res):
                raise RuntimeError("重新登录后，请求仍跳转到登录页")

        res.raise_for_status()
        return res

    def get_course_list(self) -> list[Course]:
        url = "https://mooc2-ans.chaoxing.com/mooc2-ans/visit/courselistdata"
        data = {
            "courseType": "1",
            "courseFolderId": "0",
            "query": "",
            "pageHeader": "-1",
            "single": "0",
            "superstarClass": "0",
            "isFirefly": "0",
            "courseLevelLabelId": "0",
            "fid": "",
            "from": "",
        }
        res = self._request("POST", url, data=data)
        soup = BeautifulSoup(res.content, "html.parser", from_encoding="utf-8")

        course_list = soup.select_one("#courseList")
        if course_list is None:
            raise RuntimeError("响应中没有课程列表，请检查登录状态或返回内容")
        
        courses: list[Course] = []
        for div in course_list.select("div[info]"):
            clazz_id = div.select_one("input.clazzId")
            course_id = div.select_one("input.courseId")
            person_id = div.select_one("input.curPersonId")
            course_name = div.select_one(".course-name")
            if (
                clazz_id is None
                or course_id is None
                or person_id is None
                or course_name is None
            ):
                raise ValueError(f"课程字段不完整：{div.get('info')}")

            course = Course(
                clazz_id=str(clazz_id["value"]),
                course_id=str(course_id["value"]),
                cur_person_id=str(person_id["value"]),
                course_name=course_name.get_text(strip=True),
                is_finished=div.select_one(".not-open-tip") is not None,
            )
            courses.append(course)
        return courses
    
    def get_recent_notices(self, year: int | None = None) -> list[Notice]:
        if year is None:
            year = datetime.now().year
        url = "https://notice.chaoxing.com/pc/notice/getNoticeList"
        data = {
            "type": "2",
            "notice_type": "",
            "lastValue": "",
            "sort": "",
            "folderUUID": "",
            "kw": "",
            "startTime": "",
            "endTime": "",
            "gKw": "",
            "gName": "",
            "year": str(year),
            "tag": "",
            "fidsCode": "",
            "queryFolderNoticePrevYear": "0",
            "filterSenderPuids": "",
            "filterTags": "",
        }
        res = self._request("POST", url, data=data)

        notices = []
        for item in res.json()["notices"]["list"]:
            notice = Notice(
                notice_id=item["idCode"],
                title=item["title"],
                sender=item["createrName"],
                send_time=item["sendTime"],
                content=item["content"],
                content_html=item["rtf_content"],
            )
            notices.append(notice)
        return notices

    def get_im_credentials(self) -> ImCredentials:
        url = "https://learn.chaoxing.com/apis/user/getUserImToken"
        res = self._request("GET", url, params={"crossOrigin": True})
        msg = res.json()["msg"]
        return ImCredentials(uid=msg["uid"], hx_token=msg["hxToken"])

    def get_user_name(self, tuid: str) -> str:
        url = "https://im.chaoxing.com/webim/user/getUserInfoByTuid"
        params = {"crossOrigin": "true", "tuid": tuid}
        headers = {"Accept": "application/json, text/plain, */*"}
        res = self._request("GET", url, params=params, headers=headers)
        return res.json()["name"]

    def get_group_name(self, room_id: str) -> str:
        url = "https://im.chaoxing.com/webim/huanxin/getGroupInfo"
        params = {"crossOrigin": "true", "roomId": room_id}
        headers = {"Accept": "application/json, text/plain, */*"}
        res = self._request("GET", url, params=params, headers=headers)
        return res.json()[0]["name"]

    def get_channel_list(
        self, 
        credentials: ImCredentials | None = None, 
        limit: int = 50
    ) -> list[Channel]:
        if credentials is None:
            credentials = self.get_im_credentials()

        url = f"https://a3-vip6.easemob.com/cx-dev/cxstudy/sdk/user/{credentials.uid}/user_channels/list"
        params = {
            "limit": limit,
            "cursor": "",
            "need_mark": "true",
            "needEmptySession": "true",
            "_v": int(time.time() * 1000),
        }
        headers = {"Authorization": f"Bearer {credentials.hx_token}"}
        res = self._request("GET", url, params=params, headers=headers)

        channels = []
        for item in res.json()["data"]["channel_infos"]:
            meta = item.get("meta")
            if not meta or not meta.get("payload"):
                continue
            payload = json.loads(meta["payload"])
            if payload["type"] == "groupchat":
                recent_message = next(
                    (body["msg"] for body in payload["bodies"] if body["type"] == "txt"),
                    "",
                )
                channel = Channel(
                    chat_id = payload["to"],
                    group_id = payload["to"],
                    sender_id = payload["from"],
                    recent_message = recent_message,
                )
                channels.append(channel)
        return channels

    def get_channel_message(
        self, 
        chat_id: str, 
        credentials: ImCredentials | None = None, 
        limit: int = 20
    ) -> list[ChannelMessage]:
        if credentials is None:
            credentials = self.get_im_credentials()

        url = f"https://a3-vip6.easemob.com/cx-dev/cxstudy/users/{credentials.uid}/messageroaming"
        data = {
            "queue": f"{chat_id}@conference.easemob.com",
            "start": -1,
            "end": -1,
            "pull_number": limit,
            "is_positive": False,
            "msgType": "",
            "startTime": None,
            "endTime": None,
            "userId": None,
        }
        headers = {"Authorization": f"Bearer {credentials.hx_token}"}
        res = self._request("POST", url, json=data, headers=headers)

        messages = []
        for item in res.json()["data"]["msgs"]:
            raw = base64.b64decode(item["msg"], validate=True)
            meta = pb2.Meta()
            meta.ParseFromString(raw)
            if meta.ns != pb2.Meta.CHAT:
                continue

            body = pb2.MessageBody()
            body.ParseFromString(meta.payload)
            if body.type == pb2.MessageBody.GROUPCHAT:
                message = next((
                    content.text
                    for content in body.contents
                    if content.type == pb2.MessageBody.Content.TEXT
                ), "")
                attach_item = next((
                    item.stringValue
                    for item in body.ext
                    if item.key == "attachment"
                    and item.type == pb2.KeyValue.JSON_STRING
                ), None)
                
                channel_message = ChannelMessage(
                    group_id = body.to.name,
                    sender_id = getattr(body, "from").name,
                    message = message,
                    attachment = json.loads(attach_item) if attach_item is not None else None,
                )
                messages.append(channel_message)
        return messages

if __name__ == "__main__":
    client = ChaoxingClient("xxxxxxxxxxx", "xxxxxxxx")
    #....
```
