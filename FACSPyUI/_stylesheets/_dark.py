dark_stylesheet = """
/*
 *  BreezeDark stylesheet.
 *
 *  :author: Colin Duquesnoy
 *  :editor: Alex Huszagh
 *  :license: MIT, see LICENSE.md
 *
 *  This is originally a fork of QDarkStyleSheet, and is based on Breeze/
 *  BreezeDark color scheme, but is in no way affiliated with KDE.
 *
 * ---------------------------------------------------------------------
 *  The MIT License (MIT)
 *
 * Copyright (c) <2013-2014> <Colin Duquesnoy>
 * Copyright (c) <2015-2021> <Alex Huszagh>
 *
 * Permission is hereby granted, free of charge, to any person obtaining
 * a copy of this software and associated documentation files (the
 * "Software"), to deal in the Software without restriction, including
 * without limitation the rights to use, copy, modify, merge, publish,
 * distribute, sublicense, and/or sell copies of the Software, and to
 * permit persons to whom the Software is furnished to do so, subject to
 * the following conditions:
 *
 * The above copyright notice and this permission notice shall be included in
 * all copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
 * OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
 * MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
 * IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
 * CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
 * TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
 * SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
 * ---------------------------------------------------------------------
 */

/**
 *  MAIN STYLESHEET
 *  ---------------
 */

QToolTip
{
    /* 0.2ex is the smallest value that's not ignored on Windows. */
    border: 0.04em solid #eff0f1;
    background-image: none;
    background-color: #31363b;
    alternate-background-color: #31363b;
    color: #eff0f1;
    padding: 0.1em;
    opacity: 200;
}

QWidget
{
    color: #eff0f1;
    background-color: #31363b;
    selection-background-color: #3daee9;
    selection-color: #eff0f1;
    background-clip: border;
    border-image: none;

    /* QDialogButtonBox icons */
    dialog-cancel-icon: url(:/dark/dialog_cancel.svg);
    dialog-close-icon: url(:/dark/dialog_close.svg);
    dialog-ok-icon: url(:/dark/dialog_ok.svg);
    dialog-open-icon: url(:/dark/dialog_open.svg);
    dialog-reset-icon: url(:/dark/dialog_reset.svg);
    dialog-save-icon: url(:/dark/dialog_save.svg);
    dialog-yes-icon: url(:/dark/dialog_ok.svg);
    dialog-help-icon: url(:/dark/dialog_help.svg);
    dialog-no-icon: url(:/dark/dialog_no.svg);
    dialog-apply-icon: url(:/dark/dialog_ok.svg);
    dialog-discard-icon: url(:/dark/dialog_discard.svg);

    /* File icons */
    filedialog-backward-icon: url(:/dark/left_arrow.svg);
    filedialog-contentsview-icon: url(:/dark/file_dialog_contents.svg);
    filedialog-detailedview-icon: url(:/dark/file_dialog_detailed.svg);
    filedialog-end-icon: url(:/dark/file_dialog_end.svg);
    filedialog-infoview-icon: url(:/dark/file_dialog_info.svg);
    filedialog-listview-icon: url(:/dark/file_dialog_list.svg);
    filedialog-new-directory-icon: url(:/dark/folder.svg);
    filedialog-parent-directory-icon: url(:/dark/up_arrow.svg);
    filedialog-start-icon: url(:/dark/file_dialog_start.svg);
    directory-closed-icon: url(:/dark/folder.svg);
    directory-icon: url(:/dark/folder.svg);
    directory-link-icon: url(:/dark/folder_link.svg);
    directory-open-icon: url(:/dark/folder_open.svg);
    file-icon: url(:/dark/file.svg);
    file-link-icon: url(:/dark/file_link.svg);
    home-icon: url(:/dark/home_directory.svg);

    /* QMessageBox icons */
    messagebox-critical-icon: url(:/dark/message_critical.svg);
    messagebox-information-icon: url(:/dark/message_information.svg);
    messagebox-question-icon: url(:/dark/message_question.svg);
    messagebox-warning-icon: url(:/dark/message_warning.svg);

    /* Computer icons */
    computer-icon: url(:/dark/computer.svg);
    desktop-icon: url(:/dark/desktop.svg);
    cd-icon: url(:/dark/disc_drive.svg);
    dvd-icon: url(:/dark/disc_drive.svg);
    floppy-icon: url(:/dark/floppy_drive.svg);
    harddisk-icon: url(:/dark/hard_drive.svg);
    network-icon: url(:/dark/network_drive.svg);
    trash-icon: url(:/dark/trash.svg);

    /* Arrow icons */
    uparrow-icon: url(:/dark/up_arrow.svg);
    downarrow-icon: url(:/dark/down_arrow.svg);
    leftarrow-icon: url(:/dark/left_arrow.svg);
    rightarrow-icon: url(:/dark/right_arrow.svg);
    backward-icon: url(:/dark/left_arrow.svg);
    forward-icon: url(:/dark/right_arrow.svg);

    /* Titlebar icons */
    titlebar-close-icon: url(:/dark/window_close.svg);
    titlebar-contexthelp-icon: url(:/dark/help.svg);
    titlebar-maximize-icon: url(:/dark/maximize.svg);
    titlebar-menu-icon: url(:/dark/menu.svg);
    titlebar-minimize-icon: url(:/dark/minimize.svg);
    titlebar-normal-icon: url(:/dark/restore.svg);
    titlebar-shade-icon: url(:/dark/shade.svg);
    titlebar-unshade-icon: url(:/dark/unshade.svg);

    /* Other icons */
    dockwidget-close-icon: url(:/dark/close.svg);
    /**
     *  Only available in Qt6, and causes other issues. See #62.
     *  lineedit-clear-button-icon: url(:/dark/clear_text.svg);
     */
}

QWidget:disabled
{
    color: #454545;
    background-color: #31363b;
}

QCheckBox
{
    spacing: 0.23em;
    outline: none;
    color: #eff0f1;
    margin-bottom: 0.09em;
    opacity: 200;
}

QCheckBox:disabled
{
    color: #b0b0b0;
}

QGroupBox
{
    /* Need to make sure the groupbox doesn't compress below the title. */
    min-height: 1.2em;
    border: 0.04em solid #76797c;
    border-radius: 0.09em;
    /**
     * This gives us enough space at the top to ensure we can move the
     * title to be inside the guidelines, and the padding at the top
     * ensures we have space below the title.
     */
    margin-top: 0.5em;
    padding-top: 1em;
}

QGroupBox:focus
{
    border: 0.04em solid #76797c;
    border-radius: 0.09em;
}

QGroupBox::title
{
    /* We need to move 0.6em up to be inside the lines, +1em for padding. */
    top: -1.6em;
    subcontrol-origin: content;
    subcontrol-position: top center;
    background: #31363b;
    padding-left: 0.2em;
    padding-right: 0.2em;
}

QGroupBox:flat
{
    border-top: 0.04em solid #626568;
    border-left: 0.04em transparent #76797c;
    border-right: 0.04em transparent #76797c;
    border-bottom: 0.04em transparent #76797c;
}

QCheckBox::indicator,
QTreeView::indicator,
QGroupBox::indicator
{
    width: 1em;
    height: 1em;
}

QGroupBox::indicator:unchecked,
QGroupBox::indicator:unchecked:focus,
QCheckBox::indicator:unchecked,
QCheckBox::indicator:unchecked:focus,
QTreeView::indicator:unchecked,
QTreeView::indicator:unchecked:focus
{
    border-image: url(:/dark/checkbox_unchecked_disabled.svg);
}

QGroupBox::indicator:unchecked,
QCheckBox::indicator:unchecked:hover,
QCheckBox::indicator:unchecked:pressed,
QTreeView::indicator:unchecked:hover,
QTreeView::indicator:unchecked:pressed,
QGroupBox::indicator:unchecked:hover,
QGroupBox::indicator:unchecked:pressed
{
    border: none;
    border-image: url(:/dark/checkbox_unchecked.svg);
}

QCheckBox::indicator:checked,
QTreeView::indicator:checked,
QGroupBox::indicator:checked
{
    border-image: url(:/dark/checkbox_checked.svg);
}

QCheckBox::indicator:checked:hover,
QCheckBox::indicator:checked:focus,
QCheckBox::indicator:checked:pressed,
QTreeView::indicator:checked:hover,
QTreeView::indicator:checked:focus,
QTreeView::indicator:checked:pressed,
QGroupBox::indicator:checked:hover,
QGroupBox::indicator:checked:focus,
QGroupBox::indicator:checked:pressed
{
    border: none;
    border-image: url(:/dark/checkbox_checked.svg);
}

QCheckBox::indicator:indeterminate,
QTreeView::indicator:indeterminate
{
    border-image: url(:/dark/checkbox_indeterminate.svg);
}

QCheckBox::indicator:indeterminate:focus,
QCheckBox::indicator:indeterminate:hover,
QCheckBox::indicator:indeterminate:pressed,
QTreeView::indicator:indeterminate:focus,
QTreeView::indicator:indeterminate:hover,
QTreeView::indicator:indeterminate:pressed
{
    border-image: url(:/dark/checkbox_indeterminate.svg);
}

QCheckBox::indicator:indeterminate:disabled,
QTreeView::indicator:indeterminate:disabled
{
    border-image: url(:/dark/checkbox_indeterminate_disabled.svg);
}

QCheckBox::indicator:checked:disabled,
QTreeView::indicator:checked:disabled,
QGroupBox::indicator:checked:disabled
{
    border-image: url(:/dark/checkbox_checked_disabled.svg);
}

QCheckBox::indicator:unchecked:disabled,
QTreeView::indicator:unchecked:disabled,
QGroupBox::indicator:unchecked:disabled
{
    border-image: url(:/dark/checkbox_unchecked_disabled.svg);
}

QRadioButton
{
    spacing: 0.23em;
    outline: none;
    color: #eff0f1;
    margin-bottom: 0.09em;
}

QRadioButton:disabled
{
    color: #76797c;
}

QRadioButton::indicator
{
    width: 1em;
    height: 1em;
}

QRadioButton::indicator:unchecked,
QRadioButton::indicator:unchecked:focus
{
    border-image: url(:/dark/radio_unchecked_disabled.svg);
}

QRadioButton::indicator:unchecked:hover,
QRadioButton::indicator:unchecked:pressed
{
    border: none;
    outline: none;
    border-image: url(:/dark/radio_unchecked.svg);
}

QRadioButton::indicator:checked
{
    border: none;
    outline: none;
    border-image: url(:/dark/radio_checked.svg);
}

QRadioButton::indicator:checked:hover,
QRadioButton::indicator:checked:focus,
QRadioButton::indicator:checked:pressed
{
    border: none;
    outline: none;
    border-image: url(:/dark/radio_checked.svg);
}

QRadioButton::indicator:checked:disabled
{
    outline: none;
    border-image: url(:/dark/radio_checked_disabled.svg);
}

QRadioButton::indicator:unchecked:disabled
{
    border-image: url(:/dark/radio_unchecked_disabled.svg);
}

QMenuBar
{
    background-color: #31363b;
    color: #eff0f1;
}

QMenuBar::item
{
    background: transparent;
}

QMenuBar::item:selected
{
    background: transparent;
    border: 0.04em solid #3daee9;
}

QMenuBar::item:disabled
{
    color: #76797c;
}

QMenuBar::item:pressed
{
    background-color: #3daee9;
    color: #eff0f1;
    margin-bottom: -0.09em;
    padding-bottom: 0.09em;
}

QMenu
{
    color: #eff0f1;
    margin: 0.09em;
}

QMenu::icon
{
    margin: 0.23em;
}

QMenu::item
{
    /* Add extra padding on the right for the QMenu arrow */
    padding: 0.23em 1.5em 0.23em 1.3em;
    border: 0.09em solid transparent;
    background: transparent;
}

QMenu::item:selected
{
    color: #eff0f1;
    background-color: #3daee9;
}

QMenu::item:selected:disabled
{
    background-color: #31363b;
}

QMenu::item:disabled
{
    color: #76797c;
}

QMenu::indicator
{
    width: 0.8em;
    height: 0.8em;
    /* To align with QMenu::icon, which has a 0.23em margin. */
    margin-left: 0.3em;
    subcontrol-position: center left;
}

QMenu::indicator:non-exclusive:unchecked
{
    border-image: url(:/dark/checkbox_unchecked_disabled.svg);
}

QMenu::indicator:non-exclusive:unchecked:selected
{
    border-image: url(:/dark/checkbox_unchecked_disabled.svg);
}

QMenu::indicator:non-exclusive:checked
{
    border-image: url(:/dark/checkbox_checked.svg);
}

QMenu::indicator:non-exclusive:checked:selected
{
    border-image: url(:/dark/checkbox_checked.svg);
}

QMenu::indicator:exclusive:unchecked
{
    border-image: url(:/dark/radio_unchecked_disabled.svg);
}

QMenu::indicator:exclusive:unchecked:selected
{
    border-image: url(:/dark/radio_unchecked_disabled.svg);
}

QMenu::indicator:exclusive:checked
{
    border-image: url(:/dark/radio_checked.svg);
}

QMenu::indicator:exclusive:checked:selected
{
    border-image: url(:/dark/radio_checked.svg);
}

QMenu::right-arrow
{
    margin: 0.23em;
    border-image: url(:/dark/right_arrow.svg);
    width: 0.5em;
    height: 0.8em;
}

QMenu::right-arrow:disabled
{
    border-image: url(:/dark/right_arrow_disabled.svg);
}

QAbstractItemView
{
    alternate-background-color: #31363b;
    color: #eff0f1;
    border: 0.09em solid #31363b;
    border-radius: 0.09em;
}

QTabWidget:focus,
QCheckBox:focus,
QRadioButton:focus,
QSlider:focus
{
    border: none;
}

QLineEdit
{
    background-color: #1d2023;
    padding: 0.23em;
    border-style: solid;
    border: 0.04em solid #76797c;
    border-radius: 0.09em;
    color: #eff0f1;
}

QAbstractScrollArea
{
    border-radius: 0.09em;
    border: 0.09em solid #76797c;
    background-color: transparent;
}

/**
 *  This is the background for the box in the bottom-right corner
 *  whene both scrollbars are active.
 */
QAbstractScrollArea::corner
{
    background: #31363b;
}

/**
 *  Can't do the KDE style of where the scrollbar handle
 *  becomes light on the hover, and only when the handle
 *  is hovered does it become stylized. This is because
 *  both the handle and the background events are treated
 *  together.
 */
QScrollBar:horizontal
{
    background-color: #1d2023;
    height: 0.65em;
    margin: 0.13em 0.65em 0.13em 0.65em;
    border: 0.04em transparent #1d2023;
    border-radius: 0.17em;
}

QScrollBar:horizontal:hover
{
    background-color: #76797c;
}

QScrollBar::handle:horizontal
{
    background-color: #3daee9;
    border: 0.04em solid #3daee9;
    min-width: 0.5em;
    border-radius: 0.17em;
}

QScrollBar::handle:horizontal:hover
{
    background-color: #3daee9;
    border: 0.04em solid #3daee9;
}

QScrollBar::add-line:horizontal
{
    margin: 0em 0.13em 0em 0.13em;
    border-image: url(:/dark/transparent.svg);
    width: 0.41em;
    height: 0.41em;
    subcontrol-position: right;
    subcontrol-origin: margin;
}

QScrollBar::sub-line:horizontal
{
    margin: 0em 0.13em 0em 0.13em;
    border-image: url(:/dark/transparent.svg);
    width: 0.41em;
    height: 0.41em;
    subcontrol-position: left;
    subcontrol-origin: margin;
}

QScrollBar::add-line:horizontal:hover,
QScrollBar::add-line:horizontal:on
{
    border-image: url(:/dark/transparent.svg);
    width: 0.41em;
    height: 0.41em;
    subcontrol-position: right;
    subcontrol-origin: margin;
}

QScrollBar::sub-line:horizontal:hover,
QScrollBar::sub-line:horizontal:on
{
    border-image: url(:/dark/transparent.svg);
    width: 0.41em;
    height: 0.41em;
    subcontrol-position: left;
    subcontrol-origin: margin;
}

QScrollBar::up-arrow:horizontal,
QScrollBar::down-arrow:horizontal
{
    background: none;
}

QScrollBar::add-page:horizontal,
QScrollBar::sub-page:horizontal
{
    background: none;
}

QScrollBar:vertical
{
    background-color: #1d2023;
    width: 0.65em;
    margin: 0.65em 0.13em 0.65em 0.13em;
    border: 0.04em transparent #1d2023;
    border-radius: 0.17em;
}

QScrollBar:vertical:hover
{
    background-color: #76797c;
}

QScrollBar::handle:vertical
{
    background-color: #3daee9;
    border: 0.04em solid #3daee9;
    min-height: 0.5em;
    border-radius: 0.17em;
}

QScrollBar::handle:vertical:hover
{
    background-color: #3daee9;
    border: 0.04em solid #3daee9;
}

QScrollBar::sub-line:vertical
{
    margin: 0.13em 0em 0.13em 0em;
    border-image: url(:/dark/transparent.svg);
    height: 0.41em;
    width: 0.41em;
    subcontrol-position: top;
    subcontrol-origin: margin;
}

QScrollBar::add-line:vertical
{
    margin: 0.13em 0em 0.13em 0em;
    border-image: url(:/dark/transparent.svg);
    height: 0.41em;
    width: 0.41em;
    subcontrol-position: bottom;
    subcontrol-origin: margin;
}

QScrollBar::sub-line:vertical:hover,
QScrollBar::sub-line:vertical:on
{
    border-image: url(:/dark/transparent.svg);
    height: 0.41em;
    width: 0.41em;
    subcontrol-position: top;
    subcontrol-origin: margin;
}

QScrollBar::add-line:vertical:hover,
QScrollBar::add-line:vertical:on
{
    border-image: url(:/dark/transparent.svg);
    height: 0.41em;
    width: 0.41em;
    subcontrol-position: bottom;
    subcontrol-origin: margin;
}

QScrollBar::up-arrow:vertical,
QScrollBar::down-arrow:vertical
{
    background: none;
}

QScrollBar::add-page:vertical,
QScrollBar::sub-page:vertical
{
    background: none;
}

QTextEdit
{
    background-color: #1d2023;
    color: #eff0f1;
    border: 0.04em solid #76797c;
}

QPlainTextEdit
{
    background-color: #1d2023;
    color: #eff0f1;
    border-radius: 0.09em;
    border: 0.04em solid #76797c;
}

QSizeGrip
{
    border-image: url(:/dark/sizegrip.svg);
    width: 0.5em;
    height: 0.5em;
}

/**
 *  Set the separator to be transparent, since the dock has a border.
 *  On PyQt6, neither the border nor the background seem to be respected.
 */
QMainWindow::separator
{
    border: 0.09em transparent #76797c;
    background: transparent;
}

QMenu::separator
{
    height: 0.09em;
    background-color: #76797c;
    padding-left: 0.2em;
    margin-top: 0.2em;
    margin-bottom: 0.2em;
    margin-left: 0.41em;
    margin-right: 0.41em;
}

QFrame[frameShape="2"], /* QFrame::Panel == 0x0003 */
QFrame[frameShape="3"], /* QFrame::WinPanel == 0x0003 */
QFrame[frameShape="4"], /* QFrame::HLine == 0x0004 */
QFrame[frameShape="5"], /* QFrame::VLine == 0x0005 */
QFrame[frameShape="6"]  /* QFrame::StyledPanel == 0x0006 */
{
    border-width: 0.04em;
    padding: 0.09em;
    border-style: solid;
    border-color: #31363b;
    background-color: #76797c;
    border-radius: 0.23em;
}

/* Provide highlighting for frame objects. */
QFrame[frameShape="2"]:hover,
QFrame[frameShape="3"]:hover,
QFrame[frameShape="4"]:hover,
QFrame[frameShape="5"]:hover,
QFrame[frameShape="6"]:hover
{
    border: 0.04em solid #3daee9;
}

/* Don't provide an outline if we have a widget that takes up the space. */
QFrame[frameShape] QAbstractItemView:hover
{
    border: 0em solid black;
}

/**
 *  Note: I can't really change the background of the toolbars
 *  independently, since KDE Breeze has different colors for the
 *  window bar and the rest of the UI. The top toolbar uses
 *  the window style, and the rest use the application style,
 *  which we can't do.
 */
QToolBar
{
    font-weight: bold;
}

QToolBar:horizontal
{
    background: 0.09em solid #31363b;
}

QToolBar:vertical
{
    background: 0.09em solid #31363b;
}

QToolBar::handle:horizontal
{
    border-image: url(:/dark/hmovetoolbar.svg);
}

QToolBar::handle:vertical
{
    border-image: url(:/dark/vmovetoolbar.svg);
}

QToolBar::separator:horizontal
{
    border-image: url(:/dark/hseptoolbar.svg);
}

QToolBar::separator:vertical
{
    border-image: url(:/dark/vseptoolbar.svg);
}

QToolBar QToolButton
{
    font-weight: bold;
    border: 0.04em transparent black;
    padding-left: 0.2em;
    padding-right: 0.3em;
}

QToolBar QToolButton:hover
{
    border: 0.04em solid #3daee9;
}

QToolBar QToolButton:pressed
{
    border: 0.04em solid #3daee9;
    /* The padding doesn't inherit from `QToolBar QToolButton`, so leave it in. */
    padding-left: 0.2em;
    padding-right: 0.3em;
}

/**
 *  Special rules for a QFileDialog.
 *
 *  Due to the widgets, we get rid of the min sizes to allow them
 *  to pack closer together, and ensure we have enough padding for
 *  the drop-down menu in the popup.
 */
QDialog QToolBar QToolButton[popupMode="0"],
QDialog QToolBar QToolButton[popupMode="1"]
{
    padding-left: 0.1em;
    padding-right: 0.1em;
}

QDialog QToolBar QToolButton[popupMode="2"]
{
    padding-left: 0.1em;
    padding-right: 0.7em;
}

QPushButton
{
    color: #eff0f1;
    background-color: #31363b;
    border: 0.04em solid #76797c;
    padding: 0.23em;
    border-radius: 0.09em;
    outline: none;
}

QPushButton:flat,
QPushButton:flat:hover
{
    border: 0.04em transparent #76797c;
}

QComboBox:open,
QPushButton:open
{
    border-width: 0.04em;
    border-color: #76797c;
}

QComboBox:closed,
QPushButton:closed
{
    border-width: 0.04em;
    border-color: #76797c;
}

QPushButton:disabled
{
    background-color: #31363b;
    border-width: 0.04em;
    border-color: #76797c;
    border-style: solid;
    padding-top: 0.23em;
    padding-bottom: 0.23em;
    padding-left: 1ex;
    padding-right: 1ex;
    border-radius: 0.04em;
    color: #454545;
}

QPushButton:focus
{
    color: #eff0f1;
}

QPushButton:pressed
{
    background-color: #454a4f;
    padding-top: -0.65em;
    padding-bottom: -0.74em;
    color: #eff0f1;
}

QComboBox
{
    border: 0.04em solid #76797c;
    border-radius: 0.09em;
    padding: 0.23em;
    min-width: 2.5em;
}

QComboBox:editable
{
    background-color: #1d2023;
}

QPushButton:checked
{
    background-color: #626568;
    border: 0.04em solid #76797c;
    color: #eff0f1;
}

QPushButton:hover
{
    background-color: #31363b;
    border: 0.04em solid #3daee9;
    color: #eff0f1;
}

QPushButton:checked:hover
{
    background-color: #626568;
    border: 0.04em solid #3daee9;
    color: #eff0f1;
}

QComboBox:hover,
QComboBox:focus,
QAbstractSpinBox:hover,
QAbstractSpinBox:focus,
QLineEdit:hover,
QLineEdit:focus,
QTextEdit:hover,
QTextEdit:focus,
QPlainTextEdit:hover,
QPlainTextEdit:focus,
QAbstractView:hover,
QTreeView:hover,
QTreeView:focus
{
    border: 0.04em solid #3daee9;
    color: #eff0f1;
}

QComboBox:hover:pressed:!editable,
QPushButton:hover:pressed,
QAbstractSpinBox:hover:pressed,
QLineEdit:hover:pressed,
QTextEdit:hover:pressed,
QPlainTextEdit:hover:pressed,
QAbstractView:hover:pressed,
QTreeView:hover:pressed
{
    background-color: #31363b;
}

QColumnView
{
    border: 0.04em transparent #31363b;
}

QColumnViewGrip
{
    border-image: url(:/dark/sizegrip.svg);
}

/* Each column in the view is a QAbstractItemView. */
QColumnView QAbstractItemView
{
    border: 0.04em transparent #3daee9;
}

/**
 *  In order to set consistency between Qt5 and Qt6, we need
 *  to ensure that we do the following steps:
 *      1. Set a consistent `max-height` in the item. Anything
 *         below `0.8em` will cause clipping, so set that value
 *         to ensure the icon isn't larger.
 *      2. Set padding to ensure the item is properly padded.
 *      3. Set `0.2em` margins on the top and bottom of the arrows,
 *         and `0.1em` on the left and right to ensure the arrows
 *         are properly padded and have the same size.
 *
 *  The size consistency only works if both the `::item` subcontrol
 *  `max-height` and the `::*-arrow` subcontrol `margin` is set.
 */
QColumnView QAbstractItemView::item
{
    padding: 0.23em;
    max-width: 0.5em;
    max-height: 0.8em;
}

QColumnView QAbstractItemView::right-arrow
{
    image: url(:/dark/right_arrow.svg);
    margin: 0.2em 0.1em 0.2em 0.1em;
}

QColumnView QAbstractItemView::right-arrow:selected,
QColumnView QAbstractItemView::right-arrow:hover
{
    image: url(:/dark/right_arrow_hover.svg);
}

QColumnView QAbstractItemView::left-arrow
{
    image: url(:/dark/left_arrow.svg);
    margin: 0.2em 0.1em 0.2em 0.1em;
}

QColumnView QAbstractItemView::left-arrow:selected,
QColumnView QAbstractItemView::left-arrow:hover
{
    image: url(:/dark/left_arrow_hover.svg);
}

QComboBox:hover:pressed:editable
{
    background-color: #1d2023;
}

QComboBox QAbstractItemView
{
    /* This happens for the drop-down menu always, whether editable or not.*/
    background-color: #1d2023;
    selection-background-color: #2a79a3;
    outline-color: 0em;
    border-radius: 0.09em;
}

QComboBox::drop-down
{
    subcontrol-origin: padding;
    subcontrol-position: top right;
    width: 0.65em;

    border-left-width: 0em;
    border-left-style: solid;
    border-top-right-radius: 0.13em;
    border-bottom-right-radius: 0.13em;
}

QComboBox::down-arrow
{
    border-image: url(:/dark/down_arrow_disabled.svg);
    width: 0.8em;
    height: 0.5em;
    margin-right: 0.41em;
}

QComboBox::down-arrow:on,
QComboBox::down-arrow:hover,
QComboBox::down-arrow:focus
{
    border-image: url(:/dark/down_arrow.svg);
    width: 0.8em;
    height: 0.5em;
    margin-right: 0.41em;
}

QAbstractSpinBox
{
    padding: 0.23em;
    border: 0.09em solid #76797c;
    background-color: #1d2023;
    color: #eff0f1;
    border-radius: 0.09em;
    min-width: 3em;
    min-height: 1em;
}

QAbstractSpinBox:hover
{
    border: 0.09em solid #3daee9;
}

QAbstractSpinBox:up-button,
QAbstractSpinBox:up-button:hover
{
    background-color: transparent;
    subcontrol-origin: padding;
    subcontrol-position: center right;
    padding-right: 0.1em;
    width: 0.8em;
    height: 0.5em;
}

QAbstractSpinBox:down-button,
QAbstractSpinBox:down-button:hover
{
    background-color: transparent;
    subcontrol-origin: padding;
    subcontrol-position: center left;
    padding-left: 0.1em;
    width: 0.8em;
    height: 0.5em;
}

/**
 *  Bug fixes for elongated items in QSpinBoxes.
 *  By default, the items are bounded by `down-button`
 *  and `up-button`, so this doesn't actually affect the styling.
 *
 *  This does however affect some custom styling using
 *  QStyle.CC_ComboBox, which affects QDateEdit. This cannot
 *  be selected using QDateEdit, since it uses a global style.
 *  This sounds nonsensical, because CC_ComboBox isn't a spin box,
 *  but through trial and error, this is in fact the case.
 *
 *  Affects #40.
 */
QAbstractSpinBox::up-arrow,
QAbstractSpinBox::up-arrow:disabled,
QAbstractSpinBox::up-arrow:off,
QAbstractSpinBox::up-arrow:!off:!disabled:hover,
QAbstractSpinBox::down-arrow,
QAbstractSpinBox::down-arrow:disabled,
QAbstractSpinBox::down-arrow:off,
QAbstractSpinBox::down-arrow:!off:!disabled:hover
{
    border-image: none;
    width: 0.8em;
    height: 0.5em;
}

QAbstractSpinBox::up-arrow
{
    image: url(:/dark/up_arrow.svg);
}

QAbstractSpinBox::up-arrow:disabled,
QAbstractSpinBox::up-arrow:off
{
    image: url(:/dark/up_arrow_disabled.svg);
}

QAbstractSpinBox::up-arrow:hover
{
    image: url(:/dark/up_arrow_hover.svg);
}

QAbstractSpinBox::down-arrow
{
    image: url(:/dark/down_arrow.svg);
}

QAbstractSpinBox::down-arrow:disabled,
QAbstractSpinBox::down-arrow:off
{
    image: url(:/dark/down_arrow_disabled.svg);
}

QAbstractSpinBox::down-arrow:!off:!disabled:hover
{
    image: url(:/dark/down_arrow_hover.svg);
}

QDoubleSpinBox
{
    min-width: 4em;
}

/**
 *  `QCalendarWidget QAbstractItemView:enabled` sets the color, background
 *  color, and selection color for active dates in the view.
 *  `QCalendarWidget QAbstractItemView:enabled` sets the disabled dates.
 */
QCalendarWidget QAbstractItemView:enabled
{
    color: #eff0f1;
    selection-color: #eff0f1;
    selection-background-color: #3daee9;
}

/* Won't take hover events. */
QPrevNextCalButton
{
    min-width: 0.8em;
    min-height: 1.2em;
    qproperty-iconSize: 0px 0px;
}

QPrevNextCalButton#qt_calendar_nextmonth
{
    image: url(:/dark/calendar_next.svg);
}

QPrevNextCalButton#qt_calendar_prevmonth
{
    image: url(:/dark/calendar_previous.svg);
}

/**
 *  Setting for the month and year displays and drop-down menu for the
 *  month select. We style this separately because we want a drop-down
 *  indicator in the bottom right, unlike the normal QToolButton.
 */
QCalendarWidget QToolButton
{
    background-color: transparent;
    border: 0.04em solid #76797c;
    border-radius: 0.09em;
    margin: 0.23em;
    padding: 0.23em;
    padding-top: 0.1em;
    padding-right: 1.2em;
    min-height: 1.1em;
}

QCalendarWidget QToolButton:hover
{
    border: 0.04em solid #3daee9;
}

QCalendarWidget QToolButton:checked,
QCalendarWidget QToolButton:pressed
{
    background-color: #3daee9;
    padding: 0.23em;
    padding-right: 1.2em;
    min-height: 1.3em;
    outline: none;
}

/**
 *  The QCalendarWidget for QDateTimeEdit seems to improperly
 *  style the year QToolButton, which has an object name
 *  `qt_datetimedit_calendar`, so ensure we style it as well.
 */
QCalendarWidget QToolButton::menu-indicator,
#qt_datetimedit_calendar QCalendarWidget QToolButton::menu-indicator
{
    border-image: none;
    image: url(:/dark/down_arrow.svg);
    width: 0.8em;
    height: 0.5em;
    top: -0.7ex;
    left: -0.09em;
    padding-right: -1.11em;
    subcontrol-origin: content;
    subcontrol-position: bottom right;
}

QCalendarWidget QToolButton::menu-arrow,
#qt_datetimedit_calendar QCalendarWidget QToolButton::menu-arrow
{
    border-image: none;
    image: url(:/dark/down_arrow.svg);
    width: 0.8em;
    height: 0.5em;
    padding-right: 0.09em;
    subcontrol-origin: content;
    subcontrol-position: bottom right;
}

/**
 *  Setting for the year button. Both the month select and the year
 *  select are QToolButtons, and both are auto-raised. The year
 *  button however has the popup mode set to `DelayedPopup`.
 */
QCalendarWidget QToolButton[autoRaise="true"][popupMode="0"]
{
    padding: 0.23em;
}

QCalendarWidget QSpinBox
{
    max-height: 1.5em;
    min-width: 3.5em;
    margin: 0em;
    margin-top: 0.2em;
    padding: 0em;
    outline: 0em;
    padding-left: 0.5em;
}

QLabel
{
    border: 0em solid black;
}

/* BORDERS */
QTabWidget::pane
{
    padding: 0.23em;
    margin: 0.04em;
}

QTabWidget::pane:top
{
    border: 0.04em solid #76797c;
    top: -0.04em;
}

QTabWidget::pane:bottom
{
    border: 0.04em solid #76797c;
    bottom: -0.04em;
}

QTabWidget::pane:left
{
    border: 0.04em solid #76797c;
    left: -0.04em;
}

QTabWidget::pane:right
{
    border: 0.04em solid #76797c;
    right: -0.04em;
}

QTabBar
{
    qproperty-drawBase: 0;
    left: 0.23em;
    border-radius: 0.13em;
    /**
     *  Note: this is the underline for each tab title. It's not
     *  documented, and this took forever to track down. At least
     *  10 hours have been wasted trying to turn off this line,
     *  do not deleted this comment.
     */
    selection-color: transparent;
}

QTabBar:focus
{
    border: 0em transparent black;
}

QTabBar::close-button
{
    /* Doesn't seem possible to resize these buttons */
    border-image: url(:/dark/transparent.svg);
    image: url(:/dark/close.svg);
    background: transparent;
}

QTabBar::close-button:hover
{
    image: url(:/dark/close_hover.svg);
}

QTabBar::close-button:pressed
{
    image: url(:/dark/close_pressed.svg);
}

/* TOP TABS */
QTabBar::tab:top,
QTabBar::tab:top:last,
QTabBar::tab:top:only-one
{
    color: #eff0f1;
    border: 0.04em transparent black;
    border-left: 0.04em solid #76797c;
    border-right: 0.04em solid #76797c;
    border-top: 0.09em solid #3daee9;
    background-color: #31363b;
    padding: 0.23em;
    min-width: 50px;
    border-radius: 0.09em;
    border-bottom-left-radius: 0em;
    border-bottom-right-radius: 0em;
}

QTabBar::tab:top:!selected
{
    color: #eff0f1;
    background-color: #2c3034;
    border: 0.04em transparent black;
    border-right: 0.04em solid #76797c;
    border-bottom: 0.04em solid #76797c;
    border-radius: 0.09em;
    border-bottom-left-radius: 0em;
    border-bottom-right-radius: 0em;
}

QTabBar::tab:top:next-selected
{
    border-right: 0.04em transparent #2c3034;
    border-bottom-left-radius: 0em;
    border-bottom-right-radius: 0em;
}

QTabBar::tab:top:!selected:hover
{
    background-color: rgba(61, 173, 232, 0.1);
    border-radius: 0.09em;
    border-bottom-left-radius: 0em;
    border-bottom-right-radius: 0em;
}

QTabBar::tab:top:!selected:first:hover
{
    background-color: rgba(61, 173, 232, 0.1);
    border-radius: 0.09em;
    border-bottom-left-radius: 0em;
    border-bottom-right-radius: 0em;
}

/* BOTTOM TABS */
QTabBar::tab:bottom,
QTabBar::tab:bottom:last,
QTabBar::tab:bottom:only-one
{
    color: #eff0f1;
    border: 0.04em transparent black;
    border-left: 0.04em solid #76797c;
    border-right: 0.04em solid #76797c;
    border-bottom: 0.09em solid #3daee9;
    background-color: #31363b;
    padding: 0.23em;
    min-width: 50px;
    border-radius: 0.09em;
    border-top-left-radius: 0em;
    border-top-right-radius: 0em;
}

QTabBar::tab:bottom:!selected
{
    color: #eff0f1;
    background-color: #2c3034;
    border: 0.04em transparent black;
    border-top: 0.04em solid #76797c;
    border-right: 0.04em solid #76797c;
    border-radius: 0.09em;
    border-top-left-radius: 0em;
    border-top-right-radius: 0em;
}

QTabBar::tab:bottom:next-selected
{
    border-right: 0.04em transparent #2c3034;
    border-top-left-radius: 0em;
    border-top-right-radius: 0em;
}

QTabBar::tab:bottom:!selected:hover
{
    background-color: rgba(61, 173, 232, 0.1);
    border-radius: 0.09em;
    border-top-left-radius: 0em;
    border-top-right-radius: 0em;
}

QTabBar::tab:bottom:!selected:first:hover
{
    background-color: rgba(61, 173, 232, 0.1);
    border-radius: 0.09em;
    border-top-left-radius: 0em;
    border-top-right-radius: 0em;
}

/* LEFT TABS */
QTabBar::tab:left,
QTabBar::tab:left:last,
QTabBar::tab:left:only-one
{
    color: #eff0f1;
    border: 0.04em transparent black;
    border-top: 0.09em solid #3daee9;
    border-bottom: 0.04em solid #76797c;
    border-left: 0.04em solid #76797c;
    background-color: #31363b;
    padding: 0.23em;
    min-height: 50px;
    border-radius: 0.09em;
    border-top-right-radius: 0em;
    border-bottom-right-radius: 0em;
}

QTabBar::tab:left:!selected
{
    color: #eff0f1;
    background-color: #2c3034;
    border: 0.04em transparent black;
    border-top: 0.04em solid #76797c;
    border-right: 0.04em solid #76797c;
    border-radius: 0.09em;
    border-top-right-radius: 0em;
    border-bottom-right-radius: 0em;
}

QTabBar::tab:left:previous-selected
{
    border-top: 0.04em transparent #2c3034;
    border-top-right-radius: 0em;
    border-bottom-right-radius: 0em;
}

QTabBar::tab:left:!selected:hover
{
    background-color: rgba(61, 173, 232, 0.1);
    border-radius: 0.09em;
    border-top-right-radius: 0em;
    border-bottom-right-radius: 0em;
}

QTabBar::tab:left:!selected:first:hover
{
    background-color: rgba(61, 173, 232, 0.1);
    border-radius: 0.09em;
    border-top-right-radius: 0em;
    border-bottom-right-radius: 0em;
}

/* RIGHT TABS */
QTabBar::tab:right,
QTabBar::tab:right:last,
QTabBar::tab:right:only-one
{
    color: #eff0f1;
    border: 0.04em transparent black;
    border-top: 0.09em solid #3daee9;
    border-bottom: 0.04em solid #76797c;
    border-right: 0.04em solid #76797c;
    background-color: #31363b;
    padding: 0.23em;
    min-height: 50px;
    border-radius: 0.09em;
    border-top-left-radius: 0em;
    border-bottom-left-radius: 0em;
}

QTabBar::tab:right:!selected
{
    color: #eff0f1;
    background-color: #2c3034;
    border: 0.04em transparent black;
    border-top: 0.04em solid #76797c;
    border-left: 0.04em solid #76797c;
    border-radius: 0.09em;
    border-top-left-radius: 0em;
    border-bottom-left-radius: 0em;
}

QTabBar::tab:right:previous-selected
{
    border-top: 0.04em transparent #2c3034;
    border-top-left-radius: 0em;
    border-bottom-left-radius: 0em;
}

QTabBar::tab:right:!selected:hover
{
    background-color: rgba(61, 173, 232, 0.1);
    border-radius: 0.09em;
    border-top-left-radius: 0em;
    border-bottom-left-radius: 0em;
}

QTabBar::tab:right:!selected:first:hover
{
    background-color: rgba(61, 173, 232, 0.1);
    border-radius: 0.09em;
    border-top-left-radius: 0em;
    border-bottom-left-radius: 0em;
}

/**
 *  Special styles for triangular QTabWidgets.
 *  These ignore the border attributes, and the border and
 *  text color seems to be set via the `QTabBar::tab` color
 *  property. This seemingly cannot be changed.
 *
 *  The rounded shapes are 0-3, and the triangular ones are 4-7.
 *
 *  The QTabBar outline doesn't respect on QTabBar::tab:
 *      border-color
 *      outline-color
 */
QTabBar[shape="4"]::tab,
QTabBar[shape="5"]::tab,
QTabBar[shape="6"]::tab,
QTabBar[shape="7"]::tab,
QTabBar[shape="4"]::tab:last,
QTabBar[shape="5"]::tab:last,
QTabBar[shape="6"]::tab:last,
QTabBar[shape="7"]::tab:last,
QTabBar[shape="4"]::tab:only-one,
QTabBar[shape="5"]::tab:only-one,
QTabBar[shape="6"]::tab:only-one,
QTabBar[shape="7"]::tab:only-one
{
    /* Need a dark color without alpha channel since it affects the text. */
    color: #3daee9;
    background-color: #31363b;
    padding: 0.23em;
}

QTabBar[shape="4"]::tab,
QTabBar[shape="5"]::tab,
QTabBar[shape="4"]::tab:last,
QTabBar[shape="5"]::tab:last,
QTabBar[shape="4"]::tab:only-one,
QTabBar[shape="5"]::tab:only-one
{
    min-width: 50px;
}

QTabBar[shape="6"]::tab,
QTabBar[shape="7"]::tab,
QTabBar[shape="6"]::tab:last,
QTabBar[shape="7"]::tab:last,
QTabBar[shape="6"]::tab:only-one,
QTabBar[shape="7"]::tab:only-one
{
    min-height: 50px;
}

QTabBar[shape="4"]::tab:!selected,
QTabBar[shape="5"]::tab:!selected,
QTabBar[shape="6"]::tab:!selected,
QTabBar[shape="7"]::tab:!selected
{
    color: #eff0f1;
    background-color: #2c3034;
}

/**
 *  Increase padding on the opposite side of the icon to avoid text clipping.
 *
 *  BUG: The padding works for North, West, and East in Qt5, South does not
 *  work. All tab positions work for triangular tabs in Qt6.
 */
QTabBar[shape="4"][tabsClosable="true"]::tab,
QTabBar[shape="5"][tabsClosable="true"]::tab
{
    padding-left: 0.5em;
}

QTabBar[shape="6"][tabsClosable="true"]::tab
{
    padding-bottom: 0.5em;
}

QTabBar[shape="7"][tabsClosable="true"]::tab
{
    padding-top: 0.5em;
}

/**
*   Undo the padding for the tab.
*
*   Enumerated values are North, South, West, East in that order,
*   from 4-7.
*
*   NOTE: Any higher padding will clip the icon.
*/
QTabBar[shape="4"]::close-button,
QTabBar[shape="5"]::close-button
{
    padding-left: -0.12em;
}

QTabBar[shape="6"]::close-button
{
    padding-bottom: -0.18em;
}

QTabBar[shape="7"]::close-button
{
    padding-top: -0.18em;
}

QDockWidget
{
    background: #31363b;
    /**
     *  It doesn't seem possible to change the border of the
     *  QDockWidget without changing the content margins.
     */
    /**
     *  This is a bug fix so we can handle hover, pressed, and other events.
     *  Reference: https://stackoverflow.com/questions/32145080/qdockwidget-float-close-button-hover-images
     */
    titlebar-close-icon: url(:/dark/transparent.svg);
    titlebar-normal-icon: url(:/dark/transparent.svg);
}

/**
 *  Don't style the title, since it gives a weird, missing border
 *  around the rest of the dock widget, which the remaining border
 *  cannot be removed.
 *
 *  There is a bug in non-Breeze styles, where the icons are small. It 
 *  doesn't change if we use `image` instead of `border-image`, nor if 
 *  we use `qproperty-icon`, etc. The icon seem to be half the size
 *  of our desired values.
 */
QDockWidget::close-button,
QDockWidget::float-button
{
    border: 0.04em solid transparent;
    border-radius: 0.09em;
    background: transparent;
    /* Maximum icon size for buttons */
    icon-size: 14px;
}

QDockWidget::float-button
{
    border-image: url(:/dark/transparent.svg);
    image: url(:/dark/undock.svg);
}

QDockWidget::float-button:hover
{
    image: url(:/dark/undock_hover.svg);
}

/* The :pressed events don't register, seems to be a Qt bug. */
QDockWidget::float-button:pressed
{
    image: url(:/dark/undock_hover.svg);
}

QDockWidget::close-button
{
    border-image: url(:/dark/transparent.svg);
    image: url(:/dark/close.svg);
}

QDockWidget::close-button:hover
{
    image: url(:/dark/close_hover.svg);
}

/* The :pressed events don't register, seems to be a Qt bug. */
QDockWidget::close-button:pressed
{
    image: url(:/dark/close_pressed.svg);
}

QTreeView,
QListView
{
    background-color: #1d2023;
    border: 0em solid black;
}

QTreeView:selected,
QTreeView:!selected,
QListView:selected,
QListView:!selected
{
    border: 0em solid black;
}

QTreeView::branch:has-siblings
{
    border-image: url(:/dark/vline.svg);
    image: none;
}

/* These branch indicators don't scale */
QTreeView::branch:!has-siblings
{
    border-image: none;
    image: none;
}

QTreeView::branch:has-siblings:adjoins-item
{
    border-image: url(:/dark/branch_more.svg);
}

QTreeView::branch:!has-children:!has-siblings:adjoins-item
{
    border-image: url(:/dark/branch_end.svg);
}

QTreeView::branch:has-children:!has-siblings:closed,
QTreeView::branch:closed:has-children:has-siblings
{
    image: url(:/dark/branch_closed.svg);
}

QTreeView::branch:has-children:!has-siblings:closed:hover,
QTreeView::branch:closed:has-children:has-siblings:hover
{
    image: url(:/dark/branch_closed_hover.svg);
}

QTreeView::branch:has-children:!has-siblings:closed,
QTreeView::branch:open:has-children:!has-siblings
{
    border-image: url(:/dark/branch_end_arrow.svg);
}

QTreeView::branch:closed:has-children:has-siblings,
QTreeView::branch:open:has-children:has-siblings
{
    border-image: url(:/dark/branch_more_arrow.svg);
}

QTreeView::branch:open:has-children:!has-siblings,
QTreeView::branch:open:has-children:has-siblings
{
    image: url(:/dark/branch_open.svg);
}

QTreeView::branch:open:has-children:!has-siblings:hover,
QTreeView::branch:open:has-children:has-siblings:hover
{
    image: url(:/dark/branch_open_hover.svg);
}

QListView
{
    /* Give space for elements aligned left or right. */
    padding: 0.2em;
}

QTableView::item,
QListView::item,
QTreeView::item
{
    padding: 0.13em;
    color: #eff0f1;
}

QTreeView::item
{
    /**
     *  Need to set the background color in Qt6, or else
     *  the QTreeView indicators use the style defaults,
     *  along with the box model, which conflicts with our
     *  theme (except with hover/focus/selected pseudostates).
     *
     *  Affects issue #51.
     */
    background-color: #1d2023;
    outline: 0;
}

QTableView::item:!selected:hover,
QListView::item:!selected:hover,
QTreeView::item:!selected:hover
{
    background-color: rgba(61, 173, 232, 0.1);
    outline: 0;
    color: #eff0f1;
    padding: 0.13em;
}

QAbstractItemView::item QLineEdit
{
    border: 0em transparent black;
    /*
     *  The top/bottom padding causes the editable widget to conceal text.
     *  https://github.com/Alexhuszagh/BreezeStyleSheets/issues/69
     */
    padding: 0em;
}

QSlider::handle:horizontal,
QSlider::handle:vertical
{
    background: #1d2023;
    border: 0.04em solid #626568;
    width: 0.7em;
    height: 0.7em;
    border-radius: 0.35em;
}

QSlider:horizontal
{
    height: 2em;
}

QSlider:vertical
{
    width: 2em;
}

QSlider::handle:horizontal
{
    margin: -0.23em 0;
}

QSlider::handle:vertical
{
    margin: 0 -0.23em;
}

QSlider::groove:horizontal,
QSlider::groove:vertical
{
    background: #2c3034;
    border: 0em solid #31363b;
    border-radius: 0.19em;
}

QSlider::groove:horizontal
{
    height: 0.4em;
}

QSlider::groove:vertical
{
    width: 0.4em;
}

QSlider::handle:horizontal:hover,
QSlider::handle:horizontal:focus,
QSlider::handle:vertical:hover,
QSlider::handle:vertical:focus
{
    border: 0.04em solid #3daee9;
}

QSlider::handle:horizontal:!focus:!hover,
QSlider::handle:vertical:!focus:!hover
{
    border: 0.04em solid #626568;
}

QSlider::sub-page:horizontal,
QSlider::add-page:vertical
{
    background: #3daee9;
    border-radius: 0.19em;
}

QSlider::add-page:horizontal,
QSlider::sub-page:vertical
{
    background: #626568;
    border-radius: 0.19em;
}

/* QToolButton */
/**
 *  QToolButton's that have a push button need to be styled differently,
 *  depending on whether there are actions (a menu) associated with it.
 *  This is signaled by a drop-down arrow on the right of the push button.
 *  Unfortunately, there's no good property to determine this. The property
 *  we need is `QWidget::actions`, however, it's a method and not a
 *  property.Note that the drop-down menu is not signaled by any of the
 *  following:
 *      popupMode: any pop-up mode does not affect the right arrow style.
 *      arrowType: only replaces the icon.
 *      toolButtonStyle: this is almost always set to icon only, even with text.
 *      text: can have a drop-down menu with or without text.
 *
 *  Notably, we need to ensure we don't pad the widgets in the following
 *  cases:
 *      1. If the QToolButton is auto-raised.
 *          This adds undesired padding in`QFileDialog`. These widgets
 *          have text, even though no text is visible. This is not the
 *          default, so it won't affect most situations.
 *      2. If the QToolButton does not have text.
 *          Normally, text-less buttons do not have a menu, and this
 *          is required for #47, since the padding affects the scroll
 *          bar icons in QTabBar. This causes major issues in the
 *          UI, so disable the padding by default.
 *
 *  The padding can affect the placement of icons and other things
 *  inside the toolbutton: near the menu-button in QFileDialog,
 *  the clear text icon is misplaced vertically, making it nearly
 *  illegible.
 *
 *  We provide special styles for a custom, dynamic property to
 *  override the padding decisions with or without a menu.
 *  To force styling as if there is a menu, set the `hasMenu` property
 *  to true. Setting `hasMenu` to false will style as if there is no menu.
 *  You can use `QWidget::setProperty` to set this property dynamically.
 *
 *  The affected issues are #22, #28, #47.
 *      https://github.com/Alexhuszagh/BreezeStyleSheets/issues/22
 *      https://github.com/Alexhuszagh/BreezeStyleSheets/issues/28
 *      https://github.com/Alexhuszagh/BreezeStyleSheets/issues/47
 */

/**
 *  Use an overly specific selector here to ensure no margins,
 *  or for the default QToolButton. We must have `autoRaise="false"`
 *  and `text` to have padding, so just add a `hasMenu="false"` to
 *  undo the padding in that case. Also add selectors for QDialog
 *  if a menu is explicitly forbidden.
 */
QToolButton,
QToolButton[hasMenu="false"][autoRaise="false"][text],
QDialog QToolBar QToolButton[hasMenu="false"][popupMode="0"],
QDialog QToolBar QToolButton[hasMenu="false"][popupMode="1"],
QDialog QToolBar QToolButton[hasMenu="false"][popupMode="2"]
{
    margin: 0em;
    padding: 0em;
}

QToolButton[autoRaise="false"]
{
    background-color: #31363b;
    border: 0.04em solid #76797c;
    border-radius: 0.09em;
}

QToolButton[autoRaise="true"]
{
    background-color: #31363b;
    border: 0.04em solid transparent;
}

/* Add selectors for the QDialog if a menu is explicitly requested. */
QToolButton[hasMenu="true"],
QToolButton[autoRaise="false"][text],
QDialog QToolBar QToolButton[hasMenu="true"][popupMode="0"],
QDialog QToolBar QToolButton[hasMenu="true"][popupMode="1"],
QDialog QToolBar QToolButton[hasMenu="true"][popupMode="2"]
{
    margin: 0.23em;
    padding: 0.23em;
    padding-top: 0.1em;
    padding-right: 1.2em;
}

QToolButton:hover
{
    border: 0.04em solid #3daee9;
}

QToolButton:checked,
QToolButton:pressed
{
    border: 0.04em solid #3daee9;
    background-color: #3daee9;
}

QToolButton::right-arrow,
QToolButton::left-arrow,
QToolButton::up-arrow,
QToolButton::down-arrow
{
    /**
     *  Do not set the arrow width/height here. It causes
     *  small icons in Qt6, and doesn't affect the styling
     *  in Qt5. Both look ideal without manually specified sizes.
     */
    subcontrol-origin: content;
    subcontrol-position: center;
    margin: 0em;
    padding: 0em;
}

QToolButton::right-arrow:enabled
{
    image: url(:/dark/right_arrow.svg);
}

QToolButton::left-arrow:enabled
{
    image: url(:/dark/left_arrow.svg);
}

QToolButton::up-arrow:enabled
{
    image: url(:/dark/up_arrow.svg);
}

QToolButton::down-arrow:enabled
{
    image: url(:/dark/down_arrow.svg);
}

QToolButton::right-arrow:disabled
{
    image: url(:/dark/right_arrow_disabled.svg);
}

QToolButton::left-arrow:disabled
{
    image: url(:/dark/left_arrow_disabled.svg);
}

QToolButton::up-arrow:disabled
{
    image: url(:/dark/up_arrow_disabled.svg);
}

QToolButton::down-arrow:disabled
{
    image: url(:/dark/down_arrow_disabled.svg);
}

QToolButton::menu-indicator
{
    border-image: none;
    image: url(:/dark/down_arrow.svg);
    width: 0.8em;
    height: 0.5em;
    left: -0.09em;
    /* -1.2em + 0.09em */
    padding-right: -1.11em;
    /**
     *  Qt5 and Qt6 differ if the subcontrol-origin is set to
     *  the default, AKA, padding. Setting it to the content,
     *  which we adjust the padding to, makes it uniform between
     *  both.
     */
    subcontrol-origin: content;
    subcontrol-position: right;
}

/**
 *  Special rule for the drop-down indicator in a QFileDialog.
 *  We want these to be more compact, hence the smaller padding.
 */
QDialog QToolBar QToolButton[popupMode="2"]::menu-indicator
{
    padding-right: -0.7em;
}

QToolButton::menu-arrow
{
    border-image: none;
    image: url(:/dark/down_arrow.svg);
    width: 0.8em;
    height: 0.5em;
    padding-right: 0.09em;
    subcontrol-position: right;
}

QToolButton::menu-button
{
    border-top-right-radius: 0.5em;
    border-bottom-right-radius: 0.5em;
    /* 1ex width + 0.4ex for border + no text = 2ex allocated above */
    width: 1.3em;
    padding: 0.23em;
    outline: none;
}

QToolButton::menu-button::menu-arrow
{
    left: -0.09em;
    subcontrol-position: right;
}

QToolButton::menu-button:hover
{
    background-color: transparent;
}

QToolButton::menu-button:pressed
{
    background-color: transparent;
    padding: 0.23em;
    outline: none;
}

QTableView
{
    border: 0em solid black;
    gridline-color: #31363b;
    background-color: #1d2023;
}

QTableView:!selected,
QTableView:selected
{
    border: 0em solid black;
}

QTableView
{
    border-radius: 0em;
}

QAbstractItemView::item
{
    color: #eff0f1;
}

QAbstractItemView::item:pressed
{
    background: #2a79a3;
    color: #eff0f1;
}

QAbstractItemView::item:selected:!active
{
    background: rgba(61, 173, 232, 0.1);
}

/* Use background with qlineargradient to avoid ugly border on widget. */
QAbstractItemView::item:selected:active
{
    background: qlineargradient(
        x1: 0.5, y1: 0.5
        x2: 0.5, y2: 1,
        stop: 0 #2a79a3,
        stop: 1 #2a79a3
    );
    color: #eff0f1;
}

QAbstractItemView::item:selected:hover
{
    background: qlineargradient(
        x1: 0.5, y1: 0.5
        x2: 0.5, y2: 1,
        stop: 0 #2f88b7,
        stop: 1 #2f88b7
    );
    color: #eff0f1;
}

QHeaderView
{
    background-color: #31363b;
    border: 0.04em transparent;
    border-radius: 0em;
    margin: 0em;
    padding: 0em;
}

QHeaderView::section
{
    background-color: #31363b;
    border: 0.04em solid #76797c;
    color: #eff0f1;
    border-radius: 0em;
    padding: 0em 0.23em 0em 0.23em;
    text-align: center;
}

QHeaderView::section::vertical::first,
QHeaderView::section::vertical::only-one
{
    border-top: 0.04em solid #76797c;
}

QHeaderView::section::vertical
{
    border-top: transparent;
}

QHeaderView::section::horizontal::first,
QHeaderView::section::horizontal::only-one
{
    border-left: 0.04em solid #76797c;
}

QHeaderView::section::horizontal
{
    border-left: transparent;
}

QHeaderView[showSortIndicator="true"]::section::horizontal
{
    /* Same as the width of the arrow subcontrols below. */
    padding-right: 0.8em;
}

QHeaderView::section:checked
{
    color: #ffffff;
    background-color: #334e5e;
}

/* Note that this doesn't work for QTreeView unless the header is clickable */
QHeaderView::section:hover,
QHeaderView::section::horizontal::first:hover,
QHeaderView::section::horizontal::only-one:hover,
QHeaderView::section::vertical::first:hover,
QHeaderView::section::vertical::only-one:hover
{
    border: 0.04em solid #3daee9;
}

QHeaderView[showSortIndicator="true"]::down-arrow
{
    image: url(:/dark/down_arrow.svg);
    /**
     *  Qt5 and Qt6 differ if the subcontrol-origin is set to
     *  the default, AKA, padding. Setting it to the content,
     *  which we adjust the padding to, makes it uniform between
     *  both.
     */
    subcontrol-origin: content;
    subcontrol-position: center right;
    width: 0.8em;
    height: 0.5em;
    /**
     *  Qt5 and Qt6 have different ideas of the padding of the
     *  arrow subcontrols: using `padding-left` to ensure that
     *  the width is undone fixes the padding of the content by
     *  an extra `0.8em` in Qt6, but doesn't affect Qt5.
     */
    padding-right: 0.09em;
    padding-left: -0.8em;
}

QHeaderView[showSortIndicator="true"]::up-arrow
{
    image: url(:/dark/up_arrow.svg);
    subcontrol-origin: content;
    subcontrol-position: center right;
    width: 0.8em;
    height: 0.5em;
    padding-right: 0.09em;
    padding-left: -0.8em;
}

QTableView QTableCornerButton::section
{
    background-color: #31363b;
    border: 0.04em transparent #76797c;
    border-top: 0.04em solid #76797c;
    border-left: 0.04em solid #76797c;
    border-radius: 0em;
}

/* No hover event */
QTableView QTableCornerButton:hover
{
    border: 0.04em transparent #76797c;
}

QTableView QTableCornerButton::section:pressed
{
    border: 0.04em solid #3daee9;
    border-radius: 0em;
}

QToolBox
{
    padding: 0.23em;
    border: 0.09em transparent black;
}

QToolBox::tab
{
    border-bottom: 0.09em solid #76797c;
    margin-left: 1.5em;
}

QToolBox::tab:selected,
QToolBox::tab:hover
{
    border-bottom: 0.09em solid #3daee9;
}

QSplitter::handle
{
    border: 0.09em solid #2c3034;
    background: -0.5em solid #2c3034;
    max-width: 0em;
    max-height: 0em;
}

/**
 *  It's not possible to get satisfactory rounded borders here.
 *  If you set the border to be negative, while adjusting the
 *  widths, you get an asymmetrical curve which produces an
 *  unappealing border.
 */
QProgressBar:horizontal,
QProgressBar:vertical
{
    background-color: #626568;
    border: 0.9em solid #31363b;
    border-radius: 0.13em;
    padding: 0em;
}

QProgressBar:horizontal
{
    height: 0.2em;
    min-width: 6em;
    text-align: right;
    padding-left: -0.03em;
    padding-right: -0.03em;
    margin-top: 0.2em;
    margin-bottom: 0.2em;
    margin-right: 1.3em;
}

QProgressBar:vertical
{
    width: 0.2em;
    min-height: 6em;
    text-align: bottom;
    padding-top: -0.03em;
    padding-bottom: -0.03em;
    margin-left: 0.2em;
    margin-right: 0.2em;
    margin-bottom: 0.41em;
}

QProgressBar::chunk:horizontal,
QProgressBar::chunk:vertical
{
    background-color: #3daee9;
    border: 0.9em transparent;
    border-radius: 0.08em;
}

QScrollArea,
QScrollArea:focus,
QScrollArea:hover
{
    border: 0em solid black;
}

/* ICONS */
/**
 *  Qt's built-in icons can look pretty bad if the system theme
 *  is a different color than the current one. For example, when
 *  using a dark theme, with a light UI, the `Ok` button is greyed
 *  out for an about dialog.
 *
 *  QDialogButtonBox will apply for all standard buttons in all standard
 *  widgets, such as QMessageBox, etc. However, we do need to override
 *  standard icons elsewhere.
 *
 *  The rest of the icons make little sense to implement:
 *      Qt uses native window decorations.
 *      Qt normally uses native file dialogs, which look nicer.
 *      Media controls are used in custom widgets, which aren't standard.
 */
QDialogButtonBox
{
    dialogbuttonbox-buttons-have-icons: true;

    dialog-cancel-icon: url(:/dark/dialog_cancel.svg);
    dialog-close-icon: url(:/dark/dialog_close.svg);
    dialog-ok-icon: url(:/dark/dialog_ok.svg);
    dialog-open-icon: url(:/dark/dialog_open.svg);
    dialog-reset-icon: url(:/dark/dialog_reset.svg);
    dialog-save-icon: url(:/dark/dialog_save.svg);
    /**
     *  No support yet for overriding saveall.
     *  dialog-saveall-icon: url(:/dark/dialog_saveall.svg);
     */
    dialog-yes-icon: url(:/dark/dialog_ok.svg);
    dialog-help-icon: url(:/dark/dialog_help.svg);
    dialog-no-icon: url(:/dark/dialog_no.svg);
    dialog-apply-icon: url(:/dark/dialog_ok.svg);
    dialog-discard-icon: url(:/dark/dialog_discard.svg);
}

/* Set some styles for these custom dialog buttons */
QDialogButtonBox QPushButton,
QMessageBox QPushButton
{
    min-height: 1.1em;
    min-width: 5em;
}

/**
 *  Special rules for creating a custom titlebar. This can only work
 *  when setting the Qt property `isTitlebar` to `true`.
 */
QWidget[isTitlebar="true"],
QWidget[isTitlebar="true"] *
{
    background-color: #2c3034;
}

/**
 *  Special rules for creating a border around a top-level frame of a window. 
 *  This can only work when setting the Qt property `isWindow` to `true`.
 *  We've manually enumerated border widths from 1-5 below.
 */
QFrame[isWindow="true"],
QFrame[frameShape][isWindow="true"]
{
    border: 0px transparent #2c3034;
}

QFrame[isWindow="true"][windowFrame="1"],
QFrame[frameShape][isWindow="true"][windowFrame="1"]
{
    border: 1px solid #2c3034;
    border-radius: 3px;
}

QFrame[isWindow="true"][windowFrame="2"],
QFrame[frameShape][isWindow="true"][windowFrame="2"]
{
    border: 2px solid #2c3034;
    border-radius: 3px;
}

QFrame[isWindow="true"][windowFrame="3"],
QFrame[frameShape][isWindow="true"][windowFrame="3"]
{
    border: 3px solid #2c3034;
    border-radius: 3px;
}

QFrame[isWindow="true"][windowFrame="4"],
QFrame[frameShape][isWindow="true"][windowFrame="4"]
{
    border: 4px solid #2c3034;
    border-radius: 3px;
}

QFrame[isWindow="true"][windowFrame="5"],
QFrame[frameShape][isWindow="true"][windowFrame="5"]
{
    border: 5px solid #2c3034;
    border-radius: 3px;
}
"""
