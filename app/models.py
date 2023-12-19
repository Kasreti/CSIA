from typing import Optional
import sqlalchemy as sa
import sqlalchemy.orm as so
from app import db

class Lexicon(db.Model):
    __tablename__ = 'Lexicon'
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    word: so.Mapped[str] = so.mapped_column(sa.String(50), index=True)
    pronunciation: so.Mapped[str] = so.mapped_column(sa.String(50), nullable=True)
    conscript: so.Mapped[str] = so.mapped_column(sa.String(50), nullable=True)
    definition: so.Mapped[str] = so.mapped_column(sa.String(255), index=True)
    partofspeech: so.Mapped[str] = so.mapped_column(sa.String(1), nullable=True)
    infclass: so.Mapped[str] = so.mapped_column(sa.String(10), nullable=True)
    wordclass: so.Mapped[int] = so.mapped_column(sa.String(1), nullable=True)
    notes: so.Mapped[str] = so.mapped_column(nullable=True)
    etymology: so.Mapped[str] = so.mapped_column(nullable=True)
    def __repr__(self):
        return 'Word {} with definition {}'.format(self.word, self.definition)

    def __init__(self, word, pronunciation, conscript, definition, partofspeech, infclass, wordclass, notes, etymology):
        self.word = word
        self.pronunciation = pronunciation
        self.conscript = conscript
        self.wordclass = wordclass
        self.definition = definition
        self.notes = notes
        self.infclass = infclass
        self.etymology = etymology
        self.partofspeech = partofspeech