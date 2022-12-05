#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -*- Python -*-

# <rtc-template block="description">
"""
 @file youtubeAPI_comment.py
 @brief Component that uses youtubeAPI to retrieve comments from youtube video URLs
 @date $Date$


"""
# </rtc-template>

import sys
import time
sys.path.append(".")

# Import RTM module
import RTC
import OpenRTM_aist
import requests
import json

# Import Service implementation class
# <rtc-template block="service_impl">

# </rtc-template>

# Import Service stub modules
# <rtc-template block="consumer_import">
# </rtc-template>


# This module's spesification
# <rtc-template block="module_spec">
youtubeapi_comment_spec = ["implementation_id", "youtubeAPI_comment", 
         "type_name",         "youtubeAPI_comment", 
         "description",       "Component that uses youtubeAPI to retrieve comments from youtube video URLs", 
         "version",           "1.0.0", 
         "vendor",            "tbou30897", 
         "category",          "Information acquisition", 
         "activity_type",     "STATIC", 
         "max_instance",      "1", 
         "language",          "Python", 
         "lang_type",         "SCRIPT",
         ""]
# </rtc-template>

# <rtc-template block="component_description">
##
# @class youtubeAPI_comment
# @brief Component that uses youtubeAPI to retrieve comments from youtube video URLs
# 
# 
# </rtc-template>
class youtubeAPI_comment(OpenRTM_aist.DataFlowComponentBase):
	
    ##
    # @brief constructor
    # @param manager Maneger Object
    # 
    def __init__(self, manager):
        OpenRTM_aist.DataFlowComponentBase.__init__(self, manager)

        self._d_urlin = OpenRTM_aist.instantiateDataType(RTC.TimedWString)
        """
        urlを受け取るポートです
        """
        self._urlinIn = OpenRTM_aist.InPort("urlin", self._d_urlin)
        self._d_textout = OpenRTM_aist.instantiateDataType(RTC.TimedWStringSeq)
        """
        指定されたurlのコメントをリスト型で出力するポートです。
         - Semantics: ['コメント1','コメント2']のように出力されます。
        """
        self._textoutOut = OpenRTM_aist.OutPort("textout", self._d_textout)


		


        # initialize of configuration-data.
        # <rtc-template block="init_conf_param">
		
        # </rtc-template>


		 
    ##
    #
    # The initialize action (on CREATED->ALIVE transition)
    # 
    # @return RTC::ReturnCode_t
    # 
    #
    def onInitialize(self):
        # Bind variables and configuration variable
		
        # Set InPort buffers
        self.addInPort("urlin",self._urlinIn)
		
        # Set OutPort buffers
        self.addOutPort("textout",self._textoutOut)
		
        # Set service provider to Ports
		
        # Set service consumers to Ports
		
        # Set CORBA Service Ports
		
        return RTC.RTC_OK

    def print_video_comment(self,no, video_id, next_page_token):

        params = {
            'key': self.API_KEY,
            'part': 'snippet',
            'videoId': video_id,
            'order': 'relevance',
            'textFormat': 'plaintext',
            'maxResults': 100,
        }
        if next_page_token is not None:
            params['pageToken'] = next_page_token
        response = requests.get(self.URL + 'commentThreads', params=params)
        resource = response.json()

        for comment_info in resource['items']:
            # コメント
            text = comment_info['snippet']['topLevelComment']['snippet']['textDisplay']
            # グッド数
            like_cnt = comment_info['snippet']['topLevelComment']['snippet']['likeCount']
            # 返信数
            reply_cnt = comment_info['snippet']['totalReplyCount']
            # ユーザー名
            user_name = comment_info['snippet']['topLevelComment']['snippet']['authorDisplayName']
            # Id
            parentId = comment_info['snippet']['topLevelComment']['id']
            #print('{:0=4}\t{}\t{}\t{}\t{}'.format(no, text.replace('\r', '\n').replace('\n', ' '), like_cnt, user_name, reply_cnt))
            if reply_cnt > 0:
                cno = 1
                self.print_video_reply(no, cno, video_id, None, parentId)
                no = no + 1
            if text != "" or text != "\n":
                self.textlist.append(text)
        if 'nextPageToken' in resource:
            self.print_video_comment(no, video_id, resource["nextPageToken"])



    def print_video_reply(self,no, cno, video_id, next_page_token, id):
        params = {
        'key': self.API_KEY,
        'part': 'snippet',
        'videoId': video_id,
        'textFormat': 'plaintext',
        'maxResults': 50,
        'parentId': id,
    }

        if next_page_token is not None:
            params['pageToken'] = next_page_token
        response = requests.get(self.URL + 'comments', params=params)
        resource = response.json()

        for comment_info in resource['items']:
            # コメント
            text = comment_info['snippet']['textDisplay']
            # グッド数
            like_cnt = comment_info['snippet']['likeCount']
            # ユーザー名
            user_name = comment_info['snippet']['authorDisplayName']

            cno = cno + 1

        if 'nextPageToken' in resource:
            self.print_video_reply(no, cno, video_id, resource["nextPageToken"], id)
    ###
    ## 
    ## The finalize action (on ALIVE->END transition)
    ## 
    ## @return RTC::ReturnCode_t
    #
    ## 
    #def onFinalize(self):
    #

    #    return RTC.RTC_OK
	
    ###
    ##
    ## The startup action when ExecutionContext startup
    ## 
    ## @param ec_id target ExecutionContext Id
    ##
    ## @return RTC::ReturnCode_t
    ##
    ##
    #def onStartup(self, ec_id):
    #
    #    return RTC.RTC_OK
	
    ###
    ##
    ## The shutdown action when ExecutionContext stop
    ##
    ## @param ec_id target ExecutionContext Id
    ##
    ## @return RTC::ReturnCode_t
    ##
    ##
    #def onShutdown(self, ec_id):
    #
    #    return RTC.RTC_OK
	
    ##
    #
    # The activated action (Active state entry action)
    #
    # @param ec_id target ExecutionContext Id
    # 
    # @return RTC::ReturnCode_t
    #
    #
    def onActivated(self, ec_id):
    
        return RTC.RTC_OK
	
    ##
    #
    # The deactivated action (Active state exit action)
    #
    # @param ec_id target ExecutionContext Id
    #
    # @return RTC::ReturnCode_t
    #
    #
    def onDeactivated(self, ec_id):
    
        return RTC.RTC_OK
	
    ##
    #
    # The execution action that is invoked periodically
    #
    # @param ec_id target ExecutionContext Id
    #
    # @return RTC::ReturnCode_t
    #
    #
    def onExecute(self, ec_id):
        if self._urlinIn.isNew(): #新しいデータが来たか確認
            self._d_urlin = self._urlinIn.read() #値を読み込む

            self.URL = 'https://www.googleapis.com/youtube/v3/'

            # ここにAPI KEYを入力
            self.API_KEY = 'AIzaSyAmTJsk5Is7IZLSera6FHisanDVOsnWWlg'

                        # ここにURLを入力
            videourl= self._d_urlin.data

                        
            #URLからビデオIDを取得
            video_id = videourl.split("v=")[1]
            no = 1
            self.textlist = []

                            
            self.print_video_comment(no, video_id, None)

            print(self.textlist)        
        return RTC.RTC_OK
	
    ###
    ##
    ## The aborting action when main logic error occurred.
    ##
    ## @param ec_id target ExecutionContext Id
    ##
    ## @return RTC::ReturnCode_t
    ##
    ##
    #def onAborting(self, ec_id):
    #
    #    return RTC.RTC_OK
	
    ###
    ##
    ## The error action in ERROR state
    ##
    ## @param ec_id target ExecutionContext Id
    ##
    ## @return RTC::ReturnCode_t
    ##
    ##
    #def onError(self, ec_id):
    #
    #    return RTC.RTC_OK
	
    ###
    ##
    ## The reset action that is invoked resetting
    ##
    ## @param ec_id target ExecutionContext Id
    ##
    ## @return RTC::ReturnCode_t
    ##
    ##
    #def onReset(self, ec_id):
    #
    #    return RTC.RTC_OK
	
    ###
    ##
    ## The state update action that is invoked after onExecute() action
    ##
    ## @param ec_id target ExecutionContext Id
    ##
    ## @return RTC::ReturnCode_t
    ##

    ##
    #def onStateUpdate(self, ec_id):
    #
    #    return RTC.RTC_OK
	
    ###
    ##
    ## The action that is invoked when execution context's rate is changed
    ##
    ## @param ec_id target ExecutionContext Id
    ##
    ## @return RTC::ReturnCode_t
    ##
    ##
    #def onRateChanged(self, ec_id):
    #
    #    return RTC.RTC_OK
	



def youtubeAPI_commentInit(manager):
    profile = OpenRTM_aist.Properties(defaults_str=youtubeapi_comment_spec)
    manager.registerFactory(profile,
                            youtubeAPI_comment,
                            OpenRTM_aist.Delete)

def MyModuleInit(manager):
    youtubeAPI_commentInit(manager)

    # create instance_name option for createComponent()
    instance_name = [i for i in sys.argv if "--instance_name=" in i]
    if instance_name:
        args = instance_name[0].replace("--", "?")
    else:
        args = ""
  
    # Create a component
    comp = manager.createComponent("youtubeAPI_comment" + args)

def main():
    # remove --instance_name= option
    argv = [i for i in sys.argv if not "--instance_name=" in i]
    # Initialize manager
    mgr = OpenRTM_aist.Manager.init(sys.argv)
    mgr.setModuleInitProc(MyModuleInit)
    mgr.activateManager()
    mgr.runManager()

if __name__ == "__main__":
    main()

