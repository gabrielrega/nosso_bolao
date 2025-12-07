import streamlit as st
import pandas as pd
import os
import json

# --- TABELA OFICIAL DA COPA 2026 (72 JOGOS) ---
TABELA_GRUPOS = [
    # GRUPO A
    {"id": "A1", "grupo": "A", "time_a": "México", "time_b": "África do Sul"},
    {"id": "A2", "grupo": "A", "time_a": "Coreia do Sul", "time_b": "Repescagem UEFA D"},
    {"id": "A3", "grupo": "A", "time_a": "Repescagem UEFA D", "time_b": "África do Sul"},
    {"id": "A4", "grupo": "A", "time_a": "México", "time_b": "Coreia do Sul"},
    {"id": "A5", "grupo": "A", "time_a": "Repescagem UEFA D", "time_b": "México"},
    {"id": "A6", "grupo": "A", "time_a": "África do Sul", "time_b": "Coreia do Sul"},
    # GRUPO B
    {"id": "B1", "grupo": "B", "time_a": "Canadá", "time_b": "Repescagem UEFA A"},
    {"id": "B2", "grupo": "B", "time_a": "Catar", "time_b": "Suíça"},
    {"id": "B3", "grupo": "B", "time_a": "Suíça", "time_b": "Repescagem UEFA A"},
    {"id": "B4", "grupo": "B", "time_a": "Canadá", "time_b": "Catar"},
    {"id": "B5", "grupo": "B", "time_a": "Suíça", "time_b": "Canadá"},
    {"id": "B6", "grupo": "B", "time_a": "Repescagem UEFA A", "time_b": "Catar"},
    # GRUPO C (BRASIL)
    {"id": "C1", "grupo": "C", "time_a": "Brasil", "time_b": "Marrocos"},
    {"id": "C2", "grupo": "C", "time_a": "Haiti", "time_b": "Escócia"},
    {"id": "C3", "grupo": "C", "time_a": "Escócia", "time_b": "Marrocos"},
    {"id": "C4", "grupo": "C", "time_a": "Brasil", "time_b": "Haiti"},
    {"id": "C5", "grupo": "C", "time_a": "Escócia", "time_b": "Brasil"},
    {"id": "C6", "grupo": "C", "time_a": "Marrocos", "time_b": "Haiti"},
    # GRUPO D
    {"id": "D1", "grupo": "D", "time_a": "EUA", "time_b": "Paraguai"},
    {"id": "D2", "grupo": "D", "time_a": "Austrália", "time_b": "Repescagem UEFA C"},
    {"id": "D3", "grupo": "D", "time_a": "EUA", "time_b": "Austrália"},
    {"id": "D4", "grupo": "D", "time_a": "Repescagem UEFA C", "time_b": "Paraguai"},
    {"id": "D5", "grupo": "D", "time_a": "Repescagem UEFA C", "time_b": "EUA"},
    {"id": "D6", "grupo": "D", "time_a": "Paraguai", "time_b": "Austrália"},
    # GRUPO E
    {"id": "E1", "grupo": "E", "time_a": "Alemanha", "time_b": "Curaçao"},
    {"id": "E2", "grupo": "E", "time_a": "Costa do Marfim", "time_b": "Equador"},
    {"id": "E3", "grupo": "E", "time_a": "Alemanha", "time_b": "Costa do Marfim"},
    {"id": "E4", "grupo": "E", "time_a": "Equador", "time_b": "Curaçao"},
    {"id": "E5", "grupo": "E", "time_a": "Equador", "time_b": "Alemanha"},
    {"id": "E6", "grupo": "E", "time_a": "Curaçao", "time_b": "Costa do Marfim"},
    # GRUPO F
    {"id": "F1", "grupo": "F", "time_a": "Holanda", "time_b": "Japão"},
    {"id": "F2", "grupo": "F", "time_a": "Repescagem UEFA B", "time_b": "Tunísia"},
    {"id": "F3", "grupo": "F", "time_a": "Holanda", "time_b": "Repescagem UEFA B"},
    {"id": "F4", "grupo": "F", "time_a": "Tunísia", "time_b": "Japão"},
    {"id": "F5", "grupo": "F", "time_a": "Tunísia", "time_b": "Holanda"},
    {"id": "F6", "grupo": "F", "time_a": "Japão", "time_b": "Repescagem UEFA B"},
    # GRUPO G
    {"id": "G1", "grupo": "G", "time_a": "Bélgica", "time_b": "Egito"},
    {"id": "G2", "grupo": "G", "time_a": "Irã", "time_b": "Nova Zelândia"},
    {"id": "G3", "grupo": "G", "time_a": "Bélgica", "time_b": "Irã"},
    {"id": "G4", "grupo": "G", "time_a": "Nova Zelândia", "time_b": "Egito"},
    {"id": "G5", "grupo": "G", "time_a": "Nova Zelândia", "time_b": "Bélgica"},
    {"id": "G6", "grupo": "G", "time_a": "Egito", "time_b": "Irã"},
    # GRUPO H
    {"id": "H1", "grupo": "H", "time_a": "Espanha", "time_b": "Cabo Verde"},
    {"id": "H2", "grupo": "H", "time_a": "Arábia Saudita", "time_b": "Uruguai"},
    {"id": "H3", "grupo": "H", "time_a": "Espanha", "time_b": "Arábia Saudita"},
    {"id": "H4", "grupo": "H", "time_a": "Uruguai", "time_b": "Cabo Verde"},
    {"id": "H5", "grupo": "H", "time_a": "Uruguai", "time_b": "Espanha"},
    {"id": "H6", "grupo": "H", "time_a": "Cabo Verde", "time_b": "Arábia Saudita"},
    # GRUPO I
    {"id": "I1", "grupo": "I", "time_a": "França", "time_b": "Senegal"},
    {"id": "I2", "grupo": "I", "time_a": "Repescagem FIFA 2", "time_b": "Noruega"},
    {"id": "I3", "grupo": "I", "time_a": "França", "time_b": "Repescagem FIFA 2"},
    {"id": "I4", "grupo": "I", "time_a": "Noruega", "time_b": "Senegal"},
    {"id": "I5", "grupo": "I", "time_a": "Noruega", "time_b": "França"},
    {"id": "I6", "grupo": "I", "time_a": "Senegal", "time_b": "Repescagem FIFA 2"},
    # GRUPO J
    {"id": "J1", "grupo": "J", "time_a": "Argentina", "time_b": "Argélia"},
    {"id": "J2", "grupo": "J", "time_a": "Áustria", "time_b": "Jordânia"},
    {"id": "J3", "grupo": "J", "time_a": "Argentina", "time_b": "Áustria"},
    {"id": "J4", "grupo": "J", "time_a": "Jordânia", "time_b": "Argélia"},
    {"id": "J5", "grupo": "J", "time_a": "Jordânia", "time_b": "Argentina"},
    {"id": "J6", "grupo": "J", "time_a": "Argélia", "time_b": "Áustria"},
    # GRUPO K
    {"id": "K1", "grupo": "K", "time_a": "Portugal", "time_b": "Repescagem FIFA 1"},
    {"id": "K2", "grupo": "K", "time_a": "Uzbequistão", "time_b": "Colômbia"},
    {"id": "K3", "grupo": "K", "time_a": "Portugal", "time_b": "Uzbequistão"},
    {"id": "K4", "grupo": "K", "time_a": "Colômbia", "time_b": "Repescagem FIFA 1"},
    {"id": "K5", "grupo": "K", "time_a": "Colômbia", "time_b": "Portugal"},
    {"id": "K6", "grupo": "K", "time_a": "Repescagem FIFA 1", "time_b": "Uzbequistão"},
    # GRUPO L
    {"id": "L1", "grupo": "L", "time_a": "Inglaterra", "time_b": "Croácia"},
    {"id": "L2", "grupo": "L", "time_a": "Gana", "time_b": "Panamá"},
    {"id": "L3", "grupo": "L", "time_a": "Inglaterra", "time_b": "Gana"},
    {"id": "L4", "grupo": "L", "time_a": "Panamá", "time_b": "Croácia"},
    {"id": "L5", "grupo": "L", "time_a": "Panamá", "time_b": "Inglaterra"},
    {"id": "L6", "grupo": "L", "time_a": "Croácia", "time_b": "Gana"},
]

# --- ESTRUTURA DO MATA-MATA ---
MATA_MATA_ESTRUTURA = {
    "16avos": 16,
    "Oitavas": 8,
    "Quartas": 4,
    "Semi": 2,
    "Final": 1,
    "3Lugar": 1
}

# --- CONFIGURAÇÃO DO ARQUIVO DE DADOS ---
FILE_DB = 'bolao_db.json'

# --- REGRAS DE PONTUAÇÃO (Incluindo Regra Linear para 16-avos) ---
REGRAS = {
    'Grupos': {'cheio': 3, 'gol': 1},
    '16avos': {'time': 5, 'cheio': 3, 'gol': 1},
    'Oitavas': {'time': 10, 'cheio': 6, 'gol': 2},
    'Quartas': {'time': 15, 'cheio': 9, 'gol': 3},
    'Semi': {'time': 20, 'cheio': 12, 'gol': 4},
    'Final': {'time': 20, 'cheio': 15, 'gol': 5},
    '3Lugar': {'time': 10, 'cheio': 6, 'gol': 2}
}

# --- FUNÇÕES ---
def load_data():
    if not os.path.exists(FILE_DB):
        return {"participantes": {}, "gabarito": {}, "config": {}}
    with open(FILE_DB, 'r') as f:
        return json.load(f)

def save_data(data):
    with open(FILE_DB, 'w') as f:
        json.dump(data, f, indent=4)

def calcular_pontos(palpite, gabarito, fase):
    if not gabarito: return 0
    pts = 0
    
    # 1. Pontos de Time (Só Mata-Mata)
    if fase != 'Grupos':
        tp = {palpite.get('time_a', '').strip().lower(), palpite.get('time_b', '').strip().lower()}
        tg = {gabarito.get('time_a', '').strip().lower(), gabarito.get('time_b', '').strip().lower()}
        tp.discard('')
        tg.discard('')
        acertos = len(tp.intersection(tg))
        pts += acertos * REGRAS[fase]['time']

    # 2. Pontos de Placar
    match_valido = True
    if fase != 'Grupos':
        # No mata-mata, só vale placar se acertar o confronto exato
        tp = {palpite.get('time_a', '').strip().lower(), palpite.get('time_b', '').strip().lower()}
        tg = {gabarito.get('time_a', '').strip().lower(), gabarito.get('time_b', '').strip().lower()}
        if tp != tg or len(tp) < 2:
            match_valido = False
    
    if match_valido and gabarito.get('placar_a') is not None and gabarito.get('placar_a') != "":
        try:
            pa, pb = int(palpite['placar_a']), int(palpite['placar_b'])
            ga, gb = int(gabarito['placar_a']), int(gabarito['placar_b'])
            
            # Resultado (Vencedor/Empate)
            venc_p = 'A' if pa > pb else ('B' if pb > pa else 'E')
            venc_g = 'A' if ga > gb else ('B' if gb > ga else 'E')
            
            if venc_p == venc_g:
                pts += REGRAS[fase]['cheio']
            
            # Gols Exatos
            if pa == ga: pts += REGRAS[fase]['gol']
            if pb == gb: pts += REGRAS[fase]['gol']
        except:
            pass
            
    return pts

# --- INTERFACE GRÁFICA ---
st.set_page_config(page_title="Bolão Copa 2026", layout="wide", page_icon="⚽")
st.title("⚽ Bolão da Copa 2026 - 48 Times")

dados = load_data()

# Menu lateral
with st.sidebar:
    st.header("Menu")
    menu = st.radio("Ir para:", ["Meus Palpites", "Ranking Geral", "Área Admin"])
    st.markdown("---")
    st.info("Regras Rápidas:\n- Mata-mata: Placar só vale se acertar o confronto.\n- 16-avos: Nova fase valendo 5 pts por time.")

if menu == "Meus Palpites":
    st.header("📝 Preencha sua Tabela")
    user_input = st.text_input("Digite seu Nome para começar:", placeholder="Ex: Renato")
    
    if user_input:
        user = user_input.strip()
        if user not in dados['participantes']: dados['participantes'][user] = {}
        
        tab1, tab2 = st.tabs(["🌎 Fase de Grupos", "🏆 Mata-Mata (Simulação)"])
        
        # --- ABA 1: FASE DE GRUPOS (LAYOUT NOVO) ---
        with tab1:
            st.subheader("Jogos da Primeira Fase")
            st.write("Preencha os placares. Os times já estão definidos.")
            
            # Agrupar jogos
            jogos_por_grupo = {}
            for j in TABELA_GRUPOS:
                if j['grupo'] not in jogos_por_grupo: jogos_por_grupo[j['grupo']] = []
                jogos_por_grupo[j['grupo']].append(j)
            
            # Layout em colunas para os grupos (3 colunas de grupos lado a lado)
            cols_main = st.columns(3)
            
            for idx, (grupo, lista_jogos) in enumerate(jogos_por_grupo.items()):
                with cols_main[idx % 3]:
                    st.markdown(f"### Grupo {grupo}")
                    st.markdown("---")
                    
                    for jogo in lista_jogos:
                        jid = jogo['id']
                        palpite = dados['participantes'][user].get(jid, {})
                        
                        # Layout linha do jogo: [Time A (Right)] [Input] [x] [Input] [Time B (Left)]
                        c1, c2, c3, c4, c5 = st.columns([3, 1, 0.5, 1, 3])
                        
                        # Time A (Alinhado à direita para ficar perto do placar)
                        c1.markdown(f"<div style='text-align: right; padding-top: 10px; font-weight: bold;'>{jogo['time_a']}</div>", unsafe_allow_html=True)
                        
                        # Input A
                        pa = c2.text_input(f"A_{jid}", value=palpite.get('placar_a', ''), label_visibility="collapsed", key=f"pa_{jid}_{user}")
                        
                        # X no meio
                        c3.markdown("<div style='text-align: center; padding-top: 10px;'>x</div>", unsafe_allow_html=True)
                        
                        # Input B
                        pb = c4.text_input(f"B_{jid}", value=palpite.get('placar_b', ''), label_visibility="collapsed", key=f"pb_{jid}_{user}")
                        
                        # Time B (Alinhado à esquerda)
                        c5.markdown(f"<div style='text-align: left; padding-top: 10px; font-weight: bold;'>{jogo['time_b']}</div>", unsafe_allow_html=True)
                        
                        # Espaçamento entre jogos
                        st.write("") 

                        # Salvar
                        dados['participantes'][user][jid] = {
                            "time_a": jogo['time_a'], "time_b": jogo['time_b'],
                            "placar_a": pa, "placar_b": pb
                        }
                    st.divider()

        # --- ABA 2: MATA-MATA ---
        with tab2:
            st.subheader("O Caminho até a Final")
            st.info("Aqui você deve preencher QUEM PASSA e o placar. Preveja a copa inteira!")
            
            for fase, qtd in MATA_MATA_ESTRUTURA.items():
                with st.expander(f"{fase} ({qtd} jogos)", expanded=(fase=="16avos")):
                    for i in range(1, qtd + 1):
                        jid = f"{fase}_{i}"
                        palpite = dados['participantes'][user].get(jid, {})
                        
                        st.markdown(f"**Jogo {i}**")
                        # Layout igual ao de cima, mas com Inputs para os nomes dos times
                        c1, c2, c3, c4, c5 = st.columns([3, 1, 0.5, 1, 3])
                        
                        ta = c1.text_input("Time A", value=palpite.get('time_a', ''), key=f"ta_{jid}_{user}", placeholder="Time A...")
                        pa = c2.text_input("Gols A", value=palpite.get('placar_a', ''), key=f"pa_{jid}_{user}", label_visibility="collapsed")
                        c3.markdown("<div style='text-align: center; padding-top: 10px;'>x</div>", unsafe_allow_html=True)
                        pb = c4.text_input("Gols B", value=palpite.get('placar_b', ''), key=f"pb_{jid}_{user}", label_visibility="collapsed")
                        tb = c5.text_input("Time B", value=palpite.get('time_b', ''), key=f"tb_{jid}_{user}", placeholder="Time B...")
                        
                        dados['participantes'][user][jid] = {
                            "time_a": ta, "time_b": tb,
                            "placar_a": pa, "placar_b": pb
                        }

        st.markdown("---")
        if st.button("💾 SALVAR MEUS PALPITES", type="primary"):
            save_data(dados)
            st.success(f"Palpites de {user} salvos com sucesso!")
            st.balloons()

elif menu == "Ranking Geral":
    st.header("🏆 Classificação")
    if not dados['participantes']:
        st.warning("Ainda não há palpites registrados.")
    else:
        # Botão para recalcular
        if st.button("Atualizar Ranking"):
            pass
            
        resumo = []
        for p_user, p_dict in dados['participantes'].items():
            pts_total = 0
            detalhes = ""
            for jid, gab in dados['gabarito'].items():
                palp = p_dict.get(jid)
                if palp:
                    # Determinar fase
                    fase = 'Grupos'
                    for f in REGRAS.keys():
                        if f in jid: fase = f; break
                    
                    pts = calcular_pontos(palp, gab, fase)
                    pts_total += pts
            
            resumo.append({"Participante": p_user, "Pontos": pts_total})
        
        df = pd.DataFrame(resumo).sort_values("Pontos", ascending=False).reset_index(drop=True)
        # Hackzinho visual para destacar o líder
        st.dataframe(df, use_container_width=True)
        
        st.subheader("Gabarito Oficial (Parcial)")
        st.json(dados.get('gabarito', {}), expanded=False)

elif menu == "Área Admin":
    st.header("🔒 Área Restrita")
    senha = st.text_input("Senha Admin", type="password")
    if senha == "admin123":
        st.success("Logado.")
        st.write("Preencha aqui os resultados reais da Copa conforme eles acontecem.")
        
        tab_g, tab_m = st.tabs(["Resultados Grupos", "Resultados Mata-Mata"])
        
        with tab_g:
            for j in TABELA_GRUPOS:
                jid = j['id']
                gab = dados['gabarito'].get(jid, {})
                c1, c2, c3, c4, c5 = st.columns([3, 1, 0.5, 1, 3])
                
                c1.markdown(f"<div style='text-align: right; padding-top: 10px;'>{j['time_a']}</div>", unsafe_allow_html=True)
                ga = c2.text_input("", value=gab.get('placar_a', ''), key=f"adm_ga_{jid}", label_visibility="collapsed")
                c3.markdown("<div style='text-align: center; padding-top: 10px;'>x</div>", unsafe_allow_html=True)
                gb = c4.text_input("", value=gab.get('placar_b', ''), key=f"adm_gb_{jid}", label_visibility="collapsed")
                c5.markdown(f"<div style='text-align: left; padding-top: 10px;'>{j['time_b']}</div>", unsafe_allow_html=True)
                
                if ga and gb:
                    dados['gabarito'][jid] = {"placar_a": ga, "placar_b": gb, "time_a": j['time_a'], "time_b": j['time_b']}
        
        with tab_m:
            for fase, qtd in MATA_MATA_ESTRUTURA.items():
                with st.expander(fase):
                    for i in range(1, qtd+1):
                        jid = f"{fase}_{i}"
                        gab = dados['gabarito'].get(jid, {})
                        
                        c1, c2, c3, c4, c5 = st.columns([3, 1, 0.5, 1, 3])
                        ta = c1.text_input("Time A Real", value=gab.get('time_a', ''), key=f"adm_ta_{jid}")
                        pa = c2.text_input("GA", value=gab.get('placar_a', ''), key=f"adm_pa_{jid}")
                        c3.markdown("x")
                        pb = c4.text_input("GB", value=gab.get('placar_b', ''), key=f"adm_pb_{jid}")
                        tb = c5.text_input("Time B Real", value=gab.get('time_b', ''), key=f"adm_tb_{jid}")
                        
                        if ta and tb:
                             dados['gabarito'][jid] = {"time_a": ta, "time_b": tb, "placar_a": pa, "placar_b": pb}

        if st.button("Atualizar Gabarito Oficial"):
            save_data(dados)
            st.success("Gabarito atualizado.")
