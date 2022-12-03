#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -*- Python -*-

# <rtc-template block="description">
"""
 @file restricted_wordTest.py
 @brief This component determines whether or not a Separation word or part of speech is a bad word when it is received and regulate the vocabulary..
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

import restricted_word

# </rtc-template>

# Import Service stub modules
# <rtc-template block="consumer_import">
# </rtc-template>


# This module's spesification
# <rtc-template block="module_spec">
restricted_wordtest_spec = ["implementation_id", "restricted_wordTest", 
         "type_name",         "restricted_wordTest", 
         "description",       "This component determines whether or not a Separation word or part of speech is a bad word when it is received and regulate the vocabulary..", 
         "version",           "1.0.0", 
         "vendor",            "tbou30897", 
         "category",          "language processing", 
         "activity_type",     "STATIC", 
         "max_instance",      "1", 
         "language",          "Python", 
         "lang_type",         "SCRIPT",
         ""]
# </rtc-template>

# <rtc-template block="component_description">
##
# @class restricted_wordTest
# @brief This component determines whether or not a Separation word or part of speech is a bad word when it is received and regulate the vocabulary..
# 
# 
# </rtc-template>
class restricted_wordTest(OpenRTM_aist.DataFlowComponentBase):
    
    ##
    # @brief constructor
    # @param manager Maneger Object
    # 
    def __init__(self, manager):
        OpenRTM_aist.DataFlowComponentBase.__init__(self, manager)

        self._d_TextOut = OpenRTM_aist.instantiateDataType(RTC.TimedShortSeq)
        """
        伏せ字にする場所を送るコンポーネントです。
         - Semantics: ↓のように出力
		              [[‘悪口の位置 1’,’悪口の位置 2’],[‘悪口の位置 3’]]
		              例:[[‘3’,’7’],[‘17’]] ※←一つ目の文章の 3 つ目と 7
		              つ目の単語、二つ目の文章の 17
		              つ目の単語が悪口であるという意味
        """
        self._TextOutIn = OpenRTM_aist.InPort("TextOut", self._d_TextOut)
        self._d_WordIn = OpenRTM_aist.instantiateDataType(RTC.TimedWStringSeq)
        """
        分かち書き結果を受信するデータポートです。
        """
        self._WordInOut = OpenRTM_aist.OutPort("WordIn", self._d_WordIn)
        self._d_PartOfSpeechIn = OpenRTM_aist.instantiateDataType(RTC.TimedWStringSeq)
        """
        品詞のデータを受信するデータポートです。
        """
        self._PartOfSpeechInOut = OpenRTM_aist.OutPort("PartOfSpeechIn", self._d_PartOfSpeechIn)


        


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
        self.addInPort("TextOut",self._TextOutIn)
        
        # Set OutPort buffers
        self.addOutPort("WordIn",self._WordInOut)
        self.addOutPort("PartOfSpeechIn",self._PartOfSpeechInOut)
        
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
    comp = manager.getComponent("restricted_wordTest0")
    if comp is None:
        print('Component get failed.', file=sys.stderr)
        return False
    return comp.runTest()

def restricted_wordTestInit(manager):
    profile = OpenRTM_aist.Properties(defaults_str=restricted_wordtest_spec)
    manager.registerFactory(profile,
                            restricted_wordTest,
                            OpenRTM_aist.Delete)

def MyModuleInit(manager):
    restricted_wordTestInit(manager)
    restricted_word.restricted_wordInit(manager)

    # Create a component
    comp = manager.createComponent("restricted_wordTest")

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

