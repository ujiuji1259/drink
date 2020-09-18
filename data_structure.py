import copy
from pathlib import Path
import json
import pickle

class InputInstance(object):
    def __init__(self, date):
        self.date = date
        self.text = ""
        self.other = ""
        self.alc_dict = {}
        self.tags = []
        self.nes = []
        self.image_url = ""

        self.liqueur = {'beer':14, 'syo':22, 'wine':12, 'highball':22, 'other':12, 'jap':22, 'other':15}

    def set_text(self, text):
        self.text = text

    def set_other(self, other):
        self.other = other

    def set_alc_dict(self, alc_dict):
        self.alc_dict = alc_dict
        self.get_alc_sum()

    def set_tags(self, tags):
        self.tags = tags

    def set_nes(self, nes):
        self.nes = nes

    def get_alc_sum(self):
        alc = 0
        for key, value in self.alc_dict.items():
            alc += self.liqueur[key] * value

        if alc > 40:
            self.image_url = "http://aoi.naist.jp/~ujiie/sick_alcohol_chudoku.png"
        elif alc > 30:
            self.image_url = "http://aoi.naist.jp/~ujiie/futsukayoi.png"
        elif alc > 20:
            self.image_url = "http://aoi.naist.jp/~ujiie/images.jpg"
        elif alc > 0:
            self.image_url = "http://aoi.naist.jp/~ujiie/list.png"
        else:
            self.image_url = "http://aoi.naist.jp/~ujiie/gaman_osake.png"

        return alc

    def get_calendar_format(self):
        return {"extendedProps":{"imageurl":self.image_url}}

    def get_user_format(self):
        if self.tags and len(self.tags[0]) > 1:
            tags = [t[1] for t in self.tags]
        else:
            tags = self.tags
        return {"tags":tags, "nes":self.nes, "text":self.text, "alc":self.alc_dict}

    def get_chart_format(self):
        return self.get_alc_sum()


class UserInformation(object):
    def __init__(self, name, user_dir, cal_dir, chart_dir):
        self.input_dict = {}
        self.user_name = name
        self.user_dir = Path(user_dir) if isinstance(user_dir, str) else user_dir
        self.cal_dir = Path(cal_dir) if isinstance(cal_dir, str) else cal_dir
        self.chart_dir = Path(chart_dir) if isinstance(chart_dir, str) else chart_dir

    def get_chart_format(self):
        output = {}
        for key, value in self.input_dict.items():
            output[key] = value.get_chart_format()

        return output

    def get_user_format(self):
        output = {}
        for key, value in self.input_dict.items():
            output[key] = value.get_user_format()

        return output

    def save_file(self):
        fn = self.user_name + ".json"
        fn_pkl = self.user_name + ".pkl"
        output = {}
        for key, value in self.input_dict.items():
            output[key] = value.get_calendar_format()

        with open(str(self.cal_dir / fn), 'w') as f:
            json.dump(output, f, ensure_ascii=False)


        output = {}
        for key, value in self.input_dict.items():
            output[key] = value.get_chart_format()

        with open(str(self.chart_dir / fn), 'w') as f:
            json.dump(output, f, ensure_ascii=False)


        with open(str(self.user_dir / fn_pkl), 'wb') as f:
            pickle.dump(self.input_dict, f)

    def load_file(self):
        fn = self.user_name + ".pkl"
        if (self.user_dir / fn).is_file():
            with open(str(self.user_dir / fn), 'rb') as f:
                self.input_dict = pickle.load(f)

    def save_instance(self, input_instance):
        self.input_dict[input_instance.date] = input_instance

    def load_instance(self, date):
        if date not in self.input_dict:
            return None
        return self.input_dict[date]



class Buffer(object):
    def __init__(self):
        self.buffer_ = {}

    def add_buffer(self, name, date, input_instance=None):
        if input_instance is None:
            self.buffer_[name] = InputInstance(date)
        else:
            self.buffer_[name] = copy.deepcopy(input_instance)

    def remove_buffer(self, name):
        self.buffer_.pop(name)

    def get_instance(self, name):
        return self.buffer_[name]


