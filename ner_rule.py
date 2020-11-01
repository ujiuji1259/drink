import json
import re
import heapq

def specify_char_tag(text_len, spans):
    tags = {i:'O' for i in range(text_len)}
    while spans:
        p = heapq.heappop(spans)
        if all(tags[i] == 'O' for i in range(p[1], p[2])):
            for idx in range(p[1], p[2]):
                if idx == p[1]:
                    tags[idx] = "B-" + p[3]
                else:
                    tags[idx] = "I-" + p[3]

    return tags

def is_chunk_start(prev_tag, tag):
    if prev_tag == "O":
        prev_iob = "O"
        prev_char_tag = ""
    else:
        prev_iob, prev_char_tag = prev_tag.split('-')

    if tag == "O":
        iob = "O"
        char_tag = ""
    else:
        iob, char_tag = tag.split('-')

    return prev_char_tag != char_tag and iob != "O"

def is_chunk_end(tag, post_tag):
    if post_tag == "O":
        post_iob = "O"
        post_char_tag = ""
    else:
        post_iob, post_char_tag = post_tag.split('-')

    if tag == "O":
        iob = "O"
        char_tag = ""
    else:
        iob, char_tag = tag.split('-')

    return post_char_tag != char_tag and iob != "O"

def convert_tags_to_html(text, tags, tag2value):
    """
    text:   "ノンアルコールビール"
    tags:   {0:"O"....}

    return: "<span value="">ノンアルコールビール</span>"
    """

    output = ""
    for idx in range(len(text)):
        pre_tag = "O" if idx == 0 else tags[idx-1]
        post_tag = "O" if idx == len(text) - 1 else tags[idx+1]

        if is_chunk_start(pre_tag, tags[idx]):
            output += '<span class="' + tag2value[tags[idx].split('-')[-1]] + '">'

        output += text[idx]

        if is_chunk_end(tags[idx], post_tag):
            output += '</span>'

    return output


class NER(object):
    def __init__(self, keywords, colors, path):
        """
        keywords:   {"DP": [""] ...}
        colors:     {"DP":"priority" ..}
        """
        self.keywords = keywords
        self.colors = colors

        self._load_keywords(path)

    def add_hashtag(self, text):
        """
        input:  "ノンアルコールビールを飲んで，ビールを我慢する"
        output: "<span>ノンアルコールビール</span>を飲んで，<span>ビール</span>を我慢する"
        """
        spans = []
        words = []
        for v in self.dtoc.keys():
            iters = re.finditer("(" + "|".join(v) + ")", text)
            for ite in iters:
                s_pos, e_pos = ite.start(), ite.end()
                words.append(ite.groups()[0])
                heapq.heappush(spans, (s_pos - e_pos, s_pos, e_pos, self.dtoc[words[-1]]))

        tags = specify_char_tag(len(text), spans)
        html = convert_tags_to_html(text, tags, self.colors)
        return html, words

    def add_tag(self, text):
        """
        input:  "ノンアルコールビールを飲んで，ビールを我慢する"
        output: "<span>ノンアルコールビール</span>を飲んで，<span>ビール</span>を我慢する"
        """
        spans = []
        words = []
        for k, v in self.keywords.items():
            iters = re.finditer("(" + "|".join(v) + ")", text)
            for ite in iters:
                s_pos, e_pos = ite.start(), ite.end()
                heapq.heappush(spans, (s_pos - e_pos, s_pos, e_pos, k))
                words.append(ite.groups()[0])

        tags = specify_char_tag(len(text), spans)
        html = convert_tags_to_html(text, tags, self.colors)
        return html, words

    def _load_keywords(self, path):
        with open(path, 'r') as f:
            self.dtoc = json.load(f)

if __name__ == "__main__":
    dic = {}
    dic["DN"] = ["ワイン", "ビール", "チューハイ", "お酒", "アルコール", "焼酎", 
            "泡盛", "ウオッカ", "ウイスキー", "シャンパン", "甘酒"]
    
    dic["M"] = ["こらえて", "我慢", "つらい", "つらかった", "イライラ", "辛かった",
            "荒れた", "優しい", "穏やか", "落ち着きがなくなって", "物足りなかった",
            "もの足りなかった", "口がさびしかった", "耐えよう", "葛藤"]

    dic["DP"] = ["紅茶", "お茶", "ソフトドリンク", "炭酸水", "ノンアルコールビール"]

    tag2value = {"DN":"bg-primary", "M":"bg-info", "DP":"bg-danger"}

    with open("ner_keywords.json", "w") as f:
        json.dump(dic, f, ensure_ascii=False)

    model = NER(dic, tag2value)
    word = "ノンアルコールビールと炭酸水"
    print(model.add_tag(word))
