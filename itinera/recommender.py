import os
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Load dataset
_BASE_DIR = os.path.dirname(os.path.abspath(__file__))
df = pd.read_csv(os.path.join(_BASE_DIR, "data", "processed_travel_dataset.csv"))

# -----------------------------
# Content-Based Recommendation
# -----------------------------

tfidf = TfidfVectorizer()

tfidf_matrix = tfidf.fit_transform(df["Tags"])

cosine_sim = cosine_similarity(tfidf_matrix)

indices = pd.Series(
    df.index,
    index=df["Name"]
).drop_duplicates()


def recommend_places(place_name, top_n=5):
    """
    Recommend places similar to the selected place.
    """

    if place_name not in indices:
        return pd.DataFrame()

    idx = indices[place_name]

    sim_scores = list(enumerate(cosine_sim[idx]))

    sim_scores = sorted(
        sim_scores,
        key=lambda x: x[1],
        reverse=True
    )

    sim_scores = sim_scores[1:top_n + 1]

    place_indices = [i[0] for i in sim_scores]

    return df.iloc[place_indices][
        [
            "Name",
            "Type",
            "City",
            "Student Score"
        ]
    ]


# -----------------------------
# Preference Based Recommendation
# -----------------------------

def recommend_by_preferences(
    attraction_type=None,
    budget=None,
    visit_time=None,
    top_n=5
):

    filtered = df.copy()

    if attraction_type:
        filtered = filtered[
            filtered["Type"].str.contains(
                attraction_type,
                case=False,
                na=False
            )
        ]

    if budget:
        filtered = filtered[
            filtered["Budget Category"] == budget
        ]

    if visit_time:
        filtered = filtered[
            filtered["Best Time to visit"] == visit_time
        ]

    if filtered.empty:
        return (
            df.sort_values(
                "Student Score",
                ascending=False
            )
            .head(top_n)
        )

    if len(filtered) < top_n:
        remaining = (
            df[~df.index.isin(filtered.index)]
            .sort_values(
                "Student Score",
                ascending=False
            )
        )

        filtered = pd.concat(
            [
                filtered.sort_values(
                    "Student Score",
                    ascending=False
                ),
                remaining
            ]
        )

    return filtered.head(top_n)


# -----------------------------
# Interest Recommendation
# -----------------------------

def recommend_trip(
    interest,
    top_n=10
):

    results = df.copy()

    results["Match Score"] = 0

    results.loc[
        results["Tags"].str.contains(
            interest,
            case=False,
            na=False
        ),
        "Match Score"
    ] += 5

    results["Final Score"] = (
        results["Match Score"]
        + results["Student Score"] * 5
    )

    return (
        results
        .sort_values(
            "Final Score",
            ascending=False
        )
        .head(top_n)[
            [
                "Name",
                "Type",
                "City",
                "Student Score",
                "Final Score"
            ]
        ]
    )


# -----------------------------
# Budget Recommendation
# -----------------------------

def recommend_trip_budget(
    interest,
    total_budget,
    top_n=10
):

    results = df.copy()

    results["Match Score"] = 0

    results.loc[
        results["Tags"].str.contains(
            interest,
            case=False,
            na=False
        ),
        "Match Score"
    ] += 5

    results["Final Score"] = (
        results["Match Score"]
        + results["Student Score"] * 5
    )

    recommendations = results.sort_values(
        "Final Score",
        ascending=False
    )

    selected = []

    remaining_budget = total_budget

    for _, row in recommendations.iterrows():

        fee = row["Entrance Fee in INR"]

        if fee <= remaining_budget:
            selected.append(row)
            remaining_budget -= fee

        if len(selected) >= top_n:
            break

    return pd.DataFrame(selected)