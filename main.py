import json

import requests
import azure.cognitiveservices.speech as speechsdk

from azure.cognitiveservices.speech.audio import AudioOutputConfig

speech_key, service_region = "6d5afa14828c469e8a75d8801db8e408", "chinanorth2"
speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region,
                                       speech_recognition_language="zh-cn")


def record():
	# Creates a recognizer with the given settings
	speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config)

	print("Say something...")
	result = speech_recognizer.recognize_once()

	# Checks result.
	if result.reason == speechsdk.ResultReason.RecognizedSpeech:
		print("Recognized: {}".format(result.text))
	elif result.reason == speechsdk.ResultReason.NoMatch:
		print("No speech could be recognized: {}".format(result.no_match_details))
	elif result.reason == speechsdk.ResultReason.Canceled:
		cancellation_details = result.cancellation_details
		print("Speech Recognition canceled: {}".format(cancellation_details.reason))
		if cancellation_details.reason == speechsdk.CancellationReason.Error:
			print("Error details: {}".format(cancellation_details.error_details))

	return result.text


def chat(text_words=""):
	api_key = "1dde879fa943438e9af1ee88269f3852"
	api_url = "http://openapi.tuling123.com/openapi/api/v2"
	headers = {"Content-Type": "application/json;charset=UTF-8"}

	req = {
		"reqType": 0,
		"perception": {
			"inputText": {
				"text": text_words
			},
			"selfInfo": {
				"location": {
					"city": "天津",
					"province": "天津",
					"street": "天津科技大学"
				}
			}
		},
		"userInfo": {
			"apiKey": api_key,
			"userId": "Alex"
		}
	}

	req["perception"]["inputText"]["text"] = text_words
	response = requests.request("post", api_url, json=req, headers=headers)
	response_dict = json.loads(response.text)

	result = response_dict["results"][0]["values"]["text"]
	print("AI Robot said: " + result)
	return result


def speak(text_words):
	speech_config.speech_synthesis_language = "zh-cn"
	audio_config = AudioOutputConfig(use_default_speaker=True)
	speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)

	result = speech_synthesizer.speak_text_async(text_words).get()

	# Checks result.
	if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
		print("Speech synthesized to speaker for text [{}]".format(text_words))
	elif result.reason == speechsdk.ResultReason.Canceled:
		cancellation_details = result.cancellation_details
		print("Speech synthesis canceled: {}".format(cancellation_details.reason))
		if cancellation_details.reason == speechsdk.CancellationReason.Error:
			if cancellation_details.error_details:
				print("Error details: {}".format(cancellation_details.error_details))
		print("Did you update the subscription info?")


if __name__ == '__main__':
	while True:
		text = record()
		if "退出" in text:
			break
		res = chat(text)
		speak(res)
