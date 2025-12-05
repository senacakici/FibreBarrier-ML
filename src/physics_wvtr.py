import numpy as np

def saturation_pressure(Tc: float) -> float:
    """
    Saturation vapour pressure of water (kPa)
    Tetens equation, valid roughly between 0–50 °C.
    Tc: temperature in °C
    """
    return 0.61078 * np.exp((17.27 * Tc) / (Tc + 237.3))

def mixing_ratio(Tc: float, RH: float) -> float:
    """
    Mixing ratio ω (kg water / kg dry air)
    Based on Lahtinen & Kuusipalo WVTR study:
    ω = 0.622 * ph / (p - ph)
    where ph is partial pressure of water vapour.
    """
    p = 101.3  # kPa, atmospheric pressure
    ph_sat = saturation_pressure(Tc)      # kPa
    ph = (RH / 100.0) * ph_sat            # kPa
    return 0.622 * ph / (p - ph)

def coating_thickness_m(w: float, rho: float = 920.0) -> float:
    """
    Convert coating weight (g/m^2) to thickness (m).
    w   : coating weight in g/m^2
    rho : density in kg/m^3 (default ~920 kg/m^3 for LDPE-like polymer)
    """
    w_kg_m2 = w / 1000.0          # g/m^2 -> kg/m^2
    return w_kg_m2 / rho          # m

def wvtr_physics(Tc: float, RH: float, w: float) -> float:
    """
    Physics-informed WVTR model.

    WVTR ∝ (mixing ratio) × (temperature factor) / thickness

    - Humidity effect via mixing ratio (ω)
    - Temperature effect via a simple linear factor
    - Thickness effect via 1 / thickness

    Returns WVTR in arbitrary but realistic units ~ g/m^2·day
    """
    # 1) Humidity effect (mixing ratio)
    omega = mixing_ratio(Tc, RH)

    # 2) Temperature effect (simple linear scaling around 23 °C)
    aT = 1.0 + 0.03 * (Tc - 23.0)

    # 3) Thickness effect
    thickness = coating_thickness_m(w)   # m

    # 4) Scaling constant to bring numbers into realistic WVTR range
    K = 500.0

    WVTR = (K * omega * aT) / thickness

    # 5) Add ~5% Gaussian noise to mimic experimental scatter
    noise = np.random.normal(0.0, 0.05 * WVTR)
    return WVTR + noise
