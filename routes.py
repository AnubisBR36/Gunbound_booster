from flask import render_template, request, redirect, url_for, flash, session
from app import app, db
from models import User, Account, AccountPurchase
from werkzeug.security import generate_password_hash
import re

@app.route('/')
def index():
    """Homepage with featured accounts"""
    featured_accounts = Account.query.filter_by(status='disponivel').limit(6).all()
    return render_template('index.html', featured_accounts=featured_accounts)

@app.route('/loja')
def loja():
    """Shop page with all available accounts"""
    available_accounts = Account.query.filter_by(status='disponivel').all()
    return render_template('loja.html', accounts=available_accounts)

@app.route('/login', methods=['GET', 'POST'])
def login():
    """User login"""
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        if not email or not password:
            flash('Email e senha são obrigatórios', 'error')
            return render_template('login.html')
        
        user = User.query.filter_by(email=email).first()
        
        if user and user.check_password(password):
            session['user_id'] = user.id
            session['user_name'] = user.nome
            flash(f'Bem-vindo, {user.nome}!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Email ou senha incorretos', 'error')
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    """User registration"""
    if request.method == 'POST':
        nome = request.form.get('nome')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        # Validation
        errors = []
        
        if not nome or len(nome) < 2:
            errors.append('Nome deve ter pelo menos 2 caracteres')
        
        if not email or not re.match(r'^[^@]+@[^@]+\.[^@]+$', email):
            errors.append('Email inválido')
        
        if not password or len(password) < 6:
            errors.append('Senha deve ter pelo menos 6 caracteres')
        
        if password != confirm_password:
            errors.append('Senhas não coincidem')
        
        # Check if email already exists
        if User.query.filter_by(email=email).first():
            errors.append('Email já cadastrado')
        
        if errors:
            for error in errors:
                flash(error, 'error')
            return render_template('register.html')
        
        # Create new user
        user = User(nome=nome, email=email)
        user.set_password(password)
        
        try:
            db.session.add(user)
            db.session.commit()
            flash('Cadastro realizado com sucesso! Faça login para continuar.', 'success')
            return redirect(url_for('login'))
        except Exception as e:
            db.session.rollback()
            flash('Erro ao criar conta. Tente novamente.', 'error')
    
    return render_template('register.html')

@app.route('/dashboard')
def dashboard():
    """User dashboard"""
    if 'user_id' not in session:
        flash('Faça login para acessar o dashboard', 'error')
        return redirect(url_for('login'))
    
    user = User.query.get(session['user_id'])
    if not user:
        session.clear()
        flash('Usuário não encontrado', 'error')
        return redirect(url_for('login'))
    
    # Get user's purchased accounts
    purchases = AccountPurchase.query.filter_by(user_id=user.id).all()
    
    return render_template('dashboard.html', user=user, purchases=purchases)

@app.route('/videos')
def videos():
    """Videos page with YouTube integration"""
    return render_template('videos.html')

@app.route('/logout')
def logout():
    """User logout"""
    session.clear()
    flash('Logout realizado com sucesso', 'success')
    return redirect(url_for('index'))

@app.route('/buy_account/<int:account_id>')
def buy_account(account_id):
    """Simulate account purchase"""
    if 'user_id' not in session:
        flash('Faça login para comprar contas', 'error')
        return redirect(url_for('login'))
    
    account = Account.query.get_or_404(account_id)
    
    if account.status != 'disponivel':
        flash('Esta conta não está mais disponível', 'error')
        return redirect(url_for('loja'))
    
    # Create purchase record
    purchase = AccountPurchase(
        user_id=session['user_id'],
        account_id=account.id,
        purchase_price=account.preco
    )
    
    # Update account status
    account.status = 'vendido'
    
    try:
        db.session.add(purchase)
        db.session.commit()
        flash(f'Conta "{account.nome_da_conta}" comprada com sucesso!', 'success')
        return redirect(url_for('dashboard'))
    except Exception as e:
        db.session.rollback()
        flash('Erro ao processar compra. Tente novamente.', 'error')
        return redirect(url_for('loja'))

# Initialize sample data function (will be called from app.py)
def create_sample_data():
    """Create sample accounts if database is empty"""
    if Account.query.count() == 0:
        sample_accounts = [
            {
                'nome_da_conta': 'Conta Armor - Rank Dourado',
                'descricao': 'Conta premium com mobile Armor desbloqueado, rank Dourado e milhões de gold. Perfeita para jogadores que gostam de tanques resistentes.',
                'imagem_url': '/static/images/armor.png',
                'preco': 150.00
            },
            {
                'nome_da_conta': 'Lightning - Avatar Dragão',
                'descricao': 'Conta com mobile Lightning, avatar especial de Dragão e rank Platina. Ideal para jogadores que preferem velocidade e agilidade.',
                'imagem_url': '/static/images/lightning.png',
                'preco': 220.00
            },
            {
                'nome_da_conta': 'Turtle VIP - Itens Raros',
                'descricao': 'Conta VIP com mobile Turtle, coleção completa de avatares e itens limitados de eventos especiais.',
                'imagem_url': '/static/images/turtle.png',
                'preco': 180.00
            },
            {
                'nome_da_conta': 'Big Foot - Conta Lendária',
                'descricao': 'Conta lendária com mobile Big Foot, rank Diamante, todos os achievements e pets raros desbloqueados.',
                'imagem_url': '/static/images/bigfoot.png',
                'preco': 350.00
            },
            {
                'nome_da_conta': 'J.D. Sniper Elite',
                'descricao': 'Conta especialista com mobile J.D., estatísticas de precisão impressionantes e equipamentos de sniper.',
                'imagem_url': '/static/images/jd.png',
                'preco': 120.00
            },
            {
                'nome_da_conta': 'A.Sate Satellite Master',
                'descricao': 'Conta focada em mobile A.Sate com ataques de longo alcance, equipamentos de satélite e estratégias avançadas.',
                'imagem_url': '/static/images/asate.png',
                'preco': 90.00
            }
        ]
        
        for account_data in sample_accounts:
            account = Account(**account_data)
            db.session.add(account)
        
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            print(f"Error creating sample data: {e}")
