from typing import Optional
import sqlalchemy as sa
import sqlalchemy.orm as so
from app import db

class Lexicon(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    word: so.Mapped[str] = so.mapped_column(sa.String(50), index=True)
    pronunciation: so.Mapped[str] = so.mapped_column(sa.String(10))
    definition: so.Mapped[str] = so.mapped_column(sa.String(255), index=True)
    def __repr__(self):
        return 'Word {} with definition {}'.format(self.word, self.definition)