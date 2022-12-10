#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -*- Python -*-

# <rtc-template block="description">
"""
 @file result_out.py
 @brief This component outputs filtered results based on the results of sentiment analysis, the results of the sharing, and the position of the swear words.
 @date $Date$


"""
# </rtc-template>

import sys
import time
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
result_out_spec = ["implementation_id", "result_out", 
         "type_name",         "result_out", 
         "description",       "This component outputs filtered results based on the results of sentiment analysis, the results of the sharing, and the position of the swear words.", 
         "version",           "1.0.0", 
         "vendor",            "tbou30897", 
         "category",          "result output", 
         "activity_type",     "STATIC", 
         "max_instance",      "1", 
         "language",          "Python", 
         "lang_type",         "SCRIPT",
         "conf.default.emotion_selection", "0",

         "conf.__widget__.emotion_selection", "text",

         "conf.__type__.emotion_selection", "float",

         ""]
# </rtc-template>

# <rtc-template block="component_description">
##
# @class result_out
# @brief This component outputs filtered results based on the results of sentiment analysis, the results of the sharing, and the position of the swear words.
# 
# 
# </rtc-template>
class result_out(OpenRTM_aist.DataFlowComponentBase):
	
    ##
    # @brief constructor
    # @param manager Maneger Object
    # 
    def __init__(self, manager):
        OpenRTM_aist.DataFlowComponentBase.__init__(self, manager)

        self._d_SentimentScoreIn = OpenRTM_aist.instantiateDataType(RTC.TimedFloatSeq)
        """
        Label（-1~1の感情値）を受信する
        """
        self._SentimentScoreInIn = OpenRTM_aist.InPort("SentimentScoreIn", self._d_SentimentScoreIn)
        self._d_SentimentLabelIn = OpenRTM_aist.instantiateDataType(RTC.TimedWStringSeq)
        """
        Label（ポジティブorネガティブ）を受信する
        """
        self._SentimentLabelInIn = OpenRTM_aist.InPort("SentimentLabelIn", self._d_SentimentLabelIn)
        self._d_TextIn = OpenRTM_aist.instantiateDataType(RTC.TimedWStringSeq)
        """
        分かち書き結果を受信する。
        """
        self._TextInIn = OpenRTM_aist.InPort("TextIn", self._d_TextIn)
        self._d_SwearingIn = OpenRTM_aist.instantiateDataType(RTC.TimedShortSeq)
        """
        悪口の位置のデータを受信する。
        """
        self._SwearingInIn = OpenRTM_aist.InPort("SwearingIn", self._d_SwearingIn)


		


        # initialize of configuration-data.
        # <rtc-template block="init_conf_param">
        """
        
         - Name:  emotion_selection
         - DefaultValue: 0
        """
        self._emotion_selection = [0]
		
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
        self.bindParameter("emotion_selection", self._emotion_selection, "0")
		
        # Set InPort buffers
        self.addInPort("SentimentScoreIn",self._SentimentScoreInIn)
        self.addInPort("SentimentLabelIn",self._SentimentLabelInIn)
        self.addInPort("TextIn",self._TextInIn)
        self.addInPort("SwearingIn",self._SwearingInIn)
		
        # Set OutPort buffers
		
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
		#本文、感情、規制単語が入る辞書を作成
        self.word	     = []
        self.swearing    = []
        self.sentiment_positive   = []
        self.sentiment_negative   = []
        self.text                 = []
        self.resultlist           = []   
        self.labelcount           = 0
        self.scorecount           = 0  
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

		#分かち書き
        if self._TextInIn.isNew(): #新しいデータが来たか確認
            self._d_TextIn = self._TextInIn.read() #値を読み込む
            self.word.append(self._d_TextIn.data)


		#規制単語
        if self._SwearingInIn.isNew(): #新しいデータが来たか確認
            self._d_SwearingIn = self._SwearingInIn.read() #値を読み込む [['何番目のリストか','リストの悪口の位置'],['何番目のリストか','リストの悪口の位置']・・・]]  

            self.swearing = self._d_SwearingIn.data
            num = len(self.swearing) - 1
            #規制単語の場所を変数に格納
            for swearingposition in range(0, num, 2): #0・2・4 ~~ num
                self.list_position     = (self.swearing[swearingposition])
                self.swearing_position = (self.swearing[swearingposition + 1])
                
                #規制単語を伏せ字に変換
                self.word[self.list_position][self.swearing_position] = "***"


                self.result = ("".join(self.word[self.list_position]))

                # 分かち書きリストを結合、resultlistに格納
                self.resultlist.append(self.result)



		#感情値(label)
        if self._SentimentLabelInIn.isNew():
            self._d_SentimentIn = self._SentimentLabelInIn.read()
            self.sentimentLabel = self._d_SentimentLabelIn.data
            self.labelcount = 1

        #感情値(score)
        if self._SentimentScoreInIn.isNew():
            self._d_SentimentScoreIn = self._SentimentScoreInIn.read()
            self.sentimentscore = self._d_SentimentScoreIn.data
            self.scorecount = 1

        #感情値がどちらも揃っていたら最終結果を出力
        if self.labelcount == 1 and self.scorecount == 1:

			#ネガティブ、ポジティブのみ出力	
            for i , sentimentnum in enumerate (self.sentimentLabel):
                if self._emotion_selection == 0 and sentimentnum >= 0.3:
                    self.sentiment_positive.append(self.resultlist[i])

                elif self._emotion_selection == 1 and sentimentnum <0.3:
                    self.sentiment_negative.append(self.resultlist[i])
                
                else:
                    pass

            if len(self.resultlist) == 0:
                print("最終結果")
                print(self.word)
            
            else:
                print("最終結果")
                print(self.resultlist) 

            self.scorecount = 0
            self.labelcount = 0       
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
	



def result_outInit(manager):
    profile = OpenRTM_aist.Properties(defaults_str=result_out_spec)
    manager.registerFactory(profile,
                            result_out,
                            OpenRTM_aist.Delete)

def MyModuleInit(manager):
    result_outInit(manager)

    # create instance_name option for createComponent()
    instance_name = [i for i in sys.argv if "--instance_name=" in i]
    if instance_name:
        args = instance_name[0].replace("--", "?")
    else:
        args = ""
  
    # Create a component
    comp = manager.createComponent("result_out" + args)

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

