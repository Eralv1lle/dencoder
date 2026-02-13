# from cryptography_service.crypt import encrypt, decrypt
#
#
# text = "Привет"
# data_id = 100
#
# encrypted = encrypt(text, data_id)
# print(encrypted)
# print(decrypt(encrypted, data_id))
#
from db import get_all, create_data, delete
from db.models import engine, Data
from sqlalchemy.orm import Session

with Session(engine) as session:
    print(get_all(session))

from PyQt6.QtWidgets import QApplication
from app import CryptApp


def main():
    import sys
    app = QApplication(sys.argv)

    crypt_app = CryptApp()
    crypt_app.show()

    sys.exit(
        app.exec()
    )

if __name__ == '__main__':
    main()