"""Member 3: Industry adoption, ranking and changes from Eurostat survey data."""

from __future__ import annotations

import altair as alt
import streamlit as st

from src.common import OI, footer, pct, setup

size, country, sector, refresh, eu_all, years = setup("Who has adopted AI?")

st.caption("Who has adopted AI?  /  Industry intelligence")
st.header("3 · Which industries have adopted AI?")

sec_years = sorted(int(y) for y in sector["year"].unique())
latest_year = sec_years[-1]
compare_years = [y for y in sec_years if y != latest_year]

st.markdown(
    "**The story:** AI adoption is rising across European industries, but the level of uptake "
    "remains uneven. Explore who leads, how the gap evolved and where a policy adviser might "
    "investigate barriers."
)

with st.sidebar:
    st.divider()
    st.subheader("Industry explorer")
    st.caption("Adjust these controls without leaving your chart.")
    base_year = st.radio(
        f"Compare {latest_year} with",
        compare_years,
        index=0,
        horizontal=True,
        key="sector_base",
    )
    all_sectors = sorted(sector["sector"].unique())
    focus_sector = st.selectbox(
        "Industry spotlight",
        options=all_sectors,
        index=all_sectors.index("Information and communication")
        if "Information and communication" in all_sectors else 0,
        key="sector_focus",
    )
    with st.expander("Filter the 11 industries", expanded=False):
        selected_sectors = st.multiselect(
            "Industries to compare",
            options=all_sectors,
            default=all_sectors,
            key="sector_selected",
            help="Choose one or more industries; clear all to test the empty state.",
        )
    st.caption(f"{len(selected_sectors)} of {len(all_sectors)} industries selected")

st.caption(
    "**How to explore:** Use the sidebar to change filters while viewing the charts. "
    "The comparison year affects the Compare two years tab."
)

current = sector[
    (sector["year"] == latest_year) & sector["sector"].isin(selected_sectors)
].sort_values("pct_enterprises", ascending=False)
comparison = sector[
    sector["year"].isin([base_year, latest_year])
    & sector["sector"].isin(selected_sectors)
].copy()

st.caption(
    f"**Source:** Eurostat `isoc_eb_ain2`, EU27 aggregate, enterprises with 10+ persons "
    "employed, excluding financial services. **Measure:** firms using at least one AI "
    f"technology (% of firms in each industry). **Survey observations:** "
    f"{', '.join(str(y) for y in sec_years)}; 2022 is not available. "
    "Industry percentages have separate denominators and must not be added together."
)

if not current.empty:
    order = current["sector"].tolist()
    top = current.iloc[0]
    bottom = current.iloc[-1]
    difference = float(top["pct_enterprises"] - bottom["pct_enterprises"])
    history = sector[sector["sector"].isin(selected_sectors)].pivot(
        index="sector", columns="year", values="pct_enterprises"
    )
    gains = (history[latest_year] - history[sec_years[0]]).dropna().sort_values(
        ascending=False
    )

ranking_tab, heatmap_tab, compare_tab, spotlight_tab = st.tabs(
    ["2025 ranking", "Across survey years", "Compare two years", "Industry spotlight"],
    on_change="rerun",
    key="industry_chart_view",
)
with ranking_tab:
    if current.empty:
        st.info("Select at least one industry in the sidebar to view rankings and KPIs.")
    else:
        st.subheader(f"At a glance · {latest_year}")
        m1, m2, m3, m4 = st.columns(4, gap="small")
        with m1:
            st.metric("Highest adoption", pct(float(top["pct_enterprises"])))
            st.caption(top["sector"])
        with m2:
            st.metric("Lowest adoption", pct(float(bottom["pct_enterprises"])))
            st.caption(bottom["sector"])
        with m3:
            st.metric("Highest–lowest gap", f"{difference:.2f} pp")
            st.caption(f"Among {len(current)} selected industries")
        with m4:
            if not gains.empty:
                st.metric(f"Largest gain since {sec_years[0]}", f"+{gains.iloc[0]:.2f} pp")
                st.caption(gains.index[0])
            else:
                st.metric("Largest gain", "N/A")
                st.caption("Comparable observations unavailable")

        st.caption(
            "All four metrics use the selected industries. Differences are percentage points "
            "(pp), not relative percentage changes."
        )

        st.markdown(
            f"**Among the {len(current)} selected industries in {latest_year}:** "
            f"{top['sector']} led at **{pct(float(top['pct_enterprises']))}**, "
            f"while {bottom['sector'].lower()} had **{pct(float(bottom['pct_enterprises']))}**. "
            f"The difference was **{float(top['pct_enterprises'])-float(bottom['pct_enterprises']):.2f} percentage points**."
        )

        st.subheader(f"Ranking · Adoption levels in {latest_year}")
        st.caption("Visual Vocabulary: ranking. Bar length represents the percent of businesses in each industry reporting AI use. All values are printed.")
        max_val = float(current["pct_enterprises"].max())
        xscale = alt.Scale(domain=[0, min(100, max_val + 14)])
        base_rank = alt.Chart(current).encode(
            y=alt.Y("sector:N", sort=order, title=None, axis=alt.Axis(labelLimit=310, labelFontSize=12)),
            x=alt.X("pct_enterprises:Q", title="Businesses using at least one AI technology (%)", scale=xscale),
        )
        bars = base_rank.mark_bar(color=OI["blue"], size=20)
        value_labels = base_rank.mark_text(align="left", dx=7, fontSize=12, color="#F5F5F5").encode(
            text=alt.Text("pct_enterprises:Q", format=".2f")
        )
        st.altair_chart(
            (bars + value_labels).properties(height=max(300, len(order) * 34), title=f"EU27 AI use by industry, {latest_year}"),
            width="stretch",
        )

with heatmap_tab:
    if current.empty:
        st.info("Select at least one industry in the sidebar to display the heatmap.")
    else:
        st.subheader("Adoption landscape · All survey years")
        st.caption(
            "**Visual Vocabulary: heatmap / magnitude.** Each cell shows the percentage "
            "of firms using AI in that industry and survey year; every number is printed. "
            "Survey years are discrete observations, not a continuous annual series."
        )
        landscape = sector[sector["sector"].isin(selected_sectors)].copy()
        landscape["survey_year"] = landscape["year"].astype(str)
        ceiling = max(70, int(sector["pct_enterprises"].max() + 10))
        heat_base = alt.Chart(landscape).encode(
            x=alt.X(
                "survey_year:O",
                sort=[str(y) for y in sec_years],
                title="Survey year",
                axis=alt.Axis(labelAngle=0),
            ),
            y=alt.Y(
                "sector:N", sort=order, title=None,
                axis=alt.Axis(labelLimit=310, labelFontSize=12),
            ),
        )
        cells = heat_base.mark_rect(stroke="#101820", strokeWidth=3).encode(
            color=alt.Color(
                "pct_enterprises:Q", title="AI adoption (%)",
                scale=alt.Scale(
                    domain=[0, ceiling],
                    range=["#263547", "#235873", "#0B6A8B", "#0072B2"],
                ),
            ),
            tooltip=[
                alt.Tooltip("sector:N", title="Industry"),
                alt.Tooltip("year:O", title="Year"),
                alt.Tooltip("pct_enterprises:Q", title="AI adoption (%)", format=".2f"),
            ],
        )
        cell_values = heat_base.mark_text(
            color="#F5F5F5", fontSize=12, fontWeight="bold"
        ).encode(text=alt.Text("pct_enterprises:Q", format=".2f"))
        st.altair_chart(
            (cells + cell_values).properties(
                height=max(320, len(order) * 36),
                title="EU27 · Industry AI adoption by survey year (%)",
            ),
            width="stretch",
        )

with compare_tab:
    if current.empty:
        st.info("Select at least one industry in the sidebar to compare adoption years.")
    else:
        st.subheader(f"Change · {base_year} compared with {latest_year}")
        st.caption(
            f"Visual Vocabulary: change. Blue circles = {base_year}; orange diamonds = {latest_year}. "
            "Each value is labelled directly, so the comparison does not require hovering."
        )
        comparison = comparison.assign(year_label=comparison["year"].astype(str))
        common_y = alt.Y(
            "sector:N", sort=order, title=None, axis=alt.Axis(labelLimit=310, labelOverlap=False, labelFontSize=12)
        )
        common_x = alt.X(
            "pct_enterprises:Q", title="Businesses using at least one AI technology (%)",
            scale=alt.Scale(domain=[0, min(100, max_val + 14)]),
        )
        lines = alt.Chart(comparison).mark_line(color="#999999", strokeWidth=2).encode(
            y=common_y, x=common_x, detail="sector:N"
        )
        points = alt.Chart(comparison).mark_point(filled=True, size=125, opacity=1).encode(
            y=common_y,
            x=common_x,
            color=alt.Color(
                "year_label:N", title="Survey year",
                scale=alt.Scale(domain=[str(base_year), str(latest_year)], range=[OI["sky"], OI["vermillion"]]),
                legend=alt.Legend(orient="top"),
            ),
            shape=alt.Shape(
                "year_label:N",
                scale=alt.Scale(domain=[str(base_year), str(latest_year)], range=["circle", "diamond"]),
                legend=None,
            ),
        )
        earlier_labels = alt.Chart(comparison[comparison["year"] == base_year]).mark_text(
            dy=-13, fontSize=11, color="#F5F5F5"
        ).encode(y=common_y, x=common_x, text=alt.Text("pct_enterprises:Q", format=".2f"))
        latest_labels = alt.Chart(comparison[comparison["year"] == latest_year]).mark_text(
            dy=15, fontSize=11, fontWeight="bold", color="#F5F5F5"
        ).encode(y=common_y, x=common_x, text=alt.Text("pct_enterprises:Q", format=".2f"))
        st.altair_chart(
            (lines + points + earlier_labels + latest_labels).properties(
                height=max(380, len(order) * 43),
                title=f"AI use by industry, EU27, {base_year} versus {latest_year}",
            ),
            width="stretch",
        )

        leader = "Information and communication"
        leader_pair = comparison[comparison["sector"] == leader].set_index("year")["pct_enterprises"]
        if base_year in leader_pair.index and latest_year in leader_pair.index:
            change = float(leader_pair.loc[latest_year] - leader_pair.loc[base_year])
            st.markdown(
                f"**Example of change:** {leader} moved from **{pct(float(leader_pair.loc[base_year]))}** "
                f"in {base_year} to **{pct(float(leader_pair.loc[latest_year]))}** in {latest_year} "
                f"({change:+.2f} percentage points)."
            )

with spotlight_tab:
    st.subheader("Industry spotlight · Trace one industry over time")
    spotlight = sector[sector["sector"] == focus_sector].sort_values("year")
    latest_spotlight = spotlight[spotlight["year"] == latest_year]
    first_spotlight = spotlight[spotlight["year"] == sec_years[0]]
    if spotlight.empty or latest_spotlight.empty:
        st.info("No survey observations are available for the chosen industry.")
    else:
        rate_now = float(latest_spotlight.iloc[0]["pct_enterprises"])
        all_latest = sector[sector["year"] == latest_year]
        position = int((all_latest["pct_enterprises"] > rate_now).sum() + 1)
        summary = (
            f"**{focus_sector}** ranked **{position} of {len(all_latest)}** EU industries "
            f"in {latest_year}, with **{pct(rate_now)}** adoption."
        )
        if not first_spotlight.empty:
            rate_first = float(first_spotlight.iloc[0]["pct_enterprises"])
            summary += (
                f" Since {sec_years[0]}, adoption changed by "
                f"**{rate_now - rate_first:+.2f} percentage points**."
            )
        st.markdown(summary)
        focus_max = min(100, max(15, float(spotlight["pct_enterprises"].max()) + 12))
        focus_x = alt.X(
            "year:Q", title="Survey year",
            scale=alt.Scale(domain=[sec_years[0], latest_year]),
            axis=alt.Axis(values=sec_years, format="d"),
        )
        focus_y = alt.Y(
            "pct_enterprises:Q", title="Businesses using AI (%)",
            scale=alt.Scale(domain=[0, focus_max]),
        )
        focus_chart = alt.Chart(spotlight).encode(x=focus_x, y=focus_y)
        trend_line = focus_chart.mark_line(color=OI["sky"], strokeWidth=3)
        trend_points = focus_chart.mark_point(
            filled=True, color=OI["vermillion"], size=130, shape="diamond"
        )
        trend_labels = focus_chart.mark_text(
            dy=-17, color="#F5F5F5", fontSize=12, fontWeight="bold"
        ).encode(text=alt.Text("pct_enterprises:Q", format=".2f"))
        st.altair_chart(
            (trend_line + trend_points + trend_labels).properties(
                height=250,
                title=f"{focus_sector} · AI adoption by survey year (%)",
            ),
            width="stretch",
        )
        st.caption(
            "The x-axis reflects the actual year intervals, including the two-year gap "
            "from 2021 to 2023. No intervening annual observations are implied."
        )
    with st.container(border=True):
        st.subheader("What this means for policy")
        if current.empty:
            st.write("Select industries above to explore where adoption barriers may warrant study.")
        else:
            st.markdown(
                f"For **Maya**, the **{bottom['sector'].lower()}** sector's "
                f"**{pct(float(bottom['pct_enterprises']))}** adoption rate in {latest_year} "
                "makes it a candidate for investigating possible barriers to adoption. "
                "This does not show that subsidies, training or other interventions "
                "would necessarily work."
            )

    st.caption(
        "**Interpretation limit:** These are survey-based industry adoption rates, not numbers of firms "
        "or measures of productivity. Industry percentages cannot be added together; the data alone "
        "cannot establish why adoption changed. Survey definitions and breaks may affect year comparisons."
    )

footer(refresh)
