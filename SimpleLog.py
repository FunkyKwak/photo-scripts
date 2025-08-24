import logging
import os
import requests
from dotenv import load_dotenv

# charge les variables du fichier .env si présent (secret github sinon)
load_dotenv()


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)



token = os.environ["TELEGRAM_TOKEN"]
chat_id = os.environ["TELEGRAM_CHAT_ID"]



def send_telegram_message(message: str):
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    requests.post(url, data={"chat_id": chat_id, "text": message})



class SimpleLog:

    def __init__(self, method, success_message, type=None, response=None):
        self.method = method
        if (response is not None):
            self.response_code = response.status_code
            self.response_text = response.text
        if (type is None):
            self.set_type()
        self.success_message = success_message
    

    def set_type(self):
        if (self.response_code == 0 or self.response_code == 204):
            self.type = "SUCCESS"
        else:
            self.type = "ERROR"





    def print_github_action(self):
        if self.type == "SUCCESS":
            print(f"::notice::Job terminé avec succès – {self.success_message}")
        else:
            print(f"::error::Méthode {self.method} a retourné le code erreur {self.response_code}, message dans les logs")

            
    def log(self):
        if self.type == "SUCCESS":
            logging.info(f"Succès : {self.success_message}")
        else:
            logging.error("Erreur :", self.response_code, self.response_text)


    def log_and_print(self):
        self.log()
        self.print_github_action()


    def telegram(self):
        if self.type == "SUCCESS":
            send_telegram_message(f"{self.success_message}")
        else:
            send_telegram_message("Erreur :", self.response_code, self.response_text)
