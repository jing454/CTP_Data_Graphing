import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_title="Movie Ratings Explorer", page_icon="\U0001F3AC", layout="wide")

st.markdown("""
<style>
:root { color-scheme: dark; }
.stApp {
    background:
        radial-gradient(circle at 50% -20%, #2A2925 0%, #1B1A18 38%, #141413 78%);
    color: #F4F1EB;
}
[data-testid="stHeader"] { background: rgba(20, 20, 19, 0.92); }
[data-testid="stSidebar"] { background: #1E1E1C; border-right: 1px solid #343330; }
[data-testid="stMainBlockContainer"] { max-width: 1440px; padding-top: 2.2rem; }
h1, h2, h3, p, label, .stCaption { color: #F4F1EB; }
h1 { letter-spacing: -0.035em; }
[data-testid="stMarkdownContainer"] a { color: #FF9D5C; }
[data-testid="stAlert"] { background: #242320; border: 1px solid #514236; color: #F4F1EB; }
[data-testid="stDataFrame"] { border: 1px solid #343330; border-radius: 10px; overflow: hidden; }
[data-testid="stTabs"] button[role="tab"] { color: #B7B3AA; }
[data-testid="stTabs"] button[role="tab"][aria-selected="true"] { color: #FF9D5C; border-bottom-color: #FF9D5C; }
button[kind="secondary"], [data-baseweb="select"] > div, [data-baseweb="input"] > div { background: #242320; border-color: #45433F; color: #F4F1EB; }
hr { border-color: #343330; }
</style>
""", unsafe_allow_html=True)

px.defaults.template = "plotly_dark"
px.defaults.color_discrete_sequence = ["#FF9D5C", "#D9824B", "#B8673B", "#8E4F31"]

st.title("\U0001F3AC Movie Ratings Explorer")
st.caption("A visual summary of the movie rating data provided.")

genre_data = [
    ("Drama", 725, 43.1), ("Comedy", 505, 30.0), ("Thriller", 251, 14.9),
    ("Action", 251, 14.9), ("Romance", 247, 14.7), ("Adventure", 135, 8.0),
    ("Children", 122, 7.3), ("Crime", 109, 6.5), ("Sci-Fi", 101, 6.0),
    ("Horror", 92, 5.5), ("War", 71, 4.2), ("Mystery", 61, 3.6),
    ("Musical", 56, 3.3), ("Documentary", 50, 3.0), ("Animation", 42, 2.5),
    ("Western", 27, 1.6), ("Film-Noir", 24, 1.4), ("Fantasy", 22, 1.3),
    ("Unknown / blank", 2, 0.1),
]
genres = pd.DataFrame(genre_data, columns=["Genre", "Movies", "Share of rated movies (%)"])

st.header("1. Genre breakdown")
st.markdown(
    "**How multi-genre movies are counted:** each rated movie is counted once for every genre it has. "
    "For example, a Drama/Comedy movie contributes one movie to Drama and one to Comedy. "
    "Shares use the total number of rated movies as the denominator, so genre shares can add up to more than 100%. "
    "Unknown or blank genres are kept as their own category."
)
fig_genre = px.bar(
    genres.sort_values("Movies"), x="Movies", y="Genre", orientation="h",
    color="Movies", color_continuous_scale=[[0, "#5B3828"], [1, "#FF9D5C"]], text="Movies",
    hover_data={"Share of rated movies (%)": ":.1f", "Movies": True},
    labels={"Movies": "Rated movies", "Genre": ""},
)
fig_genre.update_traces(textposition="outside", cliponaxis=False)
fig_genre.update_layout(showlegend=False, coloraxis_showscale=False, height=620, margin=dict(l=10, r=30, t=20, b=10))
st.plotly_chart(fig_genre, use_container_width=True)
st.caption("The supplied table lists 1,683 rated movies. Percentages are those provided and may not sum to 100% because genres overlap and of rounding.")

st.header("2. Genre satisfaction")
st.markdown("The supplied results identify the highest and lowest average ratings. Other genre averages were not included in the provided data.")
satisfaction = pd.DataFrame([
    ("Film-Noir", 3.92, 1733), ("War", 3.82, 9398),
    ("Fantasy", 3.22, 1352), ("Unknown / blank", 3.20, 10),
], columns=["Genre", "Mean rating", "Ratings"])
fig_sat = px.bar(
    satisfaction.sort_values("Mean rating"), x="Mean rating", y="Genre", orientation="h",
    color="Mean rating", color_continuous_scale=[[0, "#5B3828"], [1, "#FF9D5C"]], range_color=(1, 5),
    text="Mean rating", hover_data={"Ratings": True, "Mean rating": ":.2f"},
    labels={"Mean rating": "Average rating (out of 5)", "Genre": ""},
)
fig_sat.update_traces(texttemplate="%{x:.2f}", textposition="outside", cliponaxis=False)
fig_sat.update_layout(showlegend=False, coloraxis_showscale=False, xaxis_range=[0, 5], height=300, margin=dict(l=10, r=25, t=20, b=10))
st.plotly_chart(fig_sat, use_container_width=True)
st.info("Film-Noir is highest at 3.92/5, followed by War at 3.82/5. Fantasy is lowest among named genres at 3.22/5; unknown/blank genres average 3.20/5 and are excluded from the named-genre comparison.")

st.header("3. Ratings over time")
st.markdown(
    "The supplied summary includes annual means for 1990 and the 1996\u20131998 period, plus an approximate range across the 1930s\u20131980s. "
    "The line is continuous for readability; the historical section is interpolated from the supplied approximate range."
)

time_anchors = pd.DataFrame([
    (1930, 3.90, "1930s\u20131980s", "Approximate supplied range"),
    (1989, 4.00, "1930s\u20131980s", "Approximate supplied range"),
    (1990, 3.58, "1990", "Provided annual mean"),
    (1998, 3.31, "1996\u20131998", "Provided range endpoint; 1998 has 851 ratings"),
], columns=["Year", "Mean rating", "Period", "Basis"])
time_data = pd.DataFrame({"Year": range(1930, 1999)})
time_data["Mean rating"] = (
    time_data["Year"]
    .map(time_anchors.set_index("Year")["Mean rating"])
    .interpolate()
)
fig_time = px.line(
    time_data, x="Year", y="Mean rating",
    color_discrete_sequence=["#FF9D5C"],
    labels={"Mean rating": "Mean rating (out of 5)", "Year": "Release year"},
)
fig_time.update_traces(
    line=dict(width=3, color="#FF9D5C"),
    hovertemplate="Year: %{x}<br>Mean rating: %{y:.2f}<extra></extra>",
)
fig_time.add_trace(
    px.scatter(
        time_anchors, x="Year", y="Mean rating",
        hover_data={"Period": True, "Basis": True, "Year": False, "Mean rating": ":.2f"},
    ).data[0]
)
fig_time.data[-1].update(
    mode="markers",
    marker=dict(size=10, color="#FF9D5C", line=dict(color="#F4F1EB", width=1.5)),
    hovertemplate="Year: %{x}<br>Mean rating: %{y:.2f}<br>%{customdata[0]}<br>%{customdata[1]}<extra></extra>",
)
fig_time.update_layout(
    height=430, plot_bgcolor="#1E1E1C", paper_bgcolor="#141413",
    font=dict(color="#F4F1EB"),
    xaxis=dict(range=[1928, 2000], dtick=10, gridcolor="#343330", zeroline=False),
    yaxis=dict(range=[3.0, 4.2], dtick=0.2, gridcolor="#343330", zeroline=False),
    margin=dict(l=10, r=20, t=35, b=10),
)
st.plotly_chart(fig_time, use_container_width=True)
st.caption("The orange line is continuous for readability. Annual values between supplied observations are interpolated and should be treated as approximate; 1998 is less stable because it is based on 851 ratings.")
st.header("4. Best movies, with a rating floor")
st.markdown("Mean ratings are ranked only among movies meeting the selected minimum number of ratings. Use the tabs to compare the two floors.")
top_50 = pd.DataFrame([
    (1, "A Close Shave", 1995, 4.491, 112),
    (2, "Schindler’s List", 1993, 4.466, 298),
    (3, "The Wrong Trousers", 1993, 4.466, 118),
    (4, "Casablanca", 1942, 4.457, 243),
    (5, "Wallace & Gromit: The Best of Aardman Animation", 1996, 4.448, 67),
], columns=["Rank", "Movie", "Year", "Mean rating", "Ratings"])
top_150 = pd.DataFrame([
    (1, "Schindler’s List", 1993, 4.466, 298),
    (2, "Casablanca", 1942, 4.457, 243),
    (3, "The Shawshank Redemption", 1994, 4.445, 283),
    (4, "Rear Window", 1954, 4.388, 209),
    (5, "The Usual Suspects", 1995, 4.386, 267),
], columns=["Rank", "Movie", "Year", "Mean rating", "Ratings"])

def movie_chart(data, floor):
    chart_data = data.copy()
    chart_data["Movie (year)"] = chart_data["Movie"] + " (" + chart_data["Year"].astype(str) + ")"
    fig = px.bar(
        chart_data.sort_values("Mean rating"), x="Mean rating", y="Movie (year)", orientation="h",
        color="Mean rating", color_continuous_scale=[[0, "#5B3828"], [1, "#FF9D5C"]], range_color=(4.3, 4.55),
        text="Mean rating", hover_data={"Ratings": True, "Mean rating": ":.3f", "Rank": True},
        labels={"Mean rating": "Mean rating (out of 5)", "Movie (year)": ""},
    )
    fig.update_traces(texttemplate="%{x:.3f}", textposition="outside", cliponaxis=False)
    fig.update_layout(showlegend=False, coloraxis_showscale=False, xaxis_range=[4.2, 4.65], height=350,
                      margin=dict(l=10, r=30, t=20, b=10), title=f"Minimum {floor} ratings")
    return fig

left, right = st.columns(2)
with left:
    st.subheader("At least 50 ratings")
    st.plotly_chart(movie_chart(top_50, 50), use_container_width=True, key="top50_chart")
    st.dataframe(top_50, hide_index=True, use_container_width=True)
with right:
    st.subheader("At least 150 ratings")
    st.plotly_chart(movie_chart(top_150, 150), use_container_width=True, key="top150_chart")
    st.dataframe(top_150, hide_index=True, use_container_width=True)

st.caption("Source: figures supplied in the prompt. The app visualizes the provided summaries; it does not recalculate them from raw ratings.")
