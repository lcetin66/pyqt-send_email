import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import sys

from PyQt5.QtWidgets import QWidget, QPlainTextEdit, QLabel, QPushButton, QLineEdit, QVBoxLayout, QHBoxLayout, QApplication


class Pencere(QWidget):

    def __init__(self):

        super().__init__()

        self.init_ui()

    def init_ui(self):

        self.kimden = QLineEdit()
        self.kime = QLineEdit()
        self.konu = QLineEdit()
        self.kimden_etiket = QLabel("Kimden:")
        self.kime_etiket = QLabel("Kime:")
        self.konu_etiket = QLabel("Konu:")
        self.yazi_alani = QPlainTextEdit()
        self.temizle = QPushButton("Temizle")
        self.gonder = QPushButton("Gönder")

        v_box = QVBoxLayout()
        h_box = QHBoxLayout()

        v_box.addWidget(self.kimden_etiket)
        v_box.addWidget(self.kimden)
        v_box.addWidget(self.kime_etiket)
        v_box.addWidget(self.kime)
        v_box.addWidget(self.konu_etiket)
        v_box.addWidget(self.konu)
        v_box.addWidget(self.yazi_alani)
        h_box.addWidget(self.temizle)
        h_box.addWidget(self.gonder)

        v_box.addLayout(h_box)
        self.setLayout(v_box)
        
        self.setWindowTitle("EMail Editörü")

        self.temizle.clicked.connect(self.click)
        self.gonder.clicked.connect(self.click)

        self.show()
        
    def click(self):
        sender = self.sender()
        if sender.text() == "Temizle":
            self.yazi_alani.clear()
        if sender.text() == "Gönder":
            mesaj = MIMEMultipart()  # Mail yapımızı oluşturuyoruz.


            mesaj["From"] = f"{self.kimden.text()}"
            print(self.kimden.text())  # Kimden Göndereceğimiz

            mesaj["To"] = self.kime.text()  # Kime Göndereceğimiz
            print(self.kime.text())
            mesaj["Subject"] = self.konu.text()  # Mailimizin Konusu
            print(self.konu.text())

            # Mailimizin İçeriği
            yazi = self.yazi_alani.toPlainText()
            print(self.yazi_alani.toPlainText())


            # Mailimizin gövdesini bu sınıftan oluşturuyoruz.
            mesaj_govdesi = MIMEText(yazi, "plain")

            mesaj.attach(mesaj_govdesi)  # Mailimizin gövdesini mail yapımıza ekliyoruz.


            try:
                # SMTP objemizi oluşturuyoruz ve gmail smtp server'ına bağlanıyoruz.
                mail = smtplib.SMTP("smtp.gmail.com", 587)

                mail.ehlo()  # SMTP serverına kendimizi tanıtıyoruz.

                mail.starttls()  # Adresimizin ve Parolamızın şifrelenmesi için gerekli

                # SMTP server'ına giriş yapıyoruz. Kendi mail adresimizi ve parolamızı yapıyoruz.
                mail.login("email@gmail.com", "password")

                # Mailimizi gönderiyoruz.
                mail.sendmail(mesaj["From"], mesaj["To"], mesaj.as_string())
                print("Mail başarıyla gönderildi....")
                mail.close()  # Smtp serverımızın bağlantısını koparıyoz.

            except:
                # Herhangi bir bağlanma sorunu veya mail gönderme sorunu olursa
                sys.stderr.write("Mail göndermesi başarısız oldu...")
                sys.stderr.flush()

        


app = QApplication(sys.argv)

pencere = Pencere()

sys.exit(app.exec_())
