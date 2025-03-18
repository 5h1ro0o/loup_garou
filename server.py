import socket
import threading
import json
import random
from typing import Dict, List
from game_logic import GameLogic

class GameRoom:
    def __init__(self, game_id: str):
        self.game_id = game_id
        self.players: Dict[socket.socket, dict] = {}  # socket -> {name: str, role: None}
        self.messages: List[dict] = []
        self.started = False
        self.game_logic = GameLogic()
        self.current_turn = None
        self.min_players = 4  # Minimum requis pour démarrer
        self.announced_deaths = set()  # Pour tracker les morts annoncées
        self.admin_socket = None  # Socket du moteur d'administration

    def add_player(self, client_socket: socket.socket, player_name: str) -> None:
        """Ajoute un joueur sans rôle"""
        self.players[client_socket] = {
            "name": player_name,
            "role": None
        }
        self.broadcast_player_list()
        
        # Envoie un message au moteur d'administration
        if self.admin_socket:
            admin_message = {
                "action": "player_join",
                "username": player_name
            }
            self.send_message_to_admin(admin_message)
        
        # Vérifie si on peut démarrer
        if len(self.players) >= self.min_players:
            self.broadcast_system_message(f"La partie peut démarrer ! ({len(self.players)} joueurs connectés)")

    def send_message_to_admin(self, message: dict):
        """Envoie un message au moteur d'administration"""
        if self.admin_socket:
            try:
                self.admin_socket.send(json.dumps(message).encode())
            except Exception as e:
                print(f"Erreur d'envoi au moteur d'admin: {str(e)}")

    def start_game(self, client_socket=None):
        """Démarre la partie"""
        if self.started:
            return

        if len(self.players) < self.min_players:
            if client_socket:
                self.send_message_to_player(client_socket, {
                    "type": "system_message",
                    "content": f"Impossible de démarrer: il faut au moins {self.min_players} joueurs."
                })
            return

        self.started = True
        self.assign_roles()
        
        # Initialise la logique du jeu avec les joueurs
        player_data = {}
        for socket, player_info in self.players.items():
            player_data[player_info["name"]] = {
                "role": player_info["role"],
                "status": "alive"
            }
        
        self.game_logic.initialize(player_data, self.game_id)
        
        # Définit le premier joueur
        self.current_turn = list(self.players.keys())[0]
        
        # Notifie tout le monde du démarrage
        self.broadcast_system_message("La partie a démarré!")
        self.broadcast_game_state()

        # Notifie le moteur d'administration
        if self.admin_socket:
            self.send_message_to_admin({"action": "start_game"})

    def handle_admin_message(self, message: dict):
        """Traite les messages provenant du moteur d'administration"""
        action = message.get("action")
        
        if action == "open_game":
            # Ouvrir une nouvelle partie
            self.broadcast_system_message("La partie est maintenant ouverte aux joueurs!")
            
        elif action == "start_game":
            # Démarrer la partie
            self.start_game()
            
        elif action == "end_game":
            # Terminer la partie
            self.broadcast_system_message("La partie a été terminée par l'administrateur.")
            self.started = False
            
        elif action == "add_player":
            # Ajouter un joueur (note: ça peut être différent de player_join)
            username = message.get("username")
            # Logique pour ajouter un joueur via admin si nécessaire
            
        elif action == "player_join":
            # Un joueur a rejoint (note: peut-être géré différemment)
            username = message.get("username")
            self.broadcast_system_message(f"{username} a rejoint la partie!")


class GameServer:
    def __init__(self, host: str = 'localhost', port: int = 12345, admin_port: int = 12346):
        self.host = host
        self.port = port
        self.admin_port = admin_port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.admin_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.rooms: Dict[str, GameRoom] = {}
        self.client_room: Dict[socket.socket, str] = {}  # socket -> game_id
        self.admin_sockets = set()  # Pour suivre les connexions admin

    def start(self):
        """Démarre le serveur client et admin"""
        # Serveur pour les clients
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen()
        print(f"Serveur client démarré sur {self.host}:{self.port}")
        threading.Thread(target=self.handle_client_connections, daemon=True).start()
        
        # Serveur pour le moteur d'administration
        self.admin_server_socket.bind((self.host, self.admin_port))
        self.admin_server_socket.listen()
        print(f"Serveur admin démarré sur {self.host}:{self.admin_port}")
        threading.Thread(target=self.handle_admin_connections, daemon=True).start()

    def handle_client_connections(self):
        """Gère les connexions des clients"""
        while True:
            client_socket, address = self.server_socket.accept()
            print(f"Nouvelle connexion client de {address}")
            threading.Thread(target=self.handle_client, args=(client_socket,), daemon=True).start()

    def handle_admin_connections(self):
        """Gère les connexions du moteur d'administration"""
        while True:
            admin_socket, address = self.admin_server_socket.accept()
            print(f"Nouvelle connexion admin de {address}")
            self.admin_sockets.add(admin_socket)
            
            # Crée une salle par défaut si elle n'existe pas
            default_game_id = "default_game"
            if default_game_id not in self.rooms:
                self.rooms[default_game_id] = GameRoom(default_game_id)
            
            # Associe le socket admin à la salle
            self.rooms[default_game_id].admin_socket = admin_socket
            
            threading.Thread(target=self.handle_admin, args=(admin_socket, default_game_id), daemon=True).start()

    def handle_admin(self, admin_socket: socket.socket, game_id: str):
        """Traite les messages du moteur d'administration"""
        try:
            buffer = ""
            while True:
                data = admin_socket.recv(1024).decode()
                if not data:
                    break
                
                buffer += data
                
                # Traite tous les messages complets dans le buffer
                while True:
                    try:
                        # Trouve la première occurrence d'un message JSON complet
                        json_end = buffer.find('}') + 1
                        if json_end <= 0:
                            break
                            
                        message = json.loads(buffer[:json_end])
                        
                        # Traite le message admin
                        if game_id in self.rooms:
                            self.rooms[game_id].handle_admin_message(message)
                        
                        # Retire le message traité du buffer
                        buffer = buffer[json_end:].strip()
                        
                    except json.JSONDecodeError:
                        # Si JSON incomplet, on attend plus de données
                        break
                    except Exception as e:
                        print(f"Erreur traitement message admin: {str(e)}")
                        break
        
        except Exception as e:
            print(f"Erreur connexion admin: {str(e)}")
        finally:
            if admin_socket in self.admin_sockets:
                self.admin_sockets.remove(admin_socket)
            if game_id in self.rooms and self.rooms[game_id].admin_socket == admin_socket:
                self.rooms[game_id].admin_socket = None
            admin_socket.close()

    # Les méthodes existantes restent inchangées...
    def handle_client(self, client_socket: socket.socket):
        """Gère les connexions individuelles des clients"""
        try:
            buffer = ""
            while True:
                data = client_socket.recv(1024).decode()
                if not data:
                    break

                buffer += data
                
                # Traite tous les messages complets dans le buffer
                while True:
                    try:
                        # Trouve la première occurrence d'un message JSON complet
                        json_end = buffer.find('}') + 1
                        if json_end <= 0:
                            break
                            
                        message = json.loads(buffer[:json_end])
                        self.process_message(client_socket, message)
                        
                        # Retire le message traité du buffer
                        buffer = buffer[json_end:].strip()
                        
                    except json.JSONDecodeError:
                        # Si JSON incomplet, on attend plus de données
                        break
                    except Exception as e:
                        print(f"Erreur traitement message client: {str(e)}")
                        break
                        
        except Exception as e:
            print(f"Erreur de connexion client: {str(e)}")
        finally:
            self.disconnect_client(client_socket)

    # Tu peux garder le reste de ton code inchangé

if __name__ == "__main__":
    server = GameServer(host='localhost', port=12345, admin_port=12346)
    server.start()
    
    # Maintient le thread principal actif
    try:
        while True:
            pass
    except KeyboardInterrupt:
        print("Serveur arrêté")
