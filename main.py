
# < ======================================================================================================
# < Imports
# < ======================================================================================================

import sys
import os
import json
import logging
from PyQt5.QtCore import Qt
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

# < ======================================================================================================
# < Constants
# < ======================================================================================================

with open("settings.json", 'r') as f:
    SETTINGS: dict = json.load(f)
    
FOLDER_ID: str = SETTINGS["FOLDER_ID"]
TOKEN_PATH: str = SETTINGS["TOKEN_PATH"]
CLIENT_SECRET_PATH: str = SETTINGS["CLIENT_SECRET_PATH"]
SCOPES: list[str] = SETTINGS["SCOPES"]
IGNORED_PATTERNS: list[str] = SETTINGS["IGNORED_PATTERNS"]

# < ======================================================================================================
# < Tools
# < ======================================================================================================

class tools:

    @staticmethod
    def get_default_icon():
        """Get default icon from saved bitmap"""

        bitmap: list[str] = [
            "11111111",
            "11111111",
            "11000011",
            "11000011",
            "11000011",
            "11000011",
            "11111111",
            "11111111"
            ]
        
        size = len(bitmap)
        pixmap = QPixmap(size, size)
        pixmap.fill(QColor(Qt.transparent))
        painter = QPainter(pixmap)
        painter.setPen(QPen(QColor(255, 255, 255)))
        for y in range(size):
            for x in range(size):
                if bitmap[y][x] == '1':
                    painter.drawPoint(x, y)
        painter.end()
        return QIcon(pixmap)
    
    @staticmethod
    def get_main_window() -> QMainWindow | None:
        """Function to find the QMainWindow of the current QApplication"""
        app = QApplication.instance()
        for widget in app.topLevelWidgets():
            if isinstance(widget, QMainWindow):
                return widget
        return None
    
    @staticmethod
    @property
    def window():
        """Property to return the QMainWindow of the current QApplication"""
        return tools.get_main_window()
    
    @staticmethod
    def set_opacity(widget: QWidget, opacity: float = 1.0) -> None:
        """Set opacity for a given widget"""
        effect = QGraphicsOpacityEffect()
        effect.setOpacity(opacity)
        widget.setGraphicsEffect(effect)

    @staticmethod
    def rgba_to_hex(r: int, g: int, b: int, a: int = 255) -> str:
        """Convert RGBA value to a hex color code"""
        return f'#{r:02X}{g:02X}{b:02X}{a:02X}'
    
    @staticmethod
    def center(window) -> None:
        """Center window in the center of the active display"""
        frameGm = window.frameGeometry()
        screen = QApplication.desktop().screenNumber(QApplication.desktop().cursor().pos())
        centerPoint = QApplication.desktop().screenGeometry(screen).center()
        frameGm.moveCenter(centerPoint)
        window.move(frameGm.topLeft())
        
    @staticmethod
    def get_filename(extension: str = "") -> str:
        """Get filename from current date and time"""
        from datetime import datetime
        current_date: str = datetime.now().strftime("%Y-%m-%d")
        current_time: str = datetime.now().strftime("%H%M")
        return f"data_{current_date}_{current_time}" + extension

    @staticmethod
    def get_current_date_and_time() -> str:
        """Get the current date and time as a string"""
        from datetime import datetime
        current_date: str = datetime.now().strftime("%Y-%m-%d")
        current_time: str = datetime.now().strftime("%H:%M:%S")
        return f"[{current_date} | {current_time}]"
    
    @staticmethod
    def clear_table(table: QTableWidget) -> None:
        """Clear data and rows from a QTableWidget"""
        table.clear() # < Not required but adds an extra layer of protection
        table.setRowCount(0)

    def open_explorer_to_file(filepath):
        """Open a windows explorer window and highlight / select the specified filepath"""
        import subprocess
        explorer = os.path.join(os.getenv('WINDIR'), 'explorer.exe')
        filepath = os.path.normpath(filepath)
        if os.path.isdir(filepath):
            subprocess.run([explorer, filepath])
        elif os.path.isfile(filepath):
            subprocess.run([explorer, '/select,', filepath])

    @staticmethod
    def get_screen_size() -> tuple[int, int]:
        """Get the size of the current screen"""
        app = QApplication.instance()
        screen = app.primaryScreen()
        screen_geometry = screen.geometry()
        return screen_geometry.width(), screen_geometry.height()

    @staticmethod
    def test() -> None:
        """Logs text, mainly used as a test function to check if a PyQt action is called correctly"""
        logging.info("tools.test function called")

# < ======================================================================================================
# < Table QWidget Class
# < ======================================================================================================

class Table(QWidget):

    def __init__(self):
        """Initialize the Table"""
        super().__init__()
        self.setup_ui()

    def setup_ui(self) -> None:
        """Setup UI for the Table"""

        with open("settings.json", 'r') as f:
            self.settings = json.load(f)

        self.setAcceptDrops(True)
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.table = QTableWidget(0, 3)
        self.table.setHorizontalHeaderLabels(["Filename", "Path", "Type"])
        self.table.setColumnWidth(0, 200)
        self.table.setColumnWidth(1, 200)
        self.table.setColumnWidth(2, 200)
        self.layout.addWidget(self.table)

        self.upload_button = QPushButton("Upload")
        self.upload_button.clicked.connect(self.upload)
        self.layout.addWidget(self.upload_button)

    def update_folder_id(self) -> None:
        """Change FOLDER_ID in settings.json to the value of the resulting QInputDialog"""

        current_folder_id = self.settings.get('FOLDER_ID')

        dialog = QInputDialog(self)                 
        dialog.setInputMode(QInputDialog.TextInput)
        dialog.setLabelText("Google Drive Folder ID")
        dialog.setTextValue(current_folder_id)
        dialog.setWindowTitle("Update Folder ID")
        dialog.resize(500, 100)
        ok = dialog.exec()
        value = dialog.textValue()

        if not ok:
            return
        elif not value:
            QMessageBox.warning(self, "Input Error", "Valid text must be provided")
            return
        else:
            self.change_setting("FOLDER_ID", value)

    def change_setting(self, name: str, value: any, filepath: str = "settings.json") -> None:
        """Change a setting in the settings.json file"""

        with open(filepath, 'r') as file:
            settings = json.load(file)
        
        if name in settings:
            settings[name] = value
            with open(filepath, 'w') as file:
                json.dump(settings, file, indent = 4)
            logging.info(f"Setting for '{name}' updated successfully to {value} in {filepath}")
        else:
            logging.info(f"Setting '{name}' not found in the {filepath}")

    def clear(self) -> None:
        """Clear all entries from the file table"""
        if self.confirmation():
            self.table.clearContents()
            self.table.setRowCount(0)

    def confirmation(self) -> bool:
        """Show confirmation dialog before an action and return boolean"""
        reply = QMessageBox.question(
            self,
            'Confirmation',
            'Are you sure?',
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            return True
        else:
            return False
        
    def get_table_rows(self) -> list[list[str]]:
        """Get table data as a list of rows"""
        output: list[list[str]] = []
        for row_index in range(self.table.rowCount()):
            row: list[str] = []
            for column_index in range(self.table.columnCount()):
                item = self.table.item(row_index, column_index)
                text = item.text()
                row.append(text)
            output.append(row)
        return output
    
    # < ======================================================================================================
    # < Upload Method
    # < ======================================================================================================
        
    def upload(self) -> None:
        """Upload files to Google Drive"""

        rows: list[list[str]] = self.get_table_rows()
      
        if not rows:
            QMessageBox.warning(self, "Upload Error", "No files or folders selected for upload")
            return
        
        filepaths: list[str] = [item[1] for item in rows if item[2] == 'File']
        folderpaths: list[str] = [item[1] for item in rows if item[2] == 'Folder']

        from authenticator import get_drive_service
        from uploader import upload_mixed

        drive_service = get_drive_service(TOKEN_PATH, CLIENT_SECRET_PATH, SCOPES)

        try:
            upload_mixed(drive_service, filepaths, folderpaths, FOLDER_ID)

        except Exception as e:
            QMessageBox.warning(self, "Upload Error", f"An error occurred: {repr(e)}")
            return
        
        QMessageBox.information(self, "Success", "Upload completed successfully")
        QApplication.quit()
        
    # < ======================================================================================================

    def open_folder_dialog(self) -> None:
        """Open folder dialog to select folder and add to the table"""

        folder_path = QFileDialog.getExistingDirectory(self, "Select Folder")
        if folder_path:
            self.add_files([folder_path])

    def open_file_dialog(self) -> None:
        """Open file dialog to select files and add them to the table"""

        output: tuple[list[str]] = QFileDialog().getOpenFileNames(self, "Select File(s)")
        filenames, _ = output
        self.add_files(filenames)

    def add_files(self, paths: list[str]) -> None:
        """Add selected files or folders to the table, avoiding duplicates"""
        existing_filenames = {self.table.item(row, 0).text() for row in range(self.table.rowCount())}
        new_items = []

        for path in paths:
            if os.path.isdir(path):
                new_items.append((os.path.basename(path), path, "Folder"))
            else:
                filename = os.path.basename(path)
                if filename not in existing_filenames:
                    new_items.append((filename, path, "File"))

        if new_items:
            current_row_count = self.table.rowCount()
            self.table.setRowCount(current_row_count + len(new_items))
            
            for row, (filename, full_path, item_type) in enumerate(new_items):
                self.table.setItem(current_row_count + row, 0, QTableWidgetItem(filename))
                self.table.setItem(current_row_count + row, 1, QTableWidgetItem(full_path))
                self.table.setItem(current_row_count + row, 2, QTableWidgetItem(item_type))

            self.table.setColumnWidth(0, 200)
            self.table.resizeColumnToContents(1)

    def dragEnterEvent(self, event: QDragEnterEvent) -> None:
        """Handle drag enter event"""
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event: QDropEvent) -> None:
        """Handle drop event"""
        urls = event.mimeData().urls()
        paths = [url.toLocalFile() for url in urls]
        self.add_files(paths)

# < ======================================================================================================
# < Main Window
# < ======================================================================================================

class Window(QMainWindow):

    def __init__(self, level: int = logging.DEBUG, w: int = 800, h: int = 600, x: int = 100, y: int = 100) -> None:
        """Initialise the main window"""
        super().__init__()
        self.setup_all(level, w, h, x, y)
        self.show()

    def setup_all(self, level: int, w: int, h: int, x: int, y: int):
        """Run all setup methods"""
        self.setup_window(w, h, x, y)
        self.setup_ui(w, h, x, y)
        self.setup_shortcuts()
        self.setup_menus()
        self.setup_statusbar()
        logging.info("Setup complete")

    def setup_window(self, w: int, h: int, x: int, y: int):
        """Setup the window"""
        self.setWindowTitle("Upload Files to Google Drive")
        self.setWindowIcon(tools.get_default_icon())
        self.setGeometry(x, y, w, h)
        self.resize(w, h)
        tools.center(self)

    def setup_ui(self, w: int, h: int, x: int, y: int):
        """Setup the ui of the window"""

        self.central_widget = QWidget()
        self.central_layout = QVBoxLayout()
        self.central_layout.setContentsMargins(10, 10, 10, 10)
        self.central_widget.setLayout(self.central_layout)
        self.setCentralWidget(self.central_widget)

        # < Integrate Table as a widget
        self.table = Table()
        self.central_layout.addWidget(self.table)

    def setup_menus(self) -> None:
        """Setup the menus at the top of the application"""

        icon = self.style().standardIcon(QStyle.SP_ArrowRight)

        # < ======================================================================================================
        # < Menu Headers
        # < ======================================================================================================

        self.fileMenu = self.menuBar().addMenu("&File")
        self.helpMenu = self.menuBar().addMenu("&Help")

        # < ======================================================================================================
        # < File Actions
        # < ======================================================================================================
        
        action = QAction(icon, "&Add File(s)", self)
        action.setStatusTip("Add file or multiple files to the list")
        action.triggered.connect(self.table.open_file_dialog)
        self.fileMenu.addAction(action)

        action = QAction(icon, "&Add Folder", self)
        action.setStatusTip("Add a folder to the list")
        action.triggered.connect(self.table.open_folder_dialog)
        self.fileMenu.addAction(action)

        self.fileMenu.addSeparator()

        action = QAction(icon, "&Upload", self)
        action.setStatusTip("Upload all files and folders in the list")
        action.triggered.connect(self.table.upload)
        self.fileMenu.addAction(action)

        self.fileMenu.addSeparator()

        action = QAction(icon, "&Clear List", self)
        action.setStatusTip("Remove all files and folders from the list")
        action.triggered.connect(self.table.clear)
        self.fileMenu.addAction(action)

        self.fileMenu.addSeparator()

        action = QAction(icon, "&Change Folder ID", self)
        action.setStatusTip("Change the ID of the parent Google Drive folder")
        action.triggered.connect(self.table.update_folder_id)
        self.fileMenu.addAction(action)

        self.fileMenu.addSeparator()

        action = QAction(icon, "&Exit", self)
        action.setStatusTip("Exit the application")
        action.triggered.connect(quit)
        self.fileMenu.addAction(action)

        # < ======================================================================================================
        # < Help Actions
        # < ======================================================================================================
        
        action = QAction(icon, "&Help", self)
        action.setStatusTip("View helpful information")
        action.triggered.connect(tools.test)
        self.helpMenu.addAction(action)

    def setup_shortcuts(self) -> None:
        """Setup for keyboard shortcuts"""
        def shortcut(*args):
            """Shortcut function"""
            logging.info("shortcut running")

        self.shortcut = QShortcut(QKeySequence("Ctrl+O"), self)
        self.shortcut.activated.connect(shortcut)

    def setup_statusbar(self) -> None:
        """Enable the statusbar message at the bottom of the application"""
        # self.statusBar()
        message: str = "Drag and drop files or folders to add to list"
        self.statusBar().showMessage(message)

# < ======================================================================================================
# < Main Function
# < ======================================================================================================

def main():
    """Main function"""
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec())

# < ======================================================================================================
# < Execution
# < ======================================================================================================

if __name__ == "__main__":
    logging.basicConfig(filename = 'app.log', level = logging.INFO, format = '%(asctime)s - %(levelname)s - %(message)s', filemode = 'w')
    logging.info(f"Module '{__name__}' running")
    main()