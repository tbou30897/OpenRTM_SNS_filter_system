#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -*- Python -*-

# <rtc-template block="description">
"""
 @file morphological_analysis.py
 @brief A component that performs morphological analysis using Mecab.
 @date $Date$


"""
# </rtc-template>

import sys
import time
sys.path.append(".")

# Import RTM module
import RTC
import OpenRTM_aist

#import関係
import MeCab
from pprint import pprint
import time

# Import Service implementation class
# <rtc-template block="service_impl">

# </rtc-template>

# Import Service stub modules
# <rtc-template block="consumer_import">
# </rtc-template>


# This module's spesification
# <rtc-template block="module_spec">
morphological_analysis_spec = ["implementation_id", "morphological_analysis", 
         "type_name",         "morphological_analysis", 
         "description",       "A component that performs morphological analysis using Mecab.", 
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
# @class morphological_analysis
# @brief A component that performs morphological analysis using Mecab.
# 
# 
# </rtc-template>
class morphological_analysis(OpenRTM_aist.DataFlowComponentBase):
	
    ##
    # @brief constructor
    # @param manager Maneger Object
    # 
    def __init__(self, manager):
        OpenRTM_aist.DataFlowComponentBase.__init__(self, manager)

        self._d_TextIn = OpenRTM_aist.instantiateDataType(RTC.TimedWStringSeq)
        """
        他コンポーネントから送信されてきたリスト型データを受信する。
        """
        self._TextInIn = OpenRTM_aist.InPort("TextIn", self._d_TextIn)
        self._d_WordOut = OpenRTM_aist.instantiateDataType(RTC.TimedWStringSeq)
        """
        リスト型で送信されてきた文字列を分かち書きしてリスト型で送信する。
         - Semantics: WordOut からは、以下のように出力
		              [‘単語 1’,’単語 2’,’単語 3’,’単語 4’]
		              例:[‘今’,’は’,’一時’,’です’,]

        """
        self._WordOutOut = OpenRTM_aist.OutPort("WordOut", self._d_WordOut)
        self._d_PartOfSpeechOut = OpenRTM_aist.instantiateDataType(RTC.TimedWStringSeq)
        """
        リスト型で送信されてきた文字列を形態素解析して品詞をリスト型で送信する。

         - Semantics: PartOfSpeechOut からは、以下のように出力
		              [‘品詞データ 1(例:名詞,非自立,一般,*,*,*)’,’品詞データ
		              2’,’品詞データ 3’]
        """
        self._PartOfSpeechOutOut = OpenRTM_aist.OutPort("PartOfSpeechOut", self._d_PartOfSpeechOut)


		


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
        self.addOutPort("WordOut",self._WordOutOut)
        self.addOutPort("PartOfSpeechOut",self._PartOfSpeechOutOut)
		
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
        if self._TextInIn.isNew(): #新しいデータが来たか確認
            self._d_TextIn = self._TextInIn.read() #値を読み込む
            textlist = self._d_TextIn.data

            #形態素解析
            for text in textlist:
                tagger = MeCab.Tagger()
                result =tagger.parse(text).split()
                num = len(result)


                wordlist = []
                partlist = []



				#単語を取得↓
                for wordnum in range(0,num,2):
                    wordlist.append(result[wordnum])
					
                print(wordlist)
				
				
				#品詞を取得↓
                for partnunm in range(1,num,2):
                    partlist.append(result[partnunm])
                print(partlist)
					
				#単語を送信
                self._d_WordOut.data= wordlist
                self._WordOutOut.write()
				

				#品詞を送信
                self._d_PartOfSpeechOut.data= partlist
                self._PartOfSpeechOutOut.write()    
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
	



def morphological_analysisInit(manager):
    profile = OpenRTM_aist.Properties(defaults_str=morphological_analysis_spec)
    manager.registerFactory(profile,
                            morphological_analysis,
                            OpenRTM_aist.Delete)

def MyModuleInit(manager):
    morphological_analysisInit(manager)

    # create instance_name option for createComponent()
    instance_name = [i for i in sys.argv if "--instance_name=" in i]
    if instance_name:
        args = instance_name[0].replace("--", "?")
    else:
        args = ""
  
    # Create a component
    comp = manager.createComponent("morphological_analysis" + args)

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

