#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import hashlib
import itertools
import argparse
import time
import os
import sys
import platform
from colorama import init, Fore, Style

# Initialisation de colorama pour la compatibilité Windows/Linux
init()

# Initialisation colorama pour Windows
init(autoreset=True)

def display_banner():
    """Affiche la bannière BLACK-H avec le logo ASCII choisi"""

    logo = [
        "██████╗░██╗░░░░░░█████╗░░█████╗░██╗░░██╗░░░░░░  ██╗░░██╗",
        "██╔══██╗██║░░░░░██╔══██╗██╔══██╗██║░██╔╝░░░░░░  ██║░░██║",
        "██████╦╝██║░░░░░███████║██║░░╚═╝█████═╝░█████╗  ███████║",
        "██╔══██╗██║░░░░░██╔══██║██║░░██╗██╔═██╗░╚════╝  ██╔══██║",
        "██████╦╝███████╗██║░░██║╚█████╔╝██║░╚██╗░░░░░░  ██║░░██║",
        "╚═════╝░╚══════╝╚═╝░░╚═╝░╚════╝░╚═╝░░╚═╝░░░░░░  ╚═╝░░╚═╝"
    ]

    banner = f"""
{Fore.RED}
╔════════════════════════════════════════════════════════════════════════════╗
║                                                                            ║
║  {Fore.WHITE}{logo[0]}{Fore.RED}                  ║
║  {Fore.WHITE}{logo[1]}{Fore.RED}                  ║
║  {Fore.WHITE}{logo[2]}{Fore.RED}                  ║
║  {Fore.WHITE}{logo[3]}{Fore.RED}                  ║
║  {Fore.WHITE}{logo[4]}{Fore.RED}                  ║
║  {Fore.WHITE}{logo[5]}{Fore.RED}ashs              ║
║                                                                            ║
║  Version: {Fore.GREEN}V1.1.0{Fore.WHITE}            Auteur/Équipe: {Fore.CYAN}DilaneNg{Fore.WHITE}                        ║
║  GitHub: {Fore.BLUE}https://github.com/DilaneNg/BLACKHASH{Fore.WHITE}                             ║
║                                                                            ║
║  {Fore.YELLOW}Un outil de cracking de hash simple, rapide et polyvalent{Fore.WHITE}                 ║
║  {Fore.YELLOW}pour MD5, SHA1 et SHA256.{Fore.WHITE}                                                 ║
║                                                                            ║
║  {Fore.RED}⚠️ CET OUTIL EST FOURNI UNIQUEMENT À DES FINS ÉDUCATIVES{Fore.WHITE}                   ║
║  {Fore.RED}ET DE TESTS LÉGAUX. L'AUTEUR DÉCLINE TOUTE RESPONSABILITÉ{Fore.WHITE}                 ║
║  {Fore.RED}EN CAS D'USAGE MALVEILLANT.{Fore.WHITE}                                               ║
║                                                                            ║
╚════════════════════════════════════════════════════════════════════════════╝
{Style.RESET_ALL}
"""
    print(banner)


def detect_hash_type(hash_value):
    """Tente de détecter le type de hash basé sur sa longueur"""
    length = len(hash_value)
    if length == 32:
        return "MD5"
    elif length == 40:
        return "SHA1"
    elif length == 64:
        return "SHA256"
    else:
        return None

def hash_text(text, algorithm):
    """Hash un texte avec l'algorithme spécifié"""
    if algorithm.upper() == "MD5":
        return hashlib.md5(text.encode()).hexdigest()
    elif algorithm.upper() == "SHA1":
        return hashlib.sha1(text.encode()).hexdigest()
    elif algorithm.upper() == "SHA256":
        return hashlib.sha256(text.encode()).hexdigest()
    else:
        raise ValueError("Algorithme non supporté")

# Répertoire racine du projet (là où est ton blackhash.py)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def find_wordlist_file(wordlist_path):
    """Cherche le fichier wordlist dans plusieurs emplacements possibles (Windows & Linux)"""
    
    wordlist_path = os.path.normpath(wordlist_path)

    # 1) Chemins relatifs au projet
    possible_paths = [
        os.path.join(BASE_DIR, wordlist_path),
        os.path.join(BASE_DIR, "utilitaire", "wordlist", wordlist_path),
        os.path.join(BASE_DIR, "utilitaire", "wordlist", "wordlist.txt"),
        os.path.join(BASE_DIR, "wordlist.txt"),
        os.path.join(BASE_DIR, "utilitaire", "wordlist", "common_passwords.txt"),
        os.path.join(BASE_DIR, "utilitaire", "wordlist", "rockyou.txt"),
    ]

    # 2) Chemins spécifiques Linux
    if platform.system().lower().startswith("linux"):
        possible_paths.extend([
            f"/usr/share/wordlists/{wordlist_path}",
            "/usr/share/wordlists/rockyou.txt",
            "/usr/share/wordlists/rockyou.txt.gz",
        ])

    # Vérifie chaque chemin
    for path in possible_paths:
        if os.path.isfile(path):
            return path
        if os.path.isfile(path + ".gz"):
            return path + ".gz"

    return None


def dictionary_attack(hash_value, algorithm, wordlist_path):
    """Tente de cracker le hash en utilisant une attaque par dictionnaire"""
    # Chercher le fichier wordlist
    actual_path = find_wordlist_file(wordlist_path)
    
    if actual_path is None:
        print(f"{Fore.RED}[!] Aucun fichier wordlist trouvé. Vérifiez les emplacements:{Style.RESET_ALL}")
        print(f"{Fore.RED}[!] - {wordlist_path}{Style.RESET_ALL}")
        print(f"{Fore.RED}[!] - ./utilitaire/wordlist/{wordlist_path}{Style.RESET_ALL}")
        print(f"{Fore.RED}[!] - ./utilitaire/wordlist/wordlist.txt{Style.RESET_ALL}")
        print(f"{Fore.RED}[!] Vous pouvez créer un wordlist simple avec des mots de passe courants.{Style.RESET_ALL}")
        return None
    
    print(f"{Fore.GREEN}[+] Utilisation du wordlist: {actual_path}{Style.RESET_ALL}")
    
    attempts = 0
    start_time = time.time()
    
    try:
        # Gérer les fichiers .gz
        if actual_path.endswith('.gz'):
            import gzip
            file = gzip.open(actual_path, 'rt', encoding='utf-8', errors='ignore')
        else:
            file = open(actual_path, 'r', encoding='utf-8', errors='ignore')
        
        with file:
            for password in file:
                password = password.strip()
                if not password:  # Ignorer les lignes vides
                    continue
                    
                attempts += 1
                
                if hash_text(password, algorithm) == hash_value:
                    end_time = time.time()
                    return {
                        'password': password,
                        'attempts': attempts,
                        'time': end_time - start_time
                    }
                    
                # Afficher la progression toutes les 10000 tentatives
                if attempts % 10000 == 0:
                    print(f"{Fore.CYAN}[*] {attempts} mots de passe testés...{Style.RESET_ALL}")
    
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}[!] Attaque interrompue par l'utilisateur.{Style.RESET_ALL}")
        return None
    except Exception as e:
        print(f"{Fore.RED}[!] Erreur lors de la lecture du wordlist: {e}{Style.RESET_ALL}")
        return None
    
    end_time = time.time()
    return {
        'password': None,
        'attempts': attempts,
        'time': end_time - start_time
    }

def brute_force_attack(hash_value, algorithm, max_length=8, charset=None):
    """Tente de cracker le hash en utilisant une attaque par force brute"""
    if charset is None:
        charset = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()_+-=[]{}|;:,.<>?"
    
    attempts = 0
    start_time = time.time()
    
    try:
        for length in range(1, max_length + 1):
            print(f"{Fore.CYAN}[*] Test des mots de passe de longueur {length}...{Style.RESET_ALL}")
            for candidate in itertools.product(charset, repeat=length):
                password = ''.join(candidate)
                attempts += 1
                
                if hash_text(password, algorithm) == hash_value:
                    end_time = time.time()
                    return {
                        'password': password,
                        'attempts': attempts,
                        'time': end_time - start_time
                    }
                
                # Afficher la progression toutes les 10000 tentatives
                if attempts % 10000 == 0:
                    print(f"{Fore.CYAN}[*] {attempts} combinaisons testées...{Style.RESET_ALL}")
    
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}[!] Attaque interrompue par l'utilisateur.{Style.RESET_ALL}")
        return None
    
    end_time = time.time()
    return {
        'password': None,
        'attempts': attempts,
        'time': end_time - start_time
    }

# Répertoire racine du projet (dossier où se trouve blackhash.py)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def check_or_create_default_wordlist():
    """Vérifie si un wordlist existe déjà, sinon en crée un par défaut"""
    default_path = os.path.join(BASE_DIR, "utilitaire", "wordlist", "wordlist.txt")
    
    # Vérifier si le wordlist existe déjà
    if os.path.exists(default_path):
        print(f"[+] Wordlist trouvé: {default_path}")
        return default_path
    
    # Si le wordlist n'existe pas, le créer
    print(f"[!] Création d'un wordlist par défaut...")
    os.makedirs(os.path.dirname(default_path), exist_ok=True)
    
    common_passwords = [
        "password", "123456", "admin", "letmein", "qwerty", 
        "abc123", "password1", "hello123", "test", "secret",
        "root", "administrator", "123456789", "12345678", "12345",
        "1234", "123", "000000", "111111", "monkey", "password123"
    ]
    
    with open(default_path, 'w') as f:
        for pwd in common_passwords:
            f.write(pwd + "\n")
    
    print(f"[+] Wordlist créé: {default_path}")
    return default_path


def main():
    """Fonction principale"""
    display_banner()
    
    parser = argparse.ArgumentParser(description='Outil de cracking de hash BLACKHASH')
    parser.add_argument('hash', nargs='?', help='Le hash à cracker')
    parser.add_argument('-a', '--algorithm', choices=['MD5', 'SHA1', 'SHA256'], 
                       help="Spécifier l'algorithme de hachage (sinon détection automatique)")
    parser.add_argument('-w', '--wordlist', default='wordlist.txt', 
                       help='Chemin vers le fichier wordlist (défaut: wordlist.txt)')
    parser.add_argument('-b', '--bruteforce', action='store_true', 
                       help='Utiliser une attaque par force brute au lieu du dictionnaire')
    parser.add_argument('-m', '--max-length', type=int, default=8, 
                       help='Longueur maximale pour le bruteforce (défaut: 8)')
    
    args = parser.parse_args()
    
    # Demander le hash si non fourni en argument
    if not args.hash:
        args.hash = input(f"{Fore.GREEN}[?] Entrez le hash à cracker: {Style.RESET_ALL}").strip()
    
    # Détection de l'algorithme si non spécifié
    if not args.algorithm:
        detected = detect_hash_type(args.hash)
        if detected:
            print(f"{Fore.GREEN}[+] Algorithme détecté: {detected}{Style.RESET_ALL}")
            args.algorithm = detected
        else:
            print(f"{Fore.RED}[!] Impossible de détecter l'algorithme. Veuillez le spécifier manuellement.{Style.RESET_ALL}")
            args.algorithm = input(f"{Fore.GREEN}[?] Entrez l'algorithme (MD5/SHA1/SHA256): {Style.RESET_ALL}").strip().upper()
    
    # Vérification de l'algorithme
    if args.algorithm not in ['MD5', 'SHA1', 'SHA256']:
        print(f"{Fore.RED}[!] Algorithme non supporté: {args.algorithm}{Style.RESET_ALL}")
        sys.exit(1)
    
    # Choix de la méthode d'attaque
    if not args.bruteforce:
        use_dict = input(f"{Fore.GREEN}[?] Voulez-vous utiliser un dictionnaire? (O/n): {Style.RESET_ALL}").strip().lower()
        args.bruteforce = (use_dict == 'n')
    
    # Vérifier ou créer un wordlist par défaut si nécessaire
    if not args.bruteforce:
        # Si l'utilisateur n'a pas spécifié de wordlist personnalisé, utiliser le chemin par défaut
        if args.wordlist == 'wordlist.txt':
            args.wordlist = check_or_create_default_wordlist()
    
    # Lancement de l'attaque
    print(f"{Fore.BLUE}[*] Démarrage de l'attaque...{Style.RESET_ALL}")
    
    if args.bruteforce:
        print(f"{Fore.BLUE}[*] Mode: {Fore.YELLOW}Force Brute{Style.RESET_ALL}")
        print(f"{Fore.BLUE}[*] Longueur maximale: {Fore.YELLOW}{args.max_length}{Style.RESET_ALL}")
        result = brute_force_attack(args.hash, args.algorithm, args.max_length)
    else:
        print(f"{Fore.BLUE}[*] Mode: {Fore.YELLOW}Dictionnaire{Style.RESET_ALL}")
        print(f"{Fore.BLUE}[*] Wordlist: {Fore.YELLOW}{args.wordlist}{Style.RESET_ALL}")
        result = dictionary_attack(args.hash, args.algorithm, args.wordlist)
    
    # Affichage des résultats
    if result is None:
        print(f"{Fore.RED}[!] Attaque annulée.{Style.RESET_ALL}")
        return
    
    print(f"\n{Fore.BLUE}════════════════════ RÉSULTATS ════════════════════{Style.RESET_ALL}")
    print(f"{Fore.BLUE}[*] Algorithme: {Fore.YELLOW}{args.algorithm}{Style.RESET_ALL}")
    print(f"{Fore.BLUE}[*] Tentatives: {Fore.YELLOW}{result['attempts']:,}{Style.RESET_ALL}")
    print(f"{Fore.BLUE}[*] Temps écoulé: {Fore.YELLOW}{result['time']:.2f} secondes{Style.RESET_ALL}")
    
    if result['password']:
        print(f"{Fore.BLUE}[*] Statut: {Fore.GREEN}SUCCÈS{Style.RESET_ALL}")
        print(f"{Fore.BLUE}[*] Mot de passe trouvé: {Fore.GREEN}{result['password']}{Style.RESET_ALL}")
    else:
        print(f"{Fore.BLUE}[*] Statut: {Fore.RED}ÉCHEC{Style.RESET_ALL}")
        print(f"{Fore.BLUE}[*] Mot de passe non trouvé.{Style.RESET_ALL}")
    
    print(f"{Fore.BLUE}═════════════════════════════════════════════════════{Style.RESET_ALL}")

if __name__ == "__main__":
    main()
