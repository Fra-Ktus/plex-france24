import re, string
FRANCE_24_URL = 'http://www.france24.com'
FRANCE_24_VIDEO_URL = 'http://www.france24.com/%s'
FRANCE_24_MEDIA_URL = 'http://medias.france24.com'
FRANCE_24_NEWS = '/vod/jt/jt.mp4'
FRANCE_24_METEO = '/vod/jt/meteo.mp4'
FRANCE_24_ECONOMY = '/vod/jt/eco.mp4'
FRANCE_24_NEWS_ICON = '/bundles/aefhermesf24/img/pic_video-1.png'
FRANCE_24_METEO_ICON = '/bundles/aefhermesf24/img/pic_video-3.png'
FRANCE_24_ECONOMY_ICON = '/bundles/aefhermesf24/img/pic_video-2.png'

ICON = 'france_24_logo.png'
ART = 'art-default.png'

####################################################################################################
def Start():

  Plugin.AddPrefixHandler('/video/france24', MainMenu, 'France24', ICON, ART)
  Plugin.AddViewGroup('InfoList', viewMode='InfoList', mediaType='items')
  ObjectContainer.title1 = 'France24'
  ObjectContainer.content = ContainerContent.GenericVideos
  ObjectContainer.art = R(ART)
  DirectoryObject.thumb = R(ICON)
  VideoClipObject.thumb = R(ICON)
  VideoClipObject.art = R(ART)
  HTTP.CacheTime = 1800

####################################################################################################
def MainMenu():

  oc = ObjectContainer(
    objects = [
			   DirectoryObject(key = Callback(GetItemList, url='en/video', title2='English Videos'), title = L('English Videos')),
			   DirectoryObject(key = Callback(GetNewsList, url='en/video', title2='English Latest News'), title = L('English Latest News')),
			   DirectoryObject(key = Callback(GetShowList, url='en/tv-shows/', title2='English Shows'), title = L('English Shows')),
			   DirectoryObject(key = Callback(GetItemList, url='fr/video', title2='French Videos'), title = L('French Videos')),
			   DirectoryObject(key = Callback(GetNewsList, url='fr/video', title2='French Latest News'), title = L('French Latest News')),
			   DirectoryObject(key = Callback(GetShowList, url='fr/emissions/', title2='French Shows'), title = L('French Shows')),
			   DirectoryObject(key = Callback(GetItemList, url='ar/video', title2='Arabic Videos'), title = L('Arabic Videos')),
			   DirectoryObject(key = Callback(GetNewsList, url='ar/video', title2='Arabic Latest News'), title = L('Arabic Latest News')),
			   DirectoryObject(key = Callback(GetShowList, url='ar/tv-shows/', title2='Arabic Shows'), title = L('Arabic Shows'))
    ]
  )                                 
  return oc

####################################################################################################
	
def GetItemList(url, title2, page=''):
  Log ("France24  GetItemList :" + url + " title " + title2)
  Log.Exception('GetItemList')
  cookies = HTTP.CookiesForURL(FRANCE_24_VIDEO_URL)
  oc = ObjectContainer(title2=title2, view_group='InfoList', http_cookies=cookies)
  Log.Exception('videos')
  france_24_page_url = FRANCE_24_VIDEO_URL % (url)
  html = HTML.ElementFromURL(france_24_page_url)
  videos = html.xpath('.//div[contains(@class, "v-item-2")]')
  for video in videos:
    try:
      title = video.xpath('./div[contains(@class, "copy")]/h2/text()')[0]
      Log.Info ("title:" + title)
      img = video.xpath('./div[contains(@class, "media video")]/img/@src')[0]
      Log.Info ("img:" + img)
      video_page_url = video.xpath('./p/a/@href')[0]
      video_page_url = FRANCE_24_URL + video_page_url;
      Log ("video url: " + video_page_url)

      oc.add(VideoClipObject(url = video_page_url, title = title, thumb=img))
    except:
      Log.Exception("error adding VideoClipObject")
      pass
        
  return oc
  
####################################################################################################

def GetNewsList(url, title2, page=''):
  Log ("France24  GetNewsList :" + url + " title " + title2)
  Log.Exception('GetNewsList')
  oc = ObjectContainer(title2=title2, view_group='InfoList')
  # http://medias.france24.com/en/vod/jt/jt.mp4
  url1 = FRANCE_24_MEDIA_URL + '/' + url.split('/')[0] + FRANCE_24_NEWS
  img1 = FRANCE_24_URL + FRANCE_24_NEWS_ICON
  oc.add(VideoClipObject(url = url1, title = 'Latest News', thumb=img1))

  # http:\/\/medias.france24.com\/en\/vod\/jt\/meteo.mp4
  url2 = FRANCE_24_MEDIA_URL + '/' + url.split('/')[0] + FRANCE_24_METEO
  img2 = FRANCE_24_URL + FRANCE_24_METEO_ICON
  oc.add(VideoClipObject(url = url2, title = 'Latest Meteo', thumb=img2))

  # http:\/\/medias.france24.com\/en\/vod\/jt\/eco.mp4
  url3 = FRANCE_24_MEDIA_URL + '/' + url.split('/')[0] + FRANCE_24_ECONOMY
  img3 = FRANCE_24_URL + FRANCE_24_ECONOMY_ICON
  oc.add(VideoClipObject(url = url3, title = 'Latest Economy', thumb=img3))

  return oc

####################################################################################################

def GetShowList(url, title2, page=''):
  Log ("France24  GetShowList :" + url + " title " + title2)
  Log.Exception('GetShowList')
  oc = ObjectContainer(title2=title2, view_group='InfoList')

  cookies = HTTP.CookiesForURL(FRANCE_24_VIDEO_URL)
  oc = ObjectContainer(title2=title2, view_group='InfoList', http_cookies=cookies)
  Log.Exception('GetShowList')
  france_24_page_url = FRANCE_24_VIDEO_URL % (url)
  html = HTML.ElementFromURL(france_24_page_url)
  videos = html.xpath('.//div[contains(@class, "detailed-emission-item")]')
	
  for video in videos:
    try:
      title = video.xpath('./div[@class="copy"]/p[@class="default-read-more"]/a/@title')[0]
      Log.Info ("title:" + title)
      video_page_url = video.xpath('./div[@class="copy"]/p[@class="default-read-more"]/a/@href')[0]
      video_page_url = FRANCE_24_URL + video_page_url;
      Log ("video url: " + video_page_url)
      img = video.xpath('./div[@class="media"]/img/@src')[0]
      Log.Info ("img:" + img)

      oc.add(VideoClipObject(url = video_page_url, title = title, thumb=img))
    except:
      Log.Exception("error adding VideoClipObject")
      pass

  return oc
