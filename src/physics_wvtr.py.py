import numpy as np

def saturation_pressure(Tc):
    """
    Saturation vapour pressure (kPa)
    Tetens equation (valid ~0–50°C)
    """
    return 0.61078 * np.exp((17.27 * Tc) / (Tc + 237.3))

def mixing_ratio(Tc, RH):
    """
    Mixing ratio ω (kg water / kg dry air)
    Derived from Lahtinen & Kuusipalo (TUT study)
    """
    p = 101.3  # kPa, atmospheric pressure
    ph_sat = saturation_pressure(Tc)
    ph = (RH / 100) * ph_sat
    return 0.622 * ph / (p - ph)

def coating_thickness_m(w, rho=920):
    """
    Convert coating weight (g/m2) to thickness (m)
    using density of polymer (default LDPE ~920 kg/m3)
    """
    w_kg_m2 = w / 1000
    return w_kg_m2 / rho

def wvtr_physics(Tc, RH, w):
    """
    Physics-informed WVTR model.
    WVTR ∝ (mixing ratio) × (temperature factor) / thickness
    """
    
    # 1. Humidity effect (mixing ratio)
    omega = mixing_ratio(Tc, RH)
    
    # 2. Temperature effect
    # small linear increase with temperature
    aT = 1 + 0.03 * (Tc - 23)
    
    # 3. Thickness effect
    thickness = coating_thickness_m(w)
    
    # 4. Scaling constant to match realistic WVTR ranges
    K = 500
    
    WVTR = (K * omega * aT) / thickness
    
    # Add 5% noise
    noise = np.random.normal(0, 0.05 * WVTR)
    return WVTR + noise

