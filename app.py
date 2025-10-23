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
        if gef_ferien:
            ferien_text = ""
            for f in gef_ferien:
                ferien_text += f"- {f['name'][0]['text']} ({f['startDate']} bis {f['endDate']})\n"
            st.success(ferien_text)
        if gef_feiertage:
            feiertage_text = ""
            for h in gef_feiertage:
                feiertage_text += f"- {h['name'][0]['text']} ({h['date']})\n"
            st.info(feiertage_text)
        if not gef_ferien and not gef_feiertage:
            st.warning("Keine Ferien oder Feiertage im Zeitraum.")

    with col_dk:
        st.markdown("#### Dänemark")
        gef_ferien = filter_ferien(ferien_dk, dt_von, dt_bis)
        gef_feiertage = filter_feiertage(feiertage_dk, dt_von, dt_bis)
        if gef_ferien:
            ferien_text = ""
            for f in gef_ferien:
                ferien_text += f"- {f['name'][0]['text']} ({f['startDate']} bis {f['endDate']})\n"
            st.success(ferien_text)
        if gef_feiertage:
            feiertage_text = ""
            for h in gef_feiertage:
                feiertage_text += f"- {h['name'][0]['text']} ({h['date']})\n"
            st.info(feiertage_text)
        if not gef_ferien and not gef_feiertage:
            st.warning("Keine Ferien oder Feiertage im Zeitraum.")
