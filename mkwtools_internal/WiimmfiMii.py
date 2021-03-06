import mkwtools_internal.Mii as Mii
import mkwtools_internal.common as common
import binascii
import requests
import base64

WIIMMFI_SAKE = 'http://mariokartwii.sake.gs.wiimmfi.de/SakeStorageServer/StorageServer.asmx'


#pid or fc
def get_wiimmfi_mii(playerid: str):
	playerid = common.fc_to_pid(int(playerid.replace("-","")), b'RMCJ')
	mii_data = requests.post(WIIMMFI_SAKE, data=f'<?xml version="1.0" encoding="UTF-8"?><SOAP-ENV:Envelope xmlns:SOAP-ENV="http://schemas.xmlsoap.org/soap/envelope/" xmlns:SOAP-ENC="http://schemas.xmlsoap.org/soap/encoding/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:ns1="http://gamespy.net/sake"><SOAP-ENV:Body><ns1:SearchForRecords><ns1:gameid>1687</ns1:gameid><ns1:secretKey>test</ns1:secretKey><ns1:loginTicket>23c715d620f986c22Pwwii</ns1:loginTicket><ns1:tableid>FriendInfo</ns1:tableid><ns1:filter>ownerid&#x20;=&#x20;{playerid}</ns1:filter><ns1:sort>recordid</ns1:sort><ns1:offset>0</ns1:offset><ns1:max>1</ns1:max><ns1:surrounding>0</ns1:surrounding><ns1:ownerids></ns1:ownerids><ns1:cacheFlag>0</ns1:cacheFlag><ns1:fields><ns1:string>info</ns1:string></ns1:fields></ns1:SearchForRecords></SOAP-ENV:Body></SOAP-ENV:Envelope>')
	return WiimmfiMii(mii_data, mii_data.content)


class WiimmfiMii(Mii.Mii): 
	def __init__(self, responseObject, responseContent):
		fullWiimmfiResponse = bytearray(base64.b64decode(str(responseContent)[399:527]))
		

		self.__miiBytes__ = bytes(fullWiimmfiResponse[0:74])
		super().__init__(self.__miiBytes__) #Now we have our mii data, we can initialize Mii.Mii class
		
		self.miiCRC16 = bytes(fullWiimmfiResponse[74:76])
		self.unknown1 = bytes(fullWiimmfiResponse[76]) #set to null
		self.unknown2 = binascii.hexlify(fullWiimmfiResponse[77:84])
		self.gameId = fullWiimmfiResponse[84:88].decode('utf8')
		self.countryId = int.from_bytes(fullWiimmfiResponse[88:89], 'big')
		self.countryCode = common.countryCodeFromId(self.countryId)
		self.regionId = int.from_bytes(fullWiimmfiResponse[89:90], 'big')
		self.unknown3 = bytes(fullWiimmfiResponse[90:92])
		self.playerLatitude = int.from_bytes(bytes(fullWiimmfiResponse[92:94]), 'big', signed=True)
		self.playerLongitude = int.from_bytes(bytes(fullWiimmfiResponse[94:96]), 'big', signed=True)
		self.statusCode = responseObject.status_code
		self.headers = responseObject.headers

