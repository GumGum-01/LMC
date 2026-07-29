import argparse
import sys
from math import pi

# Constants
k_B = 1.380649e-23  # Boltzmann constant (J/K)

def brownian_motion(t, T, eta, r):
    """
    Calculates the Mean Squared Displacement component (D * t) for a particle.
    
    Formula based on Stokes-Einstein equation:
    D = (k_B * T) / (6 * pi * eta * r)
    Result = D * t (Units: m^2)

    Args:
        t (float): Time in seconds (must be >= 0)
        T (float): Temperature in Kelvin (must be > 0)
        eta (float): Dynamic viscosity in Pa·s (must be > 0)
        r (float): Particle radius in meters (must be > 0)

    Returns:
        float: The calculated value of D * t.
    """
    # 1. Validaciones de Física (Safety Checks)
    if t < 0:
        raise ValueError("Time (t) cannot be negative.")
    if T <= 0:
        raise ValueError("Temperature (T) must be absolute positive (Kelvin).")
    if eta <= 0:
        raise ValueError("Viscosity (eta) must be greater than zero.")
    if r <= 0:
        raise ValueError("Particle radius (r) must be greater than zero.")

    # 2. Cálculo
    # Stokes-Einstein equation for diffusion coefficient D
    D = (k_B * T) / (6 * pi * eta * r)
    
    return D * t

def main():
    parser = argparse.ArgumentParser(description="Chemistry Skill Calculation Tool")
    subparsers = parser.add_subparsers(dest="formula", help="Select the formula to execute")

    # --- Configuración del comando brownian_motion ---
    bm_parser = subparsers.add_parser("brownian_motion", help="Calculate Brownian Motion (D*t)")
    bm_parser.add_argument("t", type=float, help="Time (s)")
    bm_parser.add_argument("T", type=float, help="Temperature (K)")
    bm_parser.add_argument("eta", type=float, help="Viscosity (Pa·s)")
    bm_parser.add_argument("r", type=float, help="Particle radius (m)")

    args = parser.parse_args()

    # --- Ejecución Segura ---
    try:
        if args.formula == "brownian_motion":
            result = brownian_motion(args.t, args.T, args.eta, args.r)
            # Imprimimos un formato claro para que el Agente lo lea sin dudas
            print(f"Computed Result: {result:.6e}")
            print(f"Unit: m^2 (Mean Squared Displacement component)")
        else:
            parser.print_help()
            
    except ValueError as ve:
        # Error específico de validación (input del usuario/agente incorrecto)
        print(f"INPUT ERROR: {ve}")
        sys.exit(1)
    except Exception as e:
        # Cualquier otro error inesperado (bug de código)
        print(f"SYSTEM ERROR: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()