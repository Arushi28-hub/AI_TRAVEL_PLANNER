import os
import pandas as pd

# Load dataset
_BASE_DIR = os.path.dirname(os.path.abspath(__file__))
df = pd.read_csv(os.path.join(_BASE_DIR, "data", "processed_travel_dataset.csv"))


def attractions_per_day(days):
    """
    Number of attractions based on trip duration.
    """
    return days * 3


def estimate_trip_cost(entrance_fee, days):
    """
    Estimate total trip cost.
    """
    food_cost = days * 400
    transport_cost = days * 300

    total_cost = (
        entrance_fee
        + food_cost
        + transport_cost
    )

    return total_cost


def plan_trip(
    interest,
    budget,
    days,
    city=None
):
    """
    Plan a trip based on interest, budget, duration and city.
    """

    num_places = attractions_per_day(days)

    matches = df[
        df["Tags"].str.contains(
            interest,
            case=False,
            na=False
        )
    ]

    if city:
        matches = matches[
            matches["City"].str.contains(
                city,
                case=False,
                na=False
            )
        ]

    matches = matches.sort_values(
        by="Student Score",
        ascending=False
    )

    selected_places = []

    total_fee = 0

    for _, row in matches.iterrows():

        fee = row["Entrance Fee in INR"]

        estimated_total = estimate_trip_cost(
            total_fee + fee,
            days
        )

        if estimated_total <= budget:

            selected_places.append(row)

            total_fee += fee

        if len(selected_places) >= num_places:
            break

    return pd.DataFrame(selected_places)


def trip_summary(
    trip,
    budget,
    days
):
    """
    Return trip summary.
    """

    total_entry_fee = trip[
        "Entrance Fee in INR"
    ].sum()

    total_cost = estimate_trip_cost(
        total_entry_fee,
        days
    )

    remaining_budget = (
        budget - total_cost
    )

    summary = {
        "Attractions Selected": len(trip),
        "Entry Fees": total_entry_fee,
        "Estimated Total Cost": total_cost,
        "Remaining Budget": remaining_budget
    }

    return summary


def get_attractions_list(trip):
    """
    Returns attraction names for Gemini.
    """

    return trip["Name"].tolist()