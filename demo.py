import logging
from sklearn.feature_extraction.text import TfidfVectorizer
import pickle
import datetime
from flask import Flask, render_template, request, url_for, redirect, Markup
from flask_login import login_user, logout_user, login_required, LoginManager, UserMixin, current_user
import json
from classification_rule import Classifier
from ner_rule import NER
from draw_calendar import draw_calendar
import json
from datetime import datetime as dt
from find_similar_episode import Episodes, space_split
from data_structure import UserInformation, Buffer

tmp_buffer = Buffer()
user_instances = {}

USER_FILE_PATH = './users/'
DRINK_FILE_PATH = './drink_num/'
DRINK_CHART_PATH = './drink_chart/'
USER_PICKLE_FILE_PATH = './users_pkl/'
liqueur = {'beer':14, 'syo':22, 'wine':12, 'highball':22, 'jap':22, 'other':15}
liqueur_to_word = {'beer':'ビール（350ml）', 'syo':'焼酎（水割り 180ml）', 'wine':'ワイン（グラス 120ml）', 'highball':'ハイボール（350ml）', 'other':'その他', 'jap':'日本酒（1合）'}
date = {}


def space_split(s):
    return s.split(' ')

with open('similar_fix.txt', 'r') as f:
    similar_episode = []
    for line in f:
        line = line.rstrip()
        if not line:
            continue

        similar_episode.append(line)

with open('episode_tfidf.pkl', 'rb') as f:
    model = pickle.load(f)

episode = Episodes(similar_episode, model)


class User(UserMixin):
    def __init__(self, id, name, password):
        super().__init__()
        self.id = id
        self.name = name
        self.password = password

    def is_authenticated(self):
        return True

    def is_active(self):
        return self.active

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id


LOGFILE = "./drink.log"

app = Flask(__name__, template_folder="./")
app.logger.setLevel(logging.DEBUG)
app.config.from_pyfile("conf/app.conf")
app.config['SECRET_KEY'] = "secret"
fh = logging.FileHandler(LOGFILE)
fh.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
app.logger.addHandler(fh)

login_manager = LoginManager()
login_manager.init_app(app)

with open("hashtag_keywords.json", "r") as f:
    keywords = json.load(f)
with open("ner_keywords.json", "r") as f:
    dic = json.load(f)

tag2value = {"DN":"bg-primary", "M":"bg-info", "DP":"bg-danger"}

lv1 = ['飲みたい', '飲みません', '禁酒', '我慢', 'ストレス', 'ビール', '酒', 'シャンパン', 'チューハイ', 'アルコール',
        '代替飲料', '体調', '調子', 'よくない', '胃', '肝臓', '血圧', '数値', '運動', '食事', '晩酌', '食欲', '睡眠', '運動',
        '車', 'お金', '家族', 'つきあい', '乗り越えた', '乗り切った', '良好', '改善', '成功', 'お酒を買わない', '気分転換',
        'できない', 'うらやましい', '口寂しい', 'もの足りない', '寂しい', '二日酔い', '倦怠感', 'アルコール依存', '相談']

lv2 = ['飲んでしまった', '飲み始めた', '無理だった', 'やめられない', 'つらい', 'つらかった', '眠れない', 'イライラ', 'モヤモヤ',
        '集中できない', '落ち着かない', '自己嫌悪', '葛藤', '負けそう', '負けた', '不機嫌', '泣きそう', '憂鬱', '不安',
        '引きこもり', '頭痛', '吐き気', '下痢', '体重', '体調が悪い', '悪化', '異常', '量が増える']

lv3 = ['症状', '痛い', '血便']
hashtag2value = {}

for l, lv in [(lv1,0), (lv2,1), (lv3,2)]:
    for token in l:
        hashtag2value[token] = lv


"""
hashtag2value = {"体調":0, "病気":1, "健康診断":2, "健康":2, 
        "肝臓":3, "胃":3, "アルコール依存症":4, "ストレス":5,
        "お金":6, "酔っ払って":4, "二日酔い":4, "人間関係":7,
        "妊娠":8, "ダイエット":9, "親の介護":10, "運転":11,
        "時間":12, "体調が良くなった":2, "快眠":2, "すっきり":2,
        "体重が落ちた":4, "運動":3, "数値が良くなった":2,
        "人間関係":5, "失敗がなくなった":6, "食事がおいしい":7, 
        "食生活":10, "気持ちが前向きになった":9, "自信が持てた":8,
        "気分転換":11, "つきあい":12, "飲めない":2, "飲みたい":2,
        "挫折":6, "つらい":5, "うらやましい":4, "イライラ":3,
        "眠れない":7, "習慣":8, "体調が悪い":9, "禁断症状":10,
        "食事":6, "口寂しい":5, "お酒を買わない":2, 
        "気持ちの切り替え":3, "体調管理":4, "ノンアルコール":2, 
        "炭酸水":2, "ソフトドリンク":2, "炭酸飲料":2,
        "お茶":3, "早く寝る":4, "家族":5, "体調が良くなった":6,
        "我慢":10}
"""

id2color = {0:"badge-blue", 1:"badge-yellow", 2:"badge-red", 3:"badge-navy",
        4:"badge-teal", 5:"badge-green", 6:"badge-lime", 7:"badge-aqua", 8:"badge-yellow",
        9:"badge-red", 10:"badge-fuchsia", 11:"badge-olive", 12:"badge-purple",
        13:"badge-maroon"}

classifier = Classifier(keywords)
ner = NER(dic, tag2value)

users = {0: User(0, 'sociocom', 'social405'), 1: User(1, 'sociocom2', 'social405'), 2: User(2, '関西医科大学', 'KMU'), 3: User(3, '荒牧', 'aramaki'), 4: User(4, 'admin', 'admin'), 5: User(5, 'yamashiki', 'yamashiki-lmu'), 6: User(6, 'ikeda', 'ikeda-kmu'), 7: User(7, 'ito', 'ito'), 8: User(8, 'yoshii', 'yoshii-kmu')}
name2id = {'sociocom':0, 'sociocom2':1, '関西医科大学':2, '荒牧':3, 'admin':4, 'yamashiki':5, 'ikeda':6, 'ito':7, 'yoshii':8}
#user_information = {'sociocom':{'2020-06-12':{'hashtag':[], 'ne':[], 'text':''}}}
user_information = {}
drink_information = {}
drink_chart_data = {}
add_keys = set(["extendedProps", "backgroundColor", "rendering"])


def transform_for_calendar(drink_dict):
    save_data = []
    for key, value in drink_dict.items():
        tmp = {"start":key}
        for k, v in value.items():
            if k in add_keys:
                tmp[k] = v

        save_data.append(tmp)

    return json.dumps(save_data)


# user
@login_manager.user_loader
def load_user(user_id):
    return users.get(user_id)


@app.route('/admin', methods=["POST", "GET"])
def admin():
    if current_user.name != 'admin':
        return render_template('index.html', name=current_user.name, prefix=prefix)

    if request.method == "GET":
        users = list(name2id.keys())
        return render_template('admin_top.html', usernames=users)
    else:
        name = request.form["username"]
        """
        load_user_data(user_information, USER_FILE_PATH, name)
        data = user_information[name]

        load_user_data(drink_chart_data, DRINK_CHART_PATH, name)
        drink_data = drink_chart_data[name]
        """
        if name in user_instances:
            user_instances[name].load_file()
        else:
            user_instances[name] = UserInformation(name, USER_PICKLE_FILE_PATH, DRINK_FILE_PATH, DRINK_CHART_PATH)
            user_instances[name].load_file()

        instance = user_instances[name]
        data = instance.get_user_format()
        drink_data = instance.get_chart_format()
        return render_template('admin.html', data=data, drink_data=drink_data, username=name, prefix=prefix)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/login', methods=["GET", "POST"])
def login():
    modal = "false"
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        userid = name2id[username] if username in name2id else ""

        if (userid in users
                and password == users[userid].password):

            login_user(users[userid])

            return redirect(url_for('top_page'))

        modal = "true"
    
    return render_template('login.html', modal=modal, prefix=prefix)


@app.route('/')
def top_page():
    if current_user.is_authenticated:

        if current_user.name in user_instances:
            user_instances[current_user.name].load_file()
        else:
            user_instances[current_user.name] = UserInformation(current_user.name, USER_PICKLE_FILE_PATH, DRINK_FILE_PATH, DRINK_CHART_PATH)
            user_instances[current_user.name].load_file()

        date_list = list(user_instances[current_user.name].input_dict.keys())

        return render_template('index.html', name=current_user.name, date_list=date_list, prefix=prefix)
    else:
        return redirect(url_for('login', modal="false"))


@app.route('/diary/<target_date>', methods=["GET"])
def diary(target_date):
    instance = user_instances[current_user.name].load_instance(target_date)
    if instance is not None:
        return redirect(url_for("top_page"))

    tmp_buffer.add_buffer(current_user.name, target_date, instance)
    bu = tmp_buffer.get_instance(current_user.name)

    initial_value = {}
    for k in liqueur.keys():
        if k in bu.alc_dict:
            initial_value[k] = str(bu.alc_dict[k])
        else:
            initial_value[k] = str(0)

    initial_value['other_re'] = bu.other
    initial_value['text'] = bu.text

    return render_template('diary.html', data=initial_value)

@app.route('/past_data/<target_date>', methods=["GET"])
def past_data(target_date):
    instance = user_instances[current_user.name].load_instance(target_date)
    if instance is None:
        return redirect(url_for("top_page"))

    tmp_buffer.add_buffer(current_user.name, target_date, instance)
    bu = tmp_buffer.get_instance(current_user.name)

    alc = []
    for k in liqueur.keys():
        if k in bu.alc_dict:
            alc.append((liqueur_to_word[k], str(bu.alc_dict[k])))
        else:
            alc.append((liqueur_to_word[k], str(0)))

    other = bu.other
    text = bu.text
    y, m, d = target_date.split('-')
    if m[0] == "0":
        m = m[1:]
    if d[0] == "0":
        d = d[1:]
    target_date = m + '月' + d + "日"
    return render_template('past_data.html', alc=alc, other=other, text=text, date=target_date)

@app.route('/data')
def return_data():
    try:
        fn = DRINK_FILE_PATH + current_user.name + '.json'
        with open(fn, 'r') as f:
            data = json.load(f)
            data = transform_for_calendar(data)
        return data
    except:
        return json.dumps([])


@app.route('/drink', methods=["POST", "GET"])
def drink():
    if request.method == "POST":
        drink = request.form.getlist("checkbox")
        other_re = request.form.get("other_re")
        reason = request.form.get("drink")
        reason = reason if reason else ""

        #dt_now = date[current_user.name]
        liq_num = {w:int(request.form.get(w)) for w in liqueur.keys()}
        #color, alc, liq_num = calc_alc(request.form)

        instance = tmp_buffer.get_instance(current_user.name)
        instance.set_text(reason)
        instance.set_alc_dict(liq_num)
        instance.set_other(other_re)

        user_instances[current_user.name].save_instance(instance)
        user_instances[current_user.name].save_file()

        return redirect(url_for("analysis", text=reason))

    return render_template("drink.html")

@app.route('/nondrink', methods=["POST", "GET"])
def nondrink():
    if request.method == "POST":
        reason = request.form.get("nondrink")
        reason = reason if reason else "None"
        #dt_now = date[current_user.name]

        instance = tmp_buffer.get_instance(current_user.name)
        instance.set_text(reason)
        instance.set_alc_dict({'beer':0, 'syo':0, 'wine':0, 'highball':0, 'other':0, 'jap':0, 'other':0})
        

        return redirect(url_for("analysis", text=reason))
    return render_template("nondrink.html")


@app.route('/analysis/<text>')
def analysis(text):
    e = episode.find_similar_episode([text], 10)[0][0]
    annotated, nes = ner.add_tag(text)
    annotated = Markup(annotated)
    tags = classifier.classify(text)
    tags = [(id2color[hashtag2value[t]], t) for t in tags]

    #add_user_information(tags, nes, text)

    instance = tmp_buffer.get_instance(current_user.name)
    instance.set_tags(tags)
    instance.set_nes(nes)

    nes = [('red', w) for w in nes]

    return render_template("analysis.html", text=annotated, tags=tags+nes, raw_text=text, episode=e)


@app.route('/save')
def save():
    instance = tmp_buffer.get_instance(current_user.name)
    user_instances[current_user.name].save_instance(instance)
    user_instances[current_user.name].save_file()

    return redirect(url_for('top_page'))

if __name__ == "__main__":
    prefix = ''
    if app.config['ENV'] == 'production':
        prefix = '/drink'
    app.run(port="8006", host="0.0.0.0", debug=True)

