# -*- coding: utf-8 -*-
"""Dynamic Home Energy Spot Tariff Arbitrage Skill for GenPark Personal Agents."""
import json
from typing import Dict, Any, List

def optimize_appliance_scheduling(hourly_rates_cents_kwh: List[float], ev_charging_kwh_required: float, ev_ready_by_hour: int) -> Dict[str, Any]:
    if len(hourly_rates_cents_kwh) != 24:
        return {"error": "hourly_rates_cents_kwh must contain exactly 24 hourly prices"}

    # EV charger rate: assume standard Level 2 home charger (7.2 kW)
    charger_kw = 7.2
    hours_needed = int(ev_charging_kwh_required / charger_kw) + (1 if (ev_charging_kwh_required % charger_kw) > 0 else 0)

    # Eligible hours before target ready time (assuming overnight window 20:00 to ready_hour)
    candidate_hours = []
    # evening previous day
    for h in range(21, 24):
        candidate_hours.append((h, hourly_rates_cents_kwh[h]))
    # morning next day
    for h in range(0, min(24, ev_ready_by_hour)):
        candidate_hours.append((h, hourly_rates_cents_kwh[h]))

    # Sort candidates by lowest price
    candidate_hours.sort(key=lambda x: x[1])
    selected_hours = candidate_hours[:min(hours_needed, len(candidate_hours))]
    selected_hours.sort(key=lambda x: (x[0] if x[0] >= 21 else x[0] + 24))

    scheduled_times = [f"{h[0]:02d}:00" for h in selected_hours]
    avg_price = round(sum(h[1] for h in selected_hours) / max(1, len(selected_hours)), 2)
    optimized_cost_usd = round((ev_charging_kwh_required * (avg_price / 100.0)), 2)
    
    # Baseline comparison (charging immediately at 18:00 peak)
    peak_price = hourly_rates_cents_kwh[18]
    baseline_cost_usd = round((ev_charging_kwh_required * (peak_price / 100.0)), 2)
    arbitrage_savings_usd = round(max(0.0, baseline_cost_usd - optimized_cost_usd), 2)

    return {
        "ev_charging_kwh": ev_charging_kwh_required,
        "hours_needed": hours_needed,
        "scheduled_charge_hours": scheduled_times,
        "average_arbitrage_rate_cents_kwh": avg_price,
        "optimized_session_cost_usd": optimized_cost_usd,
        "unhedged_peak_cost_usd": baseline_cost_usd,
        "estimated_savings_usd": arbitrage_savings_usd,
        "cost_reduction_pct": round((arbitrage_savings_usd / max(0.01, baseline_cost_usd)) * 100, 1),
        "arbitrage_engine": "GenPark Smart Energy Dispatch"
    }

def evaluate_thermal_preconditioning(target_comfort_temp_c: float, peak_tariff_start_hour: int, peak_rate_cents_kwh: float, off_peak_rate_cents_kwh: float) -> Dict[str, Any]:
    rate_spread = peak_rate_cents_kwh - off_peak_rate_cents_kwh
    
    # Pre-condition by 1.5 degrees C 2 hours prior to peak window
    preconditioning_start_hour = max(0, peak_tariff_start_hour - 2)
    preconditioned_target_temp = round(target_comfort_temp_c - 1.5, 1)

    return {
        "strategy": "THERMAL_BATTERY_PRE_CONDITIONING",
        "preconditioning_window": f"{preconditioning_start_hour:02d}:00 - {peak_tariff_start_hour:02d}:00",
        "preconditioned_setpoint_c": preconditioned_target_temp,
        "peak_window_setpoint_c": round(target_comfort_temp_c + 1.0, 1),
        "peak_tariff_cents_kwh": peak_rate_cents_kwh,
        "off_peak_tariff_cents_kwh": off_peak_rate_cents_kwh,
        "tariff_spread_delta": round(rate_spread, 2),
        "recommendation": "Coast on building thermal mass during peak pricing hours to eliminate HVAC compressor load."
    }
