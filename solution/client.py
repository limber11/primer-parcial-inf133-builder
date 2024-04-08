import requests
import json

url = "http://localhost:8000/characters"
headers = {'Content-type': 'application/json'}

# Función crear un nuevo personaje en el servidor
def create_character(data):
    try:
        response = requests.post(url, json=data, headers=headers)
        response.raise_for_status()  # Raise an HTTPError if the response code is not 2xx
        print("Character created successfully!")
        return response.json()
    except requests.exceptions.HTTPError as err:
        print(f"HTTP error: {err}")
        return None
    except json.decoder.JSONDecodeError as err:
        print(f"JSON decoding error: {err}")
        return None
    except Exception as err:
        print(f"Error: {err}")
        return None

# obtener todos los personajes del servidor
def get_characters():
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as err:
        print(f"HTTP error: {err}")
        return None
    except json.decoder.JSONDecodeError as err:
        print(f"JSON decoding error: {err}")
        return None
    except Exception as err:
        print(f"Error: {err}")
        return None

# actualiza un personaje en el servidor
def update_character(character_id, data):
    try:
        update_url = f"{url}/{character_id}"
        response = requests.put(update_url, json=data, headers=headers)
        response.raise_for_status()
        print("Character updated successfully!")
        return response.json()
    except requests.exceptions.HTTPError as err:
        print(f"HTTP error: {err}")
        return None
    except json.decoder.JSONDecodeError as err:
        print(f"JSON decoding error: {err}")
        return None
    except Exception as err:
        print(f"Error: {err}")
        return None

# eliminar un personaje del servidor
def delete_character(character_id):
    try:
        delete_url = f"{url}/{character_id}"
        response = requests.delete(delete_url)
        response.raise_for_status()
        print("Character deleted successfully!")
    except requests.exceptions.HTTPError as err:
        print(f"HTTP error: {err}")
    except Exception as err:
        print(f"Error: {err}")

# Crear un nuevo personaje
new_character_data = {
    "name": "Gandalf",
    "level": 10,
    "role": "Wizard",
    "charisma": 15,
    "strength": 10,
    "dexterity": 10
}
new_character = create_character(new_character_data)
print("New character:", new_character)

# Obtener los personajes
characters = get_characters()
print("All characters:", characters)

# Actualizo un personaje
update_data = {
    "charisma": 20,
    "strength": 15,
    "dexterity": 15
}
updated_character = update_character(1, update_data)
print("Updated character:", updated_character)

# Elimina un personaje
delete_character(1)

# Obtengo todos los personajes nuevamente
characters = get_characters()
print("All characters after deletion:", characters)
