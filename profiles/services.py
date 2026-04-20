import requests

TIMEOUT = 5


def safe_get(url, api_name):
    try:
        response = requests.get(url, timeout=TIMEOUT)
        response.raise_for_status()
        return response.json()
    except requests.RequestException:
        # Any network / HTTP error → treat as invalid upstream
        raise Exception(api_name)


def fetch_external_data(name):
    gender_res = safe_get(f"https://api.genderize.io?name={name}", "Genderize")
    age_res = safe_get(f"https://api.agify.io?name={name}", "Agify")
    country_res = safe_get(f"https://api.nationalize.io?name={name}", "Nationalize")

    return gender_res, age_res, country_res


def process_data(name):
    name = name.strip().lower()

    gender_res, age_res, country_res = fetch_external_data(name)

    # -------------------------
    # Genderize validation
    # -------------------------
    gender = gender_res.get("gender")
    probability = gender_res.get("probability")
    count = gender_res.get("count")

    if not gender or count == 0 or probability is None:
        raise Exception("Genderize")

    # -------------------------
    # Agify validation
    # -------------------------
    age = age_res.get("age")

    if age is None:
        raise Exception("Agify")

    # -------------------------
    # Nationalize validation
    # -------------------------
    countries = country_res.get("country")

    if not countries or len(countries) == 0:
        raise Exception("Nationalize")

    # Pick country with highest probability
    best_country = max(
        countries,
        key=lambda x: x.get("probability", 0)
    )

    country_id = best_country.get("country_id")
    country_probability = best_country.get("probability")

    if not country_id or country_probability is None:
        raise Exception("Nationalize")

    # -------------------------
    # Age group classification
    # -------------------------
    if age <= 12:
        age_group = "child"
    elif age <= 19:
        age_group = "teenager"
    elif age <= 59:
        age_group = "adult"
    else:
        age_group = "senior"

    # -------------------------
    # Final structured data
    # -------------------------
    return {
        "name": name,
        "gender": gender,
        "gender_probability": probability,
        "sample_size": count,
        "age": age,
        "age_group": age_group,
        "country_id": country_id,
        "country_probability": country_probability,
    }