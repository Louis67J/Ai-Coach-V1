# charts/generate_charts.py
"""
Charts generator - Full Coaching Pack
Entrées attendues :
- daily_tss : pd.Series index=dates, values=tss (0 si repos)
- power_bests : dict {sec: watts}
- time_in_zones : dict {"Z1": minutes, "Z2": minutes, ...}
- last_power_series : pd.Series(index=minutes, values=power)
- hr_power_pairs : list of (hr, power) tuples or DataFrame with ['hr','power']
- season_progress_df : DataFrame with columns like ['date','load','np','duration']
Sortie :
- fichiers PNG dans ../outputs/
"""

from pathlib import Path
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import seaborn as sns

OUTPUT_DIR = Path(__file__).resolve().parent.parent / "outputs"
OUTPUT_DIR.mkdir(exist_ok=True, parents=True)

def plot_ctl_atl(daily_tss: pd.Series, fname="ctl_atl.png", span_ctl=42, span_atl=7):
    if daily_tss is None or daily_tss.empty:
        return None
    ctl = daily_tss.ewm(span=span_ctl, adjust=False).mean()
    atl = daily_tss.ewm(span=span_atl, adjust=False).mean()
    tsb = ctl - atl
    plt.figure(figsize=(10,4))
    plt.plot(ctl.index, ctl.values, label="CTL (42d)", linewidth=2)
    plt.plot(atl.index, atl.values, label="ATL (7d)", linewidth=2)
    plt.plot(tsb.index, tsb.values, label="TSB", linewidth=1)
    plt.fill_between(ctl.index, 0, ctl.values, alpha=0.03)
    plt.title("CTL / ATL / TSB")
    plt.legend()
    p = OUTPUT_DIR / fname
    plt.tight_layout()
    plt.savefig(p)
    plt.close()
    return str(p)

def plot_power_curve(power_bests: dict, fname="power_curve.png"):
    if not power_bests:
        return None
    secs = sorted(power_bests.keys())
    watts = [power_bests[s] for s in secs]
    plt.figure(figsize=(8,4))
    plt.plot(secs, watts, marker='o')
    plt.xscale("log")
    plt.xticks(secs, [str(s) for s in secs])
    plt.xlabel("Duration (s)")
    plt.ylabel("Watts")
    plt.title("Power curve (best efforts)")
    plt.grid(which='both', linestyle='--', alpha=0.3)
    p = OUTPUT_DIR / fname
    plt.tight_layout()
    plt.savefig(p)
    plt.close()
    return str(p)

def plot_zone_distribution(time_in_zones: dict, fname="zone_dist.png"):
    if not time_in_zones:
        return None
    labels = list(time_in_zones.keys())
    values = [time_in_zones[k] for k in labels]
    plt.figure(figsize=(6,4))
    plt.pie(values, labels=labels, autopct='%1.0f%%', startangle=90)
    plt.title("Time in Power/HR Zones")
    p = OUTPUT_DIR / fname
    plt.tight_layout()
    plt.savefig(p)
    plt.close()
    return str(p)

def plot_intensity_mix(daily_tss: pd.Series, window=7, fname="intensity_mix.png"):
    if daily_tss is None or daily_tss.empty:
        return None
    # weekly TSS as example intensity mix
    weekly = daily_tss.resample("W").sum()
    plt.figure(figsize=(10,3))
    plt.bar(weekly.index, weekly.values, width=4)
    plt.title("Weekly TSS (example intensity mix)")
    p = OUTPUT_DIR / fname
    plt.tight_layout()
    plt.savefig(p)
    plt.close()
    return str(p)

def plot_hr_vs_power(hr_power_pairs, fname="hr_vs_power.png"):
    if not hr_power_pairs:
        return None
    df = pd.DataFrame(hr_power_pairs, columns=["hr","power"])
    plt.figure(figsize=(6,4))
    sns.regplot(x="power", y="hr", data=df, scatter_kws={'s':10, 'alpha':0.5}, line_kws={'color':'red'})
    plt.xlabel("Power (W)")
    plt.ylabel("Heart Rate (bpm)")
    plt.title("HR vs Power (scatter)")
    p = OUTPUT_DIR / fname
    plt.tight_layout()
    plt.savefig(p)
    plt.close()
    return str(p)

def plot_season_progression(season_progress_df: pd.DataFrame, fname="season_progress.png"):
    if season_progress_df is None or season_progress_df.empty:
        return None
    plt.figure(figsize=(10,4))
    if 'date' in season_progress_df.columns:
        season_progress_df = season_progress_df.set_index('date')
    if 'np' in season_progress_df.columns:
        plt.plot(season_progress_df.index, season_progress_df['np'], label="Normalized Power")
    if 'load' in season_progress_df.columns:
        plt.plot(season_progress_df.index, season_progress_df['load'], label="TSS/load")
    plt.legend()
    plt.title("Season progression")
    p = OUTPUT_DIR / fname
    plt.tight_layout()
    plt.savefig(p)
    plt.close()
    return str(p)
