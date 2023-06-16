# -*- encoding: utf-8 -*-
#
#Time    :   2023/05/11 14:23:40
#Author  :   zbchu 
# ==============================================================================
"""部署用户评论主题提取服务"""

from flask import Flask,request
import openai

app = Flask(__name__)

@app.route('/topic',methods = ['POST'])
def mess():  # put application's code here
    user_review = request.json.get('msg')
    prompt = f"""\
Identify the following items from the review text: 
- Sentiment (positive or negative or neutral)
- Topics that are being discussed
- List of key phrase for each topic

The review is delimited with triple backticks. \
Format your response as a JSON object with \
"Sentiment", "Topics" as the keys, Topics value \
is a JSON object with each topic as the keys, each \
topic value is List of it's key phrase
If the information isn't present, use "unknown" \
as the value.
Make your response as short as possible.

Review text: ```{user_review}```
"""
    openai.api_key = "sk-xxxxx"
    messages = [{"role": "user", "content": prompt}]
    try:
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-0301",
            temperature=0,
            messages=messages
            )

        res = {
                "resmsg": completion,
                "code": 200
            }
    except:
        res = {"code": 201}
    return res