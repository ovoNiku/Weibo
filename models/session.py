import time

from models.base_model import SQLModel
from utils import log


class Session(SQLModel):
    sql_create = '''
    CREATE TABLE `session` (
        `id` INT NOT NULL AUTO_INCREMENT,
        `session_id` CHAR(16) NOT NULL,
        `user_id` INT NOT NULL,
        `expired_time` INT NOT NULL,
        PRIMARY KEY (`id`)
    )'''

    def __init__(self, form):
        super().__init__(form)
        self.session_id = form.get('session_id', '')
        self.user_id = form.get('user_id', -1)
        self.expired_time = form.get('expired_time', time.time() + 3600)

    def expired(self):
        now = time.time()
        result = self.expired_time < now
        log('session 过期', result, self.expired_time, now)
        return result

    @classmethod
    def add(cls, user_id):

        session_id = random_string()
        form = dict(
            session_id=session_id,
            user_id=user_id,
        )
        Session.new(form)
        return session_id