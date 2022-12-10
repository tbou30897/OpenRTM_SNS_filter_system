#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -*- Python -*-

# <rtc-template block="description">
"""
 @file sentiment_analysisTest.py
 @brief bert-base-japanese-sentiment based on BERT (google's natural language processing AI model) and component that performs sentiment analysis using BERT (google's natural language processing AI model).
 @date $Date$


"""
# </rtc-template>

from __future__ import print_function
import sys
import time
sys.path.append(".")

# Import RTM module
import RTC
import OpenRTM_aist


# Import Service implementation class
# <rtc-template block="service_impl">

import sentiment_analysis

# </rtc-template>

# Import Service stub modules
# <rtc-template block="consumer_import">
# </rtc-template>


# This module's spesification
# <rtc-template block="module_spec">
sentiment_analysistest_spec = ["implementation_id", "sentiment_analysisTest", 
         "type_name",         "sentiment_analysisTest", 
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
# @class sentiment_analysisTest
# @brief bert-base-japanese-sentiment based on BERT (google's natural language processing AI model) and component that performs sentiment analysis using BERT (google's natural language processing AI model).
# 
# 
# </rtc-template>
class sentiment_analysisTest(OpenRTM_aist.DataFlowComponentBase):
    
    ##
    # @brief constructor
    # @param manager Maneger Object
    # 
    def __init__(self, manager):
        OpenRTM_aist.DataFlowComponentBase.__init__(self, manager)

        self._d_ScoreOut = OpenRTM_aist.instantiateDataType(RTC.TimedFloatSeq)
        """
        リスト型データで送信されてきた文章を-1~1
		の値で感情分析し、リスト型で送信する。
         - Semantics: [‘感情値 1’,’感情値 2’,’感情値 3’,’感情値
		              4’]のように出力
        """
        self._ScoreOutIn = OpenRTM_aist.InPort("ScoreOut", self._d_ScoreOut)
        self._d_LabelOut = OpenRTM_aist.instantiateDataType(RTC.TimedWStringSeq)
        """
         - Semantics: [‘感情(ポジティブ or ネガティブ)’,’感情(ポジティブ or
		              ネガティブ)’]のように出力
        """
        self._LabelOutIn = OpenRTM_aist.InPort("LabelOut", self._d_LabelOut)
        self._d_TextIn = OpenRTM_aist.instantiateDataType(RTC.TimedWStringSeq)
        """
        他コンポーネントから送られてきたリスト型データを受信する。
        """
        self._TextInOut = OpenRTM_aist.OutPort("TextIn", self._d_TextIn)


        


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
        self.addInPort("ScoreOut",self._ScoreOutIn)
        self.addInPort("LabelOut",self._LabelOutIn)
        
        # Set OutPort buffers
        self.addOutPort("TextIn",self._TextInOut)
        
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
    
    #    ##
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
    
        return RTC.RTC_OK
    
    ###
    ##
    ## The aborting action when main logic error occurred.
    ##
    ## @param ec_id target ExecutionContext Id
    ##
    ## @return RTC::ReturnCode_t
    #    #
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
    
    def runTest(self):
        return True

def RunTest():
    manager = OpenRTM_aist.Manager.instance()
    comp = manager.getComponent("sentiment_analysisTest0")
    if comp is None:
        print('Component get failed.', file=sys.stderr)
        return False
    return comp.runTest()

def sentiment_analysisTestInit(manager):
    profile = OpenRTM_aist.Properties(defaults_str=sentiment_analysistest_spec)
    manager.registerFactory(profile,
                            sentiment_analysisTest,
                            OpenRTM_aist.Delete)

def MyModuleInit(manager):
    sentiment_analysisTestInit(manager)
    sentiment_analysis.sentiment_analysisInit(manager)

    # Create a component
    comp = manager.createComponent("sentiment_analysisTest")

def main():
    mgr = OpenRTM_aist.Manager.init(sys.argv)
    mgr.setModuleInitProc(MyModuleInit)
    mgr.activateManager()
    mgr.runManager(True)

    ret = RunTest()
    mgr.shutdown()

    if ret:
        sys.exit(0)
    else:
        sys.exit(1)

if __name__ == "__main__":
    main()

