import json

class Classifier(object):
    def __init__(self, keywords):
        self.keywords = keywords

    def classify(self, text):
        """
        input:  "ずっと禁酒していて体調が良いし，お金も貯まるようになった"
        output: ["体調", "お金"]
        """

        res = []

        for k, v in self.keywords.items():
            if isClass(text, v):
                res.append(k)

        return res

def isClass(text, keywords):
    counts = [text.count(k) for k in keywords]
    return max(counts) != 0

if __name__ == "__main__":
    print(isClass("はなたれ小僧", ["はな", "いええい"]))
    hashtag = {}
    hashtag["飲みたい"] = ["飲みたい", '飲みたくなる', '誘惑']
    hashtag["飲みません"] = ["飲みません"]
    hashtag["飲禁"] = ["飲みたい", '飲みたくなる', '誘惑']
    hashtag["飲みたい"] = ["飲みたい", '飲みたくなる', '誘惑']
    hashtag["飲みたい"] = ["飲みたい", '飲みたくなる', '誘惑']
    hashtag["飲みたい"] = ["飲みたい", '飲みたくなる', '誘惑']
    hashtag["飲みたい"] = ["飲みたい", '飲みたくなる', '誘惑']
    hashtag["飲みたい"] = ["飲みたい", '飲みたくなる', '誘惑']
    hashtag["飲みたい"] = ["飲みたい", '飲みたくなる', '誘惑']
    hashtag["飲みたい"] = ["飲みたい", '飲みたくなる', '誘惑']
    with open("hashtag_keywords.json", "w") as f:
        json.dump(hashtag, f, ensure_ascii=False)
