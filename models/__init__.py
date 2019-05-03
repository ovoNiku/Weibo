import json
import time

from models.user_role import (
    NikuEncoder,
    niku_decode,
)

from utils import log


def save(data, path):
    s = json.dumps(data, indent=2, ensure_ascii=False, cls=NikuEncoder)
    with open(path, 'w+', encoding='utf-8') as f:
        log('save', path, s, data)
        f.write(s)


def load(path):
    with open(path, 'r', encoding='utf-8') as f:
        s = f.read()
        log('load', s)
        return json.loads(s, object_hook=niku_decode)


class Model(object):

    def __init__(self, form):
        self.id = form.get('id', None)

    @classmethod
    def db_path(cls):
        classname = cls.__name__
        path = 'data/{}.txt'.format(classname)
        return path

    @classmethod
    def new(cls, form):
        m = cls(form)
        m.save()
        return m

    @classmethod
    def delete(cls, id):
        ms = cls.all()
        for i, m in enumerate(ms):
            if m.id == id:
                del ms[i]
                break

        l = [m.__dict__ for m in ms]
        path = cls.db_path()
        save(l, path)

    @classmethod
    def delete_comment(cls, id):
        ms = cls.all()
        for i, m in enumerate(ms):
            if m.weibo_id == id:
                del ms[i]

        l = [m.__dict__ for m in ms]
        path = cls.db_path()
        save(l, path)

    @classmethod
    def update(cls, id, **kwargs):
        m = cls.find_by(id=id)

        for k, v in kwargs.items():
            if hasattr(m, k):
                setattr(m, k, v)

        m.updated_time = int(time.time())

        m.save()
        return m

    @classmethod
    def all(cls):

        path = cls.db_path()
        models = load(path)
        ms = [cls(m) for m in models]
        return ms

    @classmethod
    def find_by(cls, **kwargs):

        for m in cls.all():
            exist = True
            for k, v in kwargs.items():
                if not hasattr(m, k) or not getattr(m, k) == v:
                    exist = False
            if exist:
                return m

    @classmethod
    def find_all(cls, **kwargs):
        models = []

        for m in cls.all():
            exist = True
            for k, v in kwargs.items():
                if not hasattr(m, k) or not getattr(m, k) == v:
                    exist = False
            if exist:
                models.append(m)

        return models

    def save(self):
        models = self.all()

        if self.id is None:
            if len(models) > 0:
                self.id = models[-1].id + 1
            else:
                self.id = 0
            models.append(self)
        else:
            for i, m in enumerate(models):
                if m.id == self.id:
                    models[i] = self

        l = [m.__dict__ for m in models]
        path = self.db_path()
        save(l, path)

    def __repr__(self):
        classname = self.__class__.__name__
        properties = ['{}: ({})'.format(k, v) for k, v in self.__dict__.items()]
        s = '\n'.join(properties)
        return '< {}\n{} >\n'.format(classname, s)

    def json(self):
        d = self.__dict__
        return d

    @classmethod
    def all_json(cls):
        ms = cls.all()
        js = [t.json() for t in ms]
        return js
