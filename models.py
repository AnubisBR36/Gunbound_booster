from app import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationship with purchased accounts
    purchased_accounts = db.relationship('AccountPurchase', backref='user', lazy=True)
    
    def set_password(self, password):
        """Hash and set password"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Check if provided password matches hash"""
        return check_password_hash(self.password_hash, password)

class Account(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome_da_conta = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.Text, nullable=False)
    imagem_url = db.Column(db.String(255), nullable=False)
    preco = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(20), default='disponivel')  # disponivel, vendido
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationship with purchases
    purchases = db.relationship('AccountPurchase', backref='account', lazy=True)

class AccountPurchase(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    account_id = db.Column(db.Integer, db.ForeignKey('account.id'), nullable=False)
    purchase_date = db.Column(db.DateTime, default=datetime.utcnow)
    purchase_price = db.Column(db.Float, nullable=False)
