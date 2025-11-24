import unittest
from paiements import CarteBancaire, PayPal, Crypto, MontantInvalide, ValidationErreur

class TestPaiementsPolymorphisme(unittest.TestCase):

    def test_montant_negatif_leve_exception(self):
        with self.assertRaises(MontantInvalide):
            CarteBancaire(-10.0, "1234567890123", "456")
            
        with self.assertRaises(MontantInvalide):
            PayPal(0.0, "a@b.c", "token")

    def test_validation_carte_bancaire(self):
        with self.assertRaises(ValidationErreur):
            CarteBancaire(10.0, "12345", "123")
            
        with self.assertRaises(ValidationErreur):
            CarteBancaire(10.0, "1234567890123", "A")

    def test_carte_bancaire_payer_confirmation(self):
        montant = 42.50
        cb = CarteBancaire(montant, "1111222233334444", "123")
        
        confirmation = cb.payer()
        
        self.assertIn("Paiement CB de 42.50 €", confirmation)
        self.assertIn("4444", confirmation)
        
    def test_paypal_payer_confirmation(self):
        montant = 99.99
        email = "test@paypal.com"
        pp = PayPal(montant, email, "valid_token")
        
        confirmation = pp.payer()
        
        self.assertIn("Paiement PayPal de 99.99 €", confirmation)
        self.assertIn(email, confirmation)

    def test_crypto_payer_confirmation(self):
        montant = 1200.00
        crypto = Crypto(montant, "bc1qshortvalidwalletid", "DOGE")
        
        confirmation = crypto.payer()
        
        self.assertIn("Paiement Crypto (DOGE)", confirmation)
        self.assertIn("1200.00 €", confirmation)

if __name__ == '__main__':
    unittest.main()