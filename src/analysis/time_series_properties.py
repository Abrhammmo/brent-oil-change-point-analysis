import matplotlib.pyplot as plt

def plot_price_and_returns(df):
    try:
        fig, axes = plt.subplots(2, 1, figsize=(12, 8), sharex=True)

        axes[0].plot(df["Date"], df["Price"])
        axes[0].set_title("Brent Oil Price")

        axes[1].plot(df["Date"], df["log_return"])
        axes[1].set_title("Log Returns (Volatility Clustering)")

        plt.tight_layout()
        plt.show()

        print("✅ Time series plots generated.")

    except Exception as e:
        print(f"❌ Plotting failed: {e}")
        raise
