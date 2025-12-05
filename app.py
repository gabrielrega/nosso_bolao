import streamlit as st
import pandas as pd
import os
import json

# --- CONFIGURAÇÃO E REGRAS ---
FILE_DB = 'bolao_db.json'

REGRAS = {
    'Grupos': {'cheio': 3, 'gol': 1},
    '16avos': {'time': 5, 'cheio': 3, 'gol': 1},
    'Oitavas': {'time': 10, 'cheio': 6, 'gol': 2},
    'Quartas': {'time': 15, 'cheio': 9, 'gol': 3},
    'Semi': {'time': 20, 'cheio': 12, 'gol': 4},
    'Final': {'time': 20, 'cheio': 15, 'gol': 5},
    '3Lugar': {'time': 10, 'cheio': 6, 'gol': 2}
}

# Estrutura básica dos dados se o arquivo não existir
default_data = {
    "participantes": {}, # { "Nome": { "jogo_id": {"time_a": "Brasil", "placar_a": 2...} } }
    "gabarito": {},      # Mesmo formato, mas preenchido pelo Admin
    "config": {"fase_atual": "Grupos"}
}

# --- FUNÇÕES DE SUPORTE ---
def load_data():
    if not os.path.exists(FILE_DB):
        return default_data
    with open(FILE_DB, 'r') as f:
        return json.load(f)

def save_data(data):
    with open(FILE_DB, 'w') as f:
        json.dump(data, f, indent=4)

def calcular_pontos(palpite, gabarito, fase):
    pts = 0
    detalhes = []
    
    # Se não houver resultado oficial ainda
    if not gabarito: 
        return 0

    # 1. PONTOS DE TIME (MATA-MATA)
    # Verifica se os times do palpite estão presentes no jogo real (independente do lado)
    if fase != 'Grupos':
        times_palpite = {palpite.get('time_a'), palpite.get('time_b')}
        times_gabarito = {gabarito.get('time_a'), gabarito.get('time_b')}
        acertos_time = len(times_palpite.intersection(times_gabarito))
        
        # Regra: Pontos por time classificado
        # Se acertou 1 time, ganha X. Se acertou 2, ganha 2X.
        pts_time = acertos_time * REGRAS[fase]['time']
        pts += pts_time
        if pts_time > 0: detalhes.append(f"+{pts_time} (Times)")

    # 2. PONTOS DE PLACAR
    # Regra Crucial: Só vale ponto de placar se acertar o confronto (os dois times)
    # Na fase de grupos, os times são fixos, então sempre vale tentar o placar.
    pode_pontuar_placar = True
    if fase != 'Grupos':
        times_palpite = {palpite.get('time_a'), palpite.get('time_b')}
        times_gabarito = {gabarito.get('time_a'), gabarito.get('time_b')}
        if times_palpite != times_gabarito:
            pode_pontuar_placar = False
    
    if pode_pontuar_placar and gabarito.get('placar_a') is not None:
        p_a, p_b = int(palpite['placar_a']), int(palpite['placar_b'])
        g_a, g_b = int(gabarito['placar_a']), int(gabarito['placar_b'])
        
        # Acerto Cheio (Vencedor ou Empate)
        # Lógica: Quem venceu?
        venc_p = 'A' if p_a > p_b else ('B' if p_b > p_a else 'E')
        venc_g = 'A' if g_a > g_b else ('B' if g_b > g_a else 'E')
        
        if venc_p == venc_g:
            pts += REGRAS[fase]['cheio']
            detalhes.append(f"+{REGRAS[fase]['cheio']} (Resultado)")
        
        # Acerto de Gols (Exato)
        # Regra: Inversão não pontua. Tem que acertar o gol do time certo.
        # Como o mata-mata pode ter times trocados de lado, simplificamos comparando sets
        if fase == 'Grupos':
            if p_a == g_a: pts += REGRAS[fase]['gol']
            if p_b == g_b: pts += REGRAS[fase]['gol']
        else:
            # No mata-mata, se acertou os times, compara gols do vencedor e perdedor
            # Simplificação para o código: compara exato A com A e B com B assumindo ordem do gabarito
            if p_a == g_a: pts += REGRAS[fase]['gol']
            if p_b == g_b: pts += REGRAS[fase]['gol']

    return pts

# --- INTERFACE STREAMLIT ---
st.set_page_config(page_title="Bolão Copa 48", layout="wide")
st.title("⚽ Bolão da Copa - 48 Times")

dados = load_data()
menu = st.sidebar.selectbox("Menu", ["Meus Palpites", "Ranking & Resultados", "Área do Administrador"])

# LISTA DE GRUPOS E FASES
grupos = list("ABCDEFGHIJKL")
fases_mata_mata = ["16avos", "Oitavas", "Quartas", "Semi", "Final"]

if menu == "Meus Palpites":
    st.header("Faça seus palpites")
    nome_usuario = st.text_input("Seu Nome (ex: Gabriel, Renato, Eduardo):")
    
    if nome_usuario:
        if nome_usuario not in dados['participantes']:
            dados['participantes'][nome_usuario] = {}
        
        st.info("Dica: Salve seus palpites fase por fase.")
        
        aba_grupos, aba_mata = st.tabs(["Fase de Grupos", "Mata-Mata"])
        
        with aba_grupos:
            st.subheader("Fase de Grupos (Exemplo Simulado)")
            # Loop simplificado para demonstração. Na real seriam 72 jogos.
            col1, col2 = st.columns(2)
            for g in grupos:
                with col1 if g <= 'F' else col2:
                    st.markdown(f"**Grupo {g}**")
                    # Exemplo de 1 jogo por grupo para não poluir o código demo
                    jid = f"grp_{g}_1"
                    palpite_atual = dados['participantes'][nome_usuario].get(jid, {})
                    
                    c1, c2, c3, c4 = st.columns([2,1,1,2])
                    c1.text(f"Time {g}1")
                    pa = c2.number_input(f"Gols A", 0, 10, key=f"{jid}_a", value=palpite_atual.get('placar_a', 0), label_visibility="collapsed")
                    pb = c3.number_input(f"Gols B", 0, 10, key=f"{jid}_b", value=palpite_atual.get('placar_b', 0), label_visibility="collapsed")
                    c4.text(f"Time {g}2")
                    
                    dados['participantes'][nome_usuario][jid] = {
                        "time_a": f"Time {g}1", "time_b": f"Time {g}2",
                        "placar_a": pa, "placar_b": pb
                    }
        
        with aba_mata:
            st.warning("Lembre-se: No mata-mata, você precisa acertar QUEM joga para pontuar o placar.")
            fase_sel = st.selectbox("Escolha a fase:", fases_mata_mata)
            
            # Exemplo genérico de jogos de mata-mata
            for i in range(1, 3): # Mostrando apenas 2 jogos de exemplo
                st.markdown(f"--- **Jogo {i} - {fase_sel}** ---")
                jid = f"{fase_sel}_{i}"
                palpite_atual = dados['participantes'][nome_usuario].get(jid, {})
                
                c1, c2, c3, c4, c5 = st.columns([3, 1, 1, 1, 3])
                ta = c1.text_input("Time A", value=palpite_atual.get('time_a', ''), key=f"t_{jid}_a", placeholder="Ex: Brasil")
                pa = c2.number_input("Gols", 0, 20, value=palpite_atual.get('placar_a', 0), key=f"p_{jid}_a")
                c3.markdown("<h3 style='text-align: center;'>X</h3>", unsafe_allow_html=True)
                pb = c4.number_input("Gols", 0, 20, value=palpite_atual.get('placar_b', 0), key=f"p_{jid}_b")
                tb = c5.text_input("Time B", value=palpite_atual.get('time_b', ''), key=f"t_{jid}_b", placeholder="Ex: França")
                
                dados['participantes'][nome_usuario][jid] = {
                    "time_a": ta, "time_b": tb,
                    "placar_a": pa, "placar_b": pb
                }

        if st.button("Salvar Meus Palpites"):
            save_data(dados)
            st.success("Palpites salvos com sucesso!")

elif menu == "Área do Administrador":
    st.header("Gabarito Oficial (Apenas Admin)")
    senha = st.text_input("Senha Admin", type="password")
    if senha == "1234": # Senha simples para exemplo
        st.write("Preencha os resultados reais dos jogos aqui.")
        
        # Interface simplificada para preencher resultados (mesma lógica de palpites)
        # Para o Admin, é importante definir o gabarito.
        # Aqui, replico a lógica simplificada de Grupos
        st.subheader("Definir Resultados - Grupos")
        for g in grupos:
            jid = f"grp_{g}_1"
            res_atual = dados['gabarito'].get(jid, {})
            c1, c2, c3, c4 = st.columns([2,1,1,2])
            c1.text(f"Time {g}1")
            pa = c2.number_input(f"G A", 0, 10, key=f"adm_{jid}_a", value=res_atual.get('placar_a', 0))
            pb = c3.number_input(f"G B", 0, 10, key=f"adm_{jid}_b", value=res_atual.get('placar_b', 0))
            c4.text(f"Time {g}2")
            
            dados['gabarito'][jid] = {
                "time_a": f"Time {g}1", "time_b": f"Time {g}2",
                "placar_a": pa, "placar_b": pb
            }
        
        if st.button("Atualizar Gabarito Oficial"):
            save_data(dados)
            st.success("Resultados oficiais atualizados.")

elif menu == "Ranking & Resultados":
    st.header("🏆 Classificação Geral")
    
    if not dados['participantes']:
        st.warning("Nenhum palpite registrado ainda.")
    else:
        placar_geral = []
        
        for user, palpites in dados['participantes'].items():
            total_pts = 0
            # Varre todos os jogos do gabarito
            for jid, gabarito_jogo in dados['gabarito'].items():
                palpite_jogo = palpites.get(jid)
                if palpite_jogo:
                    # Identifica fase pelo ID (grp, 16avos, Oitavas...)
                    if 'grp' in jid: fase = 'Grupos'
                    elif '16avos' in jid: fase = '16avos'
                    elif 'Oitavas' in jid: fase = 'Oitavas'
                    else: fase = 'Grupos' # Default fallback
                    
                    pts = calcular_pontos(palpite_jogo, gabarito_jogo, fase)
                    total_pts += pts
            
            placar_geral.append({"Participante": user, "Pontos": total_pts})
        
        df_ranking = pd.DataFrame(placar_geral).sort_values("Pontos", ascending=False)
        st.dataframe(df_ranking, use_container_width=True)
        
        st.subheader("Regras Ativas")
        st.json(REGRAS)
