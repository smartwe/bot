"""
kakao.py
=======
kakao.py is a very simple kakaotalk LOCO/HTTP API protocol wrapper for python.

-------------

Introduction
------------
Loco protocol compatible python library

This is rewritten version of KakaoBot by jhlee.

DO NOT USE IN ABUSING. ABUSING CAN CAUSE PERMANENT SERVICE RESTRICTION.

Quick Start
-------
```python
import kakao

class Myclass(kakao.Client):
    async def onReady(self):
        print("Logged on")

    async def onMessage(self, chat):
        if chat.message == "ping":
            await chat.reply("pong!")

kakao.check_reg("LoginId", "LoginPw")
client = Myclass("LoginId", "LoginPw")
client.run()
```

Thanks to
-------
idev-develop/KakaoBot

License
-------
MIT Licence
"""

import json
from socket import socket
import asyncio
import struct

from .booking import getBookingData
from .checkIn import getCheckInData
from .cryptoManager import CryptoManager
from .httpApi import postText, Login
from .writer import Writer
from .chat import Message
from .channel import Channel
from .packet import Packet

try:
    import bson
except ImportError as e:
    print("ImportError: {}".format(str(e)))
    exit()


class Client:
    """
    Represents a client connection that connects to KakaoTalk.

    Parameters:
        LoginId: account ID [type str]
        LoginPw: account PW [type str]
        device_name : Device's Name. [type str]
        device_uuid : Device's Uuid. [type str]
        debug: if debug is true, it prints some log to console. [type bool]

    Returns:

    Remarks:
        You can pass any string to 'device_uuid' but base64-encoded string recommended.
        Default value of device_name is "kakao.py".
        Default value of device_uuid id base64-encoded str of "kakaopydev1202".
    """

    def __init__(
        self,
        LoginId,
        LoginPw,
        device_name="kakao.py",
        device_uuid="a2FrYW9weWRldjEyMDI=",
        debug=False,
    ):
        self.__sock: socket
        self.__StreamReader: asyncio.StreamReader
        self.__StreamWriter: asyncio.StreamWriter
        self.__crypto: CryptoManager
        self.__writer: Writer
        self.__accessKey: str

        self.LoginId = LoginId
        self.LoginPw = LoginPw
        self.device_name = device_name
        self.device_uuid = device_uuid
        self.debug = debug

        self.__packetID = 0

        self.__processingBuffer = b""
        self.__processingHeader = b""
        self.__processingSize = 0

        self.packetDict = {}

    def postText(self, chatId, li, text, notice=False):
        """
        Description.

        Parameters:

        Returns:

        Remarks:
        """
        postText(chatId, li, text, notice, self.__accessKey, self.device_uuid)

    async def __recvPacket(self):
        encryptedBuffer = b""
        currentPacketSize = 0

        while True:
            recv = await self.__StreamReader.read(256)

            if not recv:
                print(recv)
                self.loop.stop()
                break

            encryptedBuffer += recv

            if not currentPacketSize and len(encryptedBuffer) >= 4:
                currentPacketSize = struct.unpack("<I", encryptedBuffer[0:4])[0]

            if currentPacketSize:
                encryptedPacketSize = currentPacketSize + 4

                if len(encryptedBuffer) >= encryptedPacketSize:
                    self.loop.create_task(
                        self.__processingPacket(encryptedBuffer[0:encryptedPacketSize])
                    )
                    encryptedBuffer = encryptedBuffer[encryptedPacketSize:]
                    currentPacketSize = 0

    async def __processingPacket(self, encryptedPacket):
        encLen = encryptedPacket[0:4]
        IV = encryptedPacket[4:20]
        BODY = encryptedPacket[20:]

        self.__processingBuffer += self.__crypto.aesDecrypt(BODY, IV)

        if not self.__processingHeader and len(self.__processingBuffer) >= 22:
            self.__processingHeader = self.__processingBuffer[0:22]
            self.__processingSize = (
                struct.unpack("<i", self.__processingHeader[18:22])[0] + 22
            )

        if self.__processingHeader:
            if len(self.__processingBuffer) >= self.__processingSize:
                p = Packet()
                p.readLocoPacket(self.__processingBuffer[: self.__processingSize])

                self.loop.create_task(self.__onPacket(p))

                self.__processingBuffer = self.__processingBuffer[
                    self.__processingSize :
                ]
                self.__processingHeader = b""

    async def __onPacket(self, packet):
        if packet.PacketID in self.packetDict:
            self.packetDict[packet.PacketID].set_result(packet)
            del self.packetDict[packet.PacketID]

        self.loop.create_task(self.onPacket(packet))

        body = packet.toJsonBody()

        if self.debug == True:
            print(packet.PacketName)

        if packet.PacketName == "MSG":
            chatId = body["chatLog"]["chatId"]

            if "li" in body:
                li = body["li"]
            else:
                li = 0

            channel = Channel(chatId, li, self.__writer)
            chat = Message(channel, body)

            self.loop.create_task(self.onMessage(chat))

        if packet.PacketName == "NEWMEM":
            chatId = body["chatLog"]["chatId"]

            if "li" in body:
                li = body["li"]
            else:
                li = 0

            channel = Channel(chatId, li, self.__writer)
            self.loop.create_task(self.onJoin(packet, channel))

        if packet.PacketName == "DELMEM":
            chatId = body["chatLog"]["chatId"]

            if "li" in body:
                li = body["li"]
            else:
                li = 0

            channel = Channel(chatId, li, self.__writer)
            self.loop.create_task(self.onQuit(packet, channel))

        if packet.PacketName == "DECUNREAD":
            chatId = body["chatId"]

            channel = Channel(chatId, 0, self.__writer)
            self.loop.create_task(self.onRead(channel, body))

    async def onReady(self):
        pass

    async def onPacket(self, packet):
        pass

    async def onMessage(self, chat):
        pass

    async def onJoin(self, packet, channel):
        pass

    async def onQuit(self, packet, channel):
        pass

    async def onRead(self, channel, packet):
        pass

    async def __heartbeat(self):
        while True:
            await asyncio.sleep(180)
            PingPacket = Packet(0, 0, "PING", 0, bson.encode({}))
            self.loop.create_task(self.__writer.sendPacket(PingPacket))

    async def __login(
        self,
        LoginId,
        LoginPw,
    ):
        r = json.loads(Login(LoginId, LoginPw, self.device_name, self.device_uuid))

        if r["status"] == -101:
            print("이전에 로그인이 되어있는 PC에서 로그아웃 해주세요")

        elif r["status"] == -100:
            print("디바이스 등록이 되어 있지 않습니다")

        elif r["status"] == 12:
            print("카카오계정 또는 비밀번호를 다시 확인해 주세요")

        if r["status"] != 0:
            self.loop.stop()
            raise Exception(str(r))

        self.__accessKey = r["access_token"]

        bookingData = getBookingData().toJsonBody()

        checkInData = getCheckInData(
            bookingData["ticket"]["lsl"][0], bookingData["wifi"]["ports"][0]
        ).toJsonBody()

        self.__StreamReader, self.__StreamWriter = await asyncio.open_connection(
            checkInData["host"], int(checkInData["port"])
        )

        self.__crypto = CryptoManager()
        self.__writer = Writer(self.__crypto, self.__StreamWriter, self.packetDict)

        LoginListPacket = Packet(
            0,
            0,
            "LOGINLIST",
            0,
            bson.encode(
                {
                    "appVer": "3.2.7",
                    "prtVer": "1",
                    "os": "win32",
                    "lang": "ko",
                    "duuid": self.device_uuid,
                    "oauthToken": self.__accessKey,
                    "dtype": 1,
                    "ntype": 0,
                    "MCCMNC": "999",
                    "revision": 0,
                    "chatIds": [],
                    "maxIds": [],
                    "lastTokenId": 0,
                    "lbk": 0,
                    "bg": False,
                }
            ),
        )

        if self.debug:
            print(bookingData)
            print(checkInData)
            print(LoginListPacket)

        self.__StreamWriter.write(self.__crypto.getHandshakePacket())

        self.loop.create_task(self.__writer.sendPacket(LoginListPacket))

        self.loop.create_task(self.__recvPacket())
        self.loop.create_task(self.__heartbeat())
        self.loop.create_task(self.onReady())

    def run(self):
        """
        A blocking function that logs in to the client and run.

        Parameters:

        Returns:

        Remarks:
        """
        self.loop = asyncio.get_event_loop()
        self.loop.create_task(self.__login(self.LoginId, self.LoginPw))
        self.loop.run_forever()