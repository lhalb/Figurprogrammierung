from PyQt5.QtWidgets import QMessageBox as QMB

def show_error_box(text='Fehler'):
    msg = QMB()
    msg.setWindowTitle("Hinweis")
    msg.setText(text)
    msg.setIcon(QMB.Critical)
    msg.setStandardButtons(QMB.Ok)
    msg.setDefaultButton(QMB.Ok)

    msg.exec()


def show_info_box(text='Info'):
    msg = QMB()
    msg.setWindowTitle("Information")
    msg.setText(text)
    msg.setIcon(QMB.Information)
    msg.setStandardButtons(QMB.Ok)
    msg.setDefaultButton(QMB.Ok)

    msg.exec()


def show_msg_box(text='Dies ist eine Warnung.'):
    msg = QMB()
    msg.setWindowTitle("Warnung")
    msg.setText(text)
    msg.setIcon(QMB.Warning)
    msg.setStandardButtons(QMB.Cancel | QMB.Ok)
    msg.setDefaultButton(QMB.Ok)

    returnvalue = msg.exec()
    if returnvalue == QMB.Ok:
        press = True
    else:
        press = False

    return press
