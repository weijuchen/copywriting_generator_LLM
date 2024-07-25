from langchain.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_community.tools import WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper
import os
import opencc

title_template = ChatPromptTemplate.from_messages(
        [
            ("human", "請為'{subject}'這個主題的影片，想出一個引人注目及激發用戶情緒的標題")
        ]
    )
# print(title_template)

copywriting_template = ChatPromptTemplate.from_messages(
    [
        ("human",
         """你是一個youtuber，以製作短影音為主，請依據以下標題和內容，完成一個短影音文本，
         影片標題:{title},
         影片長度:{duration}分鐘，
         製作的文本長度請盡可能的遵守影片長度的要求。
         腳本格式請依照[開頭、中間、結尾]做區隔，開頭希望能抓住吸引力，中間提供實用的技巧、經驗、方法等，
         結尾要給使用者驚喜感，整體內容的表示方式要可以吸引年輕人且輕鬆有趣。

         """)
    ]
)
copywriting_template = ChatPromptTemplate.from_messages(
    [
        ("human",
         """你是一個youtuber，以製作短影音為主，請依據以下標題和內容，完成一個短影音文本，
         影片標題:{title},
         影片長度:{duration}分鐘，
         製作的文本長度請盡可能的遵守影片長度的要求。
         腳本格式請依照[開頭、中間、結尾]做區隔，開頭希望能抓住吸引力，請從以下9種方式，任選用其中一種，
         但不用寫出使用哪種方式，


         1. 好奇類鉤子：用得不到、沒體驗過的事物激發好奇心
            OO 是一種什麼體驗
例如：不用上班是一種什麼體驗？
如何不 OO 也能 OO
例如：如何不花錢也能到處旅行？
2. 借勢類鉤子：借用名人、權威者的影響力

OO 都愛用的 OO
例如：IU 李知恩都愛用的保養品
3. 痛點類鉤子：痛點不解決會難受，戳得越痛效果越好
為什麼你 OO 卻 OO
例如：為什麼你這麼努力卻還是交不到女朋友？
你總是在 OO 時 OO 嗎？
例如：你總是在上台時腦袋一片空白嗎？
4. 引導式鉤子：引導受眾發現他自己的期望
想要找回 OO 嗎？
例如：想要找回年輕水潤的肌膚嗎？
5. 恐嚇類鉤子：起到警示作用，引起危機感
如果你再不 OO 就會 OO
例如：如果你再不學習就會被 AI 取代了
6. 反差類鉤子：利用前後對比形成反差
為什麼 OO 卻 OO
例如：為什麼你很努力卻總是失敗？
7. 利益類鉤子：利用人性、想佔便宜的心理
分享一個 OO 的小技巧
例如：分享一個月賺 3 萬的小技巧

8. 「提問法」鉤子：提出問題，引發觀眾的思考和好奇心
例如：如果你有 1000 萬你會幹嘛？你會拿去投資房地產嗎？還是拿去實現夢想？

9. 「故事引入法」鉤子：說故事來引起觀眾注意
例如：我小時候想要自己開一間遊戲公司，然後擁有這遊戲裡面所有的資源……

         中間提供實用的技巧、經驗、方法等，但重點應該專注傳達一個特定訊息或故事就好，

         結尾要給使用者驚喜感，
         ，重點在呼籲觀眾做出按讚、訂閱、分享、留言等行動，你可以結合短影音「鉤子」來吸引觀眾做出行動，或者使用以下幾個 CTA 技巧：

1. 提供好處
提供觀眾好處是最直接有效的方式，例如：留言領取懶人包、電子書

2. 創造急迫性
你可以用一些強力字詞像是：立刻、立即、馬上、現在、快速、現即、即刻、速速、立馬、今天就……等，後面加上你希望觀眾做的動作，例如：現在就訂閱！

3. 創造危機感
告知觀眾不採取按讚、訂閱、分享、留言等行動的風險，例如：如果你不按讚收藏這部影片，你很可能會錯過一個輕鬆賺錢的機會！
4. 激發熱情
根據你的短影音內容來激發觀眾的積極情緒，例如：你的短影音教觀眾怎麼摺造型氣球，那你的 CTA 可以寫說：「馬上按讚收藏這部影片，今天回家就給她一個驚喜！」
         整體內容的表示方式要可以吸引年輕人且輕鬆有趣。

         """)
    ]
)


def copywriting_generator(subject, video_length, creativity, api_key):
    model = ChatOpenAI(openai_api_key=api_key, temperature=creativity)

    title_chain = title_template | model
    copywriting_chain = copywriting_template | model

    title = title_chain.invoke({"subject": subject}).content

    # search = WikipediaAPIWrapper(lang="en")
    search = WikipediaAPIWrapper(lang="zh-tw")
    # search_result = search.run(subject, url="https://zh.wikipedia.org/zh-tw/" + subject)

    search_result = search.run(subject)

    converter = opencc.OpenCC('s2t')
    search_result = converter.convert(search_result)

    copywriting = copywriting_chain.invoke({"title": title, "duration": video_length,
                                  "wikipedia_search": search_result}).content

    # copywriting = copywriting_chain.invoke({"title": title, "duration": video_length}).content

    return search_result, title, copywriting
    # return title, copywriting


# print(copywriting_generator("個人理財", 1, 0.7, os.getenv("OPENAI_API_KEY")))