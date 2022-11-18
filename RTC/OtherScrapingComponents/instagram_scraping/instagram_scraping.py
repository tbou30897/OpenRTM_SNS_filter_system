#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -*- Python -*-

# <rtc-template block="description">
"""
 @file instagram_scraping.py
 @brief ModuleDescription
 @date $Date$


"""
# </rtc-template>

import sys
import time
import instaloader
import os
sys.path.append(".")

# Import RTM module
import RTC
import OpenRTM_aist


# Import Service implementation class
# <rtc-template block="service_impl">

# </rtc-template>

# Import Service stub modules
# <rtc-template block="consumer_import">
# </rtc-template>


# This module's spesification
# <rtc-template block="module_spec">
instagram_scraping_spec = ["implementation_id", "instagram_scraping", 
         "type_name",         "instagram_scraping", 
         "description",       "ModuleDescription", 
         "version",           "1.0.0", 
         "vendor",            "VenderName", 
         "category",          "Category", 
         "activity_type",     "STATIC", 
         "max_instance",      "1", 
         "language",          "Python", 
         "lang_type",         "SCRIPT",
         "conf.default.DataType", "image",

         "conf.__widget__.DataType", "text",

         "conf.__type__.DataType", "string",

         ""]
# </rtc-template>

# <rtc-template block="component_description">
##
# @class instagram_scraping
# @brief ModuleDescription
# 
# 
class GetImageFromInstagram():
    def __init__(self, my_user_name, password):
        self.L = instaloader.Instaloader()
        self.my_user_name = my_user_name
        self.password = password
        self.L.login(my_user_name, password)

    def download_user_posts(self, target_username, limitation=100):
        posts = instaloader.Profile.from_username(self.L.context, target_username).get_posts()

        for index, post in enumerate(posts, 1):
            self.L.download_post(post, target_username)
            print("a")
            if index >= limitation:
                print(f'{target_username}の画像を{limitation}枚保存しました。')
                break
# </rtc-template>
class instagram_scraping(OpenRTM_aist.DataFlowComponentBase):
	
    ##
    # @brief constructor
    # @param manager Maneger Object
    # 
    def __init__(self, manager):
        OpenRTM_aist.DataFlowComponentBase.__init__(self, manager)

        self._d_UsernameIn = OpenRTM_aist.instantiateDataType(RTC.TimedWString)
        """
        """
        self._UsernameInIn = OpenRTM_aist.InPort("UsernameIn", self._d_UsernameIn)
        self._d_TextOut = OpenRTM_aist.instantiateDataType(RTC.TimedWStringSeq)
        """
        """
        self._TextOutOut = OpenRTM_aist.OutPort("TextOut", self._d_TextOut)
        self._d_ImageOut = OpenRTM_aist.instantiateDataType(RTC.TimedWStringSeq)
        """
        """
        self._ImageOutOut = OpenRTM_aist.OutPort("ImageOut", self._d_ImageOut)


		


        # initialize of configuration-data.
        # <rtc-template block="init_conf_param">
        """
        
         - Name:  DataType
         - DefaultValue: image
        """
        self._DataType = ['image']
		
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
        self.bindParameter("DataType", self._DataType, "image")
		
        # Set InPort buffers
        self.addInPort("UsernameIn",self._UsernameInIn)
		
        # Set OutPort buffers
        self.addOutPort("TextOut",self._TextOutOut)
        self.addOutPort("ImageOut",self._ImageOutOut)
		
        # Set service provider to Ports
		
        # Set service consumers to Ports
		
        # Set CORBA Service Ports
		
        return RTC.RTC_OK
	
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
        self.text_name  = []
        self.image_name = []      
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
        self.FileNameList = []
        if self._UsernameInIn.isNew(): #新しいデータが来たか確認
            self._d_UsernameIn = self._UsernameInIn.read() #値を読み込む
            self.Username = self._d_UsernameIn.data
            print(self.Username)


            TARGET_ID = self.Username
            USER_ID = "デベロッパーのユーザーネーム"
            PASSWORD = "デベロッパーのパスワード"
            number_of_picture = 20 # 取得したい投稿数（推奨:10~100）

            cls = GetImageFromInstagram(USER_ID, PASSWORD)
            cls.download_user_posts(TARGET_ID, number_of_picture)

            path = "./" + TARGET_ID

            files = os.listdir(path)

            #jpg,pngのみを残してその他を削除
            for filename in files:
                if ".jpg" in filename or ".png" in filename and self._DataType[0] == "image":
                    self.image_name.append("ワークスペースの指定（絶対パス）" + "/instagram_scraping/" + TARGET_ID + "/" + filename)
                elif".txt" in filename and self._DataType[0] == "text":
                    self.text_name.append("ワークスペースの指定（絶対パス）" + "/instagram_scraping/" + TARGET_ID + "/" + filename)
                else:
                    os.remove(TARGET_ID + "/" + filename)

            #データを送信（画像の絶対パス）
            if self._DataType[0] == "image":
                self._d_ImageOut.data= self.image_name
                self._ImageOutOut.write()   

            #データを送信（テキスト）
            elif self._DataType[0] == "text":
                for name in self.text_name:
                    f = open(TARGET_ID + "/" + name, 'r')
                    datalist = f.readlines()
                    self.FileNameList.append(datalist)
                self._d_TextOut.data= self.FileNameList
                self._TextOutOut.write()    
        
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
	



def instagram_scrapingInit(manager):
    profile = OpenRTM_aist.Properties(defaults_str=instagram_scraping_spec)
    manager.registerFactory(profile,
                            instagram_scraping,
                            OpenRTM_aist.Delete)

def MyModuleInit(manager):
    instagram_scrapingInit(manager)

    # create instance_name option for createComponent()
    instance_name = [i for i in sys.argv if "--instance_name=" in i]
    if instance_name:
        args = instance_name[0].replace("--", "?")
    else:
        args = ""
  
    # Create a component
    comp = manager.createComponent("instagram_scraping" + args)

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

