#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -*- Python -*-

# <rtc-template block="description">
"""
 @file twitter_api.py
 @brief This component retrieves tweets (latest tweets) related to specified keywords from twitter.
 @date $Date$


"""
# </rtc-template>

import sys
import time
sys.path.append(".")

# Import RTM module
import RTC
import OpenRTM_aist

import json
from requests_oauthlib import OAuth1Session
from pprint import pprint

# Import Service implementation class
# <rtc-template block="service_impl">

# </rtc-template>

# Import Service stub modules
# <rtc-template block="consumer_import">
# </rtc-template>


# This module's spesification
# <rtc-template block="module_spec">
twitter_api_spec = ["implementation_id", "twitter_api", 
         "type_name",         "twitter_api", 
         "description",       "This component retrieves tweets (latest tweets) related to specified keywords from twitter.", 
         "version",           "1.0.0", 
         "vendor",            "tbou30897", 
         "category",          "Information_acquisition", 
         "activity_type",     "STATIC", 
         "max_instance",      "1", 
         "language",          "Python", 
         "lang_type",         "SCRIPT",
         ""]
# </rtc-template>

# <rtc-template block="component_description">
##
# @class twitter_api
# @brief This component retrieves tweets (latest tweets) related to specified keywords from twitter.
# 
# 
# </rtc-template>
class twitter_api(OpenRTM_aist.DataFlowComponentBase):
	
    ##
    # @brief constructor
    # @param manager Maneger Object
    # 
    def __init__(self, manager):
        OpenRTM_aist.DataFlowComponentBase.__init__(self, manager)

        self._d_TextOut = OpenRTM_aist.instantiateDataType(RTC.TimedWStringSeq)
        """
        本コンポーネントが取得したデータをリスト型で送信するデータポートです。
         - Type: TimedWStrintSeq
         - Semantics: [‘ツイート 1’,’ ツイート 2’,’ ツイート 3’,’ ツイート
		              4’]
		              ↑のように検索ワードに関するツイートをリスト型で出力
        """
        self._TextOutOut = OpenRTM_aist.OutPort("TextOut", self._d_TextOut)


		


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
		
        # Set OutPort buffers
        self.addOutPort("TextOut",self._TextOutOut)
		
        # Set service provider to Ports
		
        # Set service consumers to Ports
		
        # Set CORBA Service Ports
		
        return RTC.RTC_OK
	
    def twitterAPI (self):
        API_KEY = "QDHwDFGyIOTt2EY9BYkWuNA9B"
        API_KEY_SECRET = "KSWgDxzd5BJNduZ37OSqeambmSwchA1QautjMhWBRgjitKS5wk"
        ACCESS_TOKEN = "1561239063440801792-ERs8llSM4RUP2Q1iMDBDHftE1q5G98"
        ACCESS_TOKEN_SECRET = "FoVSHgXxw0EBoRXS7J4XtVHsB6l6fIJlrrXeLWUbL8Hn0"


        twitter_oauth = OAuth1Session(API_KEY, API_KEY_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
            
        # APIのリソースURL
        request_search_url = "https://api.twitter.com/1.1/search/tweets.json"

        # 検索キーワードを指定
        query = self.search_word

        # パラメータの設定
        params = {
        "q": query,
        "count": 4,
        "locale": "ja",
        "result_type": "recent"
        }

        self.count = params["count"]
        # Twitter APIで検索を実行
        res = twitter_oauth.get(request_search_url, params=params)
        self.response = json.loads(res.text)
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
        self.outlist = []

        self.search_word = "ツイッター"
        self.twitterAPI()

        #検索結果からツイート本文のみをリストに格納
        response_statuses = self.response['statuses']
        for i in range(self.count):
            outtext = (response_statuses[i]["text"].replace("\n","").replace("\u3000",""))
            result = ("".join(outtext))
            self.outlist.append(result)



        pprint(self.outlist)


        #結果を入れたリストを送信
        self._d_TextOut.data = self.outlist
        self._TextOutOut.write()        
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
	



def twitter_apiInit(manager):
    profile = OpenRTM_aist.Properties(defaults_str=twitter_api_spec)
    manager.registerFactory(profile,
                            twitter_api,
                            OpenRTM_aist.Delete)

def MyModuleInit(manager):
    twitter_apiInit(manager)

    # create instance_name option for createComponent()
    instance_name = [i for i in sys.argv if "--instance_name=" in i]
    if instance_name:
        args = instance_name[0].replace("--", "?")
    else:
        args = ""
  
    # Create a component
    comp = manager.createComponent("twitter_api" + args)

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

