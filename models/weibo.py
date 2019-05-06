from models.base_model import SQLModel
from models.comment import Comment
from utils import log


class Weibo(SQLModel):
    sql_create = '''
        CREATE TABLE `weibo` (
            `id` INT NOT NULL AUTO_INCREMENT,
            `user_id` INT NOT NULL,
            `content` VARCHAR(64) NOT NULL,
            PRIMARY KEY (`id`)
    )'''

    def __init__(self, form):
        super().__init__(form)
        self.content = form.get('content', '')
        self.user_id = form.get('user_id', None)

    @classmethod
    def add(cls, form, user_id):
        w = cls(form)
        w.user_id = user_id
        _id = cls.insert(w.__dict__)
        w.id = _id
        return w

    def comments(self):
        cs = Comment.all(weibo_id=self.id)
        return cs

    @classmethod
    def comment_add(cls, form, user_id):
        weibo_id = int(form['weibo_id'])
        c = Comment(form)
        c.user_id = user_id
        c.weibo_id = weibo_id
        c.insert(c.__dict__)

        log('comment add', c, user_id, form)

    @classmethod
    def update(cls, _id, **kwargs):
        super().update(
            id=_id,
            content=kwargs['content']
        )

        w = Weibo.one(id=_id)
        return w
