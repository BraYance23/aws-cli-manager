"""
Flujos de selección de sesión: región y perfil de AWS
"""
from core.aws_profiles import get_profiles
from config.aws_config import AWS_REGIONS
from ui.prompts import choice_options_table, choice_profile
from ui.tables import print_regions, print_profiles


def format_region_name() -> tuple[list, dict]:

    rich_rows = []
    dict_region_id = {}

    for indice, (region_name, location_name) in enumerate(AWS_REGIONS.items(), start=1):
        dict_region_id[str(indice)] = region_name
        rich_rows.append(
            {
                "id": indice,
                "region_name": region_name,
                "location_name": location_name
            }
        )

    return rich_rows, dict_region_id


def format_profiles(profiles: list):

    dict_profile = {}
    list_profile = []

    for indice, profile in enumerate(profiles, start=2):
        dict_profile[str(indice)] = profile
        list_profile.append([str(indice),
                             profile])

    return list_profile, dict_profile


def select_region_name():

    rich_rows, dict_region_name = format_region_name()
    print_regions(title_regions="Regiones disponibles para administrar", rows=rich_rows)
    region_name = choice_options_table(dict_data=dict_region_name, context="de la region que desea administrar ")
    location_name = AWS_REGIONS[region_name]
    return region_name, location_name


def select_profile():

    profiles = get_profiles()

    rich_rows, dict_profiles = format_profiles(profiles=profiles)
    print_profiles(list_profile=rich_rows)
    selected_profile = choice_profile(dict_options=dict_profiles)
    return selected_profile
