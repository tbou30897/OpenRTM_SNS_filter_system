#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -*- Python -*-

# <rtc-template block="description">
"""
 @file restricted_word.py
 @brief This component determines whether or not a Separation word or part of speech is a bad word when it is received and regulate the vocabulary..
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
restricted_word_spec = ["implementation_id", "restricted_word", 
         "type_name",         "restricted_word", 
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
# @class restricted_word
# @brief This component determines whether or not a Separation word or part of speech is a bad word when it is received and regulate the vocabulary..
# 
# 
# </rtc-template>
class restricted_word(OpenRTM_aist.DataFlowComponentBase):
	
    ##
    # @brief constructor
    # @param manager Maneger Object
    # 
    def __init__(self, manager):
        OpenRTM_aist.DataFlowComponentBase.__init__(self, manager)

        self._d_WordIn = OpenRTM_aist.instantiateDataType(RTC.TimedWStringSeq)
        """
        分かち書き結果を受信するデータポートです。
        """
        self._WordInIn = OpenRTM_aist.InPort("WordIn", self._d_WordIn)
        self._d_PartOfSpeechIn = OpenRTM_aist.instantiateDataType(RTC.TimedWStringSeq)
        """
        品詞のデータを受信するデータポートです。
        """
        self._PartOfSpeechInIn = OpenRTM_aist.InPort("PartOfSpeechIn", self._d_PartOfSpeechIn)
        self._d_TextOut = OpenRTM_aist.instantiateDataType(RTC.TimedShortSeq)
        """
        伏せ字にする場所を送るコンポーネントです。
         - Semantics: ↓のように出力
		              [[‘悪口の位置 1’,’悪口の位置 2’],[‘悪口の位置 3’]]
		              例:[[‘3’,’7’],[‘17’]] ※←一つ目の文章の 3 つ目と 7
		              つ目の単語、二つ目の文章の 17
		              つ目の単語が悪口であるという意味
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
        self.addInPort("WordIn",self._WordInIn)
        self.addInPort("PartOfSpeechIn",self._PartOfSpeechInIn)
		
        # Set OutPort buffers
        self.addOutPort("TextOut",self._TextOutOut)
		
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
    	#悪口単語辞書ファイル(.txt)の読み込み(restrictedword_listに入る)
        f = open('restricted word list.txt', 'r', encoding='UTF-8')	
        censoredterms = f.read()
        f.close()
        self.restrictedword_list = censoredterms.split('\n')
        print(self.restrictedword_list)


		#ニュアンス判断の品詞
        self.restrictedword_part = ["名詞","固有名詞","動詞","格助詞","終助詞","副助詞","係助詞","形容動詞"]

		#その他リスト等の定義
        self.word_list       = []
        self.part_list       = []
        self.outlist        = []
		
        self.presence_of_a_front = "false"

        self.list_number = 0


        time.sleep(1)    
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
			#単語データの受信
        if self._WordInIn.isNew(): #新しいデータが来たか確認
            self._d_WordIn = self._WordInIn.read() #値を読み込む
            self.word_list = self._d_WordIn.data
            del self.word_list[-1]#EOS表示がリストの最後に入っているので削除
			


		#品詞データの受信
        if self._PartOfSpeechInIn.isNew(): #新しいデータが来たか確認
            self._d_PartOfSpeechIn = self._PartOfSpeechInIn.read() #値を読み込む
            self.part_list = self._d_PartOfSpeechIn.data

			
			#規制単語と単語データが一致するか
            for element_number, word in enumerate(self.word_list):
                for restrictedword in self.restrictedword_list:
                    if restrictedword in word:
						
						
						#ニュアンス判断の品詞と品詞データが一致するか
                        for restrictedpart in self.restrictedword_part:

							#悪口単語の前の単語が指定の品詞なら規制リストに追加
                            if element_number  != 0 :
                                front = element_number-1
                                if restrictedpart in self.part_list[front]:
                                    self.outlist.append(self.list_number)
                                    self.outlist.append(element_number)
                                    self.presence_of_a_front = "true"

							#悪口単語の後の単語が指定の品詞かつ、すでに規制リストに入っていないなら規制リストに追加
                            if element_number != len(self.word_list)-1 and self.presence_of_a_front == "false":
                                back = element_number + 1
                                if restrictedpart in self.part_list[back]:
                                    self.outlist.append(self.list_number)
                                    self.outlist.append(element_number)
                            self.presence_of_a_front = "false"

								
            self.list_number = self.list_number + 1

            print(self.outlist)

            
            self._d_TextOut.data= self.outlist#['何番目のリストか','リストの悪口の位置']のリストを出力
            self._TextOutOut.write()


            self.outlist        = []    
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
	



def restricted_wordInit(manager):
    profile = OpenRTM_aist.Properties(defaults_str=restricted_word_spec)
    manager.registerFactory(profile,
                            restricted_word,
                            OpenRTM_aist.Delete)

def MyModuleInit(manager):
    restricted_wordInit(manager)

    # create instance_name option for createComponent()
    instance_name = [i for i in sys.argv if "--instance_name=" in i]
    if instance_name:
        args = instance_name[0].replace("--", "?")
    else:
        args = ""
  
    # Create a component
    comp = manager.createComponent("restricted_word" + args)

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

