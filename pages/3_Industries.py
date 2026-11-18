"""Member 3: Industry adoption, ranking and changes from Eurostat survey data."""

from __future__ import annotations

import altair as alt
import streamlit as st

from src.common import OI, footer, pct, setup

size, country, sector, refresh, eu_all, years = setup("Who has adopted AI?")

st.caption("Who has adopted AI? · Industries")
st.divider()
st.header("3 · Which industries have adopted AI?")

sec_years = sorted(int(y) for y in sector["year"].unique())
latest_year = sec_years[-1]
compare_years = [y for y in sec_years if y != latest_year]

st.markdown(
    "AI adoption has risen in many industries, but **the level of adoption remains uneven**. "
    "Use the 2025 ranking to find leaders and laggards, then compare it with an earlier survey year."
)

base_year = st.radio(
    "Earlier year to compare with 2025",
    compare_years,
    index=0,
    horizontal=True,
    key="sector_base",
)
all_sectors = sorted(sector["sector"].unique())
selected_sectors = st.multiselect(
    "Industries to display",
    options=all_sectors,
    default=all_sectors,
    key="sector_selected",
    help="Deselect all to see the empty-state message, or select the sectors you want to compare.",
)

current = sector[
    (sector["year"] == latest_year) & sector["sector"].isin(selected_sectors)
].sort_values("pct_enterprises", ascending=False)
comparison = sector[
    sector["year"].isin([base_year, latest_year])
    & sector["sector"].isin(selected_sectors)
].copy()

st.caption(
    f"Source: Eurostat isoc_eb_ain2; EU27, enterprises with 10 or more persons employed, "
    f"excluding financial services. Survey years: {base_year} and {latest_year}. "
    "Unit: % of enterprises within each industry using at least one AI technology. "
    "The percentages are separate denominators, not shares that add to 100%."
)

if not selected_sectors or current.empty or comparison.empty:
    st.info("No industries selected or no observations available. Select at least one industry to display the charts.")
else:
    order = current["sector"].tolist()
    top = current.iloc[0]
    bottom = current.iloc[-1]
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
    value_labels = base_rank.mark_text(align="left", dx=7, fontSize=12, color="#222222").encode(
        text=alt.Text("pct_enterprises:Q", format=".2f")
    )
    st.altair_chart(
        (bars + value_labels).properties(height=max(300, len(order) * 34), title=f"EU27 AI use by industry, {latest_year}"),
        width="stretch",
    )

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
        dy=-13, fontSize=11, color="#222222"
    ).encode(y=common_y, x=common_x, text=alt.Text("pct_enterprises:Q", format=".2f"))
    latest_labels = alt.Chart(comparison[comparison["year"] == latest_year]).mark_text(
        dy=15, fontSize=11, fontWeight="bold", color="#222222"
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

st.caption(
    "**Interpretation limit:** These are survey-based industry adoption rates, not numbers of firms "
    "or measures of productivity. Industry percentages cannot be added together; the data alone "
    "cannot establish why adoption changed. Survey definitions and breaks may affect year comparisons."
)
footer(refresh)
