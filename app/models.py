from datetime import datetime
from flask_sqlalchemy import backref

from .ext import db


class LicenseKey(db.Model):
    __tablename__ = 'license_keys'

    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(64), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    expires_at = db.Column(db.DateTime, nullable=False)
    activation_ip = db.Column(db.String(45), nullable=True)
    is_active = db.Column(db.Boolean, default=False, nullable=False)
    user = db.relationship('User', back_populates='license_key')

    def __repr__(self):
        return f'<LicenseKey {self.key}>'

    def activate(self, ip_address):
        self.is_active = True
        self.activation_ip = ip_address
        db.session.commit()

    def is_expired(self):
        return datetime.utcnow() > self.expires_at

    def deactivate(self):
        self.is_active = False
        self.activation_ip = None
        db.session.commit()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), unique=False, nullable=False)
    payed = db.Column(db.Boolean(60), default=False)
    license_key = db.relationship('LicenseKey', back_populates='user')

    def __repr__(self):
        return f'<User {self.username}>'