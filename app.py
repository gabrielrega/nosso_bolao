import streamlit as st
import pandas as pd
import os
import json

# --- CONFIGURAÇÃO: TABELA DE JOGOS REAIS ---
# O Admin deve preencher aqui os jogos reais da Copa.
# Exemplo preenchido com alguns jogos fictícios para teste.

TABELA_GRUPOS = [
    # GRUPO A: México, África do Sul, Coreia do Sul, Repescagem UEFA D
    {"id": "A1", "grupo": "A", "time_a": "México", "time_b": "África do Sul"},
    {"id": "A2", "grupo": "A", "time_a": "Coreia do Sul", "time_b": "Repescagem UEFA D"},
    {"id": "A3", "grupo": "A", "time_a": "Repescagem UEFA D", "time_b": "África do Sul"},
    {"id": "A4", "grupo": "A", "time_a": "México", "time_b": "Coreia do Sul"},
    {"id": "A5", "grupo": "A", "time_a": "Repescagem UEFA D", "time_b": "México"},
    {"id": "A6", "grupo": "A", "time_a": "África do Sul", "time_b": "Coreia do Sul"},

    # GRUPO B: Canadá, Suíça, Catar, Repescagem UEFA A
    {"id": "B1", "grupo": "B", "time_a": "Canadá", "time_b": "Repescagem UEFA A"},
    {"id": "B2", "grupo": "B", "time_a": "Catar", "time_b": "Suíça"},
    {"id": "B3", "grupo": "B", "time_a": "Suíça", "time_b": "Repescagem UEFA A"},
    {"id": "B4", "grupo": "B", "time_a": "Canadá", "time_b": "Catar"},
    {"id": "B5", "grupo": "B", "time_a": "Suíça", "time_b": "Canadá"},
    {"id": "B6", "grupo": "B", "time_a": "Repescagem UEFA A", "time_b": "Catar"},

    # GRUPO C: Brasil, Marrocos, Escócia, Haiti
    {"id": "C1", "grupo": "C", "time_a": "Brasil", "time_b": "Marrocos"},
    {"id": "C2", "grupo": "C", "time_a": "Haiti", "time_b": "Escócia"},
    {"id": "C3", "grupo": "C", "time_a": "Escócia", "time_b": "Marrocos"},
    {"id": "C4", "grupo": "C", "time_a": "Brasil", "time_b": "Haiti"},
    {"id": "C5", "grupo": "C", "time_a": "Escócia", "time_b": "Brasil"},
    {"id": "C6", "grupo": "C", "time_a": "Marrocos", "time_b": "Haiti"},

    # GRUPO D: EUA, Paraguai, Austrália, Repescagem UEFA C
    {"id": "D1", "grupo": "D", "time_a": "EUA", "time_b": "Paraguai"},
    {"id": "D2", "grupo": "D", "time_a": "Austrália", "time_b": "Repescagem UEFA C"},
    {"id": "D3", "grupo": "D", "time_a": "EUA", "time_b": "Austrália"},
    {"id": "D4", "grupo": "D", "time_a": "Repescagem UEFA C", "time_b": "Paraguai"},
    {"id": "D5", "grupo": "D", "time_a": "Repescagem UEFA C", "time_b": "EUA"},
    {"id": "D6", "grupo": "D", "time_a": "Paraguai", "time_b": "Austrália"},

    # GRUPO E: Alemanha, Curaçao, C. do Marfim, Equador
    {"id": "E1", "grupo": "E", "time_a": "Alemanha", "time_b": "Curaçao"},
    {"id": "E2", "grupo": "E", "time_a": "Costa do Marfim", "time_b": "Equador"},
    {"id": "E3", "grupo": "E", "time_a": "Alemanha", "time_b": "Costa do Marfim"},
    {"id": "E4", "grupo": "E", "time_a": "Equador", "time_b": "Curaçao"},
    {"id": "E5", "grupo": "E", "time_a": "Equador", "time_b": "Alemanha"},
    {"id": "E6", "grupo": "E", "time_a": "Curaçao", "time_b": "Costa do Marfim"},

    # GRUPO F: Holanda, Japão, Repescagem UEFA B, Tunísia
    {"id": "F1", "grupo": "F", "time_a": "Holanda", "time_b": "Japão"},
    {"id": "F2", "grupo": "F", "time_a": "Repescagem UEFA B", "time_b": "Tunísia"},
    {"id": "F3", "grupo": "F", "time_a": "Holanda", "time_b": "Repescagem UEFA B"},
    {"id": "F4", "grupo": "F", "time_a": "Tunísia", "time_b": "Japão"},
    {"id": "F5", "grupo": "F", "time_a": "Tunísia", "time_b": "Holanda"},
    {"id": "F6", "grupo": "F", "time_a": "Japão", "time_b": "Repescagem UEFA B"},

    # GRUPO G: Bélgica, Egito, Irã, Nova Zelândia
    {"id": "G1", "grupo": "G", "time_a": "Bélgica", "time_b": "Egito"},
    {"id": "G2", "grupo": "G", "time_a": "Irã", "time_b": "Nova Zelândia"},
    {"id": "G3", "grupo": "G", "time_a": "Bélgica", "time_b": "Irã"},
    {"id": "G4", "grupo": "G", "time_a": "Nova Zelândia", "time_b": "Egito"},
    {"id": "G5", "grupo": "G", "time_a": "Nova Zelândia", "time_b": "Bélgica"},
    {"id": "G6", "grupo": "G", "time_a": "Egito", "time_b": "Irã"},

    # GRUPO H: Espanha, Cabo Verde, Arábia Saudita, Uruguai
    {"id": "H1", "grupo": "H", "time_a": "Espanha", "time_b": "Cabo Verde"},
    {"id": "H2", "grupo": "H", "time_a": "Arábia Saudita", "time_b": "Uruguai"},
    {"id": "H3", "grupo": "H", "time_a": "Espanha", "time_b": "Arábia Saudita"},
    {"id": "H4", "grupo": "H", "time_a": "Uruguai", "time_b": "Cabo Verde"},
    {"id": "H5", "grupo": "H", "time_a": "Uruguai", "time_b": "Espanha"},
    {"id": "H6", "grupo": "H", "time_a": "Cabo Verde", "time_b": "Arábia Saudita"},

    # GRUPO I: França, Senegal, Repescagem FIFA 2, Noruega
    {"id": "I1", "grupo": "I", "time_a": "França", "time_b": "Senegal"},
    {"id": "I2", "grupo": "I", "time_a": "Repescagem FIFA 2", "time_b": "Noruega"},
    {"id": "I3", "grupo": "I", "time_a": "França", "time_b": "Repescagem FIFA 2"},
    {"id": "I4", "grupo": "I", "time_a": "Noruega", "time_b": "Senegal"},
    {"id": "I5", "grupo": "I", "time_a": "Noruega", "time_b": "França"},
    {"id": "I6", "grupo": "I", "time_a": "Senegal", "time_b": "Repescagem FIFA 2"},

    # GRUPO J: Argentina, Argélia, Áustria, Jordânia
    {"id": "J1", "grupo": "J", "time_a": "Argentina", "time_b": "Argélia"},
    {"id": "J2", "grupo": "J", "time_a": "Áustria", "time_b": "Jordânia"},
    {"id": "J3", "grupo": "J", "time_a": "Argentina", "time_b": "Áustria"},
    {"id": "J4", "grupo": "J", "time_a": "Jordânia", "time_b": "Argélia"},
    {"id": "J5", "grupo": "J", "time_a": "Jordânia", "time_b": "Argentina"},
    {"id": "J6", "grupo": "J", "time_a": "Argélia", "time_b": "Áustria"},

    # GRUPO K: Portugal, Repescagem FIFA 1, Uzbequistão, Colômbia
    {"id": "K1", "grupo": "K", "time_a": "Portugal", "time_b": "Repescagem FIFA 1"},
    {"id": "K2", "grupo": "K", "time_a": "Uzbequistão", "time_b": "Colômbia"},
    {"id": "K3", "grupo": "K", "time_a": "Portugal", "time_b": "Uzbequistão"},
    {"id": "K4", "grupo": "K", "time_a": "Colômbia", "time_b": "Repescagem FIFA 1"},
    {"id": "K5", "grupo": "K", "time_a": "Colômbia", "time_b": "Portugal"},
    {"id": "K6", "grupo": "K", "time_a": "Repescagem FIFA 1", "time_b": "Uzbequistão"},

    # GRUPO L: Inglaterra, Croácia, Gana, Panamá
    {"id": "L1", "grupo": "L", "time_a": "Inglaterra", "time_b": "Croácia"},
    {"id": "L2", "grupo": "L", "time_a": "Gana", "time_b": "Panamá"},
    {"id": "L3", "grupo": "L", "time_a": "Inglaterra", "time_b": "Gana"},
    {"id": "L4", "grupo": "L", "time_a": "Panamá", "time_b": "Croácia"},
    {"id": "L5", "grupo": "L", "time_a": "Panamá", "time_b": "Inglaterra"},
    {"id": "L6", "grupo": "L", "time_a": "Croácia", "time_b": "Gana"},
]
# Definição dos confrontos de Mata-Mata (Slots vazios para preencher)
MATA_MATA_ESTRUTURA = {
    "16avos": 16, # 16 jogos
    "Oitavas": 8,
    "Quartas": 4,
    "Semi": 2,
    "Final": 1,
    "3Lugar": 1
}

FILE_DB = 'bolao_db.json'

REGRAS = {
    'Grupos': {'cheio': 3, 'gol': 1},
    '16avos': {'time': 5, 'cheio': 3, 'gol': 1}, # Regra da Regressão Linear
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
    
    # 1. Pontos de Time (Só no Mata-Mata)
    if fase != 'Grupos':
        times_p = {palpite.get('time_a', '').strip().lower(), palpite.get('time_b', '').strip().lower()}
        times_g = {gabarito.get('time_a', '').strip().lower(), gabarito.get('time_b', '').strip().lower()}
        # Interseção ignora vazios
        times_p.discard('')
        times_g.discard('')
        acertos = len(times_p.intersection(times_g))
        pts += acertos * REGRAS[fase]['time']

    # 2. Pontos de Placar (Só se acertar o confronto exato)
    match_valido = True
    if fase != 'Grupos':
        # No mata-mata, placar só vale se acertar OS DOIS times
        tp = {palpite.get('time_a', '').strip().lower(), palpite.get('time_b', '').strip().lower()}
        tg = {gabarito.get('time_a', '').strip().lower(), gabarito.get('time_b', '').strip().lower()}
        if tp != tg or len(tp) < 2:
            match_valido = False
    
    if match_valido and gabarito.get('placar_a') is not None:
        try:
            pa, pb = int(palpite['placar_a']), int(palpite['placar_b'])
            ga, gb = int(gabarito['placar_a']), int(gabarito['placar_b'])
            
            # Resultado (V/E/D)
            venc_p = 'A' if pa > pb else ('B' if pb > pa else 'E')
            venc_g = 'A' if ga > gb else ('B' if gb > ga else 'E')
            
            if venc_p == venc_g:
                pts += REGRAS[fase]['cheio']
            
            # Gols (Sem inversão)
            if pa == ga: pts += REGRAS[fase]['gol']
            if pb == gb: pts += REGRAS[fase]['gol']
        except:
            pass
            
    return pts

# --- INTERFACE ---
st.set_page_config(page_title="Bolão Copa 48 - Oficial", layout="wide")
st.title("⚽ Bolão da Copa - 48 Times")

dados = load_data()
menu = st.sidebar.selectbox("Navegação", ["Meus Palpites", "Ranking Geral", "Área Admin"])

if menu == "Meus Palpites":
    st.header("Preencha sua Tabela")
    user = st.text_input("Seu Nome (Identificação):")
    
    if user:
        if user not in dados['participantes']: dados['participantes'][user] = {}
        
        tab1, tab2 = st.tabs(["1ª Fase: Grupos (Jogos Reais)", "2ª Fase: Mata-Mata (Simulação)"])
        
        # --- ABA 1: FASE DE GRUPOS ---
        with tab1:
            st.subheader("Jogos da Fase de Grupos")
            st.info("Preencha os placares dos jogos já definidos.")
            
            # Agrupar jogos por grupo para visualização
            jogos_por_grupo = {}
            for j in TABELA_GRUPOS:
                g = j['grupo']
                if g not in jogos_por_grupo: jogos_por_grupo[g] = []
                jogos_por_grupo[g].append(j)
            
            cols = st.columns(3)
            idx_col = 0
            
            for grupo, lista_jogos in jogos_por_grupo.items():
                with cols[idx_col % 3]:
                    st.markdown(f"### Grupo {grupo}")
                    for jogo in lista_jogos:
                        jid = jogo['id']
                        palpite = dados['participantes'][user].get(jid, {})
                        
                        c1, c2, c3, c4 = st.columns([3, 1, 0.5, 1])
                        c1.caption(f"{jogo['time_a']} x {jogo['time_b']}")
                        pa = c2.text_input(f"A_{jid}", value=palpite.get('placar_a', ''), label_visibility="collapsed", key=f"p_a_{jid}_{user}")
                        c3.text("x")
                        pb = c4.text_input(f"B_{jid}", value=palpite.get('placar_b', ''), label_visibility="collapsed", key=f"p_b_{jid}_{user}")
                        
                        # Salva automaticamente na estrutura (Time A e B são fixos aqui)
                        dados['participantes'][user][jid] = {
                            "time_a": jogo['time_a'], "time_b": jogo['time_b'],
                            "placar_a": pa, "placar_b": pb
                        }
                    st.divider()
                idx_col += 1
        
        # --- ABA 2: MATA-MATA (TUDO DE UMA VEZ) ---
        with tab2:
            st.subheader("O Caminho até a Final")
            st.warning("Aqui você define quem passa! Digite o nome das seleções e o placar previsto.")
            
            for fase, qtd in MATA_MATA_ESTRUTURA.items():
                with st.expander(f"{fase} ({qtd} jogos)", expanded=(fase=="16avos")):
                    for i in range(1, qtd + 1):
                        jid = f"{fase}_{i}"
                        palpite = dados['participantes'][user].get(jid, {})
                        
                        st.markdown(f"**Jogo {i}**")
                        c1, c2, c3, c4, c5 = st.columns([3, 1, 0.5, 1, 3])
                        
                        ta = c1.text_input("Time A", value=palpite.get('time_a', ''), key=f"t_a_{jid}_{user}", placeholder="Ex: Brasil")
                        pa = c2.text_input("Gols", value=palpite.get('placar_a', ''), key=f"p_a_{jid}_{user}")
                        c3.markdown("x")
                        pb = c4.text_input("Gols ", value=palpite.get('placar_b', ''), key=f"p_b_{jid}_{user}")
                        tb = c5.text_input("Time B", value=palpite.get('time_b', ''), key=f"t_b_{jid}_{user}", placeholder="Ex: Argentina")
                        
                        dados['participantes'][user][jid] = {
                            "time_a": ta, "time_b": tb,
                            "placar_a": pa, "placar_b": pb
                        }

        if st.button("💾 SALVAR TUDO"):
            save_data(dados)
            st.success("✅ Palpites registrados com sucesso!")

elif menu == "Ranking Geral":
    st.header("🏆 Classificação")
    if not dados['participantes']:
        st.write("Ainda não há palpites.")
    else:
        resumo = []
        for p_user, p_dict in dados['participantes'].items():
            pts_total = 0
            for jid, gab in dados['gabarito'].items():
                palp = p_dict.get(jid)
                if palp:
                    # Descobre a fase pelo ID
                    fase = 'Grupos'
                    for f in REGRAS.keys():
                        if f in jid: fase = f; break
                    
                    pts_total += calcular_pontos(palp, gab, fase)
            resumo.append({"Participante": p_user, "Pontos": pts_total})
        
        df = pd.DataFrame(resumo).sort_values("Pontos", ascending=False)
        st.dataframe(df, use_container_width=True)

elif menu == "Área Admin":
    pass_input = st.text_input("Senha Admin", type="password")
    if pass_input == "admin123":
        st.info("Aqui você preenche os RESULTADOS REAIS conforme eles acontecem.")
        
        tab_g_adm, tab_m_adm = st.tabs(["Resultados Grupos", "Resultados Mata-Mata"])
        
        with tab_g_adm:
            for j in TABELA_GRUPOS:
                jid = j['id']
                gab = dados['gabarito'].get(jid, {})
                c1, c2, c3, c4 = st.columns([3,1,0.5,1])
                c1.write(f"{j['time_a']} x {j['time_b']}")
                ga = c2.text_input("Gols A", value=gab.get('placar_a', ''), key=f"adm_a_{jid}")
                gb = c4.text_input("Gols B", value=gab.get('placar_b', ''), key=f"adm_b_{jid}")
                
                if ga and gb:
                    dados['gabarito'][jid] = {"placar_a": ga, "placar_b": gb, "time_a": j['time_a'], "time_b": j['time_b']}
        
        with tab_m_adm:
            st.write("Preencha os classificados e placares reais.")
            for fase, qtd in MATA_MATA_ESTRUTURA.items():
                with st.expander(fase):
                    for i in range(1, qtd+1):
                        jid = f"{fase}_{i}"
                        gab = dados['gabarito'].get(jid, {})
                        
                        c1, c2, c3, c4, c5 = st.columns([3, 1, 0.5, 1, 3])
                        ta = c1.text_input("Time A Real", value=gab.get('time_a', ''), key=f"adm_ta_{jid}")
                        pa = c2.text_input("Gols A", value=gab.get('placar_a', ''), key=f"adm_pa_{jid}")
                        pb = c4.text_input("Gols B", value=gab.get('placar_b', ''), key=f"adm_pb_{jid}")
                        tb = c5.text_input("Time B Real", value=gab.get('time_b', ''), key=f"adm_tb_{jid}")
                        
                        if ta and tb:
                             dados['gabarito'][jid] = {"time_a": ta, "time_b": tb, "placar_a": pa, "placar_b": pb}

        if st.button("Atualizar Gabarito"):
            save_data(dados)
            st.success("Resultados oficiais atualizados!")
