import streamlit as st
import requests
import pandas as pd

API_URL = "https://initial-min-mountain-chevy.trycloudflare.com"

st.set_page_config(page_title="Maintenance IA", page_icon="⚙️", layout="wide")

st.markdown("""
<style>
.stApp {background: #07111f; color: white;}
[data-testid="stSidebar"] {background: #0b1220;}
.card {
    background: #111827;
    padding: 22px;
    border-radius: 18px;
    border: 1px solid #1f2937;
    box-shadow: 0 0 18px rgba(0,0,0,0.25);
}
.big-title {
    font-size: 42px;
    font-weight: 800;
}
.subtitle {
    color: #9ca3af;
    font-size: 18px;
}
.stButton>button {
    background: #2563eb;
    color: white;
    border-radius: 12px;
    height: 48px;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

st.sidebar.title("⚙️ Maintenance IA")
page = st.sidebar.radio(
    "Navigation",
    [
        "🏠 Accueil",
        "🔮 Prédiction",
        "📊 KPI",
        "🔎 Recherche d’actif",
        "🚨 Alertes",
        "🛠️ Recommandations"
    ]
)
# ================= INFORMATIONS UTILISATEUR =================

st.sidebar.subheader("👤 Informations utilisateur")

nom_user = st.sidebar.text_input("Nom complet")
email_user = st.sidebar.text_input("Email")
role_user = st.sidebar.selectbox(
    "Rôle",
    [
        "Technicien maintenance",
        "Ingénieur maintenance",
        "Responsable production",
        "Étudiant"
    ]
)

if nom_user:
    st.sidebar.success(f"Bienvenue {nom_user}")
st.markdown('<div class="big-title">Maintenance prédictive</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Solution IA + API + application web pour la fiabilité industrielle</div>', unsafe_allow_html=True)
st.write("")

# ================= ACCUEIL =================
if page == "🏠 Accueil":
    c1, c2, c3 = st.columns(3)

    with c1:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("🤖 Intelligence Artificielle")
        st.write("Modèle Random Forest pour prédire le risque de panne.")
        st.markdown('</div>', unsafe_allow_html=True)

    with c2:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("🔗 API FastAPI")
        st.write("Endpoints : /prediction, /kpi, /equipements, /alertes.")
        st.markdown('</div>', unsafe_allow_html=True)

    with c3:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("🖥️ Interface Streamlit")
        st.write("Application interactive pour utiliser le modèle facilement.")
        st.markdown('</div>', unsafe_allow_html=True)

    st.info("Architecture : Utilisateur → Interface Streamlit → API FastAPI → Modèle IA → Résultat")

# ================= PREDICTION =================
elif page == "🔮 Prédiction":
    st.subheader("🔮 Prédiction manuelle du risque de panne")

    col1, col2, col3 = st.columns(3)

    with col1:
        temp = st.number_input("🌡 Température (°C)", value=82.0)
        pressure = st.number_input("⚙️ Pression (bar)", value=6.5)
        backlog = st.number_input("📦 Backlog maintenance", value=3)

    with col2:
        vib = st.number_input("📳 Vibration (mm/s)", value=6.7)
        humidity = st.number_input("💧 Humidité (%)", value=61.0)
        health = st.number_input("❤️ HealthScore", value=45.0)

    with col3:
        current = st.number_input("⚡ Courant (A)", value=58.0)
        alarm = st.number_input("🚨 Alarmes 7 jours", value=4)

    if st.button("Lancer la prédiction", use_container_width=True):
        data = {
            "Temperature_C": temp,
            "Vibration_mm_s": vib,
            "Current_A": current,
            "Pressure_bar": pressure,
            "Humidity_pct": humidity,
            "AlarmCount7D": int(alarm),
            "MaintenanceBacklog": int(backlog),
            "HealthScore": health
        }

        try:
            r = requests.post(API_URL + "/prediction", json=data)
            result = r.json()

            st.success("Prédiction réalisée avec succès")

            c1, c2, c3 = st.columns(3)
            c1.metric("Probabilité de panne", f"{result['prob_panne']*100:.2f} %")
            c2.metric("Classe prédite", result["classe"])
            c3.metric("RUL estimé", f"{result['RUL']} jours")

            st.warning(f"Niveau de risque : {result.get('niveau_risque', 'non défini')}")
            st.info(result.get("recommandation", "Aucune recommandation"))

        except Exception as e:
            st.error("Erreur : impossible de contacter l’API.")
            st.write(e)

# ================= KPI =================
elif page == "📊 KPI":
    st.subheader("📊 Consultation des KPI")

    try:
        r = requests.get(API_URL + "/kpi/avance")
        kpi = r.json()

        c1, c2, c3 = st.columns(3)
        c1.metric("MTBF", kpi["MTBF"])
        c2.metric("MTTR", kpi["MTTR"])
        c3.metric("Disponibilité", f"{kpi['Disponibilite']*100:.2f} %")

        st.write("Les KPI permettent d’évaluer la fiabilité, la maintenabilité et la disponibilité des équipements.")

    except Exception as e:
        st.error("Erreur lors de la récupération des KPI.")
        st.write(e)

# ================= RECHERCHE ACTIF =================
elif page == "🔎 Recherche d’actif":
    st.subheader("🔎 Recherche avancée d’un actif")

    texte = st.text_input("Entrez le nom ou une partie du nom de l’équipement")

    if st.button("Rechercher", use_container_width=True):
        try:
            r = requests.get(API_URL + f"/equipements/recherche/{texte}")

            if r.status_code == 200:
                resultats = r.json()

                st.success(f"{len(resultats)} équipement(s) trouvé(s)")

                for eq in resultats:
                    st.write("### Équipement trouvé")
                    st.json(eq)

                    df_eq = pd.DataFrame([eq])
                    st.dataframe(df_eq, use_container_width=True)
            else:
                st.warning("Aucun équipement trouvé.")

        except Exception as e:
            st.error("Erreur lors de la recherche.")
            st.write(e)
# ================= ALERTES =================
elif page == "🚨 Alertes":
    st.subheader("🚨 Détection d’alertes")

    try:
        r = requests.get(API_URL + "/alertes")
        alertes = r.json()["alertes"]

        for alerte in alertes:
            st.error(
                f"**{alerte['equipement']}** | {alerte['type']} | Niveau : {alerte['niveau']}\n\n"
                f"{alerte['message']}"
            )

    except Exception as e:
        st.error("Erreur lors du chargement des alertes.")
        st.write(e)

# ================= RECOMMANDATIONS =================
elif page == "🛠️ Recommandations":
    st.subheader("🛠️ Recommandations de maintenance")

    try:
        r = requests.get(API_URL + "/recommandations")
        recommandations = r.json()["recommandations"]

        for rec in recommandations:
            st.success(
                f"**Niveau de risque : {rec['niveau_risque']}**\n\n"
                f"Action recommandée : {rec['action']}"
            )

    except Exception as e:
        st.error("Erreur lors du chargement des recommandations.")
        st.write(e)
            
