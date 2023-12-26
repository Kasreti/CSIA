from typing import Optional
import sqlalchemy as sa
import sqlalchemy.orm as so
from app import db, app

class Lexicon(db.Model):
    __tablename__ = 'Lexicon'
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    word: so.Mapped[str] = so.mapped_column(sa.String(50), index=True)
    pronunciation: so.Mapped[str] = so.mapped_column(sa.String(50), nullable=True)
    conscript: so.Mapped[str] = so.mapped_column(sa.String(50), nullable=True)
    definition: so.Mapped[str] = so.mapped_column(sa.String(255), index=True)
    partofspeech: so.Mapped[str] = so.mapped_column(nullable=True)
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

class Phonology(db.Model):
    __tablename__ = 'Phonology'
    phoneme: so.Mapped[str] = so.mapped_column(primary_key=True)
    ipa: so.Mapped[str] = so.mapped_column(sa.String(5), index=True)
    exists: so.Mapped[bool] = so.mapped_column()
    consonant: so.Mapped[bool] = so.mapped_column()
    romanized: so.Mapped[str] = so.mapped_column(sa.String(5), nullable=True)
    conscript: so.Mapped[str] = so.mapped_column(sa.String(5), nullable=True)

    def __repr__(self):
        return 'Phoneme {}'.format(self.ipa)

    def __init__(self, phoneme, ipa, exists, consonant, romanized=None, conscript=None):
        self.phoneme = phoneme
        self.ipa = ipa
        self.exists = exists
        self.consonant = consonant
        self.romanized = romanized
        self.conscript = conscript

class Texts(db.Model):
    __tablename__ = 'Texts'
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    title: so.Mapped[str] = so.mapped_column(index=True)
    status: so.Mapped[str] = so.mapped_column(index=True)
    content: so.Mapped[str] = so.mapped_column()
    translation: so.Mapped[str] = so.mapped_column(nullable=True)

    def __repr__(self):
        return 'Translatable text {} with status {}'.format(self.id, self.status)

    def __init__(self, title, status, content):
        self.title = title
        self.status = status
        self.content = content

with app.app_context():
    db.create_all()