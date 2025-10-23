import streamlit as st
import requests
from datetime import datetime, timedelta

# Bundesländer
BUNDESLAENDER = {
    'Baden-Württemberg': 'BW',
    'Bayern': 'BY',
    'Berlin': 'BE',
    'Brandenburg': 'BB',
    'Bremen': 'HB',
    'Hamburg': 'HH',
    'Hessen': 'HE',
    'Mecklenburg-Vorpommern': 'MV',
    'Niedersachsen': 'NI',
    'Nordrhein-Westfalen': 'NW',  # ACHTUNG: OpenHolidays nutzt NW statt NRW!
    'Rheinland-Pfalz': 'RP',
    'Saarland': 'SL',
    'Sachsen': 'SN',
    'Sachsen-Anhalt': 'ST',
    'Schleswig-Holstein': 'SH',
    'Thüringen': 'TH',
}

def fetch_holidays_and_vacations(year, country, subdivision=None):
    url = f"https://api.openholidaysapi.org/v1/{year}"
    params = {"country": country}
    if subdivision:
        params["subdivisions"] = subdivision
    try:
        resp = requests.get(url, params=params, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        # Parse holidays and vacations (API response may vary)
        holidays = []
        vacations = []
        if "holidays" in data:
            for h in data["holidays"]:
                holidays.append({
                    "date": h.get("date", ""),
                    "name": h.get("localName", h.get("name", "")),
                    "type": h.get("type", "")
                })
        if "schoolVacations" in data:
            for v in data["schoolVacations"]:
                vacations.append({
                    "name": v.get("name", v.get("type", "")),
                    "start": v.get("start"),
                    "end": v.get("end")
                })
        return holidays, vacations
    except Exception as e:
        st.error(f"Fehler beim Laden der API-Daten: {e}")
        return [], []

def main():
    st.set_page_config(page_title="Ferien & Feiertags-Checker", layout="centered")
    st.title("Ferien- & Feiertags-Checker (OpenHolidays API)")
    st.markdown("Alle Daten werden **direkt und ausschließlich von der OpenHolidays API** geladen.")

    col1, col2, col3, col4 = st.columns([2,2,2,1.5])
    with col1:
        von_datum = st.text_input("Von Datum", value="15.07.2026")
    with col2:
        bis_datum = st.text_input("Bis Datum", value="31.08.2026")
    with col3:
        bundesland_name = st.selectbox("Bundesland", list(BUNDESLAENDER.keys()), index=9)
    with col4:
        jahr = st.selectbox("Jahr", list(range(2026,2037)), index=0)
    st.divider()

    if st.button("Vergleichen"):
        try:
            dt_von = datetime.strptime(von_datum, "%d.%m.%Y")
            dt_bis = datetime.strptime(bis_datum, "%d.%m.%Y")
        except Exception:
            st.error("Ungültiges Datumsformat. Bitte TT.MM.JJJJ verwenden.")
            return

        # DE: Bundesland
        holidays_de, vacations_de = fetch_holidays_and_vacations(jahr, "DE", BUNDESLAENDER[bundesland_name])

        # DK: Dänemark
        holidays_dk, vacations_dk = fetch_holidays_and_vacations(jahr, "DK")

        st.markdown("### Vergleichsergebnis")
        col_de, col_dk = st.columns(2)

        def filter_dates(items, key_date_from, key_date_to=None):
            out = []
            for item in items:
                if key_date_to:
                    try:
                        start = datetime.strptime(item[key_date_from], "%Y-%m-%d")
                        end = datetime.strptime(item[key_date_to], "%Y-%m-%d")
                        if start <= dt_bis and end >= dt_von:
                            out.append(item)
                    except:
                        continue
                else:
                    try:
                        d = datetime.strptime(item[key_date_from], "%Y-%m-%d")
                        if dt_von <= d <= dt_bis:
                            out.append(item)
                    except:
                        continue
            return out

        with col_de:
            st.markdown(f"#### Deutschland – {bundesland_name}")
            f_holidays = filter_dates(holidays_de, "date")
            f_vacations = filter_dates(vacations_de, "start", "end")
            if f_holidays:
                st.success("Feiertage:")
                for h in f_holidays:
                    st.markdown(f"- {h['date']}: {h['name']}")
            if f_vacations:
                st.success("Ferien:")
                for v in f_vacations:
                    st.markdown(f"- {v['name']}: {v['start']} bis {v['end']}")
            if not f_holidays and not f_vacations:
                st.warning("Keine Ferien oder Feiertage im Zeitraum.")

        with col_dk:
            st.markdown("#### Dänemark")
            f_holidays = filter_dates(holidays_dk, "date")
            f_vacations = filter_dates(vacations_dk, "start", "end")
            if f_holidays:
                st.success("Feiertage:")
                for h in f_holidays:
                    st.markdown(f"- {h['date']}: {h['name']}")
            if f_vacations:
                st.success("Ferien:")
                for v in f_vacations:
                    st.markdown(f"- {v['name']}: {v['start']} bis {v['end']}")
            if not f_holidays and not f_vacations:
                st.warning("Keine Ferien oder Feiertage im Zeitraum.")

if __name__ == "__main__":
    main()
