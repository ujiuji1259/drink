"""Extract hashtag from some keywords

example:
    model = NER('keywords.json')
    res = model.ner('体がだるい')

input_file_format:
    json (dict): {keyword: hashtag}

output format:
    [hashtag, ...]

"""

import re
import numpy as np
import json

class NER(object):
    def __init__(self, path):
        self._load_keywords(path)
        self.keywords = list(self.dtoc.keys())

    def ner(self, text):
        # TODO: キーワード数多くなったときはtrieに変える
        res = []
        for cnt in range(len(text)):
            for keyword in self.keywords:
                m = re.match(keyword, text[cnt:])
                if m is not None:
                    res.append((cnt, cnt+len(keyword), self.dtoc[keyword]))

        results = self.select_ne(len(text), res)

        return results

    def select_ne(self, num, words):
        is_used = np.zeros(num)
        words = sorted(words)
        results = []
        for i, j, keyword in words:
            if np.sum(is_used[i:j+1]) > 0:
                continue
            results.append(keyword)
            is_used[i:j+1] = 1

        return list(set(results))

    def _load_keywords(self, path):
        with open(path, 'r') as f:
            self.dtoc = json.load(f)


if __name__ == '__main__':
    model = NER('keywords.json')
    texts = ['手足の指などのこわばり、ホットフラッシュなど',
            'ホルモン剤の影響ですごい脱水症状で暑い',
            '発熱',
            '体を使う作業でも、考え事など集中力を要することでも、何をしていてもすぐに疲れてしまう。休んでも疲れが取れにくい。さらに忘れっぽくなる。']
    for text in texts:
        res = model.ner(text)
        print(res)

