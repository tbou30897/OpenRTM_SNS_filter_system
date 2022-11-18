﻿#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -*- Python -*-

"""
 @file morphological_analysis.py
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
		 "description",       "ModuleDescription",
		 "version",           "1.0.0",
		 "vendor",            "VenderName",
		 "category",          "Category",
		 "activity_type",     "STATIC",
		 "max_instance",      "1",
		 "language",          "Python",
		 "lang_type",         "SCRIPT",
		 ""]
# </rtc-template>

##
# @class morphological_analysis
# @brief ModuleDescription
#
#
class morphological_analysis(OpenRTM_aist.DataFlowComponentBase):

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
		self._d_WordOut = OpenRTM_aist.instantiateDataType(RTC.TimedWStringSeq)
		"""
		"""
		self._WordOutOut = OpenRTM_aist.OutPort("WordOut", self._d_WordOut)
		self._d_PartOfSpeechOut = OpenRTM_aist.instantiateDataType(RTC.TimedWStringSeq)
		"""
		"""
		self._PartOfSpeechOutOut = OpenRTM_aist.OutPort("PartOfSpeechOut", self._d_PartOfSpeechOut)





		# initialize of configuration-data.
		# <rtc-template block="init_conf_param">

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


		time.sleep(1)

		
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
	

		if self._TextInIn.isNew(): #新しいデータが来たか確認
			self._d_TextIn = self._TextInIn.read() #値を読み込む
			textlist = self._d_TextIn.data

			#形態素解析
			for text in textlist:
				tagger = MeCab.Tagger()
				result =tagger.parse(text).split()
				num = len(result)
				
				
				wordlist = []
				wordlist_out = []
				partlist = []
				partlist_out = []


				#単語を取得↓
				for wordnum in range(0,num,2):
					wordlist.append(result[wordnum])
					
				print(wordlist)
				
				
				#品詞を取得↓
				for partnunm in range(1,num,2):
					partlist.append(result[partnunm])
				
					
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




def morphological_analysisInit(manager):
    profile = OpenRTM_aist.Properties(defaults_str=morphological_analysis_spec)
    manager.registerFactory(profile,
                            morphological_analysis,
                            OpenRTM_aist.Delete)

def MyModuleInit(manager):
    morphological_analysisInit(manager)

    # Create a component
    comp = manager.createComponent("morphological_analysis")

def main():
	mgr = OpenRTM_aist.Manager.init(sys.argv)
	mgr.setModuleInitProc(MyModuleInit)
	mgr.activateManager()
	mgr.runManager()

if __name__ == "__main__":
	main()

