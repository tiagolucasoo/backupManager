from database.connection import get_connection
from services.crypto import encrypt_password, decrypt_password

def salvar_perfil(nome, host, user, senha, bancos):
    senha_criptografada = encrypt_password(senha)
    
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT OR REPLACE INTO perfis
        (nome, host, usuario, senha, bancos)
        VALUES (?, ?, ?, ?, ?)
    """, (nome, host, user, senha_criptografada, bancos))

    conn.commit()
    conn.close()

def listar_nomes_perfis():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT nome FROM perfis")
    dados = cursor.fetchall()

    conn.close()

    if not dados:
        return []

    return [x[0] for x in dados]

def obter_bancos_por_perfil(nome):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT bancos
        FROM perfis
        WHERE nome = ?
    """, (nome,))

    resultado = cursor.fetchone()
    conn.close()

    if resultado and resultado[0]:
        return [b.strip() for b in resultado[0].split(",") if b.strip()]
        
    return []

def adicionar_banco_ao_perfil(perfil, banco):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT bancos
        FROM perfis
        WHERE nome = ?
    """, (perfil,))

    atual = cursor.fetchone()[0]
    novo = f"{atual},{banco}" if atual else banco

    cursor.execute("""
        UPDATE perfis
        SET bancos = ?
        WHERE nome = ?
    """, (novo, perfil))

    conn.commit()
    conn.close()

def obter_credenciais(perfil):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT host, usuario, senha
        FROM perfis
        WHERE nome = ?
    """, (perfil,))

    dados = cursor.fetchone()
    conn.close()

    if not dados:
        return None

    senha_descriptografada = decrypt_password(dados[2])

    return {
        "host": dados[0],
        "user": dados[1],
        "pass": senha_descriptografada
    }