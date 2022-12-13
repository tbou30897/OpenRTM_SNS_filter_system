#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -*- Python -*-

# <rtc-template block="description">
"""
 @file sentiment_analysis.py
 @brief bert-base-japanese-sentiment based on BERT (google's natural language processing AI model) and component that performs sentiment analysis using BERT (google's natural language processing AI model).
 @date $Date$


"""
# </rtc-template>

import sys
import time
sys.path.append(".")

# Import RTM module
import RTC
import OpenRTM_aist
from transformers import pipeline, AutoModelForSequenceClassification, BertJapaneseTokenizer
import time


# Import Service implementation class
# <rtc-template block="service_impl">

# </rtc-template>

# Import Service stub modules
# <rtc-template block="consumer_import">
# </rtc-template>


# This module's spesification
# <rtc-template block="module_spec">
sentiment_analysis_spec = ["implementation_id", "sentiment_analysis", 
         "type_name",         "sentiment_analysis", 
         "description",       "bert-base-japanese-sentiment based on BERT (google's natural language processing AI model) and component that performs sentiment analysis using BERT (google's natural language processing AI model).", 
         "version",           "1.0.0", 
         "vendor",            "tbou30897", 
         "category",          "language_processing", 
         "activity_type",     "STATIC", 
         "max_instance",      "1", 
         "language",          "Python", 
         "lang_type",         "SCRIPT",
         ""]
# </rtc-template>

# <rtc-template block="component_description">
##
# @class sentiment_analysis
# @brief bert-base-japanese-sentiment based on BERT (google's natural language processing AI model) and component that performs sentiment analysis using BERT (google's natural language processing AI model).
# 
# 
# </rtc-template>
class sentiment_analysis(OpenRTM_aist.DataFlowComponentBase):
	
    ##
    # @brief constructor
    # @param manager Maneger Object
    # 
    def __init__(self, manager):
        OpenRTM_aist.DataFlowComponentBase.__init__(self, manager)

        self._d_TextIn = OpenRTM_aist.instantiateDataType(RTC.TimedWStringSeq)
        """
        他コンポーネントから送られてきたリスト型データを受信する。
        """
        self._TextInIn = OpenRTM_aist.InPort("TextIn", self._d_TextIn)
        self._d_ScoreOut = OpenRTM_aist.instantiateDataType(RTC.TimedFloatSeq)
        """
        リスト型データで送信されてきた文章を-1~1
		の値で感情分析し、リスト型で送信する。
         - Semantics: [‘感情値 1’,’感情値 2’,’感情値 3’,’感情値
		              4’]のように出力
        """
        self._ScoreOutOut = OpenRTM_aist.OutPort("ScoreOut", self._d_ScoreOut)
        self._d_LabelOut = OpenRTM_aist.instantiateDataType(RTC.TimedWStringSeq)
        """
         - Semantics: [‘感情(ポジティブ or ネガティブ)’,’感情(ポジティブ or
		              ネガティブ)’]のように出力
        """
        self._LabelOutOut = OpenRTM_aist.OutPort("LabelOut", self._d_LabelOut)


		


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
        self.addInPort("TextIn",self._TextInIn)
		
        # Set OutPort buffers
        self.addOutPort("ScoreOut",self._ScoreOutOut)
        self.addOutPort("LabelOut",self._LabelOutOut)
		
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
        self.model = AutoModelForSequenceClassification.from_pretrained('daigo/bert-base-japanese-sentiment') #AIモデルを取得
        self.tokenizer = BertJapaneseTokenizer.from_pretrained('cl-tohoku/bert-base-japanese-whole-word-masking')#トークンを取得
        self.nlp = pipeline("sentiment-analysis",model=self.model,tokenizer=self.tokenizer)


        self.sentiment_list = []
        self.outlist = []
        time.sleep(1)
		

        self.sentimentlabel = [] 
        self.sentimentscore = []    

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

		#感情分析対象が入ったリストを取得
        if self._TextInIn.isNew(): #新しいデータが来たか確認
            self._d_TextIn = self._TextInIn.read() #値を読み込む
            self.textlist = self._d_TextIn.data



            for text in self.textlist:

                #感情分析の実行
                self.sentiment = self.nlp(text)#self.nlp(感情分析したいテキスト)で感情分析
                print(self.sentiment)

                #label、scoreを送信
                self.sentimentlabel.append(self.sentiment[0]['label'])
                self.sentimentscore.append(self.sentiment[0]['score'])

            self._d_LabelOut.data= self.sentimentlabel
            self._LabelOutOut.write()

            self._d_ScoreOut.data= self.sentimentscore
            self._ScoreOutOut.write()    

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
	



def sentiment_analysisInit(manager):
    profile = OpenRTM_aist.Properties(defaults_str=sentiment_analysis_spec)
    manager.registerFactory(profile,
                            sentiment_analysis,
                            OpenRTM_aist.Delete)

def MyModuleInit(manager):
    sentiment_analysisInit(manager)

    # create instance_name option for createComponent()
    instance_name = [i for i in sys.argv if "--instance_name=" in i]
    if instance_name:
        args = instance_name[0].replace("--", "?")
    else:
        args = ""
  
    # Create a component
    comp = manager.createComponent("sentiment_analysis" + args)

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

