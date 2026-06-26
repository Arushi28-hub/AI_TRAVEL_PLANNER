import os
import pandas as pd
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter


def geocode_df_locations(df):
    """Geocode a dataframe with columns ['Name','City'] or a single-column 'query'.
    Returns the dataframe merged with 'latitude' and 'longitude'. Results are cached
    in 'data/geocode_cache.csv' to avoid repeated calls.
    """
    if df is None or df.empty:
        return pd.DataFrame()

    df = df.copy()
    # build query
    if 'query' not in df.columns:
        df['query'] = df['Name'].astype(str) + ", " + df['City'].astype(str)

    cache_path = os.path.join('data', 'geocode_cache.csv')
    if os.path.exists(cache_path):
        try:
            cache = pd.read_csv(cache_path)
        except Exception:
            cache = pd.DataFrame(columns=['query', 'latitude', 'longitude'])
    else:
        cache = pd.DataFrame(columns=['query', 'latitude', 'longitude'])

    # initialize geolocator
    geolocator = Nominatim(user_agent='itinera_geocoder')
    geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1)

    # for each unique query, fill cache if missing
    unique_queries = df['query'].unique()

    for q in unique_queries:
        if q in cache['query'].values:
            continue
        try:
            loc = geocode(q, timeout=10)
            if loc:
                lat = loc.latitude
                lon = loc.longitude
            else:
                lat = None
                lon = None
        except Exception:
            lat = None
            lon = None

        cache = pd.concat([cache, pd.DataFrame([{'query': q, 'latitude': lat, 'longitude': lon}])], ignore_index=True)

        # save cache incrementally
        try:
            cache.to_csv(cache_path, index=False)
        except Exception:
            pass

    # merge results back into df
    out = df.merge(cache, on='query', how='left')
    return out
