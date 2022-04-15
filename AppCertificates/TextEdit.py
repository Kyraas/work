import sys
from PyQt6 import QtWidgets

app = QtWidgets.QApplication(sys.argv)

d = QtWidgets.QDialog()
l = QtWidgets.QVBoxLayout()
d.setLayout(l)

# construct the text edit
edit = QtWidgets.QTextEdit()
edit.setText('help:<br>search:<br>run:<br>')
l.addWidget(edit)

# parse the text and add formatting. This could also be made into a function which gets called by a signal such as edit.editingFinished()
text = edit.toPlainText()
new_text = ''
for line in text.split('\n'):
    new_text += '<span style="background-color: yellow">' + line + '</span><br>'
edit.setText(new_text) # put it back to the text edit

d.show()
sys.exit(app.exec())