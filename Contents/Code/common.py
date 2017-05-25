import time, base64, unicodedata, re, random, string
from resources.lib.libraries import client, cleantitle, jsfdecoder
from resources.lib.resolvers import host_openload, host_gvideo
import interface
from __builtin__ import ord, format, eval

try:
	client.setIP4(setoveride=True)
	Log('IPv6 disabled and IPv4 set as default')
except:
	Log('Error disabling IPv6 and setting IPv4 as default')
	pass

	
JSEngines_ALLowed = ['Node']
try:
	# Twoure's check routine - https://github.com/Twoure/9anime.bundle/tree/dev
	import execjs_110 as execjs
	execjs.eval("{a:true,b:function (){}}")
	
	Engine_OK = False
	for engine in JSEngines_ALLowed:
		if engine.lower() in execjs.get().name.lower():
			Engine_OK = True
			break
	if Engine_OK:
		Log('execjs loaded from v1.1.0')
		Log('execjs using engine: %s' % execjs.get().name)
	else:
		Log.Error('execjs Unsupported engine: %s' % execjs.get().name)
		execjs = None
except Exception as e:
	Log.Error('Failed to import execjs >>> {}'.format(e))
	execjs = None

################################################################################
TITLE = "FMoviesPlus"
VERSION = '0.28' # Release notation (x.y - where x is major and y is minor)
TAG = ''
GITHUB_REPOSITORY = 'coder-alpha/FMoviesPlus.bundle'
PREFIX = "/video/fmoviesplus"
################################################################################

CACHE = {}
CACHE_META = {}
CACHE_EXPIRY_TIME = 3600 # 1 Hour
CACHE_EXPIRY = 3600
CACHE_COOKIE = []
TOKEN_CODE = []

# Help videos on Patebin
Help_Videos = "https://pastebin.com/raw/BMMHQund"

# Vibrant Emoji's (might not be supported on all clients)
EMOJI_LINK = u'\U0001F517'
EMOJI_GREEN_HEART = u'\U0001F49A'
EMOJI_BROKEN_HEART = u'\U0001F494'
EMOJI_VIDEO_CAMERA = u'\U0001F3A5'
EMOJI_CASSETTE = u'\U0001F4FC'
EMOJI_CINEMA = u'\U0001F3A6'
EMOJI_TV = u'\U0001F4FA'

# Simple Emoji's
EMOJI_HEART = u'\u2665'
EMOJI_TICK = u'\u2713'
EMOJI_CROSS = u'\u2717'
EMOJI_QUESTION = u'\u2753'

# Text Emoji equivalent
EMOJI_TXT_POS = u'(v)'
EMOJI_TXT_NEG = u'(x)'
EMOJI_TXT_QUES = u'(?)'

OPTIONS_PROXY = []
INTERNAL_SOURCES = []
OPTIONS_PROVIDERS = []
INTERNAL_SOURCES_QUALS = [{'label':'4K','enabled': 'True'},{'label':'1080p','enabled': 'True'},{'label':'720p','enabled': 'True'},{'label':'480p','enabled': 'True'},{'label':'360p','enabled': 'True'}]
INTERNAL_SOURCES_RIPTYPE = [{'label':'BRRIP','enabled': 'True'},{'label':'PREDVD','enabled': 'True'},{'label':'CAM','enabled': 'True'},{'label':'TS','enabled': 'True'},{'label':'SCR','enabled': 'True'},{'label':'UNKNOWN','enabled': 'True'}]
INTERNAL_SOURCES_FILETYPE = [{'label':'Movie/Show','enabled': 'True'},{'label':'Trailer','enabled': 'False'},{'label':'Behind the scenes','enabled': 'False'},{'label':'Music Video','enabled': 'False'}]

INTERNAL_SOURCES_QUALS_CONST = [{'label':'4K','enabled': 'True'},{'label':'1080p','enabled': 'True'},{'label':'720p','enabled': 'True'},{'label':'480p','enabled': 'True'},{'label':'360p','enabled': 'True'}]
INTERNAL_SOURCES_RIPTYPE_CONST = [{'label':'BRRIP','enabled': 'True'},{'label':'PREDVD','enabled': 'True'},{'label':'CAM','enabled': 'True'},{'label':'TS','enabled': 'True'},{'label':'SCR','enabled': 'True'},{'label':'UNKNOWN','enabled': 'True'}]
INTERNAL_SOURCES_FILETYPE_CONST = [{'label':'Movie/Show','enabled': 'True'},{'label':'Trailer','enabled': 'False'},{'label':'Behind the scenes','enabled': 'False'},{'label':'Music Video','enabled': 'False'},{'label':'Misc.','enabled': 'False'}]

DEVICE_OPTIONS = ['Dumb-Keyboard','List-View','Redirector','Simple-Emoji','Vibrant-Emoji','Multi-Link-View','Full-poster display']
DEVICE_OPTION = {DEVICE_OPTIONS[0]:'The awesome Keyboard for Search impaired devices',
				DEVICE_OPTIONS[1]:'Force List-View of Playback page listing sources',
				DEVICE_OPTIONS[2]:'Required in certain cases - *Experimental (refer forum)',
				DEVICE_OPTIONS[3]:'Enable Simple Emoji Icons (%s|%s - Supported by Most Clients)' % (EMOJI_TICK,EMOJI_CROSS),
				DEVICE_OPTIONS[4]:'Enable Vibrant Emoji Icons (%s|%s - Supported by Limited Clients)' % (EMOJI_GREEN_HEART,EMOJI_BROKEN_HEART),
				DEVICE_OPTIONS[5]:'Shows All Video Items in single container - makes many requests to server',
				DEVICE_OPTIONS[6]:'Shows Uncropped Poster - client compatibility is untested'}
DEVICE_OPTION_CONSTRAINTS = {DEVICE_OPTIONS[2]:[{'Pref':'use_https_alt','Desc':'Use Alternate SSL/TLS','ReqValue':'disabled'}]}
DEVICE_OPTION_CONSTRAINTS2 = {DEVICE_OPTIONS[5]:[{'Option':6,'ReqValue':False}], DEVICE_OPTIONS[6]:[{'Option':5,'ReqValue':False}]}

# Golbal Overrides - to disable 
USE_COOKIES = True
NoMovieInfo = False
USE_CUSTOM_TIMEOUT = False
USE_SECOND_REQUEST = False
ALT_PLAYBACK = False
USE_JSFDECODER = True
USE_JSENGINE = True
USE_JSWEBHOOK = True
DEV_DEBUG = False
WBH = 'aHR0cHM6Ly9ob29rLmlvL2NvZGVyLWFscGhhL3Rlc3Q='

####################################################################################################
# Get Key from a Dict using Val
@route(PREFIX + '/GetEmoji')
def GetEmoji(type, mode='vibrant', session=None):

	# modes = ['simple','vibrant'] - enforce mode to override Prefs for Search Filter

	type = str(type).lower()
	
	if session == None:
		session = getSession()
	
	if mode == 'simple' and (UsingOption(DEVICE_OPTIONS[3], session=session) or UsingOption(DEVICE_OPTIONS[4], session=session)):
		if type == 'pos' or type == 'true':
			return EMOJI_TICK
		elif type =='neg' or type == 'false':
			return EMOJI_CROSS
	elif mode=='vibrant' and UsingOption(DEVICE_OPTIONS[4], session=session):
		if type == 'pos' or type == 'true':
			return EMOJI_GREEN_HEART
		elif type =='neg' or type == 'false':
			return EMOJI_BROKEN_HEART
	elif UsingOption(DEVICE_OPTIONS[3], session=session):
		if type == 'pos' or type == 'true':
			return EMOJI_TICK
		elif type =='neg' or type == 'false':
			return EMOJI_CROSS
	else:
		if type == 'pos' or type == 'true':
			return EMOJI_TXT_POS
		elif type =='neg' or type == 'false':
			return EMOJI_TXT_NEG
		else:
			return EMOJI_TXT_QUES
	
	return EMOJI_QUESTION


####################################################################################################
# Get Key from a Dict using Val
@route(PREFIX + '/getkeyfromval')
def GetKeyFromVal(list, val_look):
	for key, val in list.iteritems():
		if val == val_look:
			return key
			
####################################################################################################
# Gets a client specific identifier
@route(PREFIX + '/getsession')
def getSession():

	session = 'UnknownPlexClientSession'
	if 'X-Plex-Client-Identifier' in str(Request.Headers):
		session = str(Request.Headers['X-Plex-Client-Identifier'])
	elif 'X-Plex-Target-Client-Identifier' in str(Request.Headers):
		session = str(Request.Headers['X-Plex-Target-Client-Identifier'])
	elif 'User-Agent' in str(Request.Headers) and 'X-Plex-Token' in str(Request.Headers):
		session = 'UnknownClient-'+encode(str(Request.Headers['User-Agent']) + str(Request.Headers['X-Plex-Token'][:3]))[:10]
	
	return (session)

#######################################################################################################
# base64 decode
@route(PREFIX + '/decode')
def decode(str):
	return base64.b64decode(str)
	
# base64 encode
@route(PREFIX + '/encode')
def encode(str):
	return base64.b64encode(str)
	
#######################################################################################################
@route(PREFIX + '/getHighestQualityLabel')
def getHighestQualityLabel(strr, q_label):

	try:
		i =  (q_label.lower().replace('p','').replace('hd','').strip()) # fail when q_label = TS, CAM, etc.
		i = int(i.strip())
		s = ''
		q_label = '%sp' % i
	except:
		s = ' (%s)' % q_label
	
	if '1080' in strr:
		return '1080p' + s
	elif '720' in strr:
		return '720p' + s
	elif '480' in strr:
		return '480p' + s
	elif '360' in strr:
		return '360p' + s
	else:
		return q_label
	

#######################################################################################################
@route(PREFIX + "/setDictVal")
def setDictVal(key, val, session=None):

	if str(val).lower() == 'true':
		val = 'enabled'
	elif str(val).lower() == 'false':
		val = 'disabled'
		
	key = key.replace('Toggle','')

	if DEVICE_OPTION_CONSTRAINTS != None and key in DEVICE_OPTION_CONSTRAINTS.keys():
		for key_cons in DEVICE_OPTION_CONSTRAINTS[key]:
			if Prefs[key_cons['Pref']] and val!=key_cons['ReqValue']:
				return ObjectContainer(header='Sorry', message='Sorry %s has conflict with Pref: %s needs to be %s.' % (key, key_cons['Desc'], key_cons['ReqValue']), title1=key)
				
	if DEVICE_OPTION_CONSTRAINTS2 != None and key in DEVICE_OPTION_CONSTRAINTS2.keys():
		for key_cons in DEVICE_OPTION_CONSTRAINTS2[key]:
			if str(UsingOption(DEVICE_OPTIONS[key_cons['Option']])) != str(key_cons['ReqValue']):
				return ObjectContainer(header='Sorry', message='Sorry %s has conflict with Device Option: %s needs to be %s.' % (key, DEVICE_OPTIONS[key_cons['Option']], key_cons['ReqValue']), title1=key)
				
	if session == None:
		session = getSession()

	Dict['Toggle'+key+session] = val
	Dict.Save()
	if Prefs["use_debug"]:
		Log("%s status: %s" % (key,val))
		
	return ObjectContainer(header=key, message=key + ' has been ' + val + ' for this device.', title1=key)

@route(PREFIX + "/UsingOption")
def UsingOption(key, session=None):
	if session == None:
		session = getSession()
	if Dict['Toggle'+key+session] == None or Dict['Toggle'+key+session] == 'disabled':
		return False
	else:
		return True

####################################################################################################
# Get HTTP response code (200 == good)
@route(PREFIX + '/gethttpstatus')
def GetHttpStatus(url, cookies=None):
	try:
		req = GetHttpRequest(url=url, cookies=cookies)
		if req != None:
			conn = urllib2.urlopen(req, timeout=client.GLOBAL_TIMEOUT_FOR_HTTP_REQUEST)
			resp = str(conn.getcode())
		else:
			resp = '0'
	except Exception as e:
		resp = '0'
	return resp
	
####################################################################################################
# Get HTTP request
@route(PREFIX + '/gethttprequest')
def GetHttpRequest(url, cookies=None):
	try:
		headers = {'User-Agent': client.USER_AGENT,
		   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
		   'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
		   'Accept-Encoding': 'none',
		   'Accept-Language': 'en-US,en;q=0.8',
		   'Connection': 'keep-alive',
		   'Referer': url}
		   
		if cookies != None:
			headers['Cookie'] = cookies
		if '|' in url:
			url_split = url.split('|')
			url = url_split[0]
			headers['Referer'] = url
			
			for params in url_split:
				if '=' in params:
					param_split = params.split('=')
					param = param_split[0].strip()
					param_val = urllib2.quote(param_split[1].strip(), safe='/=&')
					headers[param] = param_val

		if 'http://' in url or 'https://' in url:
			req = urllib2.Request(url, headers=headers)
		else:
			req = None
	except Exception as e:
		req = None
	return req
	
######################################################################################
def ResolveFinalUrl(isOpenLoad, data, pair_required=False, params=None, **kwargs):
	# responses - true, false, unknown
	vidurl = data
	err = ''
		
	if params != None:
		params = JSON.ObjectFromString(D(params))
		headers = params['headers']		
		cookie = params['cookie']
		
	if vidurl != None:
		if isOpenLoad and pair_required == False:
			vidurl, err = host_openload.resolve(vidurl)
		else:
			pass

	if Prefs["use_debug"]:
		Log("--- Resolved Final Url ---")
		Log("Video Url: %s : Error: %s" % (vidurl, err))
			
	return vidurl
	
######################################################################################
@route(PREFIX + "/isItemVidAvailable")
def isItemVidAvailable(isOpenLoad, data, params=None, **kwargs):
	# responses - true, false, unknown
	vidurl = None
	httpsskip = Prefs["use_https_alt"]
	use_web_proxy = Prefs["use_web_proxy"]
	
	if isOpenLoad:
		vidurl = data
	else:
		data = D(data)
		data = JSON.ObjectFromString(data)
		files = JSON.ObjectFromString(data['server'])
		sortable_list = []
		for file in files:
			furl = file['file']
			res = file['label'].replace('p','')
			if res != '1080':
				res = '0'+res
			type = file['type']
			sortable_list.append({'label': res, 'file':furl, 'type':type})
		newlist = sorted(sortable_list, key=lambda k: k['label'], reverse=True)
		for file in newlist:
			vidurl = file['file']
			break
			
	isVideoOnline = 'false'

	headers = None
	cookie = None
	if params != None:
		params = JSON.ObjectFromString(D(params))
		headers = params['headers']		
		cookie = params['cookie']
		
	if vidurl != None:
		try:
			if isOpenLoad:
				if host_openload.check(vidurl, embedpage=True, headers=headers, cookie=cookie)[0] == True:
						isVideoOnline = 'true'
			else:
				if host_gvideo.check(vidurl, headers=headers, cookie=cookie)[0] == True:
						isVideoOnline = 'true'

		except Exception as e:
			Log('ERROR common.py>isItemVidAvailable %s, %s:' % (e.args,vidurl))
			Log(data)
			isVideoOnline = 'unknown'

	if Prefs["use_debug"]:
		Log("--- LinkChecker ---")
		Log("Video Url: %s : Online: %s" % (vidurl, isVideoOnline))
			
	return isVideoOnline
	
######################################################################################
@route(PREFIX + "/GetPageElements")
def GetPageElements(url, headers=None, referer=None):

	page_data_string = None
	page_data_elems = None
	try:
		if url in CACHE_META.keys():
			try:
				CACHE_EXPIRY = 60 * int(Prefs["cache_expiry_time"])
			except:
				CACHE_EXPIRY = CACHE_EXPIRY_TIME
			if CACHE_META[url]['ts'] + CACHE_EXPIRY > time.time():
				page_data_string = D(CACHE_META[url]['data'])
				
		if page_data_string == None:
			page_data_string = GetPageAsString(url=url, headers=headers, referer=referer)

		page_data_elems = HTML.ElementFromString(page_data_string)
		
		CACHE_META[url] = {}
		CACHE_META[url]['ts'] = time.time()
		CACHE_META[url]['data'] = E(page_data_string)
		
	except Exception as e:
		Log('ERROR common.py>GetPageElements: %s URL: %s DATA: %s' % (e.args,url,page_data_string))
		pass

	return page_data_elems
	
def make_cookie_str():

	try:
		cookie_str = ''
		error = ''
		if len(CACHE_COOKIE) > 0:
			pass
		else:
			#setTokenCookie(serverts=serverts, use_debug=use_debug)
			error = "Cookie not set !"

		user_defined_reqkey_cookie = Prefs['reqkey_cookie']
		reqCookie = CACHE_COOKIE[0]['reqkey']
		if user_defined_reqkey_cookie != None and user_defined_reqkey_cookie != '':
			reqCookie = user_defined_reqkey_cookie

		p_cookie = CACHE_COOKIE[0]['cookie'] + ';' + reqCookie
		p_cookie = p_cookie.replace(';;',';')
		p_cookie_s = p_cookie.split(';')
		cookie_string_arr = []
		
		for ps in p_cookie_s:
			if '=' in ps:
				ps_s = ps.split('=')
				k = ps_s[0].strip()
				v = ps_s[1].strip()
				if k == 'reqkey':
					if len(v) > 5:
						cookie_string_arr.append(k+'='+v)
				else:
					cookie_string_arr.append(k+'='+v)
		
		try:
			cookie_str = ('; '.join(x for x in sorted(cookie_string_arr)))
		except:
			cookie_str = p_cookie
		
		return cookie_str, error
	except Exception as e:
		return cookie_str, e
		
def cleanCookie(str):
	str = str.replace('\n','')
	str_s = str.split(';')
	cookie_string_arr = []
	for str in str_s:
		if 'expires' not in str and 'path' not in str and 'Date' not in str and '=' in str:
			ps_s= str.split('=')
			k = ps_s[0].strip()
			v = ps_s[1].strip()
			if k == 'reqkey':
				if len(v) > 3:
					cookie_string_arr.append(k + '=' + v)
			else:
				cookie_string_arr.append(k + '=' + v)
			
	cookie_string = ('; '.join(x for x in cookie_string_arr))
	return cookie_string
	
######################################################################################
@route(PREFIX + "/GetPageAsString")
def GetPageAsString(url, headers=None, timeout=15, referer=None):

	use_debug = Prefs["use_debug"]
	user_defined_reqkey_cookie = Prefs['reqkey_cookie']
	
	try:
		CACHE_EXPIRY = 60 * int(Prefs["cache_expiry_time"])
	except:
		CACHE_EXPIRY = CACHE_EXPIRY_TIME

	page_data_string = None
	if headers == None:
		headers = {}
	if referer != None:
		headers['Referer'] = referer
	elif 'Referer' in headers:
		pass
	else:
		headers['Referer'] = url
	
	cookies, error = make_cookie_str()

	if error == '':
		headers['Cookie'] = cookies
		headers['User-Agent'] = CACHE_COOKIE[0]['UA']

		if use_debug:
			Log("Using Cookie retrieved at: %s" % CACHE_COOKIE[0]['ts'])
			Log("Using Cookie: %s" % (cookies))

	try:
		if Prefs["use_https_alt"]:
			if use_debug:
				Log("Using SSL Alternate Option")
				Log("Url: " + url)
			page_data_string = interface.request(url = url, headers=headers, timeout=str(timeout))
		elif Prefs["use_web_proxy"]:
			page_data_string = None
			if use_debug:
				Log("Using Web-proxy option")
				Log("Url: " + url)
			for proxy in OPTIONS_PROXY:
				if use_debug:
					Log("Using Proxy: %s - %s" % (proxy['name'], proxy['url']))
				if proxy['working']:
					page_data_string = interface.request_via_proxy(url=url, proxy_name=proxy['name'], proxy_url=proxy['url'], headers=headers, timeout=str(timeout), use_web_proxy=True)
					if page_data_string != None:
						break
		else:
			page_data_string = HTTP.Request(url, headers=headers, timeout=timeout).content
	except Exception as e:
		Log('ERROR common.py>GetPageAsString: %s URL: %s' % (e.args,url))
		pass
		
	return page_data_string
	
@route(PREFIX + "/request")
def request(url, close=True, redirect=True, followredirect=False, error=False, proxy=None, post=None, headers=None, mobile=False, limit=None, referer=None, cookie=None, output='', timeout=15, httpsskip=False, use_web_proxy=False):

	page_data_string = None
	try:
		if Prefs["use_https_alt"]:
			if Prefs["use_debug"]:
				Log("Using SSL Alternate Option")
				Log("Url: " + url)
			page_data_string = interface.request(url = url, headers=headers, timeout=str(timeout))
		elif Prefs["use_web_proxy"]:
			page_data_string = None
			use_web_proxy = True
			if Prefs["use_debug"]:
				Log("Using Web-proxy option")
				Log("Url: " + url)
			for proxy in OPTIONS_PROXY:
				if proxy['working']:
					if Prefs["use_debug"]:
						Log("Using Proxy: %s - %s" % (proxy['name'], proxy['url']))
					page_data_string = interface.request_via_proxy(url=url, proxy_name=proxy['name'], proxy_url=proxy['url'], close=close, redirect=redirect, followredirect=followredirect, error=error, proxy=proxy, post=post, headers=headers, mobile=mobile, limit=limit, referer=referer, cookie=cookie, output=output, timeout=str(timeout), httpsskip=httpsskip, use_web_proxy=use_web_proxy)
					if page_data_string != None:
						break
		else:
			if headers == None:
				page_data_string = HTTP.Request(url, timeout=timeout).content
			else:
				page_data_string = HTTP.Request(url, headers=headers, timeout=timeout).content
		
	except Exception as e:
		Log('ERROR common.py>request: %s URL: %s' % (e.args,url))
		pass
		
	return page_data_string
	
def makeid(N,arr):

	r = ''
	while r == '':
		rt = ''.join(random.choice(string.ascii_uppercase) for _ in range(N))
		rt += ''.join(random.choice(string.digits) for _ in range(N))
		if rt not in arr:
			r = rt
	return r
	
def cleanJSS1(str):
	if str == None: raise ValueError("cleanJSS: Token is None type")
	
	txt = str

	for i in range(0,len(str)):
		c = str[i]
		if (ord(c) <= 127 and c != '_'):
			pass
		else:
			txt = txt.replace(c, makeid(1))

	return txt
	
def cleanJSS2(str):
	if str == None: raise ValueError("cleanJSS: Token is None type")
	
	token = str.replace(D('KCEhW10rW10pWyshIVtdXSsoW11bW11dK1tdKVshK1tdKyEhW10rISFbXV0rW11bKCFbXStbXSlbIStbXSshIVtdKyEhW11dKyhbXSt7fSlbKyEhW11dKyghIVtdK1tdKVsrISFbXV0rKCEhW10rW10pWytbXV1dWyhbXSt7fSlbIStbXSshIVtdKyEhW10rISFbXSshIVtdXSsoW10re30pWyshIVtdXSsoW11bW11dK1tdKVsrISFbXV0rKCFbXStbXSlbIStbXSshIVtdKyEhW11dKyghIVtdK1tdKVsrW11dKyghIVtdK1tdKVsrISFbXV0rKFtdW1tdXStbXSlbK1tdXSsoW10re30pWyErW10rISFbXSshIVtdKyEhW10rISFbXV0rKCEhW10rW10pWytbXV0rKFtdK3t9KVsrISFbXV0rKCEhW10rW10pWyshIVtdXV0oKCEhW10rW10pWyshIVtdXSsoW11bW11dK1tdKVshK1tdKyEhW10rISFbXV0rKCEhW10rW10pWytbXV0rKFtdW1tdXStbXSlbK1tdXSsoISFbXStbXSlbKyEhW11dKyhbXVtbXV0rW10pWyshIVtdXSsoW10re30pWyErW10rISFbXSshIVtdKyEhW10rISFbXSshIVtdKyEhW11dKyhbXVtbXV0rW10pWytbXV0rKFtdW1tdXStbXSlbKyEhW11dKyhbXVtbXV0rW10pWyErW10rISFbXSshIVtdXSsoIVtdK1tdKVshK1tdKyEhW10rISFbXV0rKFtdK3t9KVshK1tdKyEhW10rISFbXSshIVtdKyEhW11dKygre30rW10pWyshIVtdXSsoW10rW11bKCFbXStbXSlbIStbXSshIVtdKyEhW11dKyhbXSt7fSlbKyEhW11dKyghIVtdK1tdKVsrISFbXV0rKCEhW10rW10pWytbXV1dWyhbXSt7fSlbIStbXSshIVtdKyEhW10rISFbXSshIVtdXSsoW10re30pWyshIVtdXSsoW11bW11dK1tdKVsrISFbXV0rKCFbXStbXSlbIStbXSshIVtdKyEhW11dKyghIVtdK1tdKVsrW11dKyghIVtdK1tdKVsrISFbXV0rKFtdW1tdXStbXSlbK1tdXSsoW10re30pWyErW10rISFbXSshIVtdKyEhW10rISFbXV0rKCEhW10rW10pWytbXV0rKFtdK3t9KVsrISFbXV0rKCEhW10rW10pWyshIVtdXV0oKCEhW10rW10pWyshIVtdXSsoW11bW11dK1tdKVshK1tdKyEhW10rISFbXV0rKCEhW10rW10pWytbXV0rKFtdW1tdXStbXSlbK1tdXSsoISFbXStbXSlbKyEhW11dKyhbXVtbXV0rW10pWyshIVtdXSsoW10re30pWyErW10rISFbXSshIVtdKyEhW10rISFbXSshIVtdKyEhW11dKyghW10rW10pWyErW10rISFbXV0rKFtdK3t9KVsrISFbXV0rKFtdK3t9KVshK1tdKyEhW10rISFbXSshIVtdKyEhW11dKygre30rW10pWyshIVtdXSsoISFbXStbXSlbK1tdXSsoW11bW11dK1tdKVshK1tdKyEhW10rISFbXSshIVtdKyEhW11dKyhbXSt7fSlbKyEhW11dKyhbXVtbXV0rW10pWyshIVtdXSkoKSlbIStbXSshIVtdKyEhW11dKyhbXVtbXV0rW10pWyErW10rISFbXSshIVtdXSkoKShbXVsoIVtdK1tdKVshK1tdKyEhW10rISFbXV0rKFtdK3t9KVsrISFbXV0rKCEhW10rW10pWyshIVtdXSsoISFbXStbXSlbK1tdXV1bKFtdK3t9KVshK1tdKyEhW10rISFbXSshIVtdKyEhW11dKyhbXSt7fSlbKyEhW11dKyhbXVtbXV0rW10pWyshIVtdXSsoIVtdK1tdKVshK1tdKyEhW10rISFbXV0rKCEhW10rW10pWytbXV0rKCEhW10rW10pWyshIVtdXSsoW11bW11dK1tdKVsrW11dKyhbXSt7fSlbIStbXSshIVtdKyEhW10rISFbXSshIVtdXSsoISFbXStbXSlbK1tdXSsoW10re30pWyshIVtdXSsoISFbXStbXSlbKyEhW11dXSgoISFbXStbXSlbKyEhW11dKyhbXVtbXV0rW10pWyErW10rISFbXSshIVtdXSsoISFbXStbXSlbK1tdXSsoW11bW11dK1tdKVsrW11dKyghIVtdK1tdKVsrISFbXV0rKFtdW1tdXStbXSlbKyEhW11dKyhbXSt7fSlbIStbXSshIVtdKyEhW10rISFbXSshIVtdKyEhW10rISFbXV0rKFtdW1tdXStbXSlbIStbXSshIVtdKyEhW11dKyghW10rW10pWyErW10rISFbXSshIVtdXSsoW10re30pWyErW10rISFbXSshIVtdKyEhW10rISFbXV0rKCt7fStbXSlbKyEhW11dKyhbXStbXVsoIVtdK1tdKVshK1tdKyEhW10rISFbXV0rKFtdK3t9KVsrISFbXV0rKCEhW10rW10pWyshIVtdXSsoISFbXStbXSlbK1tdXV1bKFtdK3t9KVshK1tdKyEhW10rISFbXSshIVtdKyEhW11dKyhbXSt7fSlbKyEhW11dKyhbXVtbXV0rW10pWyshIVtdXSsoIVtdK1tdKVshK1tdKyEhW10rISFbXV0rKCEhW10rW10pWytbXV0rKCEhW10rW10pWyshIVtdXSsoW11bW11dK1tdKVsrW11dKyhbXSt7fSlbIStbXSshIVtdKyEhW10rISFbXSshIVtdXSsoISFbXStbXSlbK1tdXSsoW10re30pWyshIVtdXSsoISFbXStbXSlbKyEhW11dXSgoISFbXStbXSlbKyEhW11dKyhbXVtbXV0rW10pWyErW10rISFbXSshIVtdXSsoISFbXStbXSlbK1tdXSsoW11bW11dK1tdKVsrW11dKyghIVtdK1tdKVsrISFbXV0rKFtdW1tdXStbXSlbKyEhW11dKyhbXSt7fSlbIStbXSshIVtdKyEhW10rISFbXSshIVtdKyEhW10rISFbXV0rKCFbXStbXSlbIStbXSshIVtdXSsoW10re30pWyshIVtdXSsoW10re30pWyErW10rISFbXSshIVtdKyEhW10rISFbXV0rKCt7fStbXSlbKyEhW11dKyghIVtdK1tdKVsrW11dKyhbXVtbXV0rW10pWyErW10rISFbXSshIVtdKyEhW10rISFbXV0rKFtdK3t9KVsrISFbXV0rKFtdW1tdXStbXSlbKyEhW11dKSgpKVshK1tdKyEhW10rISFbXV0rKFtdW1tdXStbXSlbIStbXSshIVtdKyEhW11dKSgpKChbXSt7fSlbK1tdXSlbK1tdXSsoIStbXSshIVtdKyEhW10rISFbXSshIVtdKyEhW10rISFbXStbXSkrKCshIVtdK1tdKSkrW11bKCFbXStbXSlbIStbXSshIVtdKyEhW11dKyhbXSt7fSlbKyEhW11dKyghIVtdK1tdKVsrISFbXV0rKCEhW10rW10pWytbXV1dWyhbXSt7fSlbIStbXSshIVtdKyEhW10rISFbXSshIVtdXSsoW10re30pWyshIVtdXSsoW11bW11dK1tdKVsrISFbXV0rKCFbXStbXSlbIStbXSshIVtdKyEhW11dKyghIVtdK1tdKVsrW11dKyghIVtdK1tdKVsrISFbXV0rKFtdW1tdXStbXSlbK1tdXSsoW10re30pWyErW10rISFbXSshIVtdKyEhW10rISFbXV0rKCEhW10rW10pWytbXV0rKFtdK3t9KVsrISFbXV0rKCEhW10rW10pWyshIVtdXV0oKCEhW10rW10pWyshIVtdXSsoW11bW11dK1tdKVshK1tdKyEhW10rISFbXV0rKCEhW10rW10pWytbXV0rKFtdW1tdXStbXSlbK1tdXSsoISFbXStbXSlbKyEhW11dKyhbXVtbXV0rW10pWyshIVtdXSsoW10re30pWyErW10rISFbXSshIVtdKyEhW10rISFbXSshIVtdKyEhW11dKyhbXVtbXV0rW10pWytbXV0rKFtdW1tdXStbXSlbKyEhW11dKyhbXVtbXV0rW10pWyErW10rISFbXSshIVtdXSsoIVtdK1tdKVshK1tdKyEhW10rISFbXV0rKFtdK3t9KVshK1tdKyEhW10rISFbXSshIVtdKyEhW11dKygre30rW10pWyshIVtdXSsoW10rW11bKCFbXStbXSlbIStbXSshIVtdKyEhW11dKyhbXSt7fSlbKyEhW11dKyghIVtdK1tdKVsrISFbXV0rKCEhW10rW10pWytbXV1dWyhbXSt7fSlbIStbXSshIVtdKyEhW10rISFbXSshIVtdXSsoW10re30pWyshIVtdXSsoW11bW11dK1tdKVsrISFbXV0rKCFbXStbXSlbIStbXSshIVtdKyEhW11dKyghIVtdK1tdKVsrW11dKyghIVtdK1tdKVsrISFbXV0rKFtdW1tdXStbXSlbK1tdXSsoW10re30pWyErW10rISFbXSshIVtdKyEhW10rISFbXV0rKCEhW10rW10pWytbXV0rKFtdK3t9KVsrISFbXV0rKCEhW10rW10pWyshIVtdXV0oKCEhW10rW10pWyshIVtdXSsoW11bW11dK1tdKVshK1tdKyEhW10rISFbXV0rKCEhW10rW10pWytbXV0rKFtdW1tdXStbXSlbK1tdXSsoISFbXStbXSlbKyEhW11dKyhbXVtbXV0rW10pWyshIVtdXSsoW10re30pWyErW10rISFbXSshIVtdKyEhW10rISFbXSshIVtdKyEhW11dKyghW10rW10pWyErW10rISFbXV0rKFtdK3t9KVsrISFbXV0rKFtdK3t9KVshK1tdKyEhW10rISFbXSshIVtdKyEhW11dKygre30rW10pWyshIVtdXSsoISFbXStbXSlbK1tdXSsoW11bW11dK1tdKVshK1tdKyEhW10rISFbXSshIVtdKyEhW11dKyhbXSt7fSlbKyEhW11dKyhbXVtbXV0rW10pWyshIVtdXSkoKSlbIStbXSshIVtdKyEhW11dKyhbXVtbXV0rW10pWyErW10rISFbXSshIVtdXSkoKShbXVsoIVtdK1tdKVshK1tdKyEhW10rISFbXV0rKFtdK3t9KVsrISFbXV0rKCEhW10rW10pWyshIVtdXSsoISFbXStbXSlbK1tdXV1bKFtdK3t9KVshK1tdKyEhW10rISFbXSshIVtdKyEhW11dKyhbXSt7fSlbKyEhW11dKyhbXVtbXV0rW10pWyshIVtdXSsoIVtdK1tdKVshK1tdKyEhW10rISFbXV0rKCEhW10rW10pWytbXV0rKCEhW10rW10pWyshIVtdXSsoW11bW11dK1tdKVsrW11dKyhbXSt7fSlbIStbXSshIVtdKyEhW10rISFbXSshIVtdXSsoISFbXStbXSlbK1tdXSsoW10re30pWyshIVtdXSsoISFbXStbXSlbKyEhW11dXSgoISFbXStbXSlbKyEhW11dKyhbXVtbXV0rW10pWyErW10rISFbXSshIVtdXSsoISFbXStbXSlbK1tdXSsoW11bW11dK1tdKVsrW11dKyghIVtdK1tdKVsrISFbXV0rKFtdW1tdXStbXSlbKyEhW11dKyhbXSt7fSlbIStbXSshIVtdKyEhW10rISFbXSshIVtdKyEhW10rISFbXV0rKFtdW1tdXStbXSlbIStbXSshIVtdKyEhW11dKyghW10rW10pWyErW10rISFbXSshIVtdXSsoW10re30pWyErW10rISFbXSshIVtdKyEhW10rISFbXV0rKCt7fStbXSlbKyEhW11dKyhbXStbXVsoIVtdK1tdKVshK1tdKyEhW10rISFbXV0rKFtdK3t9KVsrISFbXV0rKCEhW10rW10pWyshIVtdXSsoISFbXStbXSlbK1tdXV1bKFtdK3t9KVshK1tdKyEhW10rISFbXSshIVtdKyEhW11dKyhbXSt7fSlbKyEhW11dKyhbXVtbXV0rW10pWyshIVtdXSsoIVtdK1tdKVshK1tdKyEhW10rISFbXV0rKCEhW10rW10pWytbXV0rKCEhW10rW10pWyshIVtdXSsoW11bW11dK1tdKVsrW11dKyhbXSt7fSlbIStbXSshIVtdKyEhW10rISFbXSshIVtdXSsoISFbXStbXSlbK1tdXSsoW10re30pWyshIVtdXSsoISFbXStbXSlbKyEhW11dXSgoISFbXStbXSlbKyEhW11dKyhbXVtbXV0rW10pWyErW10rISFbXSshIVtdXSsoISFbXStbXSlbK1tdXSsoW11bW11dK1tdKVsrW11dKyghIVtdK1tdKVsrISFbXV0rKFtdW1tdXStbXSlbKyEhW11dKyhbXSt7fSlbIStbXSshIVtdKyEhW10rISFbXSshIVtdKyEhW10rISFbXV0rKCFbXStbXSlbIStbXSshIVtdXSsoW10re30pWyshIVtdXSsoW10re30pWyErW10rISFbXSshIVtdKyEhW10rISFbXV0rKCt7fStbXSlbKyEhW11dKyghIVtdK1tdKVsrW11dKyhbXVtbXV0rW10pWyErW10rISFbXSshIVtdKyEhW10rISFbXV0rKFtdK3t9KVsrISFbXV0rKFtdW1tdXStbXSlbKyEhW11dKSgpKVshK1tdKyEhW10rISFbXV0rKFtdW1tdXStbXSlbIStbXSshIVtdKyEhW11dKSgpKChbXSt7fSlbK1tdXSlbK1tdXSsoIStbXSshIVtdKyEhW10rISFbXSshIVtdKyEhW10rW10pKyhbXSt7fSlbIStbXSshIVtdXSkrKFtdW1tdXStbXSlbIStbXSshIVtdKyEhW11dKygrKCshIVtdKyhbXVtbXV0rW10pWyErW10rISFbXSshIVtdXSsoKyEhW10rW10pKygrW10rW10pKygrW10rW10pKygrW10rW10pKStbXSlbIStbXSshIVtdKyEhW10rISFbXSshIVtdKyEhW10rISFbXV0='),'"reqkey"')
	token = token.decode('utf-8')
	use_rep = True
	txt = token
	replaced = {}
	if use_rep:
		str = txt
		safe = '[]{}><!,()=+-;/\" $_'
		notsafe = '_'
		for i in range(0,len(str)):
			c = str[i]
			if re.search('[0-9a-zA-Z]', c) or c in safe:
				pass
			else:
				new_c = makeid(3,replaced.keys())
				replaced[new_c] = c
				txt = txt.replace(c, new_c)
	code = txt
	code = code.replace('(function(', '(function xy(').replace('}(','}; xy(')
	codes = re.findall(r"if.+$", code)[0].replace('),','), jssuckit = "; " + document.cookie,')
	code = re.sub(r"if.+$", codes, code)
	fn = re.findall(r"\(function.+?\)", code)[0]
	fncode1 = re.findall(r"{.*return", code)[0]
	fncode2 = re.findall(r"return.*}", code)[0]
	fnvars = re.findall(r"; xy\(.*", code)[0]
	occurances = [m.start() for m in re.finditer('_', fn)]
	if len(occurances) >= 2:
		new_c = makeid(2,replaced.keys())
		replaced[new_c] = '_'
		fn = fn.replace('_',new_c,1)
		code = fn + fncode1 + fncode2 + fnvars
		new_c2 = makeid(3,replaced.keys())
		replaced[new_c2] = '_'
		code = code.replace('_', new_c2)
		code = code.replace('){var','){var %s=%s; var' % (new_c,new_c2))
		code = code.replace('returnreturn','return')
		code = code[1:-1]
		code = 'var R1,R2; var jssuckit="";var window = global; var document = this; location = "https://fmovies.to/"; %s; jssuckit = document.cookie; return jssuckit' % (code)
	elif len(occurances) == 1:
		if '_=' in fncode1:
			new_c = makeid(2,replaced.keys())
			replaced[new_c] = '_'
			fn = fn.replace('_',new_c)
			new_c2 = makeid(2,replaced.keys())
			replaced[new_c2] = '_'
			fncode1 = fncode1.replace('_',new_c2)
			fncode2 = fncode2.replace('_',new_c2)
			code = fn + fncode1 + fncode2 + fnvars
			code = code.replace('){var','){var %s=%s; var' % (new_c,new_c2))
			code = code[1:-1]
			d = 'var R1,R2; var jssuckit="";var window = global; var document = this; location = "https://fmovies.to/"; %s; jssuckit = document.cookie; jssuckit=jssuckit.replace(R1,R2); return jssuckit' % (code)
			code = d.replace('}; xy(',';R1=%s; R2=%s}; xy(')
			code = code % (new_c2,new_c)
		else:
			new_c = makeid(3,replaced.keys())
			replaced[new_c] = '_'
			code = code.replace('_', new_c)
			code = code[1:-1]
			d = 'var jssuckit="";var window = global; var document = this; location = "https://fmovies.to/"; %s; jssuckit = document.cookie; return jssuckit'
			code = (d % code)
	else:
		code = code[1:-1]
		d = 'var jssuckit="";var window = global; var document = this; location = "https://fmovies.to/"; %s; jssuckit = document.cookie; return jssuckit'
		code = (d % code)
	code = code.replace('returnreturn','return')
	code = code.encode('utf-8')
	return code, replaced
		
####################################################################################################
@route(PREFIX + "/removeAccents")
def removeAccents(text):
	"""
	Convert input text to id.

	:param text: The input string.
	:type text: String.

	:returns: The processed String.
	:rtype: String.
	"""
	text = strip_accents(text.lower())
	text = re.sub('[ ]+', '_', text)
	text = re.sub('[^0-9a-zA-Z]', ' ', text)
	text = text.title()
	return text

def strip_accents(text):
	"""
	Strip accents from input String.

	:param text: The input string.
	:type text: String.

	:returns: The processed String.
	:rtype: String.
	"""
	try:
		text = unicode(text, 'utf-8')
	except NameError: # unicode is a default on python 3 
		pass
	text = unicodedata.normalize('NFD', text)
	text = text.encode('ascii', 'ignore')
	text = text.decode("utf-8")
	return str(text)


####################################################################################################
@route(PREFIX + "/MakeStringLength")
def MakeStringLength(text, n=15):

	ns = n - len(text)
	text += ' ' * ns
	return text
	
####################################################################################################
# search array item's presence in string
@route(PREFIX + "/arrayitemsinstring")
def ArrayItemsInString(arr, mystr):

	for item in arr:
		if item in mystr:
			return True
			
	return False
	
####################################################################################################
# author: Twoure
# source: https://github.com/Twoure/HindiMoviesOnline.bundle/blob/master/Contents/Code/messages.py
#
class NewMessageContainer(object):
	def __init__(self, prefix, title):
		self.title = title
		Route.Connect(prefix + '/message', self.message_container)

	def message_container(self, header, message):
		"""Setup MessageContainer depending on Platform"""

		if Client.Platform in ['Plex Home Theater', 'OpenPHT']:
			oc = ObjectContainer(
				title1=self.title, title2=header, no_cache=True,
				no_history=True, replace_parent=True
				)
			oc.add(PopupDirectoryObject(title=header, summary=message))
			return oc
		else:
			return MessageContainer(header, message)