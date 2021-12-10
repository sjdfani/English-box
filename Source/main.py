from english import Ui_MainWindow
from UpdatePage import Ui_UpdateWindow
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import backend
from random import randint
import xlsxwriter

global update_row


# line 585 -> change item[1] to item[4] : to set description for answers


class UpdatePage(QMainWindow):
    def __init__(self):
        global update_row
        QMainWindow.__init__(self)
        self.ui = Ui_UpdateWindow()
        self.ui.setupUi(self)
        self.setWindowTitle("Update")
        self.setWindowIcon(QIcon('2x\images.jfif'))
        self.ui.update_btn_update.clicked.connect(self.update_btn)
        # Destroy menubar =======================
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        # =======================================
        self.ui.update_lineEdit_meaning.setText(update_row[0][1])
        self.ui.update_lineEdit_synonym.setText(update_row[0][2])
        self.ui.update_lineEdit_antonym.setText(update_row[0][3])
        self.ui.update_lineEdit_describe.setText(update_row[0][4])
        self.ui.update_lineEdit_example.setText(update_row[0][5])
        self.ui.update_lineEdit_group.setText(update_row[0][6])

    def mousePressEvent(self, evt):
        self.oldPos = evt.globalPos()

    def mouseMoveEvent(self, evt):
        delta = QPoint(evt.globalPos() - self.oldPos)
        self.move(self.x() + delta.x(), self.y() + delta.y())
        self.oldPos = evt.globalPos()

    def lower_capital(self):
        meaning = self.ui.update_lineEdit_meaning.text().lower().capitalize()
        self.ui.update_lineEdit_meaning.setText(meaning)
        synonym = self.ui.update_lineEdit_synonym.text().lower().capitalize()
        self.ui.update_lineEdit_synonym.setText(synonym)
        antonym = self.ui.update_lineEdit_antonym.text().lower().capitalize()
        self.ui.update_lineEdit_antonym.setText(antonym)
        describe = self.ui.update_lineEdit_describe.text().lower().capitalize()
        self.ui.update_lineEdit_describe.setText(describe)
        example = self.ui.update_lineEdit_example.text().lower().capitalize()
        self.ui.update_lineEdit_example.setText(example)
        group = self.ui.update_lineEdit_group.text().lower().capitalize()
        self.ui.update_lineEdit_group.setText(group)

    def showInfo(self, title, msg):
        info = QMessageBox(self)
        info.setIcon(QMessageBox.Information)
        info.setText(msg)
        info.setWindowTitle(title)
        info.show()

    def showError(self, title, msg):
        info = QMessageBox(self)
        info.setIcon(QMessageBox.Critical)
        info.setText(msg)
        info.setWindowTitle(title)
        info.show()

    def update_btn(self):
        self.ui.update_lineEdit_group.setText(self.ui.update_lineEdit_group.text().strip())
        if len(self.ui.update_lineEdit_meaning.text()) != 0:
            if len(self.ui.update_lineEdit_group.text()) != 0:
                if self.ui.update_lineEdit_group.text().isnumeric():
                    self.lower_capital()
                    backend.update(update_row[0][0], self.ui.update_lineEdit_meaning.text(),
                                   self.ui.update_lineEdit_synonym.text(), self.ui.update_lineEdit_antonym.text(),
                                   self.ui.update_lineEdit_describe.text(), self.ui.update_lineEdit_example.text(),
                                   self.ui.update_lineEdit_group.text())
                    self.showInfo("Update", "Update is successful.")
                    self.close()
                else:
                    self.showError("Error", "Group should be number.")
            else:
                self.showError("Error", "You should fill group.")
        else:
            self.showError("Error", "You should fill meaning.")


class HomePage(QMainWindow):
    menu_num = 0
    train_random_num = 0
    setting_language_num = 0
    train_ques_num = list()
    random_ques_white = list()
    rand_radio_correct = ""
    # ==================
    correct_answer = 0
    mistake_answer = 0
    white_answer = 0
    # ==================
    current_num = 1
    all_ques_num = 0
    # ==================
    train_current_num = 0
    group_current_num = 0
    # ==================
    handle_answerToWhite = 0
    handle_answerToSubmit = 0
    handle_submitToCorrect = 0
    handle_submitToAnswer = 0

    def __init__(self):
        QMainWindow.__init__(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowTitle("English box")
        self.setWindowIcon(QIcon(r'2x\images.jfif'))
        # Destroy menubar =============
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        # =============================
        self.ui.LeftFrame.hide()
        self.ui.btn_menu.clicked.connect(self.menu)
        self.ui.mainpage.setCurrentWidget(self.ui.HomePage)
        self.ui.btn_home.clicked.connect(self.home_btn)
        self.ui.btn_addword.clicked.connect(self.addWord_btn)
        self.ui.btn_dict.clicked.connect(self.dict_btn)
        self.ui.btn_train.clicked.connect(self.train_btn)
        self.ui.btn_setting.clicked.connect(self.setting_btn)
        self.ui.train_btn_radio_1.hide()
        self.ui.train_btn_radio_2.hide()
        self.ui.train_btn_radio_3.hide()
        self.ui.train_btn_radio_4.hide()
        self.ui.Label_topFrame.hide()
        self.ui.train_frame_group.hide()
        self.ui.train_frame_ques.hide()
        self.ui.train_label_correct_ans.setText("0")
        self.ui.train_label_mistake_ans.setText("0")
        self.ui.train_label_white_ans.setText("0")
        ftn = QFont("Open Sans", 70, QFont.Bold)
        self.ui.setting_time.setFont(ftn)
        timer = QTimer(self)
        timer.timeout.connect(self.display_time)
        timer.start(1000)

    def display_time(self):
        currentTime = QTime.currentTime()
        display = currentTime.toString("hh:mm:ss")
        self.ui.setting_time.setText(display)

    def showInfo_home(self, title, msg):
        info = QMessageBox(self)
        info.setIcon(QMessageBox.Information)
        info.setText(msg)
        info.setWindowTitle(title)
        info.show()

    def showError_home(self, title, msg):
        info = QMessageBox(self)
        info.setIcon(QMessageBox.Critical)
        info.setText(msg)
        info.setWindowTitle(title)
        info.show()

    def menu(self):
        if self.menu_num == 0:
            self.ui.LeftFrame.show()
            self.menu_num = 1
        elif self.menu_num == 1:
            self.ui.LeftFrame.hide()
            self.menu_num = 0

    def home_btn(self):
        self.ui.Label_topFrame.hide()
        self.ui.mainpage.setCurrentWidget(self.ui.HomePage)

    def addWord_btn(self):
        self.ui.Label_topFrame.show()
        self.ui.Label_topFrame.setText("Add Word")
        self.ui.mainpage.setCurrentWidget(self.ui.AddWordPage)
        self.ui.add_btn_submit.clicked.connect(self.add_submit_func)
        self.ui.add_btn_clear.clicked.connect(self.add_clear_func)

    def dict_btn(self):
        self.ui.Label_topFrame.show()
        self.ui.Label_topFrame.setText("Show All Word")
        self.ui.mainpage.setCurrentWidget(self.ui.AllWordPage)
        self.dict_table_func()
        self.ui.dict_btn_update.clicked.connect(self.dict_update_func)
        self.ui.dict_btn_delete.clicked.connect(self.dict_delete_func)
        self.ui.dict_btn_search.clicked.connect(self.dict_search_func)

    def train_btn(self):
        self.ui.train_btn_radio_1.hide()
        self.ui.train_btn_radio_2.hide()
        self.ui.train_btn_radio_3.hide()
        self.ui.train_btn_radio_4.hide()
        self.ui.Label_topFrame.show()
        self.ui.Label_topFrame.setText("Train")
        self.ui.mainpage.setCurrentWidget(self.ui.TrainPage)
        self.ui.train_btn_random.clicked.connect(self.train_random_func)
        self.ui.train_btn_submit.clicked.connect(self.trainOption_radioBtn_submit)
        self.ui.train_btn_answer.clicked.connect(self.trainOption_radioBtn_answer)
        self.ui.train_btn_next.clicked.connect(self.trainOption_radioBtn_next)
        self.ui.train_btn_back.clicked.connect(self.trainOption_radioBtn_back)
        self.ui.train_btn_group.clicked.connect(self.train_group)

    def setting_btn(self):
        self.ui.Label_topFrame.show()
        self.ui.Label_topFrame.setText("Setting")
        self.ui.mainpage.setCurrentWidget(self.ui.SettingPage)
        self.ui.setting_btn_author.clicked.connect(self.setting_author)
        self.ui.setting_btn_telegram.clicked.connect(self.setting_telegram)
        self.ui.setting_btn_language.clicked.connect(self.setting_insta)
        self.ui.setting_btn_excel.clicked.connect(self.setting_excel)

    def mousePressEvent(self, evt):
        self.oldPos = evt.globalPos()

    def mouseMoveEvent(self, evt):
        delta = QPoint(evt.globalPos() - self.oldPos)
        self.move(self.x() + delta.x(), self.y() + delta.y())
        self.oldPos = evt.globalPos()

    @staticmethod
    def word_exist_func(word):
        word_exist = False
        rows = backend.view()
        for item in rows:
            if item[0] == word:
                word_exist = True
                break
        return word_exist

    def lower_capital(self):
        word = self.ui.add_lineEdit_word.text().lower()
        self.ui.add_lineEdit_word.setText(word)
        meaning = self.ui.add_lineEdit_meaning.text().lower().capitalize()
        self.ui.add_lineEdit_meaning.setText(meaning)
        synonym = self.ui.add_lineEdit_synonym.text().lower().capitalize()
        self.ui.add_lineEdit_synonym.setText(synonym)
        antonym = self.ui.add_lineEdit_antonym.text().lower().capitalize()
        self.ui.add_lineEdit_antonym.setText(antonym)
        describe = self.ui.add_lineEdit_describe.text().lower().capitalize()
        self.ui.add_lineEdit_describe.setText(describe)
        example = self.ui.add_lineEdit_example.text().lower().capitalize()
        self.ui.add_lineEdit_example.setText(example)
        group = self.ui.add_lineEdit_group.text().lower().capitalize()
        self.ui.add_lineEdit_group.setText(group)

    def add_submit_func(self):
        word_exist = self.word_exist_func(self.ui.add_lineEdit_word.text())
        self.ui.add_lineEdit_group.setText(self.ui.add_lineEdit_group.text().strip())
        self.lower_capital()
        if len(self.ui.add_lineEdit_word.text()) != 0:
            if not word_exist:
                if len(self.ui.add_lineEdit_meaning.text()) != 0:
                    if len(self.ui.add_lineEdit_describe.text()) != 0:
                        if len(self.ui.add_lineEdit_group.text()) != 0:
                            if self.ui.add_lineEdit_group.text().isnumeric():
                                backend.insert(self.ui.add_lineEdit_word.text(), self.ui.add_lineEdit_meaning.text(),
                                               self.ui.add_lineEdit_synonym.text(), self.ui.add_lineEdit_antonym.text(),
                                               self.ui.add_lineEdit_describe.text(), self.ui.add_lineEdit_example.text(),
                                               self.ui.add_lineEdit_group.text())
                                self.showInfo_home("Add", "Add is successful.")
                            else:
                                self.showError_home("Error", "Group should be number.")
                        else:
                            self.showError_home("Error", "You should fill group.")
                    else:
                        self.showError_home("Error", "You should fill description.")
                else:
                    self.showError_home("Error", "You should fill meaning.")
            else:
                self.showError_home("Error", f"{self.ui.add_lineEdit_word.text()} is exist.")
        else:
            self.showError_home("Error", "You should fill word.")

    def add_clear_func(self):
        self.ui.add_lineEdit_word.setText("")
        self.ui.add_lineEdit_describe.setText("")
        self.ui.add_lineEdit_antonym.setText("")
        self.ui.add_lineEdit_example.setText("")
        self.ui.add_lineEdit_synonym.setText("")
        self.ui.add_lineEdit_group.setText("")
        self.ui.add_lineEdit_meaning.setText("")

    def dict_table_func(self):
        rows = backend.view()
        row = 0
        self.ui.dict_tableWords.setRowCount(len(rows))
        for item in rows:
            self.ui.dict_tableWords.setItem(row, 0, QTableWidgetItem(item[0]))
            self.ui.dict_tableWords.setItem(row, 1, QTableWidgetItem(item[1]))
            self.ui.dict_tableWords.setItem(row, 2, QTableWidgetItem(item[2]))
            self.ui.dict_tableWords.setItem(row, 3, QTableWidgetItem(item[3]))
            self.ui.dict_tableWords.setItem(row, 4, QTableWidgetItem(item[4]))
            self.ui.dict_tableWords.setItem(row, 5, QTableWidgetItem(item[5]))
            self.ui.dict_tableWords.setItem(row, 6, QTableWidgetItem(item[6]))
            row += 1

    def dict_update_func(self):
        global update_row
        if len(self.ui.dict_lineEdit_word.text()) != 0:
            word = self.ui.dict_lineEdit_word.text().lower()
            self.ui.dict_lineEdit_word.setText(word)
            if self.word_exist_func(self.ui.dict_lineEdit_word.text()):
                update_row = backend.search(self.ui.dict_lineEdit_word.text())
                self.updateWin = UpdatePage()
                self.updateWin.show()
            else:
                self.showError_home("Error", f"{self.ui.dict_lineEdit_word.text()} is not exist!")
        else:
            self.showError_home("Error", "Word line Edit is empty!")

    def dict_delete_func(self):
        if len(self.ui.dict_lineEdit_word.text()) != 0:
            self.ui.dict_lineEdit_word.setText(self.ui.dict_lineEdit_word.text().lower())
            if self.word_exist_func(self.ui.dict_lineEdit_word.text()):
                backend.delete(self.ui.dict_lineEdit_word.text())
                self.showInfo_home("Delete", "Delete is successful.")
                self.dict_table_func()
                self.ui.dict_lineEdit_word.setText("")
            else:
                self.showError_home("Error", f"{self.ui.dict_lineEdit_word.text()} is not exist!")
        else:
            self.showError_home("Error", "Word line Edit is empty!")

    def dict_search_func(self):
        if len(self.ui.dict_lineEdit_word.text()) != 0:
            self.ui.dict_lineEdit_word.setText(self.ui.dict_lineEdit_word.text().lower())
            if self.word_exist_func(self.ui.dict_lineEdit_word.text()):
                rows = backend.search(self.ui.dict_lineEdit_word.text())
                self.ui.dict_tableWords.setRowCount(len(rows))
                for item in rows:
                    self.ui.dict_tableWords.setItem(0, 0, QTableWidgetItem(item[0]))
                    self.ui.dict_tableWords.setItem(0, 1, QTableWidgetItem(item[1]))
                    self.ui.dict_tableWords.setItem(0, 2, QTableWidgetItem(item[2]))
                    self.ui.dict_tableWords.setItem(0, 3, QTableWidgetItem(item[3]))
                    self.ui.dict_tableWords.setItem(0, 4, QTableWidgetItem(item[4]))
                    self.ui.dict_tableWords.setItem(0, 5, QTableWidgetItem(item[5]))
                    self.ui.dict_tableWords.setItem(0, 6, QTableWidgetItem(item[6]))
            else:
                self.showError_home("Error", f"{self.ui.dict_lineEdit_word.text()} is not exist!")
        else:
            self.showError_home("Error", "Word line Edit is empty!")

    def train_random_func(self):
        rows = backend.view()
        if len(rows) > 4:
            self.current_num = 1
            self.train_current_num = 0
            self.ui.train_frame_group.hide()
            if self.train_random_num == 0:
                self.ui.train_frame_ques.show()
                self.train_random_num = 1
            elif self.train_random_num == 1:
                self.ui.train_frame_ques.hide()
                self.train_random_num = 0
            self.train_ques_num.clear()
            num = randint(0, len(rows) - 1)
            count = 0
            while True:
                if num in self.train_ques_num:
                    num = randint(0, len(rows) - 1)
                else:
                    self.train_ques_num.append(num)
                    count += 1
                if count == len(rows):
                    break
            if self.current_num == 1:
                self.ui.train_btn_back.setEnabled(False)
            self.ui.train_label_correct_ans.setText("0")
            self.ui.train_label_mistake_ans.setText("0")
            self.ui.train_label_white_ans.setText("0")
            self.ui.train_btn_radio_1.hide()
            self.ui.train_btn_radio_2.hide()
            self.ui.train_btn_radio_3.hide()
            self.ui.train_btn_radio_4.hide()
            rows = backend.view()
            self.all_ques_num = len(rows)
            self.ui.train_label_all_count.setText(str(len(rows)))
            self.ui.train_label_curr_count.setText(str(self.current_num))
            num = self.train_ques_num[self.train_current_num]
            item = rows[num]
            answers = self.trainOption_add_correct_ans(item[4])
            self.trainOption_radioBtn(answers)
            self.trainOption_radioBtn_correct_ans(item[4])
            text = f"What is meaning of {item[0]} ? "
            self.ui.train_ques_label.setFont(QFont('Arial', 15))
            self.ui.train_ques_label.setText(text)
        else:
            self.showError_home("Error", "You must have at least 5 word.")

    def trainOption_radioBtn_back(self):
        self.handle_submitToCorrect = 1
        self.handle_submitToAnswer = 1
        self.ui.train_btn_radio_1.hide()
        self.ui.train_btn_radio_2.hide()
        self.ui.train_btn_radio_3.hide()
        self.ui.train_btn_radio_4.hide()
        self.ui.train_radioButton1.setChecked(False)
        self.ui.train_radioButton2.setChecked(False)
        self.ui.train_radioButton3.setChecked(False)
        self.ui.train_radioButton4.setChecked(False)
        if self.current_num == 2:
            self.ui.train_btn_back.setEnabled(False)
        self.current_num -= 1
        self.ui.train_label_curr_count.setText(str(self.current_num))
        if self.current_num == self.all_ques_num - 1:
            self.ui.train_btn_next.setEnabled(True)
        rows = backend.view()
        self.train_current_num -= 1
        num = self.train_ques_num[self.train_current_num]
        item = rows[num]
        answers = self.trainOption_add_correct_ans(item[4])
        self.trainOption_radioBtn(answers)
        self.trainOption_radioBtn_correct_ans(item[4])
        text = f"What is meaning of {item[0]} ? "
        self.ui.train_ques_label.setFont(QFont('Arial', 15))
        self.ui.train_ques_label.setText(text)

    def trainOption_radioBtn_next(self):
        if self.ui.train_radioButton1.isChecked() and self.ui.train_radioButton2.isChecked() and self.ui.train_radioButton3.isChecked() and self.ui.train_radioButton4.isChecked():
            if self.train_current_num not in self.random_ques_white:
                if self.white_answer != self.all_ques_num:
                    self.white_answer += 1
                self.ui.train_label_white_ans.setText(str(self.white_answer))
                self.random_ques_white.append(self.train_current_num)
                self.handle_submitToAnswer = 1
        self.ui.train_btn_radio_1.hide()
        self.ui.train_btn_radio_2.hide()
        self.ui.train_btn_radio_3.hide()
        self.ui.train_btn_radio_4.hide()
        self.ui.train_radioButton1.setChecked(False)
        self.ui.train_radioButton2.setChecked(False)
        self.ui.train_radioButton3.setChecked(False)
        self.ui.train_radioButton4.setChecked(False)
        self.ui.train_btn_back.setEnabled(True)
        if self.current_num + 1 == self.all_ques_num:
            self.ui.train_btn_next.setEnabled(False)
        self.handle_answerToWhite = 0
        self.handle_answerToSubmit = 0
        self.handle_submitToCorrect = 0
        self.handle_submitToAnswer = 0
        self.current_num += 1
        self.ui.train_label_curr_count.setText(str(self.current_num))
        rows = backend.view()
        self.train_current_num += 1
        num = self.train_ques_num[self.train_current_num]
        item = rows[num]
        answers = self.trainOption_add_correct_ans(item[4])
        self.trainOption_radioBtn(answers)
        self.trainOption_radioBtn_correct_ans(item[4])
        text = f"What is meaning of {item[0]} ? "
        self.ui.train_ques_label.setFont(QFont('Arial', 15))
        self.ui.train_ques_label.setText(text)

    def trainOption_radioBtn_answer(self):
        self.handle_answerToSubmit = 1
        if self.ui.train_radioButton1.text() == self.rand_radio_correct:
            self.ui.train_btn_radio_1.show()
        elif self.ui.train_radioButton2.text() == self.rand_radio_correct:
            self.ui.train_btn_radio_2.show()
        elif self.ui.train_radioButton3.text() == self.rand_radio_correct:
            self.ui.train_btn_radio_3.show()
        elif self.ui.train_radioButton4.text() == self.rand_radio_correct:
            self.ui.train_btn_radio_4.show()
        if self.handle_answerToWhite == 0 and self.handle_submitToAnswer == 0:
            if self.white_answer + self.mistake_answer + self.correct_answer != self.all_ques_num:
                self.white_answer += 1
            self.ui.train_label_white_ans.setText(str(self.white_answer))
            self.handle_answerToWhite = 1

    def trainOption_radioBtn_submit(self):
        if self.handle_answerToSubmit == 0:
            if self.ui.train_radioButton1.isChecked() or self.ui.train_radioButton2.isChecked() or self.ui.train_radioButton3.isChecked() or self.ui.train_radioButton4.isChecked():
                if self.ui.train_radioButton1.text() == self.rand_radio_correct:
                    self.ui.train_btn_radio_1.show()
                elif self.ui.train_radioButton2.text() == self.rand_radio_correct:
                    self.ui.train_btn_radio_2.show()
                elif self.ui.train_radioButton3.text() == self.rand_radio_correct:
                    self.ui.train_btn_radio_3.show()
                elif self.ui.train_radioButton4.text() == self.rand_radio_correct:
                    self.ui.train_btn_radio_4.show()
            else:
                self.showError_home("Error", "You should choose one answer.")
            # =================== process of correct or mistake number ===============
            if self.handle_submitToCorrect == 0:
                self.handle_submitToAnswer = 1
                if self.ui.train_radioButton1.isChecked():
                    if self.ui.train_radioButton1.text() == self.rand_radio_correct:
                        if self.correct_answer + self.mistake_answer + self.white_answer != self.all_ques_num:
                            self.correct_answer += 1
                        self.ui.train_label_correct_ans.setText(str(self.correct_answer))
                    else:
                        if self.correct_answer + self.mistake_answer + self.white_answer != self.all_ques_num:
                            self.mistake_answer += 1
                        self.ui.train_label_mistake_ans.setText(str(self.mistake_answer))
                elif self.ui.train_radioButton2.isChecked():
                    if self.ui.train_radioButton2.text() == self.rand_radio_correct:
                        if self.correct_answer + self.mistake_answer + self.white_answer != self.all_ques_num:
                            self.correct_answer += 1
                        self.ui.train_label_correct_ans.setText(str(self.correct_answer))
                    else:
                        if self.correct_answer + self.mistake_answer + self.white_answer != self.all_ques_num:
                            self.mistake_answer += 1
                        self.ui.train_label_mistake_ans.setText(str(self.mistake_answer))
                elif self.ui.train_radioButton3.isChecked():
                    if self.ui.train_radioButton3.text() == self.rand_radio_correct:
                        if self.correct_answer + self.mistake_answer + self.white_answer != self.all_ques_num:
                            self.correct_answer += 1
                        self.ui.train_label_correct_ans.setText(str(self.correct_answer))
                    else:
                        if self.correct_answer + self.mistake_answer + self.white_answer != self.all_ques_num:
                            self.mistake_answer += 1
                        self.ui.train_label_mistake_ans.setText(str(self.mistake_answer))
                elif self.ui.train_radioButton4.isChecked():
                    if self.ui.train_radioButton4.text() == self.rand_radio_correct:
                        if self.correct_answer + self.mistake_answer + self.white_answer != self.all_ques_num:
                            self.correct_answer += 1
                        self.ui.train_label_correct_ans.setText(str(self.correct_answer))
                    else:
                        if self.correct_answer + self.mistake_answer + self.white_answer != self.all_ques_num:
                            self.mistake_answer += 1
                        self.ui.train_label_mistake_ans.setText(str(self.mistake_answer))
                self.handle_submitToCorrect = 1

    def trainOption_radioBtn_correct_ans(self, correct_meaning):
        if self.ui.train_radioButton1.text() == correct_meaning:
            self.rand_radio_correct = correct_meaning
        elif self.ui.train_radioButton2.text() == correct_meaning:
            self.rand_radio_correct = correct_meaning
        elif self.ui.train_radioButton3.text() == correct_meaning:
            self.rand_radio_correct = correct_meaning
        elif self.ui.train_radioButton4.text() == correct_meaning:
            self.rand_radio_correct = correct_meaning

    def trainOption_radioBtn(self, anslist):
        chooseList = list()
        num = randint(0, 3)
        count = 0
        while True:
            if count == 0:
                if num in chooseList:
                    num = randint(0, 3)
                else:
                    self.ui.train_radioButton1.setText(anslist[num])
                    chooseList.append(num)
                    count += 1
            elif count == 1:
                if num in chooseList:
                    num = randint(0, 3)
                else:
                    self.ui.train_radioButton2.setText(anslist[num])
                    chooseList.append(num)
                    count += 1
            elif count == 2:
                if num in chooseList:
                    num = randint(0, 3)
                else:
                    self.ui.train_radioButton3.setText(anslist[num])
                    chooseList.append(num)
                    count += 1
            elif count == 3:
                if num in chooseList:
                    num = randint(0, 3)
                else:
                    self.ui.train_radioButton4.setText(anslist[num])
                    break

    def trainOption_add_correct_ans(self, meaning):
        answers = self.trainOption_answer_collect()
        while True:
            if meaning in answers:
                answers = self.trainOption_answer_collect()
            else:
                answers.append(meaning)
                break
        return answers

    @staticmethod
    def trainOption_answer_collect():
        ans_list = list()
        final_list = list()
        rows = backend.view()
        for item in rows:
            ans_list.append(item[4])
        count = 0
        while True:
            num = randint(0, len(ans_list) - 1)
            if ans_list[num] not in final_list:
                final_list.append(ans_list[num])
                count += 1
            if count == 3:
                break
        return final_list

    def train_group(self):
        self.ui.train_frame_ques.hide()
        self.ui.train_frame_group.show()
        self.ui.train_btn_frame_group.clicked.connect(self.train_group_btn)

    def train_group_btn(self):
        self.current_num = 1
        self.train_current_num = 0
        self.train_ques_num.clear()
        self.ui.train_frame_ques.hide()
        rows = list()
        if len(self.ui.train_lineEdit_group.text()) != 0:
            if self.ui.train_lineEdit_group.text().isnumeric():
                all_word = backend.view()
                for item in all_word:
                    if int(item[6]) == int(self.ui.train_lineEdit_group.text()):
                        rows.append(item)
                if len(rows) >= 5:
                    self.ui.train_frame_ques.show()
                    num = randint(0, len(rows) - 1)
                    count = 0
                    while True:
                        if num in self.train_ques_num:
                            num = randint(0, len(rows) - 1)
                        else:
                            self.train_ques_num.append(num)
                            count += 1
                        if count == len(rows):
                            break
                    if self.current_num == 1:
                        self.ui.train_btn_back.setEnabled(False)
                    self.ui.train_label_correct_ans.setText("0")
                    self.ui.train_label_mistake_ans.setText("0")
                    self.ui.train_label_white_ans.setText("0")
                    self.ui.train_btn_radio_1.hide()
                    self.ui.train_btn_radio_2.hide()
                    self.ui.train_btn_radio_3.hide()
                    self.ui.train_btn_radio_4.hide()
                    self.all_ques_num = len(rows)
                    self.ui.train_label_all_count.setText(str(len(rows)))
                    self.ui.train_label_curr_count.setText(str(self.current_num))
                    num = self.train_ques_num[self.train_current_num]
                    item = rows[num]
                    answers = self.trainOption_add_correct_ans(item[4])
                    self.trainOption_radioBtn(answers)
                    self.trainOption_radioBtn_correct_ans(item[4])
                    text = f"What is meaning of {item[0]} ? "
                    self.ui.train_ques_label.setFont(QFont('Arial', 15))
                    self.ui.train_ques_label.setText(text)
                elif len(rows) == 0:
                    self.showError_home("Error", f"There is no group number {self.ui.train_lineEdit_group.text()}.")
                elif len(rows) < 5:
                    self.showError_home("Error", "You must have at least 5 word.")
            else:
                self.showError_home("Error", "Group should be number.")
        else:
            self.showError_home("Error", "You should fill group line.")

    def setting_author(self):
        self.showInfo_home("Author", "   Sajjad fani     ")

    def setting_telegram(self):
        self.showInfo_home("Telegram", "   @sajad_fani    ")

    def setting_insta(self):
        self.showInfo_home("Instagram", "   @sjdfani    ")

    def setting_excel(self):
        workbook = xlsxwriter.Workbook('EnglishBox.xlsx')
        worksheet = workbook.add_worksheet("My sheet")
        row = 0
        rows = backend.view()
        for item in rows:
            worksheet.write(row, 0, item[0])
            worksheet.write(row, 1, item[1])
            worksheet.write(row, 2, item[2])
            worksheet.write(row, 3, item[3])
            worksheet.write(row, 4, item[4])
            worksheet.write(row, 5, item[5])
            worksheet.write(row, 6, item[6])
            row += 1
        workbook.close()
        self.showInfo_home("Excel", "Convert is successful.")


def setup():
    app = QApplication([])
    ui = HomePage()
    ui.show()
    app.exec_()


setup()
