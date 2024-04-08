from http.server import BaseHTTPRequestHandler, HTTPServer
import json

# Base de datos de personajes
characters = {}

# Clase Personaje
class Character:
    def __init__(self, name, level, role, charisma, strength, dexterity):
        self.name = name
        self.level = level
        self.role = role
        self.charisma = charisma
        self.strength = strength
        self.dexterity = dexterity

# Builder para Pipols
class CharacterBuilder:
    def __init__(self):
        self.character = Character(None, None, None, None, None, None)

    def set_name(self, name):
        self.character.name = name

    def set_level(self, level):
        self.character.level = level

    def set_role(self, role):
        self.character.role = role

    def set_charisma(self, charisma):
        self.character.charisma = charisma

    def set_strength(self, strength):
        self.character.strength = strength

    def set_dexterity(self, dexterity):
        self.character.dexterity = dexterity

    def get_character(self):
        return self.character

# Director: Creación de pipols
class CharacterCreator:
    def __init__(self, builder):
        self.builder = builder

    def create_character(self, name, level, role, charisma, strength, dexterity):
        self.builder.set_name(name)
        self.builder.set_level(level)
        self.builder.set_role(role)
        self.builder.set_charisma(charisma)
        self.builder.set_strength(strength)
        self.builder.set_dexterity(dexterity)
        return self.builder.get_character()

# principios SOLID
class CharacterService:
    def __init__(self):
        self.builder = CharacterBuilder()
        self.creator = CharacterCreator(self.builder)

    def create_character(self, data):
        character = self.creator.create_character(
            data.get("name"), data.get("level"), data.get("role"),
            data.get("charisma"), data.get("strength"), data.get("dexterity")
        )
        characters[len(characters) + 1] = character
        return character

    def read_characters(self):
        return characters

    def update_character(self, character_id, data):
        if character_id in characters:
            character = characters[character_id]
            for key, value in data.items():
                setattr(character, key, value)
            return character
        else:
            return None

    def delete_character(self, character_id):
        if character_id in characters:
            return characters.pop(character_id)
        else:
            return None

# Manejador de solicitudes HTTP
class CharacterHandler(BaseHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        self.controller = CharacterService()
        super().__init__(*args, **kwargs)

    def do_POST(self):
        if self.path == "/characters":
            data = self.get_request_data()
            response_data = self.controller.create_character(data)
            self.send_response_and_data(201, response_data.__dict__)
        else:
            self.send_error_response(404)

    def do_GET(self):
        if self.path == "/characters":
            response_data = self.controller.read_characters()
            self.send_response_and_data(200, response_data)
        else:
            self.send_error_response(404)

    def do_PUT(self):
        if self.path.startswith("/characters/"):
            character_id = int(self.path.split("/")[2])
            data = self.get_request_data()
            response_data = self.controller.update_character(character_id, data)
            if response_data:
                self.send_response_and_data(200, response_data)
            else:
                self.send_error_response(404)
        else:
            self.send_error_response(404)

    def do_DELETE(self):
        if self.path.startswith("/characters/"):
            character_id = int(self.path.split("/")[2])
            deleted_character = self.controller.delete_character(character_id)
            if deleted_character:
                self.send_response_and_data(200, {"message": f"Character with id {character_id} has been deleted successfully"})
            else:
                self.send_error_response(404)
        else:
            self.send_error_response(404)

    def get_request_data(self):
        content_length = int(self.headers["Content-Length"])
        post_data = self.rfile.read(content_length)
        return json.loads(post_data.decode("utf-8"))

    def send_response_and_data(self, status_code, data):
        self.send_response(status_code)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(data).encode("utf-8"))

    def send_error_response(self, status_code):
        self.send_response(status_code)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps({"Error": "Route not found"}).encode("utf-8"))

# Función para ejecutar el servidor
def run(server_class=HTTPServer, handler_class=CharacterHandler, port=8000):
    server_address = ("", port)
    httpd = server_class(server_address, handler_class)
    print(f"Starting HTTP server on port {port}...")
    httpd.serve_forever()

# Lanzar  el servidor
if __name__ == "__main__":
    run()
