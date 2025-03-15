from openai import OpenAI
client = OpenAI(api_key="ollama",
                base_url="http://196.21.5.218:11434/v1/",
                )

# openai_model = "qwen2.5:14b"
openai_model = "phi4:latest"
# openai_model = "deepseek-r1:32b"


def ai_diff(diff_config):
    response = client.chat.completions.create(
        model=openai_model,
        temperature=0,
        messages=[
            {"role": "system", "content": "你是思科设备配置变更分析机器人！你能识别配置的变更，并且对变更进行专业解释！"
                                          "更进一步能够对这些变更对网络的影响给出专业的介绍, "
                                          "尽量简短!突出重点!列出每一个变更点,并且给出最多100字的变更描述!"
                                          "不必提及未变更的内容!"
                                          "注意: 有些内容只是上下文, 并不是变更,不要当变更来评价!只关注变更部分!"
                                          "注意: 如果配置没有变化, 忽略行号的变化!忽略行号的变化!忽略行号的变化!"
                                          "注意: 使用中文回答问题 "
                                          "注意: 使用html标签来体现格式, 使用<h4>表明变更点标题, 使用<p>来表示变更点内容, "
                                          "使用<pre>来表示代码块, 使用<code>来表示代码片段, 使用<em>来表示强调, "
                                          "使用<strong>来表示加粗, 使用<ul>来表示无序列表, 使用<ol>来表示有序列表, "
                                          "使用<li>来表示列表项, 使用<a>来表示链接,使用<div>来表示块级元素, 使用<span>来表示行内"
             },

            {"role": "user", "content": f'变化配置: {diff_config}'},
        ]
    )

    return response.choices[0].message.content

