#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -*- Python -*-

# <rtc-template block="description">
"""
 @file morphological_analysisTest.py
 @brief A component that performs morphological analysis using Mecab.
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

import morphological_analysis

# </rtc-template>

# Import Service stub modules
# <rtc-template block="consumer_import">
# </rtc-template>


# This module's spesification
# <rtc-template block="module_spec">
morphological_analysistest_spec = ["implementation_id", "morphological_analysisTest", 
         "type_name",         "morphological_analysisTest", 
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
# @class morphological_analysisTest
# @brief A component that performs morphological analysis using Mecab.
# 
# 
# </rtc-template>
class morphological_analysisTest(OpenRTM_aist.DataFlowComponentBase):
    
    ##
    # @brief constructor
    # @param manager Maneger Object
    # 
    def __init__(self, manager):
        OpenRTM_aist.DataFlowComponentBase.__init__(self, manager)

        self._d_WordOut = OpenRTM_aist.instantiateDataType(RTC.TimedWStringSeq)
        """
        リスト型で送信されてきた文字列を分かち書きしてリスト型で送信する。
         - Semantics: WordOut からは、以下のように出力
		              [‘単語 1’,’単語 2’,’単語 3’,’単語 4’]
		              例:[‘今’,’は’,’一時’,’です’,]
        """
        self._WordOutIn = OpenRTM_aist.InPort("WordOut", self._d_WordOut)
        self._d_PartOfSpeechOut = OpenRTM_aist.instantiateDataType(RTC.TimedWStringSeq)
        """
        リスト型で送信されてきた文字列を形態素解析して品詞をリスト型で送信する。
         - Semantics: PartOfSpeechOut からは、以下のように出力
		              [‘品詞データ 1(例:名詞,非自立,一般,*,*,*)’,’品詞データ
		              2’,’品詞データ 3’]
        """
        self._PartOfSpeechOutIn = OpenRTM_aist.InPort("PartOfSpeechOut", self._d_PartOfSpeechOut)
        self._d_TextIn = OpenRTM_aist.instantiateDataType(RTC.TimedWStringSeq)
        """
        他コンポーネントから送信されてきたリスト型データを受信する。
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
        self.addInPort("WordOut",self._WordOutIn)
        self.addInPort("PartOfSpeechOut",self._PartOfSpeechOutIn)
        
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
    comp = manager.getComponent("morphological_analysisTest0")
    if comp is None:
        print('Component get failed.', file=sys.stderr)
        return False
    return comp.runTest()

def morphological_analysisTestInit(manager):
    profile = OpenRTM_aist.Properties(defaults_str=morphological_analysistest_spec)
    manager.registerFactory(profile,
                            morphological_analysisTest,
                            OpenRTM_aist.Delete)

def MyModuleInit(manager):
    morphological_analysisTestInit(manager)
    morphological_analysis.morphological_analysisInit(manager)

    # Create a component
    comp = manager.createComponent("morphological_analysisTest")

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

