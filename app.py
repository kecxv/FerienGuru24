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
