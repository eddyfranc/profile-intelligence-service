import requests

def fetch_external_data(name):
    gender_res = requests.get(f"https://api.genderize.io?name={name}").json()
    age_res = requests.get(f"https://api.agify.io?name={name}").json()
    country_res = requests.get(f"https://api.nationalize.io?name={name}").json()

    return gender_res, age_res, country_res




def process_data(name):
    gender_res, age_res, country_res = fetch_external_data(name)

    # Genderize validation
    if not gender_res.get("gender") or gender_res.get("count") == 0:
        raise Exception("Genderize")

    # Agify validation
    if age_res.get("age") is None:
        raise Exception("Agify")

    # Nationalize validation
    countries = country_res.get("country")
    if not countries:
        raise Exception("Nationalize")

    # Pick highest probability country
    best_country = max(countries, key=lambda x: x["probability"])

    # Age group classification
    age = age_res["age"]
    if age <= 12:
        age_group = "child"
    elif age <= 19:
        age_group = "teenager"
    elif age <= 59:
        age_group = "adult"
    else:
        age_group = "senior"

    return {
        "name": name,
        "gender": gender_res["gender"],
        "gender_probability": gender_res["probability"],
        "sample_size": gender_res["count"],
        "age": age,
        "age_group": age_group,
        "country_id": best_country["country_id"],
        "country_probability": best_country["probability"],
    }