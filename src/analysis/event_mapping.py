import pandas as pd

def map_tau_to_date(df, tau_index):
    try:
        event_date = df.iloc[int(tau_index)]["Date"]
        print(f"✅ Change point mapped to date: {event_date.date()}")
        return event_date

    except Exception as e:
        print(f"❌ Event mapping failed: {e}")
        raise
