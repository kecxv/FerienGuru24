import streamlit as st
import requests
from datetime import datetime, timedelta

# Bundesländer (ISO Codes für die API!)
BUNDESLAENDER = {
    'Baden-Württemberg': 'DE-BW',
    'Bayern': 'DE-BY',
    'Berlin': 'DE-BE',
    'Brandenburg': 'DE-BB',
    'Bremen': 'DE-HB',
    'Hamburg': 'DE-HH',
    'Hessen': 'DE-HE',
    'Mecklenburg-Vorpommern': 'DE-MV',
    'Niedersachsen': 'DE-NI',
    'Nordrhein-Westfalen': 'DE-NW',
    'Rheinland-Pfalz': 'DE-RP',
    'Saarland': 'DE-SL',
    'Sachsen': 'DE-SN',
    'Sachsen-Anhalt': 'DE-ST',
    'Schleswig-Holstein': 'DE-SH',
    'Thüringen': 'DE-TH',
}

def get_school_holidays(year, country_code, subdivision_code=None):
    url = "https://openholidaysapi.org/SchoolHolidays"
    params = {
        "countryIsoCode": country_code,
        "validFrom": f"{year}-01-01",
        "validTo": f"{year}-12-31",
        "languageIsoCode": "DE"
    }
    if subdivision_code:
        params["subdivisionCode"] = subdivision_code
    try:
        resp = requests.get(url, params=params, timeout=10)
        resp.raise_for_status()
        return resp.json()
    except Exception as e:
        st.error(f"Fehler beim Laden der Ferien-Daten: {e}")
        return []

def get_public_holidays_by_date(date, language_code="DE"):
    url = "https://openholidaysapi.org/PublicHolidaysByDate"
    params = {
        "date": date,
        "languageIsoCode": language_code
    }
    try:
        resp = requests.get(url, params=params, timeout=10)
        resp.raise_for_status()
        return resp.json()
    except Exception as e:
        st.error(f"Fehler beim Laden der Feiertags-Daten: {e}")
        return []

def main():
    st.set_page_config(page_title="Ferien & Feiertage Checker", layout="centered")
    st.title("Ferien- & Feiertags-Checker (OpenHolidays API)")
    st.markdown("Daten aus der **OpenHolidays API** für Deutschland und Dänemark.")

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

        # Deutschland Schulferien & Feiertage
        ferien_de = get_school_holidays(jahr, "DE", BUNDESLAENDER[bundesland_name])
        feiertage_de = []
        tag = dt_von
        while tag <= dt_bis:
            feiertage_de += get_public_holidays_by_date(tag.strftime("%Y-%m-%d"), "DE")
            tag += timedelta(days=1)

        # Dänemark Schulferien & Feiertage
        ferien_dk = get_school_holidays(jahr, "DK")
        feiertage_dk = []
        tag = dt_von
        while tag <= dt_bis:
            feiertage_dk += get_public_holidays_by_date(tag.strftime("%Y-%m-%d"), "DA")
            tag += timedelta(days=1)

        st.markdown("### Vergleichsergebnis")
        col_de, col_dk = st.columns(2)

        def filter_ferien(ferien, dt_von, dt_bis):
            result = []
            for entry in ferien:
                try:
                    start = datetime.strptime(entry['startDate'], "%Y-%m-%d")
                    end = datetime.strptime(entry['endDate'], "%Y-%m-%d")
                    if start <= dt_bis and end >= dt_von:
                        result.append(entry)
                except:
                    continue
            return result

        def filter_feiertage(feiertage, dt_von, dt_bis):
            result = []
            for entry in feiertage:
                try:
                    date = datetime.strptime(entry['date'], "%Y-%m-%d")
                    if dt_von <= date <= dt_bis:
                        result.append(entry)
                except:
                    continue
            return result

      with col_de:
    st.markdown(f"#### Deutschland – {bundesland_name}")

    gef_ferien = filter_ferien(ferien_de, dt_von, dt_bis)
    gef_feiertage = filter_feiertage(feiertage_de, dt_von, dt_bis)

    # Ferien im grünen Container
    if gef_ferien:
        ferien_text = ""
        for f in gef_ferien:
            ferien_text += f"- {f['name']} ({f['startDate']} bis {f['endDate']})\n"
        st.success(ferien_text)
    # Feiertage im blauen Container
    if gef_feiertage:
        feiertage_text = ""
        for h in gef_feiertage:
            feiertage_text += f"- {h['name']} ({h['date']})\n"
        st.info(feiertage_text)
    # Warnung, falls nichts gefunden
    if not gef_ferien and not gef_feiertage:
        st.warning("Keine Ferien oder Feiertage im Zeitraum.")

with col_dk:
    st.markdown("#### Dänemark")
    gef_ferien = filter_ferien(ferien_dk, dt_von, dt_bis)
    gef_feiertage = filter_feiertage(feiertage_dk, dt_von, dt_bis)
    if gef_ferien:
        ferien_text = ""
        for f in gef_ferien:
            ferien_text += f"- {f['name']} ({f['startDate']} bis {f['endDate']})\n"
        st.success(ferien_text)
    if gef_feiertage:
        feiertage_text = ""
        for h in gef_feiertage:
            feiertage_text += f"- {h['name']} ({h['date']})\n"
        st.info(feiertage_text)
    if not gef_ferien and not gef_feiertage:
        st.warning("Keine Ferien oder Feiertage im Zeitraum.")
        
if __name__ == "__main__":
    main()
