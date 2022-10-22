# 感情分析を用いたSNSフィルターシステムの開発
## 概要

本システムはtwitterAPI,BERT,MeCab等を利用してSNSフィルターシステムを実現するコンポーネント群によって構成されています。  

## マニュアル
[マニュアル](https://github.com/tbou30897/OpenRTM_SNS_filter_system/tree/main/Documents/Manual.pdf)
## 開発環境
言語：Python  
OS：Windows10  
RTミドルウェア：OpenRTM-aist-2.0.0
## 開発コンポーネント
### twitter_api（twitteAPIコンポーネント）  
twitterAPIを利用してtwitterからスクレイピングを行うコンポーネント
### morphological_analysis（形態素解析コンポーネント）
MeCabを利用して形態素解析を行うコンポーネント
### restricted_word（誹謗中傷伏字化コンポーネント）
規制単語リスト、形態素解析結果をもとに、ニュアンスを含めた誹謗中傷の伏せ字化を行うコンポーネント
### sentiment_analysis（感情分析コンポーネント）
BERTを利用して、感情分析（positive、negativeを-1~1の数値で出力）するコンポーネント
### result_out（結果出力コンポーネント）
送られてきたデータを受信して、結果出力を行うコンポーネント

## 動画
https://youtu.be/4y4wfGtY-S4
