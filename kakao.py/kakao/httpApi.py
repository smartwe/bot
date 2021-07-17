import json

import requests
import hashlib

Agent = "win32"
Lang = "ko"
Version = "3.2.7"
AppVersion = "3.2.7.2777"
OsVersion = "10.0"

AuthHeader = f"{Agent}/{Version}/{Lang}"
AuthUserAgent = f"KT/{Version} Wd/{OsVersion} {Lang}"

LoginUrl = "https://ac-sb-talk.kakao.com/win32/account/login.json"
RegisterDeviceUrl = "https://ac-sb-talk.kakao.com/win32/account/register_device.json"
RequestPasscodeUrl = "https://ac-sb-talk.kakao.com/win32/account/request_passcode.json"
MoreSettingUrl = (
    f"https://sb-talk.kakao.com/win32/account/more_settings.json?since={0}&lang={Lang}"
)
MediaUrl = "https://up-m.talk.kakao.com/upload"


def RequestPasscode(email, password, device_name, device_uuid):
    h = Header(email, device_uuid)
    d = Data(email, password, device_name, device_uuid)
    d["permanent"] = "true"
    d["once"] = "false"
    r = requests.post(RequestPasscodeUrl, headers=h, data=d)

    return r.content.decode()


def RegisterDevice(email, password, device_name, device_uuid, passcode):
    h = Header(email, device_uuid)
    d = Data(email, password, device_name, device_uuid)
    d["permanent"] = "true"
    d["once"] = "false"
    d["passcode"] = passcode
    r = requests.post(RegisterDeviceUrl, headers=h, data=d)

    return r.content.decode()


def Login(email, password, device_name, device_uuid):
    h = Header(email, device_uuid)
    d = Data(email, password, device_name, device_uuid)
    d["permanent"] = True
    d["forced"] = True
    r = requests.post(LoginUrl, headers=h, data=d)

    return r.content.decode()


def Header(email, device_uuid):
    return {
        "Content-Type": "application/x-www-form-urlencoded",
        "A": AuthHeader,
        "X-VC": getXVC(email, device_uuid),
        "User-Agent": AuthUserAgent,
        "Accept": "*/*",
        "Accept-Language": Lang,
    }


def getXVC(email, device_uuid, isFull=False):
    string = f"HEATH|{AuthUserAgent}|DEMIAN|{email}|{device_uuid}".encode("utf-8")
    hash = hashlib.sha512(string).hexdigest()
    if isFull:
        return hash
    return hash[0:16]


def Data(email, password, device_name, device_uuid):
    return {
        "email": email,
        "password": password,
        "device_name": device_name,
        "device_uuid": device_uuid,
        "os_version": OsVersion,
    }


def upload(data, dataType, userId):
    r = requests.post(
        MediaUrl,
        headers={
            "A": AuthHeader,
        },
        data={
            "attachment_type": dataType,
            "user_id": userId,
        },
        files={
            "attachment": data,
        },
    )
    path = r.content.decode()
    key = path.replace("/talkm", "")
    url = "https://dn-m.talk.kakao.com" + path

    return path, key, url


def postText(chatId, li, text, notice, accessKey, deviceUUID):
    if li == 0:
        url = f"https://talkmoim-api.kakao.com/chats/{chatId}/posts"
    else:
        url = f"https://open.kakao.com/moim/chats/{chatId}/posts?link_id={li}"

    r = requests.post(
        url,
        headers={
            "A": AuthHeader,
            "User-Agent": AuthUserAgent,
            "Authorization": f"{accessKey}-{deviceUUID}",
            "Accept-Language": "ko",
        },
        data={
            "content": json.dumps([{"text": text, "type": "text"}]),
            "object_type": "TEXT",
            "notice": notice,
        },
    )

    print(r.content.decode())
