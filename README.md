# AlgoTrading101 Warren Buffett ChatGPT

[Build a Warren Buffett Chatbot using OpenAI’s API
](https://algotrading101.com/learn/warren-buffett-chatbot-chatgpt-openai/)

## Introduction

This is the code used for an AlgoTrading101 article that showcases how to create
a chatbot by fine-tuning a ChatGPT model on Warren Buffett's video transcripts.

It showcases how to perform transcription and diarization and the article will be
linked here once it is published.

## Table of contents

<ol>
<li><a href="https://algotrading101.com/learn/warren-buffett-chatbot-chatgpt-openai/#how-to-build-warren-buffett-chatbot">How to build a Warren Buffett Chatbot</a></li>
<li><a href="https://algotrading101.com/learn/warren-buffett-chatbot-chatgpt-openai/#what-is-openai">What is OpenAI?</a></li>
<li><a href="https://algotrading101.com/learn/warren-buffett-chatbot-chatgpt-openai/#what-is-chatgpt">What is ChatGPT?</a></li>
<li><a href="https://algotrading101.com/learn/warren-buffett-chatbot-chatgpt-openai/#what-is-whisper">What is Whisper?</a></li>
<li><a href="https://algotrading101.com/learn/warren-buffett-chatbot-chatgpt-openai/#what-is-stable-whisper">What is StableWhisper?</a></li>
<li><a href="https://algotrading101.com/learn/warren-buffett-chatbot-chatgpt-openai/#getting-started">Getting started</a></li>
<li><a href="https://algotrading101.com/learn/warren-buffett-chatbot-chatgpt-openai/#what-is-diarization">What is Diarization?</a></li>
<li><a href="https://algotrading101.com/learn/warren-buffett-chatbot-chatgpt-openai/#perform-diarization-and-transcription">How to perform diarization and transcription with Whisper?</a>
<ul>
<li><a href="https://algotrading101.com/learn/warren-buffett-chatbot-chatgpt-openai/#pre-requisites">Installing pre-requisites</a></li>
<li><a href="https://algotrading101.com/learn/warren-buffett-chatbot-chatgpt-openai/#transcription-and-diarization">Transcription and diarization</a></li>
<li><a href="https://algotrading101.com/learn/warren-buffett-chatbot-chatgpt-openai/#cleaning-videos-and-transcripts">Cleaning videos and transcripts</a></li>
</ul>
</li>
<li><a href="https://algotrading101.com/learn/warren-buffett-chatbot-chatgpt-openai/#what-is-fine-tuning">What is fine-tuning?</a></li>
<li><a href="https://algotrading101.com/learn/warren-buffett-chatbot-chatgpt-openai/#chatgpt-fine-tuning">How to organize the data for ChatGPT finetuning?</a></li>
<li><a href="https://algotrading101.com/learn/warren-buffett-chatbot-chatgpt-openai/#fine-tune-chatgpt">How to fine-tune ChatGPT on your own data?</a></li>
<li><a href="https://algotrading101.com/learn/warren-buffett-chatbot-chatgpt-openai/#chat-with-warren-buffet-chatgpt">How to chat with Warren Buffett using ChatGPT?</a></li>
<li><a href="https://algotrading101.com/learn/warren-buffett-chatbot-chatgpt-openai/#thoughts-and-ideas">My thoughts and ideas</a></li>
<li><a href="https://algotrading101.com/learn/warren-buffett-chatbot-chatgpt-openai/#full-code">Full code</a></li>
</ol>

----------
## Info

| Author | Igor Radovanovic
--- | ---
| Published | November 15, 2023
