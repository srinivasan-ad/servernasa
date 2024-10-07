import math
import csv
import json
import sys

SOLAR_RADIUS = 6.957e8
EARTH_RADIUS = 6.371e6
AU_IN_METERS = 1.496e11
PARSEC_IN_METERS = 3.086e16
STEFAN_BOLTZMANN_CONSTANT = 5.670374419e-8

def calculate_habitable_zone(L_star):
    HZ_inner = 0.75 * math.sqrt(L_star)
    HZ_outer = 1.77 * math.sqrt(L_star)
    return HZ_inner, HZ_outer

def is_in_habitable_zone(a, HZ_inner, HZ_outer):
    return HZ_inner <= a <= HZ_outer

def calculate_equilibrium_temperature(T_eff, R_star, a, albedo):
    R_star_meters = R_star * SOLAR_RADIUS
    a_meters = a * AU_IN_METERS
    T_eq = T_eff * math.sqrt(R_star_meters / (2 * a_meters)) * (1 - albedo)**0.25
    return T_eq

def calculate_angular_separation(a, distance):
    theta = (a / distance) * 206265
    return theta

def calculate_contrast(R_planet, a, albedo):
    R_planet_meters = R_planet * EARTH_RADIUS
    a_meters = a * AU_IN_METERS
    contrast = (R_planet_meters / a_meters)**2 * albedo
    return contrast

def is_habitable_and_detectable(params):
    R_star = params['R_star']
    L_star = params['L_star']
    T_eff = params['T_eff']
    R_planet = params['R_planet']
    a = params['semi_major_axis']
    albedo = params['albedo']
    distance = params['distance']
    D_telescope = params['D_telescope']
    wavelength = params['wavelength']
    IWA = params['IWA']
    OWA = params['OWA']
    contrast_limit = params['contrast_limit']

    HZ_inner, HZ_outer = calculate_habitable_zone(L_star)
    in_habitable_zone = is_in_habitable_zone(a, HZ_inner, HZ_outer)
    suitable_size = 0.5 <= R_planet <= 2.0
    T_eq = calculate_equilibrium_temperature(T_eff, R_star, a, albedo)
    suitable_temperature = 200 <= T_eq <= 330
    theta = calculate_angular_separation(a, distance)
    within_iwa = IWA <= theta <= OWA
    contrast = calculate_contrast(R_planet, a, albedo)
    sufficient_contrast = contrast >= contrast_limit
    habitable = in_habitable_zone and suitable_size and suitable_temperature
    detectable = within_iwa and sufficient_contrast

    if habitable and detectable:
        return 1
    elif habitable:
        return 2
    else:
        return 3
if __name__ == "__main__":
    args = list(map(float, sys.argv[1:]))  
    print(args)
    params = {
        'R_star': args[0],
        'L_star': args[1],
        'T_eff': args[2],
        'R_planet': args[3],
        'M_planet': args[4],
        'semi_major_axis': args[5],
        'eccentricity': args[6],
        'inclination': args[7],
        'albedo': args[8],
        'distance': args[9],
        'D_telescope': args[10],
        'wavelength': args[11],
        'IWA': args[12],
        'OWA': args[13],
        'contrast_limit': args[14]
    }
    result = is_habitable_and_detectable(params)  # Call your main function
    print(json.dumps({"result": result}))