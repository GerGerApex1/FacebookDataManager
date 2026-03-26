# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mainVpgOsn.ui'
##
## Created by: Qt User Interface Compiler version 6.10.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
import logging
import sys
from pathlib import Path

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s  %(levelname)-8s  %(name)s  %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

from PySide6.QtWidgets import (QApplication, QCheckBox, QComboBox, QDialog,
    QFileDialog, QGridLayout, QGroupBox, QHBoxLayout, QHeaderView, QInputDialog,
    QLabel, QLineEdit, QListWidget, QListWidgetItem, QMainWindow, QMessageBox,
    QProgressBar, QPushButton, QRadioButton, QSizePolicy, QSlider, QSpinBox,
    QTabWidget, QTableWidget, QTableWidgetItem, QTextEdit, QVBoxLayout, QWidget)
from modules import face_detection, rename_images, rename_videos, file_transfer

class Ui_FacebookMediaGUI(object):
    def setupUi(self, FacebookMediaGUI):
        if not FacebookMediaGUI.objectName():
            FacebookMediaGUI.setObjectName(u"FacebookMediaGUI")
        FacebookMediaGUI.resize(900, 700)
        self.centralwidget = QWidget(FacebookMediaGUI)
        self.centralwidget.setObjectName(u"centralwidget")
        self.centralLayout = QVBoxLayout(self.centralwidget)
        self.centralLayout.setObjectName(u"centralLayout")
        self.tabs = QTabWidget(self.centralwidget)
        self.tabs.setObjectName(u"tabs")
        self.face_detection_tab = QWidget()
        self.face_detection_tab.setObjectName(u"face_detection_tab")
        self.fdMainLayout = QVBoxLayout(self.face_detection_tab)
        self.fdMainLayout.setObjectName(u"fdMainLayout")
        self.fdDirsGroup = QGroupBox(self.face_detection_tab)
        self.fdDirsGroup.setObjectName(u"fdDirsGroup")
        self.fdDirsLayout = QGridLayout(self.fdDirsGroup)
        self.fdDirsLayout.setObjectName(u"fdDirsLayout")
        self.fdSrcLabel = QLabel(self.fdDirsGroup)
        self.fdSrcLabel.setObjectName(u"fdSrcLabel")

        self.fdDirsLayout.addWidget(self.fdSrcLabel, 0, 0, 1, 1)

        self.src_dir_edit = QLineEdit(self.fdDirsGroup)
        self.src_dir_edit.setObjectName(u"src_dir_edit")

        self.fdDirsLayout.addWidget(self.src_dir_edit, 0, 1, 1, 1)

        self.fdSrcBrowseBtn = QPushButton(self.fdDirsGroup)
        self.fdSrcBrowseBtn.setObjectName(u"fdSrcBrowseBtn")

        self.fdDirsLayout.addWidget(self.fdSrcBrowseBtn, 0, 2, 1, 1)

        self.fdDestLabel = QLabel(self.fdDirsGroup)
        self.fdDestLabel.setObjectName(u"fdDestLabel")

        self.fdDirsLayout.addWidget(self.fdDestLabel, 1, 0, 1, 1)

        self.dest_dir_edit = QLineEdit(self.fdDirsGroup)
        self.dest_dir_edit.setObjectName(u"dest_dir_edit")

        self.fdDirsLayout.addWidget(self.dest_dir_edit, 1, 1, 1, 1)

        self.fdDestBrowseBtn = QPushButton(self.fdDirsGroup)
        self.fdDestBrowseBtn.setObjectName(u"fdDestBrowseBtn")

        self.fdDirsLayout.addWidget(self.fdDestBrowseBtn, 1, 2, 1, 1)


        self.fdMainLayout.addWidget(self.fdDirsGroup)

        self.fdConfigGroup = QGroupBox(self.face_detection_tab)
        self.fdConfigGroup.setObjectName(u"fdConfigGroup")
        self.fdConfigLayout = QGridLayout(self.fdConfigGroup)
        self.fdConfigLayout.setObjectName(u"fdConfigLayout")
        self.minFacesLabel = QLabel(self.fdConfigGroup)
        self.minFacesLabel.setObjectName(u"minFacesLabel")

        self.fdConfigLayout.addWidget(self.minFacesLabel, 0, 0, 1, 1)

        self.min_faces_spin = QSpinBox(self.fdConfigGroup)
        self.min_faces_spin.setObjectName(u"min_faces_spin")
        self.min_faces_spin.setMinimum(1)
        self.min_faces_spin.setMaximum(20)
        self.min_faces_spin.setValue(1)

        self.fdConfigLayout.addWidget(self.min_faces_spin, 0, 1, 1, 1)

        self.maxFacesLabel = QLabel(self.fdConfigGroup)
        self.maxFacesLabel.setObjectName(u"maxFacesLabel")
        self.maxFacesLabel.setText("Max Faces:")

        self.fdConfigLayout.addWidget(self.maxFacesLabel, 0, 2, 1, 1)

        self.max_faces_spin = QSpinBox(self.fdConfigGroup)
        self.max_faces_spin.setObjectName(u"max_faces_spin")
        self.max_faces_spin.setMinimum(0)
        self.max_faces_spin.setMaximum(20)
        self.max_faces_spin.setValue(0)

        self.fdConfigLayout.addWidget(self.max_faces_spin, 0, 3, 1, 1)

        self.threadsLabel = QLabel(self.fdConfigGroup)
        self.threadsLabel.setObjectName(u"threadsLabel")

        self.fdConfigLayout.addWidget(self.threadsLabel, 1, 0, 1, 1)

        self.threads_spin = QSpinBox(self.fdConfigGroup)
        self.threads_spin.setObjectName(u"threads_spin")
        self.threads_spin.setMinimum(1)
        self.threads_spin.setMaximum(32)
        self.threads_spin.setValue(8)

        self.fdConfigLayout.addWidget(self.threads_spin, 1, 1, 1, 1)

        self.processingModeLabel = QLabel(self.fdConfigGroup)
        self.processingModeLabel.setObjectName(u"processingModeLabel")

        self.fdConfigLayout.addWidget(self.processingModeLabel, 2, 0, 1, 1)

        self.fdModeValueLabel = QLabel(self.fdConfigGroup)
        self.fdModeValueLabel.setObjectName(u"fdModeValueLabel")

        self.fdConfigLayout.addWidget(self.fdModeValueLabel, 2, 1, 1, 1)

        self.prevent_dup_check = QCheckBox(self.fdConfigGroup)
        self.prevent_dup_check.setObjectName(u"prevent_dup_check")
        self.prevent_dup_check.setChecked(True)

        self.fdConfigLayout.addWidget(self.prevent_dup_check, 3, 0, 1, 2)

        self.confidenceLabel = QLabel(self.fdConfigGroup)
        self.confidenceLabel.setObjectName(u"confidenceLabel")
        self.confidenceLabel.setText("Confidence Level:")

        self.fdConfigLayout.addWidget(self.confidenceLabel, 4, 0, 1, 1)

        self.confidence_slider = QSlider(self.fdConfigGroup)
        self.confidence_slider.setObjectName(u"confidence_slider")
        self.confidence_slider.setMinimum(0)
        self.confidence_slider.setMaximum(100)
        self.confidence_slider.setValue(70)
        self.confidence_slider.setOrientation(Qt.Horizontal)

        self.fdConfigLayout.addWidget(self.confidence_slider, 4, 1, 1, 1)

        self.confidence_value_label = QLabel(self.fdConfigGroup)
        self.confidence_value_label.setObjectName(u"confidence_value_label")
        self.confidence_value_label.setText("0.70")

        self.fdConfigLayout.addWidget(self.confidence_value_label, 4, 2, 1, 1)

        self.fdMainLayout.addWidget(self.fdConfigGroup)

        self.fdProgressGroup = QGroupBox(self.face_detection_tab)
        self.fdProgressGroup.setObjectName(u"fdProgressGroup")
        self.fdProgressLayout = QVBoxLayout(self.fdProgressGroup)
        self.fdProgressLayout.setObjectName(u"fdProgressLayout")
        self.fd_progress_bar = QProgressBar(self.fdProgressGroup)
        self.fd_progress_bar.setObjectName(u"fd_progress_bar")
        self.fd_progress_bar.setValue(0)

        self.fdProgressLayout.addWidget(self.fd_progress_bar)

        self.fdStatusLayout = QHBoxLayout()
        self.fdStatusLayout.setObjectName(u"fdStatusLayout")
        self.label = QLabel(self.fdProgressGroup)
        self.label.setObjectName(u"label")

        self.fdStatusLayout.addWidget(self.label)

        self.processed_label = QLabel(self.fdProgressGroup)
        self.processed_label.setObjectName(u"processed_label")

        self.fdStatusLayout.addWidget(self.processed_label)

        self.label1 = QLabel(self.fdProgressGroup)
        self.label1.setObjectName(u"label1")

        self.fdStatusLayout.addWidget(self.label1)

        self.copied_label = QLabel(self.fdProgressGroup)
        self.copied_label.setObjectName(u"copied_label")

        self.fdStatusLayout.addWidget(self.copied_label)

        self.label2 = QLabel(self.fdProgressGroup)
        self.label2.setObjectName(u"label2")

        self.fdStatusLayout.addWidget(self.label2)

        self.errors_label = QLabel(self.fdProgressGroup)
        self.errors_label.setObjectName(u"errors_label")

        self.fdStatusLayout.addWidget(self.errors_label)


        self.fdProgressLayout.addLayout(self.fdStatusLayout)


        self.fdMainLayout.addWidget(self.fdProgressGroup)

        self.fdLogGroup = QGroupBox(self.face_detection_tab)
        self.fdLogGroup.setObjectName(u"fdLogGroup")
        self.fdLogLayout = QVBoxLayout(self.fdLogGroup)
        self.fdLogLayout.setObjectName(u"fdLogLayout")
        self.fd_log_text = QTextEdit(self.fdLogGroup)
        self.fd_log_text.setObjectName(u"fd_log_text")
        self.fd_log_text.setReadOnly(True)

        self.fdLogLayout.addWidget(self.fd_log_text)


        self.fdMainLayout.addWidget(self.fdLogGroup)

        self.fdBtnLayout = QHBoxLayout()
        self.fdBtnLayout.setObjectName(u"fdBtnLayout")
        self.fd_start_btn = QPushButton(self.face_detection_tab)
        self.fd_start_btn.setObjectName(u"fd_start_btn")

        self.fdBtnLayout.addWidget(self.fd_start_btn)

        self.fd_cancel_btn = QPushButton(self.face_detection_tab)
        self.fd_cancel_btn.setObjectName(u"fd_cancel_btn")
        self.fd_cancel_btn.setEnabled(False)

        self.fdBtnLayout.addWidget(self.fd_cancel_btn)


        self.fdMainLayout.addLayout(self.fdBtnLayout)

        self.tabs.addTab(self.face_detection_tab, "")
        self.file_transfer_tab = QWidget()
        self.file_transfer_tab.setObjectName(u"file_transfer_tab")
        self.ftMainLayout = QVBoxLayout(self.file_transfer_tab)
        self.ftMainLayout.setObjectName(u"ftMainLayout")
        self.ftDirsGroup = QGroupBox(self.file_transfer_tab)
        self.ftDirsGroup.setObjectName(u"ftDirsGroup")
        self.ftDirsLayout = QGridLayout(self.ftDirsGroup)
        self.ftDirsLayout.setObjectName(u"ftDirsLayout")
        self.fbSrcLabel = QLabel(self.ftDirsGroup)
        self.fbSrcLabel.setObjectName(u"fbSrcLabel")

        self.ftDirsLayout.addWidget(self.fbSrcLabel, 0, 0, 1, 1)

        self.fb_src_dir_edit = QLineEdit(self.ftDirsGroup)
        self.fb_src_dir_edit.setObjectName(u"fb_src_dir_edit")

        self.ftDirsLayout.addWidget(self.fb_src_dir_edit, 0, 1, 1, 1)

        self.fbSrcBrowseBtn = QPushButton(self.ftDirsGroup)
        self.fbSrcBrowseBtn.setObjectName(u"fbSrcBrowseBtn")

        self.ftDirsLayout.addWidget(self.fbSrcBrowseBtn, 0, 2, 1, 1)

        self.fbDestLabel = QLabel(self.ftDirsGroup)
        self.fbDestLabel.setObjectName(u"fbDestLabel")

        self.ftDirsLayout.addWidget(self.fbDestLabel, 1, 0, 1, 1)

        self.fb_dest_dir_edit = QLineEdit(self.ftDirsGroup)
        self.fb_dest_dir_edit.setObjectName(u"fb_dest_dir_edit")

        self.ftDirsLayout.addWidget(self.fb_dest_dir_edit, 1, 1, 1, 1)

        self.fbDestBrowseBtn = QPushButton(self.ftDirsGroup)
        self.fbDestBrowseBtn.setObjectName(u"fbDestBrowseBtn")

        self.ftDirsLayout.addWidget(self.fbDestBrowseBtn, 1, 2, 1, 1)


        self.ftMainLayout.addWidget(self.ftDirsGroup)

        self.fileTypesGroup = QGroupBox(self.file_transfer_tab)
        self.fileTypesGroup.setObjectName(u"fileTypesGroup")
        self.fileTypesLayout = QHBoxLayout(self.fileTypesGroup)
        self.fileTypesLayout.setObjectName(u"fileTypesLayout")
        self.include_images_check = QCheckBox(self.fileTypesGroup)
        self.include_images_check.setObjectName(u"include_images_check")
        self.include_images_check.setChecked(True)

        self.fileTypesLayout.addWidget(self.include_images_check)

        self.include_videos_check = QCheckBox(self.fileTypesGroup)
        self.include_videos_check.setObjectName(u"include_videos_check")
        self.include_videos_check.setChecked(True)

        self.fileTypesLayout.addWidget(self.include_videos_check)

        self.include_gifs_check = QCheckBox(self.fileTypesGroup)
        self.include_gifs_check.setObjectName(u"include_gifs_check")
        self.include_gifs_check.setChecked(True)

        self.fileTypesLayout.addWidget(self.include_gifs_check)


        self.ftMainLayout.addWidget(self.fileTypesGroup)

        self.idsGroup = QGroupBox(self.file_transfer_tab)
        self.idsGroup.setObjectName(u"idsGroup")
        self.idsLayout = QVBoxLayout(self.idsGroup)
        self.idsLayout.setObjectName(u"idsLayout")
        self.conversation_list = QListWidget(self.idsGroup)
        self.conversation_list.setObjectName(u"conversation_list")

        self.idsLayout.addWidget(self.conversation_list)

        self.idBtnsLayout = QHBoxLayout()
        self.idBtnsLayout.setObjectName(u"idBtnsLayout")
        self.addIdBtn = QPushButton(self.idsGroup)
        self.addIdBtn.setObjectName(u"addIdBtn")

        self.idBtnsLayout.addWidget(self.addIdBtn)

        self.removeIdBtn = QPushButton(self.idsGroup)
        self.removeIdBtn.setObjectName(u"removeIdBtn")

        self.idBtnsLayout.addWidget(self.removeIdBtn)

        self.loadIdsBtn = QPushButton(self.idsGroup)
        self.loadIdsBtn.setObjectName(u"loadIdsBtn")

        self.idBtnsLayout.addWidget(self.loadIdsBtn)

        self.saveIdsBtn = QPushButton(self.idsGroup)
        self.saveIdsBtn.setObjectName(u"saveIdsBtn")

        self.idBtnsLayout.addWidget(self.saveIdsBtn)


        self.idsLayout.addLayout(self.idBtnsLayout)


        self.ftMainLayout.addWidget(self.idsGroup)

        self.ftProgressGroup = QGroupBox(self.file_transfer_tab)
        self.ftProgressGroup.setObjectName(u"ftProgressGroup")
        self.ftProgressLayout = QVBoxLayout(self.ftProgressGroup)
        self.ftProgressLayout.setObjectName(u"ftProgressLayout")
        self.transfer_progress_bar = QProgressBar(self.ftProgressGroup)
        self.transfer_progress_bar.setObjectName(u"transfer_progress_bar")
        self.transfer_progress_bar.setValue(0)

        self.ftProgressLayout.addWidget(self.transfer_progress_bar)

        self.transfer_log = QTextEdit(self.ftProgressGroup)
        self.transfer_log.setObjectName(u"transfer_log")
        self.transfer_log.setReadOnly(True)

        self.ftProgressLayout.addWidget(self.transfer_log)


        self.ftMainLayout.addWidget(self.ftProgressGroup)

        self.ftBtnLayout = QHBoxLayout()
        self.ftBtnLayout.setObjectName(u"ftBtnLayout")
        self.transfer_start_btn = QPushButton(self.file_transfer_tab)
        self.transfer_start_btn.setObjectName(u"transfer_start_btn")

        self.ftBtnLayout.addWidget(self.transfer_start_btn)

        self.transfer_cancel_btn = QPushButton(self.file_transfer_tab)
        self.transfer_cancel_btn.setObjectName(u"transfer_cancel_btn")
        self.transfer_cancel_btn.setEnabled(False)

        self.ftBtnLayout.addWidget(self.transfer_cancel_btn)


        self.ftMainLayout.addLayout(self.ftBtnLayout)

        self.tabs.addTab(self.file_transfer_tab, "")
        self.hash_files_tab = QWidget()
        self.hash_files_tab.setObjectName(u"hash_files_tab")
        self.hashMainLayout = QVBoxLayout(self.hash_files_tab)
        self.hashMainLayout.setObjectName(u"hashMainLayout")
        self.hashDirsGroup = QGroupBox(self.hash_files_tab)
        self.hashDirsGroup.setObjectName(u"hashDirsGroup")
        self.hashDirsLayout = QGridLayout(self.hashDirsGroup)
        self.hashDirsLayout.setObjectName(u"hashDirsLayout")
        self.hashSrcLabel = QLabel(self.hashDirsGroup)
        self.hashSrcLabel.setObjectName(u"hashSrcLabel")

        self.hashDirsLayout.addWidget(self.hashSrcLabel, 0, 0, 1, 1)

        self.hash_src_dir_edit = QLineEdit(self.hashDirsGroup)
        self.hash_src_dir_edit.setObjectName(u"hash_src_dir_edit")

        self.hashDirsLayout.addWidget(self.hash_src_dir_edit, 0, 1, 1, 1)

        self.hashSrcBrowseBtn = QPushButton(self.hashDirsGroup)
        self.hashSrcBrowseBtn.setObjectName(u"hashSrcBrowseBtn")

        self.hashDirsLayout.addWidget(self.hashSrcBrowseBtn, 0, 2, 1, 1)

        self.hashTargetLabel = QLabel(self.hashDirsGroup)
        self.hashTargetLabel.setObjectName(u"hashTargetLabel")

        self.hashDirsLayout.addWidget(self.hashTargetLabel, 1, 0, 1, 1)

        self.hash_target_dir_edit = QLineEdit(self.hashDirsGroup)
        self.hash_target_dir_edit.setObjectName(u"hash_target_dir_edit")

        self.hashDirsLayout.addWidget(self.hash_target_dir_edit, 1, 1, 1, 1)

        self.hashTargetBrowseBtn = QPushButton(self.hashDirsGroup)
        self.hashTargetBrowseBtn.setObjectName(u"hashTargetBrowseBtn")

        self.hashDirsLayout.addWidget(self.hashTargetBrowseBtn, 1, 2, 1, 1)


        self.hashMainLayout.addWidget(self.hashDirsGroup)

        self.actionGroup = QGroupBox(self.hash_files_tab)
        self.actionGroup.setObjectName(u"actionGroup")
        self.actionLayout = QVBoxLayout(self.actionGroup)
        self.actionLayout.setObjectName(u"actionLayout")
        self.hash_action_combo = QComboBox(self.actionGroup)
        self.hash_action_combo.addItem("")
        self.hash_action_combo.addItem("")
        self.hash_action_combo.setObjectName(u"hash_action_combo")

        self.actionLayout.addWidget(self.hash_action_combo)


        self.hashMainLayout.addWidget(self.actionGroup)

        self.hashProgressGroup = QGroupBox(self.hash_files_tab)
        self.hashProgressGroup.setObjectName(u"hashProgressGroup")
        self.hashProgressLayout = QVBoxLayout(self.hashProgressGroup)
        self.hashProgressLayout.setObjectName(u"hashProgressLayout")
        self.hash_progress_bar = QProgressBar(self.hashProgressGroup)
        self.hash_progress_bar.setObjectName(u"hash_progress_bar")
        self.hash_progress_bar.setValue(0)

        self.hashProgressLayout.addWidget(self.hash_progress_bar)

        self.hash_log = QTextEdit(self.hashProgressGroup)
        self.hash_log.setObjectName(u"hash_log")
        self.hash_log.setReadOnly(True)

        self.hashProgressLayout.addWidget(self.hash_log)


        self.hashMainLayout.addWidget(self.hashProgressGroup)

        self.hashBtnLayout = QHBoxLayout()
        self.hashBtnLayout.setObjectName(u"hashBtnLayout")
        self.hash_start_btn = QPushButton(self.hash_files_tab)
        self.hash_start_btn.setObjectName(u"hash_start_btn")

        self.hashBtnLayout.addWidget(self.hash_start_btn)

        self.hash_cancel_btn = QPushButton(self.hash_files_tab)
        self.hash_cancel_btn.setObjectName(u"hash_cancel_btn")
        self.hash_cancel_btn.setEnabled(False)

        self.hashBtnLayout.addWidget(self.hash_cancel_btn)


        self.hashMainLayout.addLayout(self.hashBtnLayout)

        self.tabs.addTab(self.hash_files_tab, "")
        self.rename_images_tab = QWidget()
        self.rename_images_tab.setObjectName(u"rename_images_tab")
        self.renameMainLayout = QVBoxLayout(self.rename_images_tab)
        self.renameMainLayout.setObjectName(u"renameMainLayout")
        self.renameDirsGroup = QGroupBox(self.rename_images_tab)
        self.renameDirsGroup.setObjectName(u"renameDirsGroup")
        self.renameDirsLayout = QGridLayout(self.renameDirsGroup)
        self.renameDirsLayout.setObjectName(u"renameDirsLayout")
        self.renameSrcLabel = QLabel(self.renameDirsGroup)
        self.renameSrcLabel.setObjectName(u"renameSrcLabel")

        self.renameDirsLayout.addWidget(self.renameSrcLabel, 0, 0, 1, 1)

        self.rename_src_dir_edit = QLineEdit(self.renameDirsGroup)
        self.rename_src_dir_edit.setObjectName(u"rename_src_dir_edit")

        self.renameDirsLayout.addWidget(self.rename_src_dir_edit, 0, 1, 1, 1)

        self.renameSrcBrowseBtn = QPushButton(self.renameDirsGroup)
        self.renameSrcBrowseBtn.setObjectName(u"renameSrcBrowseBtn")

        self.renameDirsLayout.addWidget(self.renameSrcBrowseBtn, 0, 2, 1, 1)

        self.renameDestLabel = QLabel(self.renameDirsGroup)
        self.renameDestLabel.setObjectName(u"renameDestLabel")

        self.renameDirsLayout.addWidget(self.renameDestLabel, 1, 0, 1, 1)

        self.rename_dest_dir_edit = QLineEdit(self.renameDirsGroup)
        self.rename_dest_dir_edit.setObjectName(u"rename_dest_dir_edit")

        self.renameDirsLayout.addWidget(self.rename_dest_dir_edit, 1, 1, 1, 1)

        self.renameDestBrowseBtn = QPushButton(self.renameDirsGroup)
        self.renameDestBrowseBtn.setObjectName(u"renameDestBrowseBtn")

        self.renameDirsLayout.addWidget(self.renameDestBrowseBtn, 1, 2, 1, 1)

        self.rename_same_dir_check = QCheckBox(self.renameDirsGroup)
        self.rename_same_dir_check.setObjectName(u"rename_same_dir_check")

        self.renameDirsLayout.addWidget(self.rename_same_dir_check, 2, 0, 1, 3)

        self.renameJsonLabel = QLabel(self.renameDirsGroup)
        self.renameJsonLabel.setObjectName(u"renameJsonLabel")

        self.renameDirsLayout.addWidget(self.renameJsonLabel, 3, 0, 1, 1)

        self.rename_json_dir_edit = QLineEdit(self.renameDirsGroup)
        self.rename_json_dir_edit.setObjectName(u"rename_json_dir_edit")
        self.rename_json_dir_edit.setPlaceholderText(
            u"Optional: separate folder containing message_*.json files"
        )

        self.renameDirsLayout.addWidget(self.rename_json_dir_edit, 3, 1, 1, 1)

        self.renameJsonBrowseBtn = QPushButton(self.renameDirsGroup)
        self.renameJsonBrowseBtn.setObjectName(u"renameJsonBrowseBtn")
        self.renameJsonBrowseBtn.setText(u"Browse...")

        self.renameDirsLayout.addWidget(self.renameJsonBrowseBtn, 3, 2, 1, 1)


        self.renameMainLayout.addWidget(self.renameDirsGroup)

        self.renameOperationGroup = QGroupBox(self.rename_images_tab)
        self.renameOperationGroup.setObjectName(u"renameOperationGroup")
        self.renameOperationLayout = QVBoxLayout(self.renameOperationGroup)
        self.renameOperationLayout.setObjectName(u"renameOperationLayout")
        self.renameOperationHint = QLabel(self.renameOperationGroup)
        self.renameOperationHint.setObjectName(u"renameOperationHint")
        self.renameOperationHint.setWordWrap(True)

        self.renameOperationLayout.addWidget(self.renameOperationHint)

        self.renameRadioLayout = QHBoxLayout()
        self.renameRadioLayout.setObjectName(u"renameRadioLayout")
        self.rename_inplace_radio = QRadioButton(self.renameOperationGroup)
        self.rename_inplace_radio.setObjectName(u"rename_inplace_radio")
        self.rename_inplace_radio.setChecked(True)

        self.renameRadioLayout.addWidget(self.rename_inplace_radio)

        self.rename_copy_radio = QRadioButton(self.renameOperationGroup)
        self.rename_copy_radio.setObjectName(u"rename_copy_radio")

        self.renameRadioLayout.addWidget(self.rename_copy_radio)


        self.renameOperationLayout.addLayout(self.renameRadioLayout)


        self.renameMainLayout.addWidget(self.renameOperationGroup)

        self.renamePatternGroup = QGroupBox(self.rename_images_tab)
        self.renamePatternGroup.setObjectName(u"renamePatternGroup")
        self.renamePatternLayout = QGridLayout(self.renamePatternGroup)
        self.renamePatternLayout.setObjectName(u"renamePatternLayout")
        self.renamePrefixLabel = QLabel(self.renamePatternGroup)
        self.renamePrefixLabel.setObjectName(u"renamePrefixLabel")

        self.renamePatternLayout.addWidget(self.renamePrefixLabel, 0, 0, 1, 1)

        self.rename_prefix_edit = QLineEdit(self.renamePatternGroup)
        self.rename_prefix_edit.setObjectName(u"rename_prefix_edit")

        self.renamePatternLayout.addWidget(self.rename_prefix_edit, 0, 1, 1, 1)

        self.renameStartIndexLabel = QLabel(self.renamePatternGroup)
        self.renameStartIndexLabel.setObjectName(u"renameStartIndexLabel")

        self.renamePatternLayout.addWidget(self.renameStartIndexLabel, 1, 0, 1, 1)

        self.rename_start_index_spin = QSpinBox(self.renamePatternGroup)
        self.rename_start_index_spin.setObjectName(u"rename_start_index_spin")
        self.rename_start_index_spin.setMinimum(0)
        self.rename_start_index_spin.setMaximum(999999)
        self.rename_start_index_spin.setValue(1)

        self.renamePatternLayout.addWidget(self.rename_start_index_spin, 1, 1, 1, 1)

        self.renamePaddingLabel = QLabel(self.renamePatternGroup)
        self.renamePaddingLabel.setObjectName(u"renamePaddingLabel")

        self.renamePatternLayout.addWidget(self.renamePaddingLabel, 2, 0, 1, 1)

        self.rename_padding_spin = QSpinBox(self.renamePatternGroup)
        self.rename_padding_spin.setObjectName(u"rename_padding_spin")
        self.rename_padding_spin.setMinimum(1)
        self.rename_padding_spin.setMaximum(10)
        self.rename_padding_spin.setValue(4)

        self.renamePatternLayout.addWidget(self.rename_padding_spin, 2, 1, 1, 1)

        self.renameTemplateLabel = QLabel(self.renamePatternGroup)
        self.renameTemplateLabel.setObjectName(u"renameTemplateLabel")

        self.renamePatternLayout.addWidget(self.renameTemplateLabel, 3, 0, 1, 1)

        self.rename_template_edit = QLineEdit(self.renamePatternGroup)
        self.rename_template_edit.setObjectName(u"rename_template_edit")

        self.renamePatternLayout.addWidget(self.rename_template_edit, 3, 1, 1, 1)

        self.renameTemplateHint = QLabel(self.renamePatternGroup)
        self.renameTemplateHint.setObjectName(u"renameTemplateHint")

        self.renamePatternLayout.addWidget(self.renameTemplateHint, 4, 0, 1, 2)

        self.renamePreviewLabel = QLabel(self.renamePatternGroup)
        self.renamePreviewLabel.setObjectName(u"renamePreviewLabel")

        self.renamePatternLayout.addWidget(self.renamePreviewLabel, 5, 0, 1, 1)

        self.rename_preview_label = QLabel(self.renamePatternGroup)
        self.rename_preview_label.setObjectName(u"rename_preview_label")

        self.renamePatternLayout.addWidget(self.rename_preview_label, 5, 1, 1, 1)


        self.renameMainLayout.addWidget(self.renamePatternGroup)

        self.renameProgressGroup = QGroupBox(self.rename_images_tab)
        self.renameProgressGroup.setObjectName(u"renameProgressGroup")
        self.renameProgressLayout = QVBoxLayout(self.renameProgressGroup)
        self.renameProgressLayout.setObjectName(u"renameProgressLayout")
        self.rename_progress_bar = QProgressBar(self.renameProgressGroup)
        self.rename_progress_bar.setObjectName(u"rename_progress_bar")
        self.rename_progress_bar.setValue(0)

        self.renameProgressLayout.addWidget(self.rename_progress_bar)

        self.rename_log = QTextEdit(self.renameProgressGroup)
        self.rename_log.setObjectName(u"rename_log")
        self.rename_log.setReadOnly(True)

        self.renameProgressLayout.addWidget(self.rename_log)


        self.renameMainLayout.addWidget(self.renameProgressGroup)

        self.renameBtnLayout = QHBoxLayout()
        self.renameBtnLayout.setObjectName(u"renameBtnLayout")
        self.rename_start_btn = QPushButton(self.rename_images_tab)
        self.rename_start_btn.setObjectName(u"rename_start_btn")

        self.renameBtnLayout.addWidget(self.rename_start_btn)

        self.rename_cancel_btn = QPushButton(self.rename_images_tab)
        self.rename_cancel_btn.setObjectName(u"rename_cancel_btn")
        self.rename_cancel_btn.setEnabled(False)

        self.renameBtnLayout.addWidget(self.rename_cancel_btn)


        self.renameMainLayout.addLayout(self.renameBtnLayout)

        self.tabs.addTab(self.rename_images_tab, "")
        self.rename_videos_tab = QWidget()
        self.rename_videos_tab.setObjectName(u"rename_videos_tab")
        self.rvMainLayout = QVBoxLayout(self.rename_videos_tab)
        self.rvMainLayout.setObjectName(u"rvMainLayout")
        self.rvDirsGroup = QGroupBox(self.rename_videos_tab)
        self.rvDirsGroup.setObjectName(u"rvDirsGroup")
        self.rvDirsLayout = QGridLayout(self.rvDirsGroup)
        self.rvDirsLayout.setObjectName(u"rvDirsLayout")
        self.rvSrcLabel = QLabel(self.rvDirsGroup)
        self.rvSrcLabel.setObjectName(u"rvSrcLabel")
        self.rvDirsLayout.addWidget(self.rvSrcLabel, 0, 0, 1, 1)
        self.rv_src_dir_edit = QLineEdit(self.rvDirsGroup)
        self.rv_src_dir_edit.setObjectName(u"rv_src_dir_edit")
        self.rvDirsLayout.addWidget(self.rv_src_dir_edit, 0, 1, 1, 1)
        self.rvSrcBrowseBtn = QPushButton(self.rvDirsGroup)
        self.rvSrcBrowseBtn.setObjectName(u"rvSrcBrowseBtn")
        self.rvDirsLayout.addWidget(self.rvSrcBrowseBtn, 0, 2, 1, 1)
        self.rvDestLabel = QLabel(self.rvDirsGroup)
        self.rvDestLabel.setObjectName(u"rvDestLabel")
        self.rvDirsLayout.addWidget(self.rvDestLabel, 1, 0, 1, 1)
        self.rv_dest_dir_edit = QLineEdit(self.rvDirsGroup)
        self.rv_dest_dir_edit.setObjectName(u"rv_dest_dir_edit")
        self.rvDirsLayout.addWidget(self.rv_dest_dir_edit, 1, 1, 1, 1)
        self.rvDestBrowseBtn = QPushButton(self.rvDirsGroup)
        self.rvDestBrowseBtn.setObjectName(u"rvDestBrowseBtn")
        self.rvDirsLayout.addWidget(self.rvDestBrowseBtn, 1, 2, 1, 1)
        self.rv_same_dir_check = QCheckBox(self.rvDirsGroup)
        self.rv_same_dir_check.setObjectName(u"rv_same_dir_check")
        self.rvDirsLayout.addWidget(self.rv_same_dir_check, 2, 0, 1, 3)
        self.rvJsonLabel = QLabel(self.rvDirsGroup)
        self.rvJsonLabel.setObjectName(u"rvJsonLabel")
        self.rvDirsLayout.addWidget(self.rvJsonLabel, 3, 0, 1, 1)
        self.rv_json_dir_edit = QLineEdit(self.rvDirsGroup)
        self.rv_json_dir_edit.setObjectName(u"rv_json_dir_edit")
        self.rv_json_dir_edit.setPlaceholderText(
            u"Optional: separate folder containing message_*.json files"
        )
        self.rvDirsLayout.addWidget(self.rv_json_dir_edit, 3, 1, 1, 1)
        self.rvJsonBrowseBtn = QPushButton(self.rvDirsGroup)
        self.rvJsonBrowseBtn.setObjectName(u"rvJsonBrowseBtn")
        self.rvJsonBrowseBtn.setText(u"Browse...")
        self.rvDirsLayout.addWidget(self.rvJsonBrowseBtn, 3, 2, 1, 1)
        self.rvMainLayout.addWidget(self.rvDirsGroup)
        self.rvOperationGroup = QGroupBox(self.rename_videos_tab)
        self.rvOperationGroup.setObjectName(u"rvOperationGroup")
        self.rvOperationLayout = QVBoxLayout(self.rvOperationGroup)
        self.rvOperationLayout.setObjectName(u"rvOperationLayout")
        self.rvOperationHint = QLabel(self.rvOperationGroup)
        self.rvOperationHint.setObjectName(u"rvOperationHint")
        self.rvOperationHint.setWordWrap(True)
        self.rvOperationLayout.addWidget(self.rvOperationHint)
        self.rvRadioLayout = QHBoxLayout()
        self.rvRadioLayout.setObjectName(u"rvRadioLayout")
        self.rv_inplace_radio = QRadioButton(self.rvOperationGroup)
        self.rv_inplace_radio.setObjectName(u"rv_inplace_radio")
        self.rv_inplace_radio.setChecked(True)
        self.rvRadioLayout.addWidget(self.rv_inplace_radio)
        self.rv_copy_radio = QRadioButton(self.rvOperationGroup)
        self.rv_copy_radio.setObjectName(u"rv_copy_radio")
        self.rvRadioLayout.addWidget(self.rv_copy_radio)
        self.rvOperationLayout.addLayout(self.rvRadioLayout)
        self.rvMainLayout.addWidget(self.rvOperationGroup)
        self.rvPatternGroup = QGroupBox(self.rename_videos_tab)
        self.rvPatternGroup.setObjectName(u"rvPatternGroup")
        self.rvPatternLayout = QGridLayout(self.rvPatternGroup)
        self.rvPatternLayout.setObjectName(u"rvPatternLayout")
        self.rvPrefixLabel = QLabel(self.rvPatternGroup)
        self.rvPrefixLabel.setObjectName(u"rvPrefixLabel")
        self.rvPatternLayout.addWidget(self.rvPrefixLabel, 0, 0, 1, 1)
        self.rv_prefix_edit = QLineEdit(self.rvPatternGroup)
        self.rv_prefix_edit.setObjectName(u"rv_prefix_edit")
        self.rvPatternLayout.addWidget(self.rv_prefix_edit, 0, 1, 1, 1)
        self.rvStartIndexLabel = QLabel(self.rvPatternGroup)
        self.rvStartIndexLabel.setObjectName(u"rvStartIndexLabel")
        self.rvPatternLayout.addWidget(self.rvStartIndexLabel, 1, 0, 1, 1)
        self.rv_start_index_spin = QSpinBox(self.rvPatternGroup)
        self.rv_start_index_spin.setObjectName(u"rv_start_index_spin")
        self.rv_start_index_spin.setMinimum(0)
        self.rv_start_index_spin.setMaximum(999999)
        self.rv_start_index_spin.setValue(1)
        self.rvPatternLayout.addWidget(self.rv_start_index_spin, 1, 1, 1, 1)
        self.rvPaddingLabel = QLabel(self.rvPatternGroup)
        self.rvPaddingLabel.setObjectName(u"rvPaddingLabel")
        self.rvPatternLayout.addWidget(self.rvPaddingLabel, 2, 0, 1, 1)
        self.rv_padding_spin = QSpinBox(self.rvPatternGroup)
        self.rv_padding_spin.setObjectName(u"rv_padding_spin")
        self.rv_padding_spin.setMinimum(1)
        self.rv_padding_spin.setMaximum(10)
        self.rv_padding_spin.setValue(4)
        self.rv_padding_spin.setToolTip(u"e.g. padding 4 \u2192 0001, 0002...")
        self.rvPatternLayout.addWidget(self.rv_padding_spin, 2, 1, 1, 1)
        self.rvTemplateLabel = QLabel(self.rvPatternGroup)
        self.rvTemplateLabel.setObjectName(u"rvTemplateLabel")
        self.rvPatternLayout.addWidget(self.rvTemplateLabel, 3, 0, 1, 1)
        self.rv_template_edit = QLineEdit(self.rvPatternGroup)
        self.rv_template_edit.setObjectName(u"rv_template_edit")
        self.rvPatternLayout.addWidget(self.rv_template_edit, 3, 1, 1, 1)
        self.rvTemplateHint = QLabel(self.rvPatternGroup)
        self.rvTemplateHint.setObjectName(u"rvTemplateHint")
        self.rvPatternLayout.addWidget(self.rvTemplateHint, 4, 0, 1, 2)
        self.rvPreviewLabel = QLabel(self.rvPatternGroup)
        self.rvPreviewLabel.setObjectName(u"rvPreviewLabel")
        self.rvPatternLayout.addWidget(self.rvPreviewLabel, 5, 0, 1, 1)
        self.rv_preview_label = QLabel(self.rvPatternGroup)
        self.rv_preview_label.setObjectName(u"rv_preview_label")
        self.rvPatternLayout.addWidget(self.rv_preview_label, 5, 1, 1, 1)
        self.rvMainLayout.addWidget(self.rvPatternGroup)
        self.rvProgressGroup = QGroupBox(self.rename_videos_tab)
        self.rvProgressGroup.setObjectName(u"rvProgressGroup")
        self.rvProgressLayout = QVBoxLayout(self.rvProgressGroup)
        self.rvProgressLayout.setObjectName(u"rvProgressLayout")
        self.rv_progress_bar = QProgressBar(self.rvProgressGroup)
        self.rv_progress_bar.setObjectName(u"rv_progress_bar")
        self.rv_progress_bar.setValue(0)
        self.rvProgressLayout.addWidget(self.rv_progress_bar)
        self.rv_log = QTextEdit(self.rvProgressGroup)
        self.rv_log.setObjectName(u"rv_log")
        self.rv_log.setReadOnly(True)
        self.rvProgressLayout.addWidget(self.rv_log)
        self.rvMainLayout.addWidget(self.rvProgressGroup)
        self.rvBtnLayout = QHBoxLayout()
        self.rvBtnLayout.setObjectName(u"rvBtnLayout")
        self.rv_start_btn = QPushButton(self.rename_videos_tab)
        self.rv_start_btn.setObjectName(u"rv_start_btn")
        self.rvBtnLayout.addWidget(self.rv_start_btn)
        self.rv_cancel_btn = QPushButton(self.rename_videos_tab)
        self.rv_cancel_btn.setObjectName(u"rv_cancel_btn")
        self.rv_cancel_btn.setEnabled(False)
        self.rvBtnLayout.addWidget(self.rv_cancel_btn)
        self.rvMainLayout.addLayout(self.rvBtnLayout)
        self.tabs.addTab(self.rename_videos_tab, "")

        self.centralLayout.addWidget(self.tabs)

        FacebookMediaGUI.setCentralWidget(self.centralwidget)

        self.retranslateUi(FacebookMediaGUI)

        self.tabs.setCurrentIndex(3)


        QMetaObject.connectSlotsByName(FacebookMediaGUI)
    # setupUi

    def retranslateUi(self, FacebookMediaGUI):
        FacebookMediaGUI.setWindowTitle(QCoreApplication.translate("FacebookMediaGUI", u"Facebook Media Gather", None))
        self.fdDirsGroup.setTitle(QCoreApplication.translate("FacebookMediaGUI", u"Directory Selection", None))
        self.fdSrcLabel.setText(QCoreApplication.translate("FacebookMediaGUI", u"Source Directory:", None))
        self.fdSrcBrowseBtn.setText(QCoreApplication.translate("FacebookMediaGUI", u"Browse...", None))
        self.fdDestLabel.setText(QCoreApplication.translate("FacebookMediaGUI", u"Destination Directory:", None))
        self.fdDestBrowseBtn.setText(QCoreApplication.translate("FacebookMediaGUI", u"Browse...", None))
        self.fdConfigGroup.setTitle(QCoreApplication.translate("FacebookMediaGUI", u"Configuration", None))
        self.minFacesLabel.setText(QCoreApplication.translate("FacebookMediaGUI", u"Minimum Faces:", None))
        self.threadsLabel.setText(QCoreApplication.translate("FacebookMediaGUI", u"Thread Count:", None))
        self.processingModeLabel.setText(QCoreApplication.translate("FacebookMediaGUI", u"Processing Mode:", None))
        self.fdModeValueLabel.setText(QCoreApplication.translate("FacebookMediaGUI", u"CPU \u2014 thread pool", None))
        self.prevent_dup_check.setText(QCoreApplication.translate("FacebookMediaGUI", u"Prevent Duplication", None))
        self.fdProgressGroup.setTitle(QCoreApplication.translate("FacebookMediaGUI", u"Progress", None))
        self.label.setText(QCoreApplication.translate("FacebookMediaGUI", u"Processed:", None))
        self.processed_label.setText(QCoreApplication.translate("FacebookMediaGUI", u"0", None))
        self.label1.setText(QCoreApplication.translate("FacebookMediaGUI", u"Copied:", None))
        self.copied_label.setText(QCoreApplication.translate("FacebookMediaGUI", u"0", None))
        self.label2.setText(QCoreApplication.translate("FacebookMediaGUI", u"Errors:", None))
        self.errors_label.setText(QCoreApplication.translate("FacebookMediaGUI", u"0", None))
        self.fdLogGroup.setTitle(QCoreApplication.translate("FacebookMediaGUI", u"Log", None))
        self.fd_start_btn.setText(QCoreApplication.translate("FacebookMediaGUI", u"Start Processing", None))
        self.fd_cancel_btn.setText(QCoreApplication.translate("FacebookMediaGUI", u"Cancel", None))
        self.tabs.setTabText(self.tabs.indexOf(self.face_detection_tab), QCoreApplication.translate("FacebookMediaGUI", u"Face Detection", None))
        self.ftDirsGroup.setTitle(QCoreApplication.translate("FacebookMediaGUI", u"Directory Selection", None))
        self.fbSrcLabel.setText(QCoreApplication.translate("FacebookMediaGUI", u"Facebook Data Directory:", None))
        self.fb_src_dir_edit.setPlaceholderText(QCoreApplication.translate("FacebookMediaGUI", u"Select the Facebook messages directory", None))
        self.fbSrcBrowseBtn.setText(QCoreApplication.translate("FacebookMediaGUI", u"Browse...", None))
        self.fbDestLabel.setText(QCoreApplication.translate("FacebookMediaGUI", u"Destination Directory:", None))
        self.fb_dest_dir_edit.setPlaceholderText(QCoreApplication.translate("FacebookMediaGUI", u"Select where to copy media files", None))
        self.fbDestBrowseBtn.setText(QCoreApplication.translate("FacebookMediaGUI", u"Browse...", None))
        self.fileTypesGroup.setTitle(QCoreApplication.translate("FacebookMediaGUI", u"File Types to Include", None))
        self.include_images_check.setText(QCoreApplication.translate("FacebookMediaGUI", u"Images (JPG, PNG)", None))
        self.include_videos_check.setText(QCoreApplication.translate("FacebookMediaGUI", u"Videos (MP4)", None))
        self.include_gifs_check.setText(QCoreApplication.translate("FacebookMediaGUI", u"GIFs", None))
        self.idsGroup.setTitle(QCoreApplication.translate("FacebookMediaGUI", u"Conversation IDs", None))
        self.addIdBtn.setText(QCoreApplication.translate("FacebookMediaGUI", u"Add ID", None))
        self.removeIdBtn.setText(QCoreApplication.translate("FacebookMediaGUI", u"Remove Selected", None))
        self.loadIdsBtn.setText(QCoreApplication.translate("FacebookMediaGUI", u"Load IDs from File", None))
        self.saveIdsBtn.setText(QCoreApplication.translate("FacebookMediaGUI", u"Save IDs to File", None))
        self.ftProgressGroup.setTitle(QCoreApplication.translate("FacebookMediaGUI", u"Progress", None))
        self.transfer_start_btn.setText(QCoreApplication.translate("FacebookMediaGUI", u"Start Transfer", None))
        self.transfer_cancel_btn.setText(QCoreApplication.translate("FacebookMediaGUI", u"Cancel", None))
        self.tabs.setTabText(self.tabs.indexOf(self.file_transfer_tab), QCoreApplication.translate("FacebookMediaGUI", u"File Transfer", None))
        self.hashDirsGroup.setTitle(QCoreApplication.translate("FacebookMediaGUI", u"Directory Selection", None))
        self.hashSrcLabel.setText(QCoreApplication.translate("FacebookMediaGUI", u"Source Directory:", None))
        self.hashSrcBrowseBtn.setText(QCoreApplication.translate("FacebookMediaGUI", u"Browse...", None))
        self.hashTargetLabel.setText(QCoreApplication.translate("FacebookMediaGUI", u"Target Directory:", None))
        self.hashTargetBrowseBtn.setText(QCoreApplication.translate("FacebookMediaGUI", u"Browse...", None))
        self.actionGroup.setTitle(QCoreApplication.translate("FacebookMediaGUI", u"Action", None))
        self.hash_action_combo.setItemText(0, QCoreApplication.translate("FacebookMediaGUI", u"Calculate hashes and find matches", None))
        self.hash_action_combo.setItemText(1, QCoreApplication.translate("FacebookMediaGUI", u"Rename target files to match source files", None))

        self.hashProgressGroup.setTitle(QCoreApplication.translate("FacebookMediaGUI", u"Progress", None))
        self.hash_start_btn.setText(QCoreApplication.translate("FacebookMediaGUI", u"Start Processing", None))
        self.hash_cancel_btn.setText(QCoreApplication.translate("FacebookMediaGUI", u"Cancel", None))
        self.tabs.setTabText(self.tabs.indexOf(self.hash_files_tab), QCoreApplication.translate("FacebookMediaGUI", u"Hash & Compare Files", None))
        self.renameDirsGroup.setTitle(QCoreApplication.translate("FacebookMediaGUI", u"Directory Selection", None))
        self.renameSrcLabel.setText(QCoreApplication.translate("FacebookMediaGUI", u"Source Directory:", None))
        self.rename_src_dir_edit.setPlaceholderText(QCoreApplication.translate("FacebookMediaGUI", u"Select source directory", None))
        self.renameSrcBrowseBtn.setText(QCoreApplication.translate("FacebookMediaGUI", u"Browse...", None))
        self.renameDestLabel.setText(QCoreApplication.translate("FacebookMediaGUI", u"Destination Directory:", None))
        self.rename_dest_dir_edit.setPlaceholderText(QCoreApplication.translate("FacebookMediaGUI", u"Select destination directory (or same as source)", None))
        self.renameDestBrowseBtn.setText(QCoreApplication.translate("FacebookMediaGUI", u"Browse...", None))
        self.rename_same_dir_check.setText(QCoreApplication.translate("FacebookMediaGUI", u"Use same directory as source (rename in place)", None))
        self.renameOperationGroup.setTitle(QCoreApplication.translate("FacebookMediaGUI", u"Operation Mode", None))
        self.renameOperationHint.setText(QCoreApplication.translate("FacebookMediaGUI", u"When source and destination are the same, choose how to handle files:", None))
        self.rename_inplace_radio.setText(QCoreApplication.translate("FacebookMediaGUI", u"Rename file (in place)", None))
        self.rename_copy_radio.setText(QCoreApplication.translate("FacebookMediaGUI", u"Copy and rename (keep original)", None))
        self.renamePatternGroup.setTitle(QCoreApplication.translate("FacebookMediaGUI", u"Rename Pattern", None))
        self.renamePrefixLabel.setText(QCoreApplication.translate("FacebookMediaGUI", u"Prefix:", None))
        self.rename_prefix_edit.setPlaceholderText(QCoreApplication.translate("FacebookMediaGUI", u"e.g. photo_ (optional)", None))
        self.renameStartIndexLabel.setText(QCoreApplication.translate("FacebookMediaGUI", u"Start Index:", None))
        self.renamePaddingLabel.setText(QCoreApplication.translate("FacebookMediaGUI", u"Number Padding:", None))
#if QT_CONFIG(tooltip)
        self.rename_padding_spin.setToolTip(QCoreApplication.translate("FacebookMediaGUI", u"e.g. padding 4 \u2192 0001, 0002...", None))
#endif // QT_CONFIG(tooltip)
        self.renameTemplateLabel.setText(QCoreApplication.translate("FacebookMediaGUI", u"Template:", None))
        self.rename_template_edit.setPlaceholderText(QCoreApplication.translate("FacebookMediaGUI", u"${PREFIX}${DATE_TIME}_${THREAD_NAME}", None))
        self.renameTemplateHint.setText(QCoreApplication.translate("FacebookMediaGUI", u"Variables: ${PREFIX}  ${INDEX}  ${DATE_TIME}  ${THREAD_NAME}", None))
        self.renamePreviewLabel.setText(QCoreApplication.translate("FacebookMediaGUI", u"Preview:", None))
        self.rename_preview_label.setText(QCoreApplication.translate("FacebookMediaGUI", u"2026_03_11_12_00_00_FriendName.jpg \u2026", None))
        self.renameProgressGroup.setTitle(QCoreApplication.translate("FacebookMediaGUI", u"Progress", None))
        self.rename_start_btn.setText(QCoreApplication.translate("FacebookMediaGUI", u"Start Renaming", None))
        self.rename_cancel_btn.setText(QCoreApplication.translate("FacebookMediaGUI", u"Cancel", None))
        self.renameJsonLabel.setText(QCoreApplication.translate("FacebookMediaGUI", u"JSON Directory:", None))
        self.tabs.setTabText(self.tabs.indexOf(self.rename_images_tab), QCoreApplication.translate("FacebookMediaGUI", u"Rename Images", None))
        self.rvDirsGroup.setTitle(QCoreApplication.translate("FacebookMediaGUI", u"Directory Selection", None))
        self.rvSrcLabel.setText(QCoreApplication.translate("FacebookMediaGUI", u"Source Directory:", None))
        self.rv_src_dir_edit.setPlaceholderText(QCoreApplication.translate("FacebookMediaGUI", u"Select source directory", None))
        self.rvSrcBrowseBtn.setText(QCoreApplication.translate("FacebookMediaGUI", u"Browse...", None))
        self.rvDestLabel.setText(QCoreApplication.translate("FacebookMediaGUI", u"Destination Directory:", None))
        self.rv_dest_dir_edit.setPlaceholderText(QCoreApplication.translate("FacebookMediaGUI", u"Select destination directory (or same as source)", None))
        self.rvDestBrowseBtn.setText(QCoreApplication.translate("FacebookMediaGUI", u"Browse...", None))
        self.rv_same_dir_check.setText(QCoreApplication.translate("FacebookMediaGUI", u"Use same directory as source (rename in place)", None))
        self.rvJsonLabel.setText(QCoreApplication.translate("FacebookMediaGUI", u"JSON Directory:", None))
        self.rvOperationGroup.setTitle(QCoreApplication.translate("FacebookMediaGUI", u"Operation Mode", None))
        self.rvOperationHint.setText(QCoreApplication.translate("FacebookMediaGUI", u"When source and destination are the same, choose how to handle files:", None))
        self.rv_inplace_radio.setText(QCoreApplication.translate("FacebookMediaGUI", u"Rename file (in place)", None))
        self.rv_copy_radio.setText(QCoreApplication.translate("FacebookMediaGUI", u"Copy and rename (keep original)", None))
        self.rvPatternGroup.setTitle(QCoreApplication.translate("FacebookMediaGUI", u"Rename Pattern", None))
        self.rvPrefixLabel.setText(QCoreApplication.translate("FacebookMediaGUI", u"Prefix:", None))
        self.rv_prefix_edit.setPlaceholderText(QCoreApplication.translate("FacebookMediaGUI", u"e.g. video_ (optional)", None))
        self.rvStartIndexLabel.setText(QCoreApplication.translate("FacebookMediaGUI", u"Start Index:", None))
        self.rvPaddingLabel.setText(QCoreApplication.translate("FacebookMediaGUI", u"Number Padding:", None))
        self.rvTemplateLabel.setText(QCoreApplication.translate("FacebookMediaGUI", u"Template:", None))
        self.rv_template_edit.setPlaceholderText(QCoreApplication.translate("FacebookMediaGUI", u"${PREFIX}${DATE_TIME}_${THREAD_NAME}", None))
        self.rvTemplateHint.setText(QCoreApplication.translate("FacebookMediaGUI", u"Variables: ${PREFIX}  ${INDEX}  ${DATE_TIME}  ${THREAD_NAME}", None))
        self.rvPreviewLabel.setText(QCoreApplication.translate("FacebookMediaGUI", u"Preview:", None))
        self.rvProgressGroup.setTitle(QCoreApplication.translate("FacebookMediaGUI", u"Progress", None))
        self.rv_start_btn.setText(QCoreApplication.translate("FacebookMediaGUI", u"Start Renaming", None))
        self.rv_cancel_btn.setText(QCoreApplication.translate("FacebookMediaGUI", u"Cancel", None))
        self.tabs.setTabText(self.tabs.indexOf(self.rename_videos_tab), QCoreApplication.translate("FacebookMediaGUI", u"Rename Videos", None))
    # retranslateUi

class MainWindow(QMainWindow):
    """Application main window — wraps the generated UI and wires up
    the face_detection module."""

    def __init__(self):
        super().__init__()
        self.ui = Ui_FacebookMediaGUI()
        self.ui.setupUi(self)
        self._fd_worker       = None
        self._rename_worker   = None
        self._rv_worker       = None
        self._transfer_worker = None

        # --- Show GPU/CPU mode and explain why GPU may be unavailable ---
        if face_detection.is_gpu_available():
            self.ui.fdModeValueLabel.setText("GPU (CUDA)")
        else:
            self.ui.fdModeValueLabel.setText("CPU \u2014 thread pool")
            reason = face_detection.get_cuda_unavailable_reason()
            if reason:
                self.ui.fdModeValueLabel.setToolTip(reason)

        # --- Face Detection tab connections ---
        self.ui.fdSrcBrowseBtn.clicked.connect(self._fd_browse_src)
        self.ui.fdDestBrowseBtn.clicked.connect(self._fd_browse_dest)
        self.ui.fd_start_btn.clicked.connect(self._fd_start)
        self.ui.fd_cancel_btn.clicked.connect(self._fd_cancel)
        self.ui.confidence_slider.sliderMoved.connect(self._fd_update_confidence_label)

        # --- Rename Images tab connections ---
        self.ui.renameSrcBrowseBtn.clicked.connect(self._ri_browse_src)
        self.ui.renameDestBrowseBtn.clicked.connect(self._ri_browse_dest)
        self.ui.renameJsonBrowseBtn.clicked.connect(self._ri_browse_json)
        self.ui.rename_same_dir_check.toggled.connect(self._ri_same_dir_toggled)
        self.ui.rename_prefix_edit.textChanged.connect(self._ri_update_preview)
        self.ui.rename_padding_spin.valueChanged.connect(self._ri_update_preview)
        self.ui.rename_start_index_spin.valueChanged.connect(self._ri_update_preview)
        self.ui.rename_template_edit.textChanged.connect(self._ri_update_preview)
        self.ui.rename_start_btn.clicked.connect(self._ri_start)
        self.ui.rename_cancel_btn.clicked.connect(self._ri_cancel)
        self._ri_update_preview()

        # --- Rename Videos tab connections ---
        self.ui.rvSrcBrowseBtn.clicked.connect(self._rv_browse_src)
        self.ui.rvDestBrowseBtn.clicked.connect(self._rv_browse_dest)
        self.ui.rvJsonBrowseBtn.clicked.connect(self._rv_browse_json)
        self.ui.rv_same_dir_check.toggled.connect(self._rv_same_dir_toggled)
        self.ui.rv_prefix_edit.textChanged.connect(self._rv_update_preview)
        self.ui.rv_padding_spin.valueChanged.connect(self._rv_update_preview)
        self.ui.rv_start_index_spin.valueChanged.connect(self._rv_update_preview)
        self.ui.rv_template_edit.textChanged.connect(self._rv_update_preview)
        self.ui.rv_start_btn.clicked.connect(self._rv_start)
        self.ui.rv_cancel_btn.clicked.connect(self._rv_cancel)
        self._rv_update_preview()

        # --- File Transfer tab connections ---
        self.ui.fbSrcBrowseBtn.clicked.connect(self._ft_browse_src)
        self.ui.fbDestBrowseBtn.clicked.connect(self._ft_browse_dest)
        self.ui.addIdBtn.clicked.connect(self._ft_add_id)
        self.ui.removeIdBtn.clicked.connect(self._ft_remove_id)
        self.ui.loadIdsBtn.clicked.connect(self._ft_load_ids)
        self.ui.saveIdsBtn.clicked.connect(self._ft_save_ids)
        self.ui.transfer_start_btn.clicked.connect(self._ft_start)
        self.ui.transfer_cancel_btn.clicked.connect(self._ft_cancel)

    # ------------------------------------------------------------------
    # Face Detection slots
    # ------------------------------------------------------------------

    def _fd_browse_src(self):
        directory = QFileDialog.getExistingDirectory(self, "Select Source Directory")
        if directory:
            self.ui.src_dir_edit.setText(directory)

    def _fd_browse_dest(self):
        directory = QFileDialog.getExistingDirectory(self, "Select Destination Directory")
        if directory:
            self.ui.dest_dir_edit.setText(directory)

    def _fd_update_confidence_label(self):
        """Update the confidence value label when slider moves."""
        value = self.ui.confidence_slider.value() / 100.0
        self.ui.confidence_value_label.setText(f"{value:.2f}")

    def _fd_start(self):
        src = self.ui.src_dir_edit.text().strip()
        dest = self.ui.dest_dir_edit.text().strip()
        if not src or not dest:
            QMessageBox.warning(
                self,
                "Missing Directories",
                "Please select both a source and a destination directory.",
            )
            return

        self.ui.fd_start_btn.setEnabled(False)
        self.ui.fd_cancel_btn.setEnabled(True)
        self.ui.fd_progress_bar.setValue(0)
        self.ui.processed_label.setText("0")
        self.ui.copied_label.setText("0")
        self.ui.errors_label.setText("0")
        self.ui.fd_log_text.clear()

        self._fd_worker = face_detection.FaceDetectionWorker(
            src_dir=src,
            dest_dir=dest,
            min_faces=self.ui.min_faces_spin.value(),
            max_faces=self.ui.max_faces_spin.value(),
            threads=self.ui.threads_spin.value(),
            use_gpu=face_detection.is_gpu_available(),
            prevent_duplicates=self.ui.prevent_dup_check.isChecked(),
            confidence_level=self.ui.confidence_slider.value() / 100.0,
            parent=self,
        )
        self._fd_worker.progress.connect(self.ui.fd_progress_bar.setValue)
        self._fd_worker.log.connect(self.ui.fd_log_text.append)
        self._fd_worker.stats_updated.connect(self._fd_update_stats)
        self._fd_worker.finished.connect(self._fd_finished)
        self._fd_worker.error.connect(self._fd_error)
        self._fd_worker.start()

    def _fd_cancel(self):
        if self._fd_worker:
            self._fd_worker.cancel()

    def _fd_update_stats(self, processed: int, copied: int, errors: int):
        self.ui.processed_label.setText(str(processed))
        self.ui.copied_label.setText(str(copied))
        self.ui.errors_label.setText(str(errors))

    def _fd_finished(self):
        self.ui.fd_start_btn.setEnabled(True)
        self.ui.fd_cancel_btn.setEnabled(False)

    def _fd_error(self, message: str):
        self.ui.fd_log_text.append(f"[FATAL] {message}")
        self._fd_finished()

    # ------------------------------------------------------------------
    # Rename Images slots
    # ------------------------------------------------------------------

    def _ri_browse_src(self):
        directory = QFileDialog.getExistingDirectory(
            self, "Select Facebook Export Root Directory"
        )
        if directory:
            self.ui.rename_src_dir_edit.setText(directory)
            if self.ui.rename_same_dir_check.isChecked():
                self.ui.rename_dest_dir_edit.setText(directory)

    def _ri_browse_dest(self):
        directory = QFileDialog.getExistingDirectory(
            self, "Select Destination Directory"
        )
        if directory:
            self.ui.rename_dest_dir_edit.setText(directory)

    def _ri_browse_json(self):
        directory = QFileDialog.getExistingDirectory(
            self, "Select JSON Files Directory"
        )
        if directory:
            self.ui.rename_json_dir_edit.setText(directory)

    def _ri_same_dir_toggled(self, checked: bool):
        self.ui.rename_dest_dir_edit.setEnabled(not checked)
        self.ui.renameDestBrowseBtn.setEnabled(not checked)
        if checked:
            self.ui.rename_dest_dir_edit.setText(
                self.ui.rename_src_dir_edit.text()
            )

    def _ri_update_preview(self):
        prefix   = self.ui.rename_prefix_edit.text()
        padding  = self.ui.rename_padding_spin.value()
        index    = self.ui.rename_start_index_spin.value()
        template = self.ui.rename_template_edit.text() or "${PREFIX}${DATE_TIME}_${THREAD_NAME}"

        def _expand(tmpl: str, idx: int, date: str, thread: str) -> str:
            s = tmpl
            s = s.replace("${PREFIX}", prefix)
            s = s.replace("${INDEX}", str(idx).zfill(padding))
            s = s.replace("${DATE_TIME}", date)
            s = s.replace("${THREAD_NAME}", thread)
            return s

        ex1 = _expand(template, index,     "2026_03_11_12_00_00", "FriendName") + ".jpg"
        ex2 = _expand(template, index + 1, "2026_03_11_13_30_00", "FriendName") + ".jpg"
        self.ui.rename_preview_label.setText(f"{ex1}, {ex2} \u2026")

    def _ri_start(self):
        src = self.ui.rename_src_dir_edit.text().strip()
        dest = (
            src
            if self.ui.rename_same_dir_check.isChecked()
            else self.ui.rename_dest_dir_edit.text().strip()
        )

        if not src:
            QMessageBox.warning(
                self,
                "Missing Source Directory",
                "Please select the Facebook export root directory.",
            )
            return
        if not dest:
            QMessageBox.warning(
                self,
                "Missing Destination Directory",
                "Please select a destination directory or enable \'same as source\'.",
            )
            return

        copy_mode = self.ui.rename_copy_radio.isChecked()

        self.ui.rename_start_btn.setEnabled(False)
        self.ui.rename_cancel_btn.setEnabled(True)
        self.ui.rename_progress_bar.setValue(0)
        self.ui.rename_log.clear()

        self._rename_worker = rename_images.RenameImagesWorker(
            src_dir=src,
            dest_dir=dest,
            json_dir=self.ui.rename_json_dir_edit.text().strip(),
            prefix=self.ui.rename_prefix_edit.text(),
            start_index=self.ui.rename_start_index_spin.value(),
            padding=self.ui.rename_padding_spin.value(),
            copy_mode=copy_mode,
            name_template=self.ui.rename_template_edit.text().strip(),
            parent=self,
        )
        self._rename_worker.progress.connect(self.ui.rename_progress_bar.setValue)
        self._rename_worker.log.connect(self.ui.rename_log.append)
        self._rename_worker.stats_updated.connect(self._ri_update_stats)
        self._rename_worker.finished.connect(self._ri_finished)
        self._rename_worker.error.connect(self._ri_error)
        self._rename_worker.start()

    def _ri_cancel(self):
        if self._rename_worker:
            self._rename_worker.cancel()

    def _ri_update_stats(self, processed: int, renamed: int, errors: int):
        # Reuse the rename_log count line — progress bar covers visuals
        pass

    def _ri_finished(self):
        self.ui.rename_start_btn.setEnabled(True)
        self.ui.rename_cancel_btn.setEnabled(False)
        self.ui.rename_progress_bar.setValue(100)

    def _ri_error(self, message: str):
        self.ui.rename_log.append(f"[FATAL] {message}")
        self._ri_finished()

    # ------------------------------------------------------------------
    # Rename Videos slots
    # ------------------------------------------------------------------

    def _rv_browse_src(self):
        directory = QFileDialog.getExistingDirectory(
            self, "Select Facebook Export Root Directory"
        )
        if directory:
            self.ui.rv_src_dir_edit.setText(directory)
            if self.ui.rv_same_dir_check.isChecked():
                self.ui.rv_dest_dir_edit.setText(directory)

    def _rv_browse_dest(self):
        directory = QFileDialog.getExistingDirectory(
            self, "Select Destination Directory"
        )
        if directory:
            self.ui.rv_dest_dir_edit.setText(directory)

    def _rv_browse_json(self):
        directory = QFileDialog.getExistingDirectory(
            self, "Select JSON Files Directory"
        )
        if directory:
            self.ui.rv_json_dir_edit.setText(directory)

    def _rv_same_dir_toggled(self, checked: bool):
        self.ui.rv_dest_dir_edit.setEnabled(not checked)
        self.ui.rvDestBrowseBtn.setEnabled(not checked)
        if checked:
            self.ui.rv_dest_dir_edit.setText(self.ui.rv_src_dir_edit.text())

    def _rv_update_preview(self):
        prefix   = self.ui.rv_prefix_edit.text()
        padding  = self.ui.rv_padding_spin.value()
        index    = self.ui.rv_start_index_spin.value()
        template = self.ui.rv_template_edit.text() or "${PREFIX}${DATE_TIME}_${THREAD_NAME}"

        def _expand(tmpl: str, idx: int, date: str, thread: str) -> str:
            s = tmpl
            s = s.replace("${PREFIX}", prefix)
            s = s.replace("${INDEX}", str(idx).zfill(padding))
            s = s.replace("${DATE_TIME}", date)
            s = s.replace("${THREAD_NAME}", thread)
            return s

        ex1 = _expand(template, index,     "2026_03_11_12_00_00", "FriendName") + ".mp4"
        ex2 = _expand(template, index + 1, "2026_03_11_13_30_00", "FriendName") + ".mp4"
        self.ui.rv_preview_label.setText(f"{ex1}, {ex2} \u2026")

    def _rv_start(self):
        src = self.ui.rv_src_dir_edit.text().strip()
        dest = (
            src
            if self.ui.rv_same_dir_check.isChecked()
            else self.ui.rv_dest_dir_edit.text().strip()
        )

        if not src:
            QMessageBox.warning(
                self,
                "Missing Source Directory",
                "Please select the Facebook export root directory.",
            )
            return
        if not dest:
            QMessageBox.warning(
                self,
                "Missing Destination Directory",
                "Please select a destination directory or enable 'same as source'.",
            )
            return

        copy_mode = self.ui.rv_copy_radio.isChecked()

        self.ui.rv_start_btn.setEnabled(False)
        self.ui.rv_cancel_btn.setEnabled(True)
        self.ui.rv_progress_bar.setValue(0)
        self.ui.rv_log.clear()

        self._rv_worker = rename_videos.RenameVideosWorker(
            src_dir=src,
            dest_dir=dest,
            json_dir=self.ui.rv_json_dir_edit.text().strip(),
            prefix=self.ui.rv_prefix_edit.text(),
            start_index=self.ui.rv_start_index_spin.value(),
            padding=self.ui.rv_padding_spin.value(),
            copy_mode=copy_mode,
            name_template=self.ui.rv_template_edit.text().strip(),
            parent=self,
        )
        self._rv_worker.progress.connect(self.ui.rv_progress_bar.setValue)
        self._rv_worker.log.connect(self.ui.rv_log.append)
        self._rv_worker.stats_updated.connect(self._rv_update_stats)
        self._rv_worker.finished.connect(self._rv_finished)
        self._rv_worker.error.connect(self._rv_error)
        self._rv_worker.start()

    def _rv_cancel(self):
        if self._rv_worker:
            self._rv_worker.cancel()

    def _rv_update_stats(self, processed: int, renamed: int, errors: int):
        pass

    def _rv_finished(self):
        self.ui.rv_start_btn.setEnabled(True)
        self.ui.rv_cancel_btn.setEnabled(False)
        self.ui.rv_progress_bar.setValue(100)

    def _rv_error(self, message: str):
        self.ui.rv_log.append(f"[FATAL] {message}")
        self._rv_finished()

    # ------------------------------------------------------------------
    # File Transfer slots
    # ------------------------------------------------------------------

    def _ft_browse_src(self):
        directory = QFileDialog.getExistingDirectory(
            self, "Select Facebook Export Root Directory"
        )
        if directory:
            self.ui.fb_src_dir_edit.setText(directory)

    def _ft_browse_dest(self):
        directory = QFileDialog.getExistingDirectory(
            self, "Select Destination Directory"
        )
        if directory:
            self.ui.fb_dest_dir_edit.setText(directory)

    def _ft_add_id(self):
        src = self.ui.fb_src_dir_edit.text().strip()
        src_path = Path(src)

        if not src or src_path.name != "your_facebook_activity" or not src_path.is_dir():
            QMessageBox.warning(
                self,
                "Invalid Source Directory",
                "Please set the Facebook data export root directory "
                "(must be named exactly 'your_facebook_activity').",
            )
            return

        inbox = src_path / "messages" / "inbox"

        # Inbox missing — fall back to a plain text prompt
        if not inbox.is_dir():
            text, ok = QInputDialog.getText(
                self, "Add Conversation ID", "Enter conversation ID manually:"
            )
            if ok and text.strip():
                cid = text.strip()
                existing = [
                    self.ui.conversation_list.item(i).text()
                    for i in range(self.ui.conversation_list.count())
                ]
                if cid not in existing:
                    self.ui.conversation_list.addItem(cid)
            return

        # Scan inbox subfolders
        try:
            folders = sorted(
                [f for f in inbox.iterdir() if f.is_dir()],
                key=lambda f: f.name.lower(),
            )
        except OSError as exc:
            QMessageBox.warning(
                self, "Scan Error", f"Cannot read inbox directory:\n{exc}"
            )
            return

        # Build picker dialog
        dialog = QDialog(self)
        dialog.setWindowTitle("Select Conversations")
        dialog.resize(640, 420)
        dlg_layout = QVBoxLayout(dialog)

        table = QTableWidget(len(folders), 2, dialog)
        table.setHorizontalHeaderLabels(["Conversation Name", "Conversation ID"])
        table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        table.setSelectionMode(QTableWidget.SelectionMode.ExtendedSelection)
        table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        table.horizontalHeader().setSectionResizeMode(
            0, QHeaderView.ResizeMode.Stretch
        )
        table.horizontalHeader().setSectionResizeMode(
            1, QHeaderView.ResizeMode.ResizeToContents
        )
        table.verticalHeader().setVisible(False)

        for row, folder in enumerate(folders):
            parts = folder.name.rsplit("_", 1)
            name = parts[0] if len(parts) == 2 else folder.name
            cid  = parts[1] if len(parts) == 2 else ""
            table.setItem(row, 0, QTableWidgetItem(name))
            table.setItem(row, 1, QTableWidgetItem(cid))

        dlg_layout.addWidget(table)

        btn_layout = QHBoxLayout()
        cancel_btn = QPushButton("Cancel")
        add_btn    = QPushButton("Add Selected")
        add_btn.setDefault(True)
        btn_layout.addStretch()
        btn_layout.addWidget(cancel_btn)
        btn_layout.addWidget(add_btn)
        dlg_layout.addLayout(btn_layout)

        cancel_btn.clicked.connect(dialog.reject)
        add_btn.clicked.connect(dialog.accept)

        if dialog.exec() != QDialog.DialogCode.Accepted:
            return

        existing = [
            self.ui.conversation_list.item(i).text()
            for i in range(self.ui.conversation_list.count())
        ]
        for index in table.selectionModel().selectedRows():
            item = table.item(index.row(), 1)
            if item:
                cid = item.text()
                if cid and cid not in existing:
                    self.ui.conversation_list.addItem(cid)
                    existing.append(cid)

    def _ft_remove_id(self):
        for item in self.ui.conversation_list.selectedItems():
            self.ui.conversation_list.takeItem(
                self.ui.conversation_list.row(item)
            )

    def _ft_load_ids(self):
        import json as _json
        path, _ = QFileDialog.getOpenFileName(
            self, "Load Conversation IDs", "", "JSON Files (*.json);;Text Files (*.txt)"
        )
        if not path:
            return
        try:
            with open(path, "r", encoding="utf-8") as fh:
                if path.endswith(".json"):
                    data = _json.load(fh)
                    ids = [str(x) for x in (data if isinstance(data, list) else [])]
                else:
                    ids = [line.strip() for line in fh if line.strip()]
        except Exception as exc:
            QMessageBox.warning(self, "Load Error", f"Could not load IDs:\n{exc}")
            return
        existing = [
            self.ui.conversation_list.item(i).text()
            for i in range(self.ui.conversation_list.count())
        ]
        for cid in ids:
            if cid and cid not in existing:
                self.ui.conversation_list.addItem(cid)
                existing.append(cid)

    def _ft_save_ids(self):
        import json as _json
        path, _ = QFileDialog.getSaveFileName(
            self, "Save Conversation IDs", "conversation_ids.json",
            "JSON Files (*.json);;Text Files (*.txt)"
        )
        if not path:
            return
        ids = [
            self.ui.conversation_list.item(i).text()
            for i in range(self.ui.conversation_list.count())
        ]
        try:
            with open(path, "w", encoding="utf-8") as fh:
                if path.endswith(".json"):
                    _json.dump(ids, fh, indent=2, ensure_ascii=False)
                else:
                    fh.write("\n".join(ids))
        except Exception as exc:
            QMessageBox.warning(self, "Save Error", f"Could not save IDs:\n{exc}")

    def _ft_start(self):
        src  = self.ui.fb_src_dir_edit.text().strip()
        dest = self.ui.fb_dest_dir_edit.text().strip()
        if not src or not dest:
            QMessageBox.warning(
                self,
                "Missing Directories",
                "Please select both a source and a destination directory.",
            )
            return

        ids = [
            self.ui.conversation_list.item(i).text()
            for i in range(self.ui.conversation_list.count())
        ]

        include_types: set[str] = set()
        if self.ui.include_images_check.isChecked():
            include_types |= {".jpg", ".jpeg", ".png"}
        if self.ui.include_videos_check.isChecked():
            include_types.add(".mp4")
        if self.ui.include_gifs_check.isChecked():
            include_types.add(".gif")

        if not include_types:
            QMessageBox.warning(
                self,
                "No File Types Selected",
                "Please select at least one file type to transfer.",
            )
            return

        self.ui.transfer_start_btn.setEnabled(False)
        self.ui.transfer_cancel_btn.setEnabled(True)
        self.ui.transfer_progress_bar.setValue(0)
        self.ui.transfer_log.clear()

        self._transfer_worker = file_transfer.FileTransferWorker(
            src_dir       = src,
            dest_dir      = dest,
            ids           = ids,
            include_types = include_types,
            parent        = self,
        )
        self._transfer_worker.progress.connect(self.ui.transfer_progress_bar.setValue)
        self._transfer_worker.log.connect(self.ui.transfer_log.append)
        self._transfer_worker.stats_updated.connect(self._ft_update_stats)
        self._transfer_worker.finished.connect(self._ft_finished)
        self._transfer_worker.error.connect(self._ft_error)
        self._transfer_worker.start()

    def _ft_cancel(self):
        if self._transfer_worker:
            self._transfer_worker.cancel()

    def _ft_update_stats(
        self, images: int, videos: int, gifs: int, json_files: int, duplicates: int
    ):
        self.ui.transfer_log.append(
            f"Stats — Images: {images}  Videos: {videos}  "
            f"GIFs: {gifs}  JSON: {json_files}  Duplicates skipped: {duplicates}"
        )

    def _ft_finished(self, result: dict):
        self.ui.transfer_start_btn.setEnabled(True)
        self.ui.transfer_cancel_btn.setEnabled(False)

    def _ft_error(self, message: str):
        self.ui.transfer_log.append(f"[FATAL] {message}")
        self._ft_finished({})


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())