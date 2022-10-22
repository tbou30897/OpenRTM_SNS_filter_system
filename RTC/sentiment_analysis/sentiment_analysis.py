﻿#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -*- Python -*-

"""
 @file sentiment_analysis.py
 @brief ModuleDescription
 @date $Date$


"""
import sys
import time
sys.path.append(".")

# Import RTM module
import RTC
import OpenRTM_aist

#import関係
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
		 "description",       "ModuleDescription",
		 "version",           "1.0.0",
		 "vendor",            "VenderName",
		 "category",          "Category",
		 "activity_type",     "STATIC",
		 "max_instance",      "1",
		 "language",          "Python",
		 "lang_type",         "SCRIPT",
		 "conf.default.emotional_selection", "1",

		 "conf.__widget__.emotional_selection", "text",

         "conf.__type__.emotional_selection", "string",

		 ""]
# </rtc-template>

##
# @class sentiment_analysis
# @brief ModuleDescription
#
#
class sentiment_analysis(OpenRTM_aist.DataFlowComponentBase):

	##
	# @brief constructor
	# @param manager Maneger Object
	#
	def __init__(self, manager):
		OpenRTM_aist.DataFlowComponentBase.__init__(self, manager)

		self._d_TextIn = OpenRTM_aist.instantiateDataType(RTC.TimedWStringSeq)
		"""
		"""
		self._TextInIn = OpenRTM_aist.InPort("TextIn", self._d_TextIn)
		self._d_TextOut = OpenRTM_aist.instantiateDataType(RTC.TimedWStringSeq)
		"""
		"""
		self._TextOutOut = OpenRTM_aist.OutPort("TextOut", self._d_TextOut)





		# initialize of configuration-data.
		# <rtc-template block="init_conf_param">
		"""
		
		 - Name:  emotional_selection
		 - DefaultValue: 1
		"""
		self._emotional_selection = ['1']

		# </rtc-template>



	##
	#
	# The initialize action (on CREATED->ALIVE transition)
	# formaer rtc_init_entry()
	#
	# @return RTC::ReturnCode_t
	#
	#
	def onInitialize(self):
		# Bind variables and configuration variable
		self.bindParameter("emotional_selection", self._emotional_selection, "1")

		# Set InPort buffers
		self.addInPort("TextIn",self._TextInIn)

		# Set OutPort buffers
		self.addOutPort("TextOut",self._TextOutOut)

		# Set service provider to Ports

		# Set service consumers to Ports

		# Set CORBA Service Ports

		return RTC.RTC_OK



	def SentimentAnalysis(self):
		# 感情分析の実行
		model = AutoModelForSequenceClassification.from_pretrained('daigo/bert-base-japanese-sentiment') #AIモデルを取得
		tokenizer = BertJapaneseTokenizer.from_pretrained('cl-tohoku/bert-base-japanese-whole-word-masking')#トークンを取得
		nlp = pipeline("sentiment-analysis",model=model,tokenizer=tokenizer)

		self.sentiment = nlp(self.text)#nlp(感情分析したいテキスト)で感情分析


	###
	##
	## The finalize action (on ALIVE->END transition)
	## formaer rtc_exiting_entry()
	##
	## @return RTC::ReturnCode_t
	#
	##
	#def onFinalize(self):
	#
	#	return RTC.RTC_OK

	###
	##
	## The startup action when ExecutionContext startup
	## former rtc_starting_entry()
	##
	## @param ec_id target ExecutionContext Id
	##
	## @return RTC::ReturnCode_t
	##
	##
	#def onStartup(self, ec_id):
	#
	#	return RTC.RTC_OK

	###
	##
	## The shutdown action when ExecutionContext stop
	## former rtc_stopping_entry()
	##
	## @param ec_id target ExecutionContext Id
	##
	## @return RTC::ReturnCode_t
	##
	##
	#def onShutdown(self, ec_id):
	#
	#	return RTC.RTC_OK

	##
	#
	# The activated action (Active state entry action)
	# former rtc_active_entry()
	#
	# @param ec_id target ExecutionContext Id
	#
	# @return RTC::ReturnCode_t
	#
	#
	def onActivated(self, ec_id):
			
		self.sentiment_list = []
		self.outlist = []
		time.sleep(1)
		

		self.sentimentlabel = "score"#score or labelで指定　＃scoreの場合は感情の数値、labelは文字列
		return RTC.RTC_OK

	##
	#
	# The deactivated action (Active state exit action)
	# former rtc_active_exit()
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
	# former rtc_active_do()
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


			for self.text in self.textlist:

				self.SentimentAnalysis()
				
				
				if self.sentimentlabel == "score" and self.sentiment[0]["label"] == "ネガティブ":
					self.sentiment_list.append(self.sentiment[0][self.sentimentlabel] * -1)
					print(self.sentiment[0]["label"])

				else:
					self.sentiment_list.append(self.sentiment[0][self.sentimentlabel])
			
				
			#感情分析結果を送信
			if self.sentimentlabel == 'score':
				for text in self.sentiment_list:
					self.outlist.append(str(text))
				self.outlist.insert(0, 'score')

			elif self.sentimentlabel == "label":
				self.outlist = self.sentiment_list
				self.outlist.insert(0,'label')

			self._d_TextOut.data = self.outlist
			self._TextOutOut.write()
			print(self.sentiment_list)
			self.outlist = []
			self.sentiment_list

			

		return RTC.RTC_OK

	###
	##
	## The aborting action when main logic error occurred.
	## former rtc_aborting_entry()
	##
	## @param ec_id target ExecutionContext Id
	##
	## @return RTC::ReturnCode_t
	##
	##
	#def onAborting(self, ec_id):
	#
	#	return RTC.RTC_OK

	###
	##
	## The error action in ERROR state
	## former rtc_error_do()
	##
	## @param ec_id target ExecutionContext Id
	##
	## @return RTC::ReturnCode_t
	##
	##
	#def onError(self, ec_id):
	#
	#	return RTC.RTC_OK

	###
	##
	## The reset action that is invoked resetting
	## This is same but different the former rtc_init_entry()
	##
	## @param ec_id target ExecutionContext Id
	##
	## @return RTC::ReturnCode_t
	##
	##
	#def onReset(self, ec_id):
	#
	#	return RTC.RTC_OK

	###
	##
	## The state update action that is invoked after onExecute() action
	## no corresponding operation exists in OpenRTm-aist-0.2.0
	##
	## @param ec_id target ExecutionContext Id
	##
	## @return RTC::ReturnCode_t
	##

	##
	#def onStateUpdate(self, ec_id):
	#
	#	return RTC.RTC_OK

	###
	##
	## The action that is invoked when execution context's rate is changed
	## no corresponding operation exists in OpenRTm-aist-0.2.0
	##
	## @param ec_id target ExecutionContext Id
	##
	## @return RTC::ReturnCode_t
	##
	##
	#def onRateChanged(self, ec_id):
	#
	#	return RTC.RTC_OK




def sentiment_analysisInit(manager):
    profile = OpenRTM_aist.Properties(defaults_str=sentiment_analysis_spec)
    manager.registerFactory(profile,
                            sentiment_analysis,
                            OpenRTM_aist.Delete)

def MyModuleInit(manager):
    sentiment_analysisInit(manager)

    # Create a component
    comp = manager.createComponent("sentiment_analysis")

def main():
	mgr = OpenRTM_aist.Manager.init(sys.argv)
	mgr.setModuleInitProc(MyModuleInit)
	mgr.activateManager()
	mgr.runManager()

if __name__ == "__main__":
	main()
