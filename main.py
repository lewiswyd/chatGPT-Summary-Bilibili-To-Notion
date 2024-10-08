from bili_subtitle_downloader import BiliSubtitleDownloader
from bili_video_info_downloader import VideoInfoDownloader
#from chatgpt_summary_writer import ChatGPTSummaryWriter
#from notion_controller import NotionController
import argparse
import os
from flask import Flask, request, jsonify
import logging


class NoArgsError:
    pass


def read_command_line_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--bv", help="获取bv号")
    parser.add_argument("-p", help="分p，默认为0")
    parser.add_argument("--summary_count", help="需要的精简概括的数量（默认为10条）")
    args = parser.parse_args()
    return (args.bv, args.p, args.summary_count)


app = Flask(__name__)
app.logger.setLevel(logging.DEBUG)  # 设置日志级别

@app.route('/getBiliSubtitle', methods=['GET'])
def your_function():
    # 假设你的函数需要一个名为"param"的参数
    bv_id = request.args.get('bv', type=str)  # 获取URL参数，默认值为1

    cookie = None
    if os.path.isfile("./cookie"):
        with open("./cookie", "r") as f:
            cookie = f.read()

    #bv_id = 'BV14G1RYpErj'
    response_data = {"bv_id": [], "视频信息": {}, "字幕信息": []}

    print(f"开始处理：{bv_id}")
    response_data["bv_id"].append(f"开始处理：{bv_id}")
    video_info = VideoInfoDownloader(bv_id, cookie).download_video_info()
    p_infos = video_info["info"]["pages"]
    title = video_info["info"]["title"]
    print(f"获取到视频信息：{title}")
    response_data["视频信息"] = {"标题": title, "分P信息": []}

    p_num = 0
    while p_num < len(p_infos):
        p_info = p_infos[p_num]['part']
        print(f"分p{p_num+1}: {p_info}")
        subtitle = BiliSubtitleDownloader(bv_id, p_num, cookie).download_subtitle()
        print(subtitle)
        response_data["字幕信息"].append({"分P": p_num+1, "字幕": subtitle})
        p_num += 1
    return jsonify(response_data)
    #print("字幕获取成功，chatGPT开始编写摘要")

    #summary = ChatGPTSummaryWriter(api_key, subtitle, summary_count).write_summary()
    #print("chatGPT编写摘要成功")
    #NotionController(notion_token, database_id).insert_to_notion(video_info, summary)
    #print("导入Notion成功")

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
