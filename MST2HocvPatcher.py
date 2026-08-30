# coding: utf-8
"""
MIB STD2 HMIOFFCLOCKVIEW PATCHER v1.2
Скрывает виджет «дата из будущего» под часами в режиме ожидания
на PQ-юнитах с HMI от ZR-прошивок (SEAT / SKODA / VW).

Кроссплатформенный (Windows / Linux), PySide6.
Язык интерфейса: авто по системе, можно переопределить: --ru | --en
"""

import locale
import os
import sys

from PySide6.QtCore import Qt, QUrl
from PySide6.QtGui import QDesktopServices, QFont
from PySide6.QtWidgets import (
    QApplication,
    QFileDialog,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QMessageBox,
    QProgressBar,
    QPushButton,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

VERSION = "1.2"

LANGS = {
    "ru": {
        "window_title": "MIB STD2 HMIOFFCLOCKVIEW PATCHER for SEAT/SKODA/VW ZR-PQ Converts v{v}",
        "app_title": "MIB STD2 HMIOFF DATE PATCHER",
        "desc": "Автоматический патчер для скрытия виджета даты\nна экране часов в режиме ожидания\nдля PQ юнитов с HMI от ZR прошивок\n",
        "more": "🌐 Подробнее на Drive2.ru",
        "more_tip": "Перейти на статью на Drive2.ru",
        "files_group": "Файлы Hocv.jxe для обработки",
        "file1": "Файл Hocv_08DA85708EEB9B2F_CA54.jxe",
        "file2": "Файл Hocv_08DA85708EEB9B2F_DA1F.jxe",
        "browse1": "📁 Файл 1",
        "browse2": "📁 Файл 2",
        "run": "🚀 Запуск",
        "log_label": "Лог выполнения:",
        "ready": "Готов к работе",
        "search_area": "• Область поиска: 0x{:04X} - 0x{:04X}",
        "replace": "• Замена: 0x{:02X} → 0x{:02X}",
        "signatures": "• Сигнатуры: SEAT, SKODA, VW (ZR Navi/Non Navi)",
        "hint": "\nВыберите оба файла Hocv*.jxe из прошивки и нажмите 'Запуск'",
        "select_file": "Выберите файл {}",
        "all_files": "Все файлы (*)",
        "picked": "\n📄 Выбран файл {}: {}",
        "err_title": "Ошибка",
        "pick_both": "Выберите оба файла!",
        "confirm_title": "Подтверждение",
        "confirm": "Выбраны файлы:\n\n• Файл 1: {}\n• Файл 2: {}\nПродолжить?",
        "start": "\n🔍 Начинаю автоматический поиск и замену...",
        "processing": "📂 Обработка {}:",
        "found": "✅ Для {} найдены сигнатуры: {}",
        "bytes_replaced": "   Заменено байт: {}",
        "not_found": "❌ Для {} сигнатуры не найдены",
        "total_ok": "🎉 ОБЩИЙ ИТОГ: Исправлено {} файл(а)",
        "done_status": "Завершено. Исправлено {} файл(а)",
        "success_title": "Успех",
        "success_msg": "Патчинг завершен!\nИсправлено {} файл(а).",
        "total_fail": "😞 ОБЩИЙ ИТОГ: Сигнатуры не найдены в обоих файлах",
        "fail_status": "Сигнатуры не найдены",
        "warn_title": "Внимание",
        "warn_msg": "Сигнатуры не найдены в указанных файлах.\nПроверьте, что это файлы Hocv*.jxe от ZR прошивки.",
        "error_log": "💥 Ошибка: {}",
        "err_msg": "Произошла ошибка:\n{}",
        "sig_found": "   Найдена сигнатура {} по адресу: 0x{:04X}",
        "sig_replaced": "   Для {} заменено байт: {}",
        "sig_error": "   Ошибка при обработке {} в {}: {}",
        "file_n": "Файл {}",
    },
    "en": {
        "window_title": "MIB STD2 HMIOFFCLOCKVIEW PATCHER for SEAT/SKODA/VW ZR-PQ Converts v{v}",
        "app_title": "MIB STD2 HMIOFF DATE PATCHER",
        "desc": "Automatic patcher that hides the date widget\nbelow the clock in standby mode\non PQ units running ZR HMI firmware\n",
        "more": "🌐 More info on Drive2.ru",
        "more_tip": "Open the Drive2.ru article",
        "files_group": "Hocv.jxe files to process",
        "file1": "File Hocv_08DA85708EEB9B2F_CA54.jxe",
        "file2": "File Hocv_08DA85708EEB9B2F_DA1F.jxe",
        "browse1": "📁 File 1",
        "browse2": "📁 File 2",
        "run": "🚀 Run",
        "log_label": "Execution log:",
        "ready": "Ready",
        "search_area": "• Search area: 0x{:04X} - 0x{:04X}",
        "replace": "• Replace: 0x{:02X} → 0x{:02X}",
        "signatures": "• Signatures: SEAT, SKODA, VW (ZR Navi/Non Navi)",
        "hint": "\nSelect both Hocv*.jxe files from the firmware and press 'Run'",
        "select_file": "Select file {}",
        "all_files": "All files (*)",
        "picked": "\n📄 Selected file {}: {}",
        "err_title": "Error",
        "pick_both": "Select both files!",
        "confirm_title": "Confirmation",
        "confirm": "Selected files:\n\n• File 1: {}\n• File 2: {}\nContinue?",
        "start": "\n🔍 Starting automatic search and replace...",
        "processing": "📂 Processing {}:",
        "found": "✅ For {} signatures found: {}",
        "bytes_replaced": "   Bytes replaced: {}",
        "not_found": "❌ No signatures found for {}",
        "total_ok": "🎉 TOTAL RESULT: {} file(s) patched",
        "done_status": "Done. {} file(s) patched",
        "success_title": "Success",
        "success_msg": "Patching complete!\n{} file(s) patched.",
        "total_fail": "😞 TOTAL RESULT: No signatures found in either file",
        "fail_status": "Signatures not found",
        "warn_title": "Warning",
        "warn_msg": "No signatures found in the specified files.\nPlease check these are Hocv*.jxe files from ZR firmware.",
        "error_log": "💥 Error: {}",
        "err_msg": "An error occurred:\n{}",
        "sig_found": "   Signature {} found at address: 0x{:04X}",
        "sig_replaced": "   For {} bytes replaced: {}",
        "sig_error": "   Error processing {} in {}: {}",
        "file_n": "File {}",
    },
}


class AutoHexPatcherGUI(QMainWindow):
    START_ADDR = 0x5B00
    END_ADDR = 0x6000
    SEARCH_BYTE = 0x04
    REPLACE_BYTE = 0x03
    SIGNATURES = {
        "SEAT Non Nav": "b2 2c 00 04 11 1e 01 11 01 01 11",
        "SEAT Nav": "b2 2b 00 04 11 1e 01 11 01 01 11",
        "SKODA/VW Non Nav": "b2 2c 00 04 11 38 02 10 74 11 73",
        "SKODA/VW Nav": "b2 2b 00 04 11 38 02 10 74 11 73",
    }

    def __init__(self, lang):
        super().__init__()
        self.lang = lang
        self.file1_path = None
        self.file2_path = None

        self.setWindowTitle(
            LANGS[lang]["window_title"].format(v=VERSION)
        )
        self.setGeometry(100, 100, 900, 800)
        self.setup_ui()

    def tr(self, key):
        return LANGS[self.lang][key]

    def setup_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)

        title = QLabel(self.tr("app_title"))
        title.setFont(QFont("Arial", 18, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet(
            "padding: 15px; background-color: #2c3e50; color: white; border-radius: 10px;"
        )
        layout.addWidget(title)

        desc = QLabel(self.tr("desc"))
        desc.setAlignment(Qt.AlignCenter)
        desc.setStyleSheet("padding: 10px; font-size: 12px;")
        layout.addWidget(desc)

        link_row = QHBoxLayout()
        link_row.addStretch()
        link = QLabel(
            '<a href="https://www.drive2.ru/l/712453299302827334" '
            'style="color: #3498db; text-decoration: none; font-size: 11px;">'
            + self.tr("more")
            + "</a>"
        )
        link.setOpenExternalLinks(True)
        link.setToolTip(self.tr("more_tip"))
        link.setCursor(Qt.PointingHandCursor)
        link_row.addWidget(link)
        link_row.addStretch()
        layout.addLayout(link_row)

        group = QGroupBox(self.tr("files_group"))
        self.files_group = group
        g = QVBoxLayout(group)

        row1 = QHBoxLayout()
        self.file1_label = QLabel(self.tr("file1"))
        self.file1_label.setStyleSheet(
            "padding: 8px; border: 2px solid #3498db; border-radius: 5px;"
        )
        self.file1_label.setMinimumHeight(40)
        btn1 = QPushButton(self.tr("browse1"))
        btn1.clicked.connect(lambda: self.browse_file(1))
        btn1.setStyleSheet(self._btn_style("#3498db", "#2980b9"))
        row1.addWidget(self.file1_label, 3)
        row1.addWidget(btn1, 1)
        g.addLayout(row1)

        row2 = QHBoxLayout()
        self.file2_label = QLabel(self.tr("file2"))
        self.file2_label.setStyleSheet(
            "padding: 8px; border: 2px solid #3498db; border-radius: 5px;"
        )
        self.file2_label.setMinimumHeight(40)
        btn2 = QPushButton(self.tr("browse2"))
        btn2.clicked.connect(lambda: self.browse_file(2))
        btn2.setStyleSheet(self._btn_style("#3498db", "#2980b9"))
        row2.addWidget(self.file2_label, 3)
        row2.addWidget(btn2, 1)
        g.addLayout(row2)

        layout.addWidget(group)

        self.run_btn = QPushButton(self.tr("run"))
        self.run_btn.clicked.connect(self.auto_patch)
        self.run_btn.setStyleSheet(
            """
            QPushButton { padding: 15px; background-color: #27ae60; color: white;
                          font-weight: bold; border-radius: 8px; font-size: 16px; }
            QPushButton:hover { background-color: #229954; }
            QPushButton:disabled { background-color: #95a5a6; }
        """
        )
        self.run_btn.setMinimumHeight(50)
        self.run_btn.setEnabled(False)
        layout.addWidget(self.run_btn)

        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        self.progress_bar.setStyleSheet(
            """
            QProgressBar { border: 2px solid #34495e; border-radius: 5px;
                           text-align: center; height: 20px; }
            QProgressBar::chunk { background-color: #27ae60; }
        """
        )
        layout.addWidget(self.progress_bar)

        log_label = QLabel(self.tr("log_label"))
        log_label.setStyleSheet("font-weight: bold; padding: 5px;")
        layout.addWidget(log_label)

        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        self.log_text.setFont(QFont("Courier", 9))
        self.log_text.setStyleSheet(
            "QTextEdit { border: 2px solid #bdc3c7; border-radius: 5px; padding: 5px; }"
        )
        layout.addWidget(self.log_text, 1)

        self.statusBar().showMessage(self.tr("ready"))

        self.log("=== MIB STD2 HMIOFFCLOCKVIEW PATCHER {} ===".format(VERSION))
        self.log(self.tr("search_area").format(self.START_ADDR, self.END_ADDR))
        self.log(
            self.tr("replace").format(self.SEARCH_BYTE, self.REPLACE_BYTE)
        )
        self.log(self.tr("signatures"))
        self.log(self.tr("hint"))

    @staticmethod
    def _btn_style(base, hover):
        return (
            "QPushButton { padding: 10px; background-color: "
            + base
            + "; color: white; font-weight: bold; border-radius: 5px; }"
            "QPushButton:hover { background-color: "
            + hover
            + "; }"
        )

    def browse_file(self, file_number):
        path, _ = QFileDialog.getOpenFileName(
            self, self.tr("select_file").format(file_number), "", self.tr("all_files")
        )
        if not path:
            return
        if file_number == 1:
            self.file1_path = path
            self.file1_label.setText(os.path.basename(path))
        else:
            self.file2_path = path
            self.file2_label.setText(os.path.basename(path))

        if self.file1_path and self.file2_path:
            self.run_btn.setEnabled(True)
        self.log(self.tr("picked").format(file_number, path))

    def log(self, message):
        self.log_text.append(message)
        self.log_text.verticalScrollBar().setValue(
            self.log_text.verticalScrollBar().maximum()
        )
        QApplication.processEvents()

    def auto_patch(self):
        if not self.file1_path or not self.file2_path:
            QMessageBox.warning(self, self.tr("err_title"), self.tr("pick_both"))
            return

        reply = QMessageBox.question(
            self,
            self.tr("confirm_title"),
            self.tr("confirm").format(self.file1_path, self.file2_path),
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        )
        if reply != QMessageBox.StandardButton.Yes:
            return

        self.log(self.tr("start"))
        self.progress_bar.setVisible(True)
        self.progress_bar.setRange(0, 100)
        self.run_btn.setEnabled(False)

        try:
            total = 0
            files = [
                (1, self.file1_path),
                (2, self.file2_path),
            ]
            for num, path in files:
                name = self.tr("file_n").format(num)
                self.log(self.tr("processing").format(name))

                patched = 0
                found = []
                for sig_name, sig_hex in self.SIGNATURES.items():
                    signature = bytes.fromhex(sig_hex.replace(" ", ""))
                    n = self.patch_file_signature(path, signature, sig_name, name)
                    if n > 0:
                        patched += n
                        found.append(sig_name)

                if patched > 0:
                    self.log(self.tr("found").format(name, ", ".join(found)))
                    self.log(self.tr("bytes_replaced").format(patched))
                    total += patched
                else:
                    self.log(self.tr("not_found").format(name))

                self.progress_bar.setValue(50 if num == 1 else 100)

            self.log("\n" + "=" * 50)
            if total > 0:
                self.log(self.tr("total_ok").format(total))
                self.statusBar().showMessage(self.tr("done_status").format(total))
                QMessageBox.information(
                    self, self.tr("success_title"), self.tr("success_msg").format(total)
                )
            else:
                self.log(self.tr("total_fail"))
                self.statusBar().showMessage(self.tr("fail_status"))
                QMessageBox.warning(
                    self, self.tr("warn_title"), self.tr("warn_msg")
                )

        except Exception as e:
            self.log(self.tr("error_log").format(str(e)))
            QMessageBox.critical(
                self, self.tr("err_title"), self.tr("err_msg").format(str(e))
            )
        finally:
            self.progress_bar.setVisible(False)
            self.run_btn.setEnabled(True)

    def patch_file_signature(self, file_path, signature, sig_name, file_name):
        count = 0
        try:
            with open(file_path, "r+b") as f:
                f.seek(self.START_ADDR)
                area = f.read(self.END_ADDR - self.START_ADDR)

                pos = 0
                first_logged = False
                while pos < len(area):
                    hit = area.find(signature, pos)
                    if hit == -1:
                        break
                    abs_pos = self.START_ADDR + hit

                    if not first_logged:
                        self.log(
                            self.tr("sig_found").format(sig_name, abs_pos)
                        )
                        first_logged = True

                    for offset, byte in enumerate(signature):
                        if byte == self.SEARCH_BYTE:
                            f.seek(abs_pos + offset)
                            f.write(bytes([self.REPLACE_BYTE]))
                            count += 1

                    pos = hit + 1

                if first_logged and count > 0:
                    self.log(self.tr("sig_replaced").format(sig_name, count))

        except Exception as e:
            self.log(self.tr("sig_error").format(sig_name, file_name, str(e)))

        return count


def detect_lang():
    for arg in sys.argv[1:]:
        if arg in ("--ru", "--en"):
            return arg[2:]
    try:
        lang = locale.getdefaultlocale()[0] or ""
        return "ru" if lang.lower().startswith("ru") else "en"
    except Exception:
        return "ru"


def main():
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    window = AutoHexPatcherGUI(detect_lang())
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
