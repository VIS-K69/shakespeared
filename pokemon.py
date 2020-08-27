
# 3rd party modules
import pokebase as pb
import requests


def extract_element_from_json(obj, path):
    '''
    Extracts an element from a nested dictionary or
    a list of nested dictionaries along a specified path.
    If the input is a dictionary, a list is returned.
    If the input is a list of dictionary, a list of lists is returned.
    obj - list or dict - input dictionary or list of dictionaries
    path - list - list of strings that form the path to the desired element
    '''
    def extract(obj, path, ind, arr):
        '''
            Extracts an element from a nested dictionary
            along a specified path and returns a list.
            obj - dict - input dictionary
            path - list - list of strings that form the JSON path
            ind - int - starting index
            arr - list - output list
        '''
        key = path[ind]
        if ind + 1 < len(path):
            if isinstance(obj, dict):
                if key in obj.keys():
                    extract(obj.get(key), path, ind + 1, arr)
                else:
                    arr.append(None)
            elif isinstance(obj, list):
                if not obj:
                    arr.append(None)
                else:
                    for item in obj:
                        extract(item, path, ind, arr)
            else:
                arr.append(None)
        if ind + 1 == len(path):
            if isinstance(obj, list):
                if not obj:
                    arr.append(None)
                else:
                    for item in obj:
                        arr.append(item.get(key, None))
            elif isinstance(obj, dict):
                arr.append(obj.get(key, None))
            else:
                arr.append(None)
        return arr
    if isinstance(obj, dict):
        return extract(obj, path, 0, [])
    elif isinstance(obj, list):
        outer_arr = []
        for item in obj:
            outer_arr.append(extract(item, path, 0, []))
        return outer_arr

def read_one(name):
    """
    This function responds to a request for /api/pokemon/{name}
    with a description obtained from api.funtranslations.com
    :param name: the name of pokemon to find
    :return: pokemon matching Shakespeared description
    """

    p_name = name
    pokemon = pb.pokemon(p_name)
    p_id = pokemon.id

    url = 'http://pokeapi.co/api/v1/pokemon/' + str(p_id)
    resp = requests.get(url)

    if resp.status_code != 200:
        shakespeared_description = "Error retrieving data"
    else:
        species_data = resp.json()
        species_url = extract_element_from_json(species_data, ["species", "url"])[0]
        species_resp = requests.get(species_url)

        if species_resp.status_code != 200:
            shakespeared_description = "Error retrieving data from " + url
        else:
            pokemon_data = species_resp.json()

            pokemon_description = extract_element_from_json(
                pokemon_data,
                ["flavor_text_entries"])[0][0]["flavor_text"].replace("\n", " ")
            pokemon_description = pokemon_description.replace("\f", " ")
            pokemon_description = pokemon_description.replace(" ", "%20")

            shakespeared_url = "https://api.funtranslations.com/translate/shakespeare.json?text=" \
                         + pokemon_description
            shakespeared_resp = requests.get(shakespeared_url)

            if shakespeared_resp.status_code != 200:
                shakespeared_description = "Error retrieving data from " + shakespeared_url
            else:
                shakespeared_json = shakespeared_resp.json()

                shakespeared_description = extract_element_from_json(shakespeared_json,
                                                                     ["contents", "translated"])
                result = "NAME: " + name + " --- DESCRIPTION: " + shakespeared_description[0]

    return result


