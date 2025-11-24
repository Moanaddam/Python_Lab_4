from abc import ABC, abstractmethod
from typing import List
import uuid

class PaiementError(Exception):
    pass

class MontantInvalide(PaiementError):
    pass

class ValidationErreur(PaiementError):
    pass

class Paiement(ABC):
    def __init__(self, montant: float):
        if montant <= 0:
            raise MontantInvalide(f"Le montant du paiement doit être positif. Reçu : {montant}")
        
        self._montant = montant

    @property
    def montant(self) -> float:
        return self._montant

    @abstractmethod
    def payer(self) -> str:
        pass

class CarteBancaire(Paiement):
    def __init__(self, montant: float, numero: str, cvv: str):
        super().__init__(montant)
        
        if not (13 <= len(numero) <= 16 and numero.isdigit()):
            raise ValidationErreur("Numéro de carte invalide (longueur ou format).")
        if not (3 <= len(cvv) <= 4 and cvv.isdigit()):
            raise ValidationErreur("CVV invalide.")
            
        self._numero = numero
        self._cvv = cvv

    def payer(self) -> str:
        transaction_id = str(uuid.uuid4())[:8]
        return f"Paiement CB de {self.montant:.2f} € (ID: {transaction_id}). Carte: XXXX{self._numero[-4:]}."

class PayPal(Paiement):
    def __init__(self, montant: float, email: str, token: str):
        super().__init__(montant)
        
        if "@" not in email or len(token) < 10:
            raise ValidationErreur("Email ou jeton API PayPal invalide.")
            
        self._email = email
        self._token = token

    def payer(self) -> str:
        transaction_id = str(uuid.uuid4())[:8]
        return f"Paiement PayPal de {self.montant:.2f} € (ID: {transaction_id}). Compte: {self._email}."

class Crypto(Paiement):
    def __init__(self, montant: float, wallet_id: str, reseau: str):
        super().__init__(montant)
        
        if len(wallet_id) < 20 or not reseau.isalpha():
            raise ValidationErreur("Identifiant de portefeuille ou réseau invalide.")

        self._wallet_id = wallet_id
        self._reseau = reseau.upper()

    def payer(self) -> str:
        transaction_id = str(uuid.uuid4())[:8]
        return f"Paiement Crypto ({self._reseau}) de {self.montant:.2f} € (TX: {transaction_id}). Wallet: {self._wallet_id[:10]}..."

def traiter_paiements(liste_paiements: List[Paiement]):
    print("\n--- DÉBUT DU TRAITEMENT POLYMORPHIQUE DES PAIEMENTS ---")
    
    for p in liste_paiements:
        try:
            confirmation = p.payer()
            print(f"[OK] {confirmation}")
        except Exception as e:
            print(f"[ERREUR] Échec du paiement de type {p.__class__.__name__}: {e}")
            
    print("--- FIN DU TRAITEMENT ---")

if __name__ == "__main__":
    paiements_a_traiter = [
        CarteBancaire(25.50, "1234567890123", "456"),
        CarteBancaire(100.00, "9876543210987654", "999"),
        PayPal(50.00, "user1@mail.fr", "tokenXYZ12345"),
        PayPal(12.75, "user2@mail.fr", "tokenABC09876"),
        Crypto(800.00, "1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa", "BTC"),
        Crypto(5.99, "0xAb5801a7d39EfA4CFe1d5500F8399a", "ETH"),
    ]

    traiter_paiements(paiements_a_traiter)

    print("\n--- Test d'une validation simple ---")
    try:
        CarteBancaire(-10.00, "1234567890123", "456")
    except MontantInvalide as e:
        print(f"Validation réussie : {e}")