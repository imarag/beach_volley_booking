
from PyQt5.QtWidgets import QApplication, QHBoxLayout, QVBoxLayout, QWidget, QLineEdit, QPushButton, QLabel, QMainWindow, QComboBox, QFormLayout, QMessageBox
from PyQt5.QtCore import Qt
import os
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import sys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class BeachVolleyGUI(QMainWindow):
    players_file = 'players.xlsx'
    def __init__(self):
        super().__init__()
        self.main_widget = QWidget()

        if os.path.exists('templates/Combinear.qss'):
            self.main_widget.setStyleSheet(open('templates/Combinear.qss').read())
        self.setCentralWidget(self.main_widget)

        self.main_verbox_layout = QVBoxLayout()
        self.horlayout_top = QHBoxLayout()
        self.horlayout_middle = QHBoxLayout()
        self.verlayout_middle = QVBoxLayout()
        self.horlayout_bottom = QHBoxLayout()
        self.verlayout_middle.addLayout(self.horlayout_middle)

        self.main_verbox_layout.addWidget(QLabel('<h1>Beach Volley Kydwnias Booking GUI'))
        self.main_verbox_layout.addSpacing(200)
        self.main_verbox_layout.addLayout(self.horlayout_top)
        self.main_verbox_layout.addSpacing(100)
        self.main_verbox_layout.addLayout(self.verlayout_middle)
        self.main_verbox_layout.addSpacing(100)
        self.main_verbox_layout.addLayout(self.horlayout_bottom)
        self.main_verbox_layout.addStretch(1)

        self.main_widget.setLayout(self.main_verbox_layout)
        self.read_names()
        self.create_widgets()
        


    def create_widgets(self):

        self.formlayout_credentials = QFormLayout()
        self.en_username = QLineEdit()
        self.en_username.setPlaceholderText('insert your username')
        self.en_password = QLineEdit()
        self.en_password.setPlaceholderText('insert your password')
        self.formlayout_credentials.addRow('username: ', self.en_username)
        self.formlayout_credentials.addRow('password: ', self.en_password)
        self.horlayout_top.addLayout(self.formlayout_credentials)
        self.bt_create_players = QPushButton('create players file')
        self.bt_create_players.clicked.connect(self.create_players_list)
        self.bt_info_players_list = QPushButton('?')
        self.bt_info_players_list.clicked.connect(self.information_players_list)
        self.horlayout_top.addStretch(1)
        self.horlayout_top.addWidget(self.bt_create_players)
        self.horlayout_top.addWidget(self.bt_info_players_list)

        
        self.formlayout_names = QFormLayout()
        self.dd_names1 = QComboBox()
        self.dd_names2 = QComboBox()
        self.dd_names3 = QComboBox()
        self.formlayout_names.addRow('Player 1: ', self.dd_names1)
        self.formlayout_names.addRow('Player 2: ', self.dd_names2)
        self.formlayout_names.addRow('Player 3: ', self.dd_names3)
        

        self.lt_dds = [self.dd_names1, self.dd_names2, self.dd_names3]
        for dd in self.lt_dds:
            dd.addItems(['-- select name --'] + self.all_names)
            

        self.formlayout_court = QFormLayout()
        self.dd_court = QComboBox()
        self.dd_court.addItems(['-- select court --', 'court1', 'court2', 'court3', 'court4', 'court5'])
        self.dd_time = QComboBox()
        self.dd_time.addItems(['-- select time --', '3:30-15:00', '15:00-16:30', '16:30-18:00', '18:00-19:30', '19:30-21:00'])
        self.formlayout_court.addRow('Court: ', self.dd_court)
        self.formlayout_court.addRow('Time: ', self.dd_time)

        self.horlayout_check = QHBoxLayout()
        self.bt_check = QPushButton('Check inputs before booking')
        self.bt_check.clicked.connect(self.check_inputs_function)
        self.bt_check.setStyleSheet('background-color: #fc476b;')
        self.bt_check_information = QPushButton('?')
        self.horlayout_check.addWidget(self.bt_check)
        self.horlayout_check.addWidget(self.bt_check_information)
        self.horlayout_check.addStretch(1)
        self.bt_check_information.clicked.connect(self.information_check_button)
        
        self.horlayout_middle.addLayout(self.formlayout_names)
        self.horlayout_middle.addSpacing(80)
        self.horlayout_middle.addLayout(self.formlayout_court)
        self.verlayout_middle.addSpacing(60)
        self.verlayout_middle.addLayout(self.horlayout_check)
        

        self.bt_book = QPushButton('book')
        self.bt_book.clicked.connect(self.lets_go)
        self.horlayout_bottom.addWidget(self.bt_book)

    def read_names(self):
        if not os.path.exists(BeachVolleyGUI.players_file):
            return
        
        df = pd.read_excel(BeachVolleyGUI.players_file)
        ds = df.iloc[:, 0]
        self.all_names = list(ds)
        


    def create_players_list(self):
        time_sel = '19:30-21:00'
        court_sel = 'court3'
        time_dict = \
        {
            '13:30-15:00': '1',
            '15:00-16:30': '7',
            '16:30-18:00': '13',
            '18:00-19:30': '19',
            '19:30-21:00': '25'
        }

        court_dict = \
        {
            'court1': '2',
            'court2': '3',
            'court3': '4',
            'court4': '5',
            'court5': '6'
        }

        driver = webdriver.Chrome()
        driver.get("http://res.beachvolleychania.com/schedule")

        username_entry = driver.find_element(By.ID, 'username')
        password_entry = driver.find_element(By.ID, 'password')

        username_entry.clear()
        password_entry.clear()

        username_entry.send_keys('Ioannis')
        password_entry.send_keys('MIBeachvolley95')
        username_entry.send_keys(Keys.RETURN)

        programma_ghpedwn = WebDriverWait(driver, 30).until(
                EC.presence_of_element_located((By.XPATH, "//ul[@id='nav']/li[2]"))
            )

        programma_ghpedwn.click()
        time_and_court_string = f"//table[@id='timetable']/tbody/tr[{time_dict[time_sel]}]/td[{court_dict[court_sel]}]/a"

        cell_selected = driver.find_element(By.XPATH, time_and_court_string)


        cell_selected.click()

        all_players = driver.find_elements(By.CSS_SELECTOR, 'li.list_av_player')
        lt = []
        for pl in all_players:
            lt.append(pl.text)

        ds = pd.Series(lt)
        ds.to_excel('players.xlsx', index=None)
    
    def lets_go(self):

        self.validate_inputs()

    def validate_inputs(self):
        if not self.en_username.text() or not self.en_password.text():
            QMessageBox.critical(self, "Not enough inputs", "You need to insert both the username and the password")
            return False
        
        lt = []
        for dd in self.lt_dds:
            curr_text = dd.currentText()
            lt.append(curr_text)
            if '--' in curr_text:
                QMessageBox.critical(self, "Not enough inputs", "You need to select three names")
                return False
        if len(lt) != len(set(lt)):
            QMessageBox.critical(self, "Duplicate names found", "You need to select three unique names")
            return False
        
        if '--' in self.dd_court.currentText():
            QMessageBox.critical(self, "Not enough inputs", "You need to select the court")
            return False
        
        if '--' in self.dd_time.currentText():
            QMessageBox.critical(self, "Not enough inputs", "You need to select the time")
            return False

        return True


    def information_players_list(self):
        QMessageBox.information(self, "Information about the players list", "Το κουμπί αυτό, δημιουργεί μία λίστα με όλα τα ονόματα των παικτών που υπάρχουν στο σύλλογο. Δημιουργεί ένα αρχείο που ονομάζεται players.xlsx το οποίο έχει όλα τα ονόματα. Σε περίπτωση που μπούνε νέα μέλη στο σύλλογο πάτα αυτό το κουμπί για να δημιουργήσεις ξανά αυτό το αρχείο ώστε να ανανεωθεί η λίστα με τα ονόματα. Μην διαγράψεις το αρχείο αυτό γιατί το χρησιμοποιεί το πρόγραμμα. Το αρχείο players.xlsx που δημιουργείται πρέπει να είναι μαζί με το .exe πρόγραμμα που έχεις για να κλείσεις γήπεδο στον ίδιο φάκελο.")


    def information_check_button(self):
        QMessageBox.information(self, "Information about the check button", "Το κουμπί αυτό, μπορείς να το πατήσεις για να κάνει κάποιους ελέγχους πριν τρέξεις το πρόγραμμα. Για παράδειγμα ελέγχει αν έβαλες όλα τα στοιχείς που χρειάζεται ή αν ξέχασες κάποια γενικά. Δεν είναι ανάγκη να το πατήσεις απλά βοηθάει για να είσαι σίγουρος οτι μόλις πατήσεις το τελικό κουμπί (booking) θα τρέξει και δεν θα βγάλει κάποιο σφάλμα.")

    
    def check_inputs_function(self):
        is_ok = self.validate_inputs()

        if is_ok:
            QMessageBox.information(self, "Everything is ok", "Ολα φαίνονται μιά χαρά. Μπορείς να συνεχίσεις με το τελικό κουμπί.")
        else:
            return

app = QApplication([])

obj = BeachVolleyGUI()
obj.show()

app.exec()

