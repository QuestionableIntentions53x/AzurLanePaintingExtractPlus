# -*- coding: utf-8 -*-

###########################################################################
## Python code generated with wxFormBuilder (version Oct 26 2018)
## http://www.wxformbuilder.org/
##
## PLEASE DO *NOT* EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc
import wx.adv

# TODO: This is a bandaid fix, current wxPython layout is outdated
import os
os.environ["WXSUPPRESS_SIZER_FLAGS_CHECK"] = "1"

import gettext
_ = gettext.gettext

###########################################################################
## Class MainFrame
###########################################################################

class MainFrame ( wx.Frame ):

	def __init__( self, parent ):
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = "Azur Lane Painting Extract", pos = wx.DefaultPosition, size = wx.Size( 1024,576 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )

	def __del__( self ):
		pass

	
	def build( self, translator ):
		self.DestroyChildren()

		_ = translator.t
		
		self.SetTitle(_("Azur Lane Painting Extract"))

		self.SetSizeHints( wx.Size( 512,288 ), wx.DefaultSize )
		self.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOW ) )

		bSizer1 = wx.BoxSizer( wx.VERTICAL )

		bSizer6 = wx.BoxSizer( wx.HORIZONTAL )

		self.m_panel1 = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		self.m_panel1.SetMinSize( wx.Size( 325,-1 ) )
		self.m_panel1.SetMaxSize( wx.Size( 325,-1 ) )

		bSizer3 = wx.BoxSizer( wx.VERTICAL )

		bSizer8 = wx.BoxSizer( wx.HORIZONTAL )

		m_choice_filterChoices = _("All|Base|Skins|Retrofit|Promise|Young|MUSE μ|Other").split("|")
		self.m_choice_filter = wx.Choice( self.m_panel1, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, m_choice_filterChoices, 0 )
		self.m_choice_filter.SetSelection( 0 )
		self.m_choice_filter
		bSizer8.Add( self.m_choice_filter, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.EXPAND, 5 )

		self.m_staticline5 = wx.StaticLine( self.m_panel1, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_VERTICAL )
		bSizer8.Add( self.m_staticline5, 0, wx.EXPAND |wx.ALL, 5 )

		self.m_searchCtrl1 = wx.SearchCtrl( self.m_panel1, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.TE_CENTER )
		self.m_searchCtrl1.ShowSearchButton( False )
		self.m_searchCtrl1.ShowCancelButton( True )
		bSizer8.Add( self.m_searchCtrl1, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )


		bSizer3.Add( bSizer8, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.EXPAND, 5 )

		self.m_treeCtrl_info = wx.TreeCtrl( self.m_panel1, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TR_DEFAULT_STYLE|wx.TR_FULL_ROW_HIGHLIGHT|wx.TR_HAS_BUTTONS|wx.TR_HAS_VARIABLE_ROW_HEIGHT|wx.TR_HIDE_ROOT|wx.TR_ROW_LINES|wx.TR_SINGLE|wx.TR_TWIST_BUTTONS )
		bSizer3.Add( self.m_treeCtrl_info, 1, wx.ALL|wx.EXPAND, 5 )

		bSizer4 = wx.BoxSizer( wx.VERTICAL )

		bSizer5 = wx.BoxSizer( wx.HORIZONTAL )

		self.m_button_work = wx.Button( self.m_panel1, wx.ID_ANY, _("Export"), wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer5.Add( self.m_button_work, 0, wx.ALL, 5 )

		self.m_staticline2 = wx.StaticLine( self.m_panel1, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_VERTICAL )
		bSizer5.Add( self.m_staticline2, 0, wx.EXPAND |wx.ALL, 5 )

		self.m_bpButton_change = wx.Button( self.m_panel1, wx.ID_ANY, _("Set pairing file"), wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer5.Add( self.m_bpButton_change, 0, wx.ALL, 5 )

		self.m_staticline4 = wx.StaticLine( self.m_panel1, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_VERTICAL )
		bSizer5.Add( self.m_staticline4, 0, wx.EXPAND |wx.ALL, 5 )

		self.m_bpButton_setting = wx.BitmapButton( self.m_panel1, wx.ID_ANY, wx.NullBitmap, wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW|0 )

		self.m_bpButton_setting.SetBitmap( wx.ArtProvider.GetBitmap( wx.ART_HELP_BOOK, wx.ART_BUTTON ) )
		bSizer5.Add( self.m_bpButton_setting, 1, wx.ALL|wx.EXPAND|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.m_staticline45 = wx.StaticLine( self.m_panel1, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_VERTICAL )
		bSizer5.Add( self.m_staticline45, 0, wx.EXPAND |wx.ALL, 5 )

		self.m_bpButton_refeash = wx.BitmapButton( self.m_panel1, wx.ID_ANY, wx.NullBitmap, wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW|0 )

		self.m_bpButton_refeash.SetBitmap( wx.ArtProvider.GetBitmap( wx.ART_NEW_DIR, wx.ART_BUTTON ) )
		bSizer5.Add( self.m_bpButton_refeash, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.EXPAND, 5 )


		bSizer4.Add( bSizer5, 1, wx.EXPAND, 5 )

		self.m_gauge_state = wx.Gauge( self.m_panel1, wx.ID_ANY, 100, wx.DefaultPosition, wx.DefaultSize, wx.GA_HORIZONTAL )
		self.m_gauge_state.SetValue( 0 )
		bSizer4.Add( self.m_gauge_state, 0, wx.ALL|wx.EXPAND, 5 )


		bSizer3.Add( bSizer4, 0, wx.EXPAND, 5 )


		self.m_panel1.SetSizer( bSizer3 )
		self.m_panel1.Layout()
		bSizer3.Fit( self.m_panel1 )
		bSizer6.Add( self.m_panel1, 1, wx.EXPAND |wx.ALL, 5 )

		self.m_staticline1 = wx.StaticLine( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_VERTICAL )
		bSizer6.Add( self.m_staticline1, 0, wx.EXPAND |wx.ALL, 5 )

		self.m_scrolledWindow2 = wx.ScrolledWindow( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.HSCROLL|wx.VSCROLL )
		self.m_scrolledWindow2.SetScrollRate( 5, 5 )
		bSizer12 = wx.BoxSizer( wx.VERTICAL )

		self.m_bitmap_show = wx.StaticBitmap( self.m_scrolledWindow2, wx.ID_ANY, wx.ArtProvider.GetBitmap( wx.ART_MISSING_IMAGE, wx.ART_OTHER ), wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer12.Add( self.m_bitmap_show, 1, wx.ALL|wx.EXPAND|wx.ALIGN_CENTER_VERTICAL, 5 )


		self.m_scrolledWindow2.SetSizer( bSizer12 )
		self.m_scrolledWindow2.Layout()
		bSizer12.Fit( self.m_scrolledWindow2 )
		bSizer6.Add( self.m_scrolledWindow2, 1, wx.EXPAND |wx.ALL, 5 )


		bSizer1.Add( bSizer6, 1, wx.EXPAND, 5 )

		self.m_staticline3 = wx.StaticLine( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		bSizer1.Add( self.m_staticline3, 0, wx.EXPAND |wx.ALL, 5 )

		self.m_staticText_info = wx.StaticText( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText_info.Wrap( -1 )

		bSizer1.Add( self.m_staticText_info, 0, wx.ALL|wx.EXPAND, 5 )


		self.SetSizer( bSizer1 )
		self.Layout()
		self.m_statusBar1 = self.CreateStatusBar( 1, wx.STB_SIZEGRIP, wx.ID_ANY )

		self.Centre( wx.BOTH )

		# Connect Events
		self.Bind( wx.EVT_CLOSE, self.exit )
		self.Bind( wx.EVT_KEY_DOWN, self.on_key_Down )
		self.Bind( wx.EVT_MOVE_END, self.resize )
		self.m_choice_filter.Bind( wx.EVT_CHOICE, self.filter_work )
		self.m_searchCtrl1.Bind( wx.EVT_TEXT, self.search )
		self.m_searchCtrl1.Bind( wx.EVT_TEXT_ENTER, self.search )
		self.m_treeCtrl_info.Bind( wx.EVT_TREE_SEL_CHANGED, self.on_info_select )
		self.m_button_work.Bind( wx.EVT_BUTTON, self.work )
		self.m_bpButton_change.Bind( wx.EVT_BUTTON, self.choice_file )
		self.m_bpButton_setting.Bind( wx.EVT_BUTTON, self.setting )
		self.m_bpButton_refeash.Bind( wx.EVT_BUTTON, self.refeash )

	def rebuild( self, translator ):
		_ = translator.t
		
		self.SetTitle(_("Azur Lane Painting Extract"))
		
		m_choice_filterChoices = _("All|Base|Skins|Retrofit|Promise|Young|MUSE μ|Other").split("|")
		for i in range(len(m_choice_filterChoices)):
			self.m_choice_filter.SetString(i, m_choice_filterChoices[i])

		self.m_button_work.SetLabelText(_("Export"))
		
		self.m_bpButton_change.SetLabelText(_("Set pairing file"))
		

	# Virtual event handlers, overide them in your derived class
	def exit( self, event ):
		event.Skip()

	def on_key_Down( self, event ):
		event.Skip()

	def resize( self, event ):
		event.Skip()

	def filter_work( self, event ):
		event.Skip()

	def search( self, event ):
		event.Skip()


	def on_info_select( self, event ):
		event.Skip()

	def work( self, event ):
		event.Skip()

	def choice_file( self, event ):
		event.Skip()

	def setting( self, event ):
		event.Skip()

	def refeash( self, event ):
		event.Skip()


###########################################################################
## Class MyFrameHelp
###########################################################################

class MyFrameHelp ( wx.Frame ):

	def __init__( self, parent, translator ):
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = "Help", pos = wx.DefaultPosition, size = wx.Size( 1024,512 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )
		self.build(translator)

	def __del__( self ):
		pass


	def build(self, translation):
		_ = translation.t
		
		self.SetTitle(_("Help"))

		self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )
		self.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOW ) )

		bSizer43 = wx.BoxSizer( wx.VERTICAL )

		self.m_scrolledWindow_bg = wx.ScrolledWindow( self, wx.ID_ANY, wx.DefaultPosition, wx.Size( -1,-1 ), wx.HSCROLL|wx.VSCROLL )
		self.m_scrolledWindow_bg.SetScrollRate( 5, 5 )
		bSizer43.Add( self.m_scrolledWindow_bg, 1, wx.EXPAND |wx.ALL, 5 )

		self.m_staticline36 = wx.StaticLine( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		bSizer43.Add( self.m_staticline36, 0, wx.EXPAND |wx.ALL, 5 )

		bSizer45 = wx.BoxSizer( wx.HORIZONTAL )

		self.m_bpButton9 = wx.BitmapButton( self, wx.ID_ANY, wx.NullBitmap, wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW|0 )

		self.m_bpButton9.SetBitmap( wx.ArtProvider.GetBitmap( wx.ART_UNDO, wx.ART_TOOLBAR ) )
		bSizer45.Add( self.m_bpButton9, 0, wx.ALL, 5 )

		self.m_bpButton8 = wx.BitmapButton( self, wx.ID_ANY, wx.NullBitmap, wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW|0 )

		self.m_bpButton8.SetBitmap( wx.ArtProvider.GetBitmap( wx.ART_REDO, wx.ART_TOOLBAR ) )
		bSizer45.Add( self.m_bpButton8, 0, wx.ALL, 5 )

		self.m_staticline37 = wx.StaticLine( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL|wx.LI_VERTICAL )
		bSizer45.Add( self.m_staticline37, 0, wx.EXPAND |wx.ALL, 5 )

		self.m_bpButton11 = wx.BitmapButton( self, wx.ID_ANY, wx.NullBitmap, wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW|0 )

		self.m_bpButton11.SetBitmap( wx.ArtProvider.GetBitmap( wx.ART_GO_BACK, wx.ART_TOOLBAR ) )
		bSizer45.Add( self.m_bpButton11, 0, wx.ALL, 5 )

		self.m_bpButton12 = wx.BitmapButton( self, wx.ID_ANY, wx.NullBitmap, wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW|0 )

		self.m_bpButton12.SetBitmap( wx.ArtProvider.GetBitmap( wx.ART_GO_FORWARD, wx.ART_TOOLBAR ) )
		bSizer45.Add( self.m_bpButton12, 0, wx.ALL, 5 )

		self.m_staticline39 = wx.StaticLine( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL|wx.LI_VERTICAL )
		bSizer45.Add( self.m_staticline39, 0, wx.EXPAND |wx.ALL, 5 )

		self.m_button14 = wx.Button( self, wx.ID_ANY, _("Refresh"), wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer45.Add( self.m_button14, 0, wx.ALL, 5 )

		self.m_bpButton10 = wx.BitmapButton( self, wx.ID_ANY, wx.NullBitmap, wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW|0 )

		self.m_bpButton10.SetBitmap( wx.ArtProvider.GetBitmap( wx.ART_CLOSE, wx.ART_TOOLBAR ) )
		bSizer45.Add( self.m_bpButton10, 0, wx.ALL, 5 )

		self.m_staticline38 = wx.StaticLine( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL|wx.LI_VERTICAL )
		bSizer45.Add( self.m_staticline38, 0, wx.EXPAND |wx.ALL, 5 )

		self.m_staticText21 = wx.StaticText( self, wx.ID_ANY, _("URL:"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText21.Wrap( -1 )

		bSizer45.Add( self.m_staticText21, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.m_textCtrl8 = wx.TextCtrl( self, wx.ID_ANY, _("https://github.com/azurlane-doujin/AzurLanePaintingExtract-v1.0/blob/version1.4/HELP.md"), wx.DefaultPosition, wx.DefaultSize, wx.TE_PROCESS_ENTER|wx.TE_READONLY )
		bSizer45.Add( self.m_textCtrl8, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.m_hyperlink1 = wx.adv.HyperlinkCtrl( self, wx.ID_ANY, _("Open in browser"), _("https://github.com/azurlane-doujin/AzurLanePaintingExtract-v1.0/blob/version1.4/HELP.md"), wx.DefaultPosition, wx.DefaultSize, wx.adv.HL_DEFAULT_STYLE )
		bSizer45.Add( self.m_hyperlink1, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )


		bSizer43.Add( bSizer45, 0, wx.EXPAND, 5 )


		self.SetSizer( bSizer43 )
		self.Layout()
		self.m_statusBar2 = self.CreateStatusBar( 1, wx.STB_SIZEGRIP, wx.ID_ANY )

		self.Centre( wx.BOTH )

		# Connect Events
		self.m_bpButton9.Bind( wx.EVT_BUTTON, self.undo_page )
		self.m_bpButton8.Bind( wx.EVT_BUTTON, self.redo_page )
		self.m_bpButton11.Bind( wx.EVT_BUTTON, self.go_back )
		self.m_bpButton12.Bind( wx.EVT_BUTTON, self.go_forword )
		self.m_button14.Bind( wx.EVT_BUTTON, self.reload )
		self.m_bpButton10.Bind( wx.EVT_BUTTON, self.stop )
		self.m_textCtrl8.Bind( wx.EVT_TEXT_ENTER, self.use_target_url )

	# Virtual event handlers, overide them in your derived class
	def undo_page( self, event ):
		event.Skip()

	def redo_page( self, event ):
		event.Skip()

	def go_back( self, event ):
		event.Skip()

	def go_forword( self, event ):
		event.Skip()

	def reload( self, event ):
		event.Skip()

	def stop( self, event ):
		event.Skip()

	def use_target_url( self, event ):
		event.Skip()


###########################################################################
## Class MyDialogAtlasSpilt
###########################################################################

class MyDialogAtlasSpilt ( wx.Dialog ):

	def __init__( self, parent, translator ):
		wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = "Atlas Slicer", pos = wx.DefaultPosition, size = wx.Size( 512,256 ), style = wx.DEFAULT_DIALOG_STYLE )
		self.build(translator)

	def __del__( self ):
		pass

	def build(self, translation):
		_ = translation.t
		
		self.SetTitle(_("Atlas Slicer"))
		
		self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )

		bSizer30 = wx.BoxSizer( wx.VERTICAL )

		bSizer31 = wx.BoxSizer( wx.VERTICAL )

		bSizer32 = wx.BoxSizer( wx.HORIZONTAL )

		self.m_panel8 = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer33 = wx.BoxSizer( wx.VERTICAL )

		self.m_staticText_target_name = wx.StaticText( self.m_panel8, wx.ID_ANY, _("Target:"), wx.DefaultPosition, wx.DefaultSize, wx.ST_ELLIPSIZE_END )
		self.m_staticText_target_name.Wrap( -1 )

		bSizer33.Add( self.m_staticText_target_name, 0, wx.ALL|wx.EXPAND, 5 )

		self.m_filePicker_target_atlas = wx.FilePickerCtrl( self.m_panel8, wx.ID_ANY, wx.EmptyString, _("Select Atlas File"), _("Atlas Data File (*.atlas;*.atlas.txt)|*.atlas;*.atlas.txt"), wx.DefaultPosition, wx.DefaultSize, wx.FLP_CHANGE_DIR|wx.FLP_DEFAULT_STYLE|wx.FLP_FILE_MUST_EXIST|wx.FLP_OPEN|wx.FLP_SMALL|wx.FLP_USE_TEXTCTRL )
		bSizer33.Add( self.m_filePicker_target_atlas, 0, wx.ALL|wx.EXPAND, 5 )

		m_listBox_spilt_itemsChoices = []
		self.m_listBox_spilt_items = wx.ListBox( self.m_panel8, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, m_listBox_spilt_itemsChoices, 0 )
		bSizer33.Add( self.m_listBox_spilt_items, 1, wx.ALL|wx.EXPAND, 5 )


		self.m_panel8.SetSizer( bSizer33 )
		self.m_panel8.Layout()
		bSizer33.Fit( self.m_panel8 )
		bSizer32.Add( self.m_panel8, 1, wx.EXPAND |wx.ALL, 5 )

		self.m_staticline27 = wx.StaticLine( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL|wx.LI_VERTICAL )
		bSizer32.Add( self.m_staticline27, 0, wx.EXPAND |wx.ALL, 5 )

		self.m_bitmap_show = wx.StaticBitmap( self, wx.ID_ANY, wx.NullBitmap, wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer32.Add( self.m_bitmap_show, 1, wx.ALL|wx.EXPAND, 5 )


		bSizer31.Add( bSizer32, 1, wx.EXPAND, 5 )

		self.m_staticline28 = wx.StaticLine( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		bSizer31.Add( self.m_staticline28, 0, wx.EXPAND |wx.ALL, 5 )

		bSizer34 = wx.BoxSizer( wx.HORIZONTAL )

		m_sdbSizer2 = wx.StdDialogButtonSizer()
		self.m_sdbSizer2Save = wx.Button( self, wx.ID_SAVE )
		m_sdbSizer2.AddButton( self.m_sdbSizer2Save )
		self.m_sdbSizer2Cancel = wx.Button( self, wx.ID_CANCEL )
		m_sdbSizer2.AddButton( self.m_sdbSizer2Cancel )
		m_sdbSizer2.Realize();

		bSizer34.Add( m_sdbSizer2, 0, 0, 5 )

		self.m_staticline29 = wx.StaticLine( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL|wx.LI_VERTICAL )
		bSizer34.Add( self.m_staticline29, 0, wx.EXPAND |wx.ALL, 5 )

		self.m_staticText_info = wx.StaticText( self, wx.ID_ANY, _("Ready..."), wx.DefaultPosition, wx.DefaultSize, wx.ST_ELLIPSIZE_END )
		self.m_staticText_info.Wrap( -1 )

		bSizer34.Add( self.m_staticText_info, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )


		bSizer31.Add( bSizer34, 0, wx.EXPAND, 5 )


		bSizer30.Add( bSizer31, 1, wx.EXPAND, 5 )


		self.SetSizer( bSizer30 )
		self.Layout()

		self.Centre( wx.BOTH )

		# Connect Events
		self.m_filePicker_target_atlas.Bind( wx.EVT_FILEPICKER_CHANGED, self.load_atlas )
		self.m_listBox_spilt_items.Bind( wx.EVT_LISTBOX, self.view_item )
		self.m_listBox_spilt_items.Bind( wx.EVT_LISTBOX_DCLICK, self.save_item )
		self.m_sdbSizer2Cancel.Bind( wx.EVT_BUTTON, self.exit )
		self.m_sdbSizer2Save.Bind( wx.EVT_BUTTON, self.save_all )



	# Virtual event handlers, overide them in your derived class
	def load_atlas( self, event ):
		event.Skip()

	def view_item( self, event ):
		event.Skip()

	def save_item( self, event ):
		event.Skip()

	def exit( self, event ):
		event.Skip()

	def save_all( self, event ):
		event.Skip()


###########################################################################
## Class MyDialogSetting
###########################################################################

class SettingWindow ( wx.Dialog ):

	def __init__( self, parent, translator ):
		wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = "Settings", pos = wx.DefaultPosition, size = wx.Size( 638,481 ), style = wx.DEFAULT_DIALOG_STYLE )
		self.build(translator)

	def __del__( self ):
		pass
	
	
	def build(self, translation):
		_ = translation.t
		
		self.SetTitle(_("Settings"))
		
		self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )

		bSizer8 = wx.BoxSizer( wx.VERTICAL )

		bSizer9 = wx.BoxSizer( wx.HORIZONTAL )

		self.m_panel10 = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer10 = wx.BoxSizer( wx.VERTICAL )

		self.m_staticText99 = wx.StaticText( self.m_panel10, wx.ID_ANY, _("Language:"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText99.Wrap( -1 )
		bSizer10.Add( self.m_staticText99, 0, wx.ALL, 5 )

		m_choice_locale_options = "en-US (English)|zh-CN (中国人)".split("|")
		self.m_choice_locale = wx.Choice( self.m_panel10, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, m_choice_locale_options, 0 )
		self.m_choice_locale.SetSelection( 0 )
		bSizer10.Add( self.m_choice_locale, 0, wx.ALL|wx.EXPAND, 5 )

		bSizer11 = wx.BoxSizer( wx.HORIZONTAL )
		self.m_checkBox_auto_name_update = wx.CheckBox( self.m_panel10, wx.ID_ANY, _("Automatically check for ship name updates on startup"), wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer11.Add( self.m_checkBox_auto_name_update, 0, wx.ALL, 5 )

		self.m_button_manual_update = wx.Button( self.m_panel10, wx.ID_ANY, _("Update ship names"), wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer11.Add( self.m_button_manual_update, 0, wx.ALL, 5 )
		bSizer10.Add( bSizer11 )

		self.m_staticline99 = wx.StaticLine( self.m_panel10, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		bSizer10.Add( self.m_staticline99, 0, wx.EXPAND |wx.ALL, 5 )

		self.m_checkBox_ex_cn = wx.CheckBox( self.m_panel10, wx.ID_ANY, _("Use localized ship names on export"), wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer10.Add( self.m_checkBox_ex_cn, 0, wx.ALL, 5 )

		self.m_checkBox_new_dir = wx.CheckBox( self.m_panel10, wx.ID_ANY, _("Create new folder on export in export directory"), wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer10.Add( self.m_checkBox_new_dir, 0, wx.ALL, 5 )

		self.m_staticline8 = wx.StaticLine( self.m_panel10, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		bSizer10.Add( self.m_staticline8, 0, wx.EXPAND |wx.ALL, 5 )

		self.m_checkBox_open_dir = wx.CheckBox( self.m_panel10, wx.ID_ANY, _("Open export folder upon completion"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_checkBox_open_dir.SetValue(True)
		bSizer10.Add( self.m_checkBox_open_dir, 0, wx.ALL, 5 )

		self.m_checkBox_skip_exist = wx.CheckBox( self.m_panel10, wx.ID_ANY, _("Do not overwrite files on export"), wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer10.Add( self.m_checkBox_skip_exist, 0, wx.ALL, 5 )

		self.m_checkBox_clear_list = wx.CheckBox( self.m_panel10, wx.ID_ANY, _("Clear the original list when importing"), wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer10.Add( self.m_checkBox_clear_list, 0, wx.ALL, 5 )

		self.m_checkBox_finish_exit = wx.CheckBox( self.m_panel10, wx.ID_ANY, _("Exit after export"), wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer10.Add( self.m_checkBox_finish_exit, 0, wx.ALL, 5 )

		self.m_checkBox_ex_copy = wx.CheckBox( self.m_panel10, wx.ID_ANY, _("When exporting all, copy at the same time and cannot be restored."), wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer10.Add( self.m_checkBox_ex_copy, 0, wx.ALL, 5 )

		self.m_checkBox_ignore_case = wx.CheckBox( self.m_panel10, wx.ID_ANY, _("Case insensitive localization"), wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer10.Add( self.m_checkBox_ignore_case, 0, wx.ALL, 5 )

		"""self.m_staticline10 = wx.StaticLine( self.m_panel10, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		bSizer10.Add( self.m_staticline10, 0, wx.EXPAND |wx.ALL, 5 )

		self.m_staticText13 = wx.StaticText( self.m_panel10, wx.ID_ANY, _("Filter imports"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText13.Wrap( -1 )
		bSizer10.Add( self.m_staticText13, 0, wx.ALL, 5 )

		m_choice_inport_filterChoices = _("All|Base|Skins|Retrofit|Promise|Young|MUSE μ|Other").split("|")
		self.m_choice_inport_filter = wx.Choice( self.m_panel10, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, m_choice_inport_filterChoices, 0 )
		self.m_choice_inport_filter.SetSelection( 6 )
		bSizer10.Add( self.m_choice_inport_filter, 0, wx.ALL|wx.EXPAND, 5 )

		self.m_staticline9 = wx.StaticLine( self.m_panel10, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		bSizer10.Add( self.m_staticline9, 0, wx.EXPAND |wx.ALL, 5 )

		self.m_staticText14 = wx.StaticText( self.m_panel10, wx.ID_ANY, _("Export file organization"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText14.Wrap( -1 )
		bSizer10.Add( self.m_staticText14, 0, wx.ALL, 5 )

		m_choice_export_divisionChoices = _("None|By name|By type").split("|")
		self.m_choice_export_division = wx.Choice( self.m_panel10, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, m_choice_export_divisionChoices, 0 )
		self.m_choice_export_division.SetSelection( 0 )
		bSizer10.Add( self.m_choice_export_division, 0, wx.ALL|wx.EXPAND, 5 )"""

		self.m_staticline27 = wx.StaticLine( self.m_panel10, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		bSizer10.Add( self.m_staticline27, 0, wx.EXPAND |wx.ALL, 5 )


		self.m_panel10.SetSizer( bSizer10 )
		self.m_panel10.Layout()
		bSizer10.Fit( self.m_panel10 )
		bSizer9.Add( self.m_panel10, 1, wx.EXPAND |wx.ALL, 5 )

		self.m_staticline41 = wx.StaticLine( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL|wx.LI_VERTICAL )
		bSizer9.Add( self.m_staticline41, 0, wx.EXPAND |wx.ALL, 5 )

		self.m_panel9 = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		self.m_panel9.SetMinSize( wx.Size( 256,-1 ) )
		self.m_panel9.SetMaxSize( wx.Size( 400,-1 ) )

		bSizer46 = wx.BoxSizer( wx.VERTICAL )

		"""bSizer48 = wx.BoxSizer( wx.HORIZONTAL )

		self.m_button_guider = wx.Button( self.m_panel9, wx.ID_ANY, _("Help"), wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer48.Add( self.m_button_guider, 0, wx.ALL, 5 )

		self.m_button_lever_up_setting = wx.Button( self.m_panel9, wx.ID_ANY, _("Advanced..."), wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer48.Add( self.m_button_lever_up_setting, 0, wx.ALL|wx.ALIGN_RIGHT, 5 )


		bSizer46.Add( bSizer48, 0, wx.ALIGN_RIGHT, 5 )"""

		self.m_staticline43 = wx.StaticLine( self.m_panel9, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		bSizer46.Add( self.m_staticline43, 0, wx.EXPAND |wx.ALL, 5 )

		self.m_bitmap2 = wx.StaticBitmap( self.m_panel9, wx.ID_ANY, wx.NullBitmap, wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer46.Add( self.m_bitmap2, 1, wx.ALL|wx.EXPAND, 5 )


		self.m_panel9.SetSizer( bSizer46 )
		self.m_panel9.Layout()
		bSizer46.Fit( self.m_panel9 )
		bSizer9.Add( self.m_panel9, 1, wx.ALL|wx.EXPAND, 5 )


		bSizer8.Add( bSizer9, 1, wx.EXPAND, 5 )

		self.m_staticline7 = wx.StaticLine( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		bSizer8.Add( self.m_staticline7, 0, wx.EXPAND |wx.ALL, 5 )

		m_sdbSizer1 = wx.StdDialogButtonSizer()
		self.m_sdbSizer1OK = wx.Button( self, wx.ID_OK )
		m_sdbSizer1.AddButton( self.m_sdbSizer1OK )
		self.m_sdbSizer1Apply = wx.Button( self, wx.ID_APPLY )
		m_sdbSizer1.AddButton( self.m_sdbSizer1Apply )
		self.m_sdbSizer1Cancel = wx.Button( self, wx.ID_CANCEL )
		m_sdbSizer1.AddButton( self.m_sdbSizer1Cancel )
		m_sdbSizer1.Realize();

		bSizer8.Add( m_sdbSizer1, 0, wx.ALIGN_RIGHT, 5 )


		self.SetSizer( bSizer8 )
		self.Layout()

		self.Centre( wx.BOTH )

		# Connect Events
		self.Bind( wx.EVT_INIT_DIALOG, self.set_info )
		self.m_choice_locale.Bind( wx.EVT_CHOICE, self.locale )
		self.m_button_manual_update.Bind( wx.EVT_BUTTON, self.manual_name_update )
		#self.m_choice_inport_filter.Bind( wx.EVT_CHOICE, self.import_filter )
		#self.m_choice_export_division.Bind( wx.EVT_CHOICE, self.output_group )
		#self.m_button_guider.Bind( wx.EVT_BUTTON, self.guider )
		#self.m_button_lever_up_setting.Bind( wx.EVT_BUTTON, self.height_setting_dialog )
		self.m_sdbSizer1Apply.Bind( wx.EVT_BUTTON, self.apply_press )
		self.m_sdbSizer1Cancel.Bind( wx.EVT_BUTTON, self.cancel_press )
		self.m_sdbSizer1OK.Bind( wx.EVT_BUTTON, self.ok_press )

	
	def rebuild(self, translation):
		_ = translation.t
		
		self.SetTitle(_("Settings"))

		self.m_staticText99.SetLabelText(_("Language:"))
		
		m_choice_locale_options = "en-US (English)|zh-CN (中国人)".split("|")
		for i in range(len(m_choice_locale_options)):
			self.m_choice_locale.SetString(i, m_choice_locale_options[i])
		
		self.m_checkBox_auto_name_update.SetLabelText(_("Automatically check for ship name updates on startup"))

		self.m_button_manual_update.SetLabelText(_("Update ship names"))

		self.m_checkBox_ex_cn.SetLabelText(_("Use localized ship names on export"))
		
		self.m_checkBox_new_dir.SetLabelText(_("Create new folder on export in export directory"))

		self.m_checkBox_open_dir.SetLabelText(_("Open export folder upon completion"))
		
		self.m_checkBox_skip_exist.SetLabelText(_("Do not overwrite files on export"))
		
		self.m_checkBox_clear_list.SetLabelText(_("Clear the original list when importing"))
		
		self.m_checkBox_finish_exit.SetLabelText(_("Exit after export"))
		
		self.m_checkBox_ex_copy.SetLabelText(_("When exporting all, copy at the same time and cannot be restored."))
		
		self.m_checkBox_ignore_case.SetLabelText(_("Case insensitive localization"))
		
		# self.m_button_guider.SetLabelText(_("Help"))
		
		# self.m_button_lever_up_setting.SetLabelText(_("Advanced..."))
		

	# Virtual event handlers, overide them in your derived class
	def set_info( self, event ):
		event.Skip()

	def locale( self, event ):
		event.Skip()

	def manual_name_update( self, event ):
		event.Skip()

	#def import_filter( self, event ):
	#	event.Skip()

	#def output_group( self, event ):
	#	event.Skip()

	def guider( self, event ):
		event.Skip()

	def height_setting_dialog( self, event ):
		event.Skip()

	def apply_press( self, event ):
		event.Skip()

	def cancel_press( self, event ):
		event.Skip()

	def ok_press( self, event ):
		event.Skip()


###########################################################################
## Class MyDialogKetValueSetting
###########################################################################

class MyDialogKetValueSetting ( wx.Dialog ):

	def __init__( self, parent, translation ):
		wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = "Edit Localization Values", pos = wx.DefaultPosition, size = wx.Size( 256,512 ), style = wx.DEFAULT_DIALOG_STYLE )
		self.build(translation)

	def __del__( self ):
		pass

	def build(self, translation):
		_ = translation.t
		
		self.SetTitle(_("Edit Localization Values"))
		
		self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )

		bSizer13 = wx.BoxSizer( wx.VERTICAL )

		bSizer14 = wx.BoxSizer( wx.VERTICAL )

		m_listBox_name_existChoices = []
		self.m_listBox_name_exist = wx.ListBox( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, m_listBox_name_existChoices, wx.LB_ALWAYS_SB|wx.LB_HSCROLL|wx.LB_SINGLE )
		bSizer14.Add( self.m_listBox_name_exist, 1, wx.ALL|wx.EXPAND, 5 )


		bSizer13.Add( bSizer14, 1, wx.EXPAND, 5 )

		self.m_staticline13 = wx.StaticLine( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_VERTICAL )
		bSizer13.Add( self.m_staticline13, 0, wx.EXPAND |wx.ALL, 5 )

		bSizer15 = wx.BoxSizer( wx.VERTICAL )

		self.m_staticText3 = wx.StaticText( self, wx.ID_ANY, _("Key"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText3.Wrap( -1 )

		bSizer15.Add( self.m_staticText3, 1, wx.ALL|wx.EXPAND, 5 )

		self.m_textCtrl_new_key = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer15.Add( self.m_textCtrl_new_key, 0, wx.ALL|wx.EXPAND, 5 )

		self.m_staticText4 = wx.StaticText( self, wx.ID_ANY, _("Value"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText4.Wrap( -1 )

		bSizer15.Add( self.m_staticText4, 1, wx.ALL|wx.EXPAND|wx.ALIGN_CENTER_HORIZONTAL, 5 )

		self.m_textCtrl_new_value = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer15.Add( self.m_textCtrl_new_value, 0, wx.ALL|wx.EXPAND, 5 )

		self.m_button20 = wx.Button( self, wx.ID_ANY, _("Save to file"), wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer15.Add( self.m_button20, 0, wx.ALL, 5 )

		self.m_staticline16 = wx.StaticLine( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		bSizer15.Add( self.m_staticline16, 0, wx.EXPAND |wx.ALL, 5 )

		bSizer16 = wx.BoxSizer( wx.HORIZONTAL )

		self.m_bpButton_import_names = wx.BitmapButton( self, wx.ID_ANY, wx.NullBitmap, wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW|0 )

		self.m_bpButton_import_names.SetBitmap( wx.ArtProvider.GetBitmap( wx.ART_PLUS, wx.ART_BUTTON ) )
		bSizer16.Add( self.m_bpButton_import_names, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.m_staticline17 = wx.StaticLine( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL|wx.LI_VERTICAL )
		bSizer16.Add( self.m_staticline17, 0, wx.EXPAND |wx.ALL, 5 )

		self.m_button_clear = wx.Button( self, wx.ID_ANY, _("Overwrite on import"), wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer16.Add( self.m_button_clear, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.m_button_add = wx.Button( self, wx.ID_ANY, _("Add to"), wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer16.Add( self.m_button_add, 0, wx.ALL, 5 )


		bSizer15.Add( bSizer16, 0, wx.EXPAND|wx.ALIGN_RIGHT, 5 )


		bSizer13.Add( bSizer15, 0, wx.EXPAND, 5 )


		self.SetSizer( bSizer13 )
		self.Layout()

		self.Centre( wx.BOTH )

		# Connect Events
		self.Bind( wx.EVT_CLOSE, self.close_save )
		self.Bind( wx.EVT_INIT_DIALOG, self.editor_init )
		self.m_listBox_name_exist.Bind( wx.EVT_LISTBOX, self.edit_exist_item )
		self.m_listBox_name_exist.Bind( wx.EVT_LISTBOX_DCLICK, self.view_item )
		self.m_button20.Bind( wx.EVT_BUTTON, self.next_miss )
		self.m_bpButton_import_names.Bind( wx.EVT_BUTTON, self.import_names )
		self.m_button_clear.Bind( wx.EVT_BUTTON, self.clear_item )
		self.m_button_add.Bind( wx.EVT_BUTTON, self.add_item )

		

	# Virtual event handlers, overide them in your derived class
	def close_save( self, event ):
		event.Skip()

	def editor_init( self, event ):
		event.Skip()

	def edit_exist_item( self, event ):
		event.Skip()

	def view_item( self, event ):
		event.Skip()

	def next_miss( self, event ):
		event.Skip()

	def import_names( self, event ):
		event.Skip()

	def clear_item( self, event ):
		event.Skip()

	def add_item( self, event ):
		event.Skip()


###########################################################################
## Class MyDialogHeightSetting
###########################################################################

class MyDialogHeightSetting ( wx.Dialog ):

	def __init__( self, parent, translation ):
		wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = "Advanced Settings", pos = wx.DefaultPosition, size = wx.Size( 256,512 ), style = wx.DEFAULT_DIALOG_STYLE )
		self.build(translation)

	def __del__( self ):
		pass


	def build(self, translation):
		_ = translation.t
		
		self.SetTitle(_("Advanced Settings"))
		
		self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )

		bSizer45 = wx.BoxSizer( wx.VERTICAL )

		sbSizer1 = wx.StaticBoxSizer( wx.StaticBox( self, wx.ID_ANY, _("Mesh file pairing priority") ), wx.VERTICAL )

		self.m_staticText26 = wx.StaticText( sbSizer1.GetStaticBox(), wx.ID_ANY, _("First priority"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText26.Wrap( -1 )

		sbSizer1.Add( self.m_staticText26, 0, wx.ALL, 5 )

		self.m_textCtrl_mesh_first = wx.TextCtrl( sbSizer1.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		sbSizer1.Add( self.m_textCtrl_mesh_first, 0, wx.ALL|wx.EXPAND, 5 )

		self.m_staticText27 = wx.StaticText( sbSizer1.GetStaticBox(), wx.ID_ANY, _("Second priority"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText27.Wrap( -1 )

		sbSizer1.Add( self.m_staticText27, 0, wx.ALL, 5 )

		self.m_textCtrl_mesh_second = wx.TextCtrl( sbSizer1.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		sbSizer1.Add( self.m_textCtrl_mesh_second, 0, wx.ALL|wx.EXPAND, 5 )


		bSizer45.Add( sbSizer1, 1, wx.EXPAND, 5 )

		sbSizer2 = wx.StaticBoxSizer( wx.StaticBox( self, wx.ID_ANY, _("Texture2D pairing priority") ), wx.VERTICAL )

		self.m_staticText28 = wx.StaticText( sbSizer2.GetStaticBox(), wx.ID_ANY, _("first priority"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText28.Wrap( -1 )

		sbSizer2.Add( self.m_staticText28, 0, wx.ALL, 5 )

		self.m_textCtrl_tex_first = wx.TextCtrl( sbSizer2.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		sbSizer2.Add( self.m_textCtrl_tex_first, 0, wx.ALL|wx.EXPAND, 5 )

		self.m_staticText29 = wx.StaticText( sbSizer2.GetStaticBox(), wx.ID_ANY, _("second priority"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText29.Wrap( -1 )

		sbSizer2.Add( self.m_staticText29, 0, wx.ALL, 5 )

		self.m_textCtrl_tex_second = wx.TextCtrl( sbSizer2.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		sbSizer2.Add( self.m_textCtrl_tex_second, 0, wx.ALL|wx.EXPAND, 5 )


		bSizer45.Add( sbSizer2, 1, wx.EXPAND, 5 )

		sbSizer3 = wx.StaticBoxSizer( wx.StaticBox( self, wx.ID_ANY, _("localization editor") ), wx.VERTICAL )

		bSizer12 = wx.BoxSizer( wx.HORIZONTAL )

		self.m_button_updata_names = wx.Button( sbSizer3.GetStaticBox(), wx.ID_ANY, _("Update localized resources"), wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer12.Add( self.m_button_updata_names, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.m_staticline12 = wx.StaticLine( sbSizer3.GetStaticBox(), wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_VERTICAL )
		bSizer12.Add( self.m_staticline12, 0, wx.EXPAND |wx.ALL, 5 )

		self.m_button_edit_names = wx.Button( sbSizer3.GetStaticBox(), wx.ID_ANY, _("Edit localized resources"), wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer12.Add( self.m_button_edit_names, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )


		sbSizer3.Add( bSizer12, 0, wx.EXPAND, 5 )


		bSizer45.Add( sbSizer3, 0, wx.EXPAND, 5 )

		self.m_staticline41 = wx.StaticLine( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		bSizer45.Add( self.m_staticline41, 0, wx.EXPAND |wx.ALL, 5 )

		self.m_hyperlink3 = wx.adv.HyperlinkCtrl( self, wx.ID_ANY, _("Bigfun Tutorial"), wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.adv.HL_DEFAULT_STYLE )
		bSizer45.Add( self.m_hyperlink3, 0, wx.ALL|wx.ALIGN_RIGHT, 5 )

		self.m_staticline42 = wx.StaticLine( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		bSizer45.Add( self.m_staticline42, 0, wx.EXPAND |wx.ALL, 5 )

		m_sdbSizer4 = wx.StdDialogButtonSizer()
		self.m_sdbSizer4OK = wx.Button( self, wx.ID_OK )
		m_sdbSizer4.AddButton( self.m_sdbSizer4OK )
		self.m_sdbSizer4Cancel = wx.Button( self, wx.ID_CANCEL )
		m_sdbSizer4.AddButton( self.m_sdbSizer4Cancel )
		m_sdbSizer4.Realize();

		bSizer45.Add( m_sdbSizer4, 0, wx.EXPAND, 5 )


		self.SetSizer( bSizer45 )
		self.Layout()

		self.Centre( wx.BOTH )

		# Connect Events
		self.Bind( wx.EVT_INIT_DIALOG, self.prepare_data )
		self.m_button_updata_names.Bind( wx.EVT_BUTTON, self.update_names )
		self.m_button_edit_names.Bind( wx.EVT_BUTTON, self.edit_names )
		self.m_sdbSizer4Cancel.Bind( wx.EVT_BUTTON, self.cancel_click )
		self.m_sdbSizer4OK.Bind( wx.EVT_BUTTON, self.ok_click )

		

	# Virtual event handlers, overide them in your derived class
	def prepare_data( self, event ):
		event.Skip()

	def update_names( self, event ):
		event.Skip()

	def edit_names( self, event ):
		event.Skip()

	def cancel_click( self, event ):
		event.Skip()

	def ok_click( self, event ):
		event.Skip()


###########################################################################
## Class MyDialogAddFace
###########################################################################

class MyDialogAddFace ( wx.Dialog ):

	def __init__( self, parent, translation ):
		wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = "Expression Editor", pos = wx.DefaultPosition, size = wx.Size( 680,470 ), style = wx.DEFAULT_DIALOG_STYLE )
		self.buld(translation)

	def __del__( self ):
		pass

	def build(self, translation):
		_ = translation.t
		
		self.SetTitle(_("Expression Editor"))
		
		self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )

		bSizer17 = wx.BoxSizer( wx.VERTICAL )

		bSizer26 = wx.BoxSizer( wx.HORIZONTAL )

		self.m_scrolledWindow2 = wx.ScrolledWindow( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.HSCROLL|wx.VSCROLL )
		self.m_scrolledWindow2.SetScrollRate( 5, 5 )
		bSizer19 = wx.BoxSizer( wx.VERTICAL )

		self.m_bitmap_main_view = wx.StaticBitmap( self.m_scrolledWindow2, wx.ID_ANY, wx.NullBitmap, wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer19.Add( self.m_bitmap_main_view, 1, wx.ALL|wx.EXPAND, 5 )


		self.m_scrolledWindow2.SetSizer( bSizer19 )
		self.m_scrolledWindow2.Layout()
		bSizer19.Fit( self.m_scrolledWindow2 )
		bSizer26.Add( self.m_scrolledWindow2, 1, wx.EXPAND |wx.ALL, 5 )

		self.m_staticline16 = wx.StaticLine( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_VERTICAL )
		bSizer26.Add( self.m_staticline16, 0, wx.EXPAND |wx.ALL, 5 )

		self.m_panel6 = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		self.m_panel6.SetMinSize( wx.Size( 256,-1 ) )
		self.m_panel6.SetMaxSize( wx.Size( 192,-1 ) )

		bSizer20 = wx.BoxSizer( wx.VERTICAL )

		self.m_notebook_info = wx.Notebook( self.m_panel6, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.NB_BOTTOM )
		self.m_panel7 = wx.Panel( self.m_notebook_info, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer22 = wx.BoxSizer( wx.VERTICAL )

		self.m_staticText4 = wx.StaticText( self.m_panel7, wx.ID_ANY, _("X-Offset"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText4.Wrap( -1 )

		bSizer22.Add( self.m_staticText4, 0, wx.ALL, 5 )

		self.m_textCtrl_x_value = wx.TextCtrl( self.m_panel7, wx.ID_ANY, "0", wx.DefaultPosition, wx.DefaultSize, wx.TE_PROCESS_ENTER )
		bSizer22.Add( self.m_textCtrl_x_value, 0, wx.ALL|wx.EXPAND, 5 )

		self.m_staticText5 = wx.StaticText( self.m_panel7, wx.ID_ANY, _("Y-Offset"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText5.Wrap( -1 )

		bSizer22.Add( self.m_staticText5, 0, wx.ALL, 5 )

		self.m_textCtrl_y_value = wx.TextCtrl( self.m_panel7, wx.ID_ANY, "0", wx.DefaultPosition, wx.DefaultSize, wx.TE_PROCESS_ENTER )
		bSizer22.Add( self.m_textCtrl_y_value, 0, wx.ALL|wx.EXPAND, 5 )


		self.m_panel7.SetSizer( bSizer22 )
		self.m_panel7.Layout()
		bSizer22.Fit( self.m_panel7 )
		self.m_notebook_info.AddPage( self.m_panel7, _("Offset"), False )
		self.m_panel14 = wx.Panel( self.m_notebook_info, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer30 = wx.BoxSizer( wx.VERTICAL )

		self.m_staticText8 = wx.StaticText( self.m_panel14, wx.ID_ANY, _("X-Offset"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText8.Wrap( -1 )

		bSizer30.Add( self.m_staticText8, 0, wx.ALL, 5 )

		self.m_textCtrl_pic_x = wx.TextCtrl( self.m_panel14, wx.ID_ANY, "0", wx.DefaultPosition, wx.DefaultSize, wx.TE_PROCESS_ENTER )
		bSizer30.Add( self.m_textCtrl_pic_x, 0, wx.ALL|wx.EXPAND, 5 )

		self.m_staticText9 = wx.StaticText( self.m_panel14, wx.ID_ANY, _("Y-Offset"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText9.Wrap( -1 )

		bSizer30.Add( self.m_staticText9, 0, wx.ALL, 5 )

		self.m_textCtrl_pic_y = wx.TextCtrl( self.m_panel14, wx.ID_ANY, "0", wx.DefaultPosition, wx.DefaultSize, wx.TE_PROCESS_ENTER )
		bSizer30.Add( self.m_textCtrl_pic_y, 0, wx.ALL|wx.EXPAND, 5 )


		self.m_panel14.SetSizer( bSizer30 )
		self.m_panel14.Layout()
		bSizer30.Fit( self.m_panel14 )
		self.m_notebook_info.AddPage( self.m_panel14, _("View"), True )
		self.m_panel_face = wx.Panel( self.m_notebook_info, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer23 = wx.BoxSizer( wx.VERTICAL )

		self.m_bitmap_face = wx.StaticBitmap( self.m_panel_face, wx.ID_ANY, wx.NullBitmap, wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer23.Add( self.m_bitmap_face, 1, wx.ALL|wx.EXPAND, 5 )


		self.m_panel_face.SetSizer( bSizer23 )
		self.m_panel_face.Layout()
		bSizer23.Fit( self.m_panel_face )
		self.m_notebook_info.AddPage( self.m_panel_face, _("Preview"), False )

		bSizer20.Add( self.m_notebook_info, 1, wx.EXPAND |wx.ALL, 5 )

		self.m_staticline18 = wx.StaticLine( self.m_panel6, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_VERTICAL )
		bSizer20.Add( self.m_staticline18, 0, wx.EXPAND |wx.ALL, 5 )

		self.m_staticText6 = wx.StaticText( self.m_panel6, wx.ID_ANY, _("Imported facial expressions"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText6.Wrap( -1 )

		bSizer20.Add( self.m_staticText6, 0, wx.ALL, 5 )

		m_listBox_import_faceChoices = []
		self.m_listBox_import_face = wx.ListBox( self.m_panel6, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, m_listBox_import_faceChoices, wx.LB_HSCROLL|wx.LB_NEEDED_SB )
		bSizer20.Add( self.m_listBox_import_face, 1, wx.ALL|wx.EXPAND, 5 )

		self.m_staticline23 = wx.StaticLine( self.m_panel6, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_VERTICAL )
		bSizer20.Add( self.m_staticline23, 0, wx.EXPAND |wx.ALL, 5 )

		self.m_checkBox_alpha = wx.CheckBox( self.m_panel6, wx.ID_ANY, _("Transparent background"), wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_RIGHT )
		bSizer20.Add( self.m_checkBox_alpha, 0, wx.ALL|wx.ALIGN_RIGHT, 5 )

		self.m_checkBox_minosity_size = wx.CheckBox( self.m_panel6, wx.ID_ANY, _("Export at minimum size"), wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_RIGHT )
		bSizer20.Add( self.m_checkBox_minosity_size, 0, wx.ALL|wx.ALIGN_RIGHT, 5 )


		self.m_panel6.SetSizer( bSizer20 )
		self.m_panel6.Layout()
		bSizer20.Fit( self.m_panel6 )
		bSizer26.Add( self.m_panel6, 1, wx.ALL|wx.ALIGN_RIGHT|wx.EXPAND, 5 )


		bSizer17.Add( bSizer26, 1, wx.EXPAND, 5 )

		self.m_staticline19 = wx.StaticLine( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		bSizer17.Add( self.m_staticline19, 0, wx.EXPAND |wx.ALL, 5 )

		bSizer27 = wx.BoxSizer( wx.HORIZONTAL )

		self.m_staticText_info = wx.StaticText( self, wx.ID_ANY, _("NONE"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText_info.Wrap( -1 )

		bSizer27.Add( self.m_staticText_info, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.m_staticline20 = wx.StaticLine( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_VERTICAL )
		bSizer27.Add( self.m_staticline20, 0, wx.EXPAND |wx.ALL, 5 )

		self.m_staticText10 = wx.StaticText( self, wx.ID_ANY, _("Step size:"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText10.Wrap( -1 )

		bSizer27.Add( self.m_staticText10, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		m_choice_stepChoices = [ "1", "25", "100", "250" ]
		self.m_choice_step = wx.Choice( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, m_choice_stepChoices, 0 )
		self.m_choice_step.SetSelection( 0 )
		bSizer27.Add( self.m_choice_step, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.m_staticline21 = wx.StaticLine( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_VERTICAL )
		bSizer27.Add( self.m_staticline21, 0, wx.EXPAND |wx.ALL, 5 )

		self.m_button_export = wx.Button( self, wx.ID_ANY, _("Export"), wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer27.Add( self.m_button_export, 0, wx.ALL|wx.EXPAND, 5 )


		bSizer17.Add( bSizer27, 0, wx.EXPAND, 5 )


		self.SetSizer( bSizer17 )
		self.Layout()

		self.Centre( wx.BOTH )

		# Connect Events
		self.Bind( wx.EVT_INIT_DIALOG, self.initial )
		self.m_bitmap_main_view.Bind( wx.EVT_ERASE_BACKGROUND, self.on_erase )
		self.m_bitmap_main_view.Bind( wx.EVT_LEFT_DCLICK, self.set_face_place )
		self.m_textCtrl_x_value.Bind( wx.EVT_MOUSEWHEEL, self.wheel_x )
		self.m_textCtrl_x_value.Bind( wx.EVT_TEXT, self.value_check_x )
		self.m_textCtrl_x_value.Bind( wx.EVT_TEXT_ENTER, self.x_value )
		self.m_textCtrl_y_value.Bind( wx.EVT_MOUSEWHEEL, self.y_wheel )
		self.m_textCtrl_y_value.Bind( wx.EVT_TEXT, self.value_check_y )
		self.m_textCtrl_y_value.Bind( wx.EVT_TEXT_ENTER, self.y_value )
		self.m_textCtrl_pic_x.Bind( wx.EVT_MOUSEWHEEL, self.px_wheel )
		self.m_textCtrl_pic_x.Bind( wx.EVT_TEXT, self.value_check_px )
		self.m_textCtrl_pic_y.Bind( wx.EVT_MOUSEWHEEL, self.py_wheel )
		self.m_textCtrl_pic_y.Bind( wx.EVT_TEXT, self.value_check_py )
		self.m_listBox_import_face.Bind( wx.EVT_LISTBOX, self.view_face )
		self.m_listBox_import_face.Bind( wx.EVT_LISTBOX_DCLICK, self.select_face )
		self.m_checkBox_alpha.Bind( wx.EVT_CHECKBOX, self.change_method )
		self.m_choice_step.Bind( wx.EVT_CHOICE, self.set_step )
		self.m_button_export.Bind( wx.EVT_BUTTON, self.export )

		

	# Virtual event handlers, overide them in your derived class
	def initial( self, event ):
		event.Skip()

	def on_erase( self, event ):
		event.Skip()

	def set_face_place( self, event ):
		event.Skip()

	def wheel_x( self, event ):
		event.Skip()

	def value_check_x( self, event ):
		event.Skip()

	def x_value( self, event ):
		event.Skip()

	def y_wheel( self, event ):
		event.Skip()

	def value_check_y( self, event ):
		event.Skip()

	def y_value( self, event ):
		event.Skip()

	def px_wheel( self, event ):
		event.Skip()

	def value_check_px( self, event ):
		event.Skip()

	def py_wheel( self, event ):
		event.Skip()

	def value_check_py( self, event ):
		event.Skip()

	def view_face( self, event ):
		event.Skip()

	def select_face( self, event ):
		event.Skip()

	def change_method( self, event ):
		event.Skip()

	def set_step( self, event ):
		event.Skip()

	def export( self, event ):
		event.Skip()


###########################################################################
## Class MyDialogUpdateLocation
###########################################################################

class MyDialogUpdateLocation ( wx.Dialog ):

	def __init__( self, parent, translation ):
		wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = "Update localization files", pos = wx.DefaultPosition, size = wx.Size( 628,256 ), style = wx.DEFAULT_DIALOG_STYLE )
		self.build(translation)

	def __del__( self ):
		pass

	def build(self, translation):
		_ = translation.t
		
		self.SetTitle(_("Update localization files"))
		
		self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )

		bSizer25 = wx.BoxSizer( wx.VERTICAL )

		bSizer29 = wx.BoxSizer( wx.HORIZONTAL )

		bSizer26 = wx.BoxSizer( wx.VERTICAL )

		bSizer35 = wx.BoxSizer( wx.HORIZONTAL )

		self.m_staticText11 = wx.StaticText( self, wx.ID_ANY, _("Localization"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText11.Wrap( -1 )

		bSizer35.Add( self.m_staticText11, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.m_bpButton_remove = wx.BitmapButton( self, wx.ID_ANY, wx.NullBitmap, wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW|0 )

		self.m_bpButton_remove.SetBitmap( wx.ArtProvider.GetBitmap( wx.ART_MINUS, wx.ART_BUTTON ) )
		bSizer35.Add( self.m_bpButton_remove, 0, wx.ALL, 5 )

		self.m_bpButton_add = wx.BitmapButton( self, wx.ID_ANY, wx.NullBitmap, wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW|0 )

		self.m_bpButton_add.SetBitmap( wx.ArtProvider.GetBitmap( wx.ART_PLUS, wx.ART_BUTTON ) )
		bSizer35.Add( self.m_bpButton_add, 0, wx.ALL, 5 )


		bSizer26.Add( bSizer35, 0, wx.EXPAND, 5 )

		m_listBox_selectChoices = [ "AzurLaneTools" ]
		self.m_listBox_select = wx.ListBox( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, m_listBox_selectChoices, wx.LB_NEEDED_SB )
		bSizer26.Add( self.m_listBox_select, 1, wx.ALL|wx.EXPAND, 5 )

		self.m_staticline25 = wx.StaticLine( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		bSizer26.Add( self.m_staticline25, 0, wx.EXPAND |wx.ALL, 5 )

		self.m_button_load_file = wx.Button( self, wx.ID_ANY, _("Load file"), wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer26.Add( self.m_button_load_file, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL|wx.EXPAND, 5 )


		bSizer29.Add( bSizer26, 0, wx.EXPAND, 5 )

		self.m_staticline21 = wx.StaticLine( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL|wx.LI_VERTICAL )
		bSizer29.Add( self.m_staticline21, 0, wx.EXPAND |wx.ALL, 5 )

		bSizer27 = wx.BoxSizer( wx.VERTICAL )

		self.m_treeCtrl_info = wx.TreeCtrl( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TR_DEFAULT_STYLE|wx.TR_HIDE_ROOT|wx.TR_TWIST_BUTTONS )
		bSizer27.Add( self.m_treeCtrl_info, 1, wx.ALL|wx.EXPAND, 5 )


		bSizer29.Add( bSizer27, 1, wx.EXPAND, 5 )

		self.m_staticline22 = wx.StaticLine( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL|wx.LI_VERTICAL )
		bSizer29.Add( self.m_staticline22, 0, wx.EXPAND |wx.ALL, 5 )

		bSizer28 = wx.BoxSizer( wx.VERTICAL )

		self.m_button_apply_all = wx.Button( self, wx.ID_ANY, _("Apply All"), wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer28.Add( self.m_button_apply_all, 0, wx.ALL, 5 )

		self.m_button_apply_new = wx.Button( self, wx.ID_ANY, _("Apply New"), wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer28.Add( self.m_button_apply_new, 0, wx.ALL, 5 )

		self.m_button_apply_cover = wx.Button( self, wx.ID_ANY, _("Apply Overwrite"), wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer28.Add( self.m_button_apply_cover, 0, wx.ALL, 5 )

		self.m_button_cancel = wx.Button( self, wx.ID_ANY, _("Cancel"), wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer28.Add( self.m_button_cancel, 0, wx.ALL, 5 )


		bSizer29.Add( bSizer28, 0, wx.EXPAND, 5 )


		bSizer25.Add( bSizer29, 1, wx.EXPAND, 5 )

		self.m_staticline24 = wx.StaticLine( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		bSizer25.Add( self.m_staticline24, 0, wx.EXPAND |wx.ALL, 5 )

		self.m_staticText_info = wx.StaticText( self, wx.ID_ANY, _("Target:"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText_info.Wrap( -1 )

		bSizer25.Add( self.m_staticText_info, 0, wx.ALL|wx.EXPAND, 5 )


		self.SetSizer( bSizer25 )
		self.Layout()

		self.Centre( wx.BOTH )

		# Connect Events
		self.Bind( wx.EVT_INIT_DIALOG, self.MyDialogUpdateLocationOnInitDialog )
		self.m_bpButton_remove.Bind( wx.EVT_BUTTON, self.remove_data )
		self.m_bpButton_add.Bind( wx.EVT_BUTTON, self.add_local )
		self.m_listBox_select.Bind( wx.EVT_LISTBOX_DCLICK, self.request_info )
		self.m_button_load_file.Bind( wx.EVT_BUTTON, self.load_file )
		self.m_button_apply_all.Bind( wx.EVT_BUTTON, self.apply_all )
		self.m_button_apply_new.Bind( wx.EVT_BUTTON, self.apply_new )
		self.m_button_apply_cover.Bind( wx.EVT_BUTTON, self.apply_cover )
		self.m_button_cancel.Bind( wx.EVT_BUTTON, self.cancel )

		

	# Virtual event handlers, overide them in your derived class
	def MyDialogUpdateLocationOnInitDialog( self, event ):
		event.Skip()

	def remove_data( self, event ):
		event.Skip()

	def add_local( self, event ):
		event.Skip()

	def request_info( self, event ):
		event.Skip()

	def load_file( self, event ):
		event.Skip()

	def apply_all( self, event ):
		event.Skip()

	def apply_new( self, event ):
		event.Skip()

	def apply_cover( self, event ):
		event.Skip()

	def cancel( self, event ):
		event.Skip()


###########################################################################
## Class DialogSpiltSprite
###########################################################################

class DialogSpiltSprite ( wx.Dialog ):

	def __init__( self, parent, translation ):
		wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = "Sprite Cutting", pos = wx.DefaultPosition, size = wx.Size( 512,350 ), style = wx.DEFAULT_DIALOG_STYLE )
		self.build(translation)

	def __del__( self ):
		pass


	def build(self, translation):
		_ = translation.t
		
		self.SetTitle(_("Sprite Cutting"))
		
		self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )

		bSizer36 = wx.BoxSizer( wx.VERTICAL )

		bSizer37 = wx.BoxSizer( wx.HORIZONTAL )

		bSizer38 = wx.BoxSizer( wx.VERTICAL )

		bSizer38.SetMinSize( wx.Size( 200,-1 ) )
		self.m_staticText_name = wx.StaticText( self, wx.ID_ANY, "", wx.DefaultPosition, wx.DefaultSize, wx.ST_ELLIPSIZE_END )
		self.m_staticText_name.Wrap( -1 )

		bSizer38.Add( self.m_staticText_name, 0, wx.ALL|wx.EXPAND, 5 )

		self.m_staticline31 = wx.StaticLine( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		bSizer38.Add( self.m_staticline31, 0, wx.EXPAND |wx.ALL, 5 )

		bSizer411 = wx.BoxSizer( wx.HORIZONTAL )

		self.m_staticText19 = wx.StaticText( self, wx.ID_ANY, _("Path ID:"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText19.Wrap( -1 )

		bSizer411.Add( self.m_staticText19, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.m_textCtrl_id = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.TE_PROCESS_ENTER|wx.TE_PROCESS_TAB )
		bSizer411.Add( self.m_textCtrl_id, 1, wx.ALL, 5 )


		bSizer38.Add( bSizer411, 0, wx.EXPAND, 5 )

		self.m_staticline34 = wx.StaticLine( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		bSizer38.Add( self.m_staticline34, 0, wx.EXPAND |wx.ALL, 5 )

		bSizer42 = wx.BoxSizer( wx.HORIZONTAL )

		self.m_staticText20 = wx.StaticText( self, wx.ID_ANY, _("Dump type:"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText20.Wrap( -1 )

		bSizer42.Add( self.m_staticText20, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		m_choice_dump_typeChoices = "Text(*.txt)|Json(*.json)".split("|")
		self.m_choice_dump_type = wx.Choice( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, m_choice_dump_typeChoices, 0 )
		self.m_choice_dump_type.SetSelection( 0 )
		bSizer42.Add( self.m_choice_dump_type, 0, wx.ALL, 5 )


		bSizer38.Add( bSizer42, 0, wx.EXPAND, 5 )

		m_listBox_in_filesChoices = []
		self.m_listBox_in_files = wx.ListBox( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, m_listBox_in_filesChoices, wx.LB_ALWAYS_SB|wx.LB_HSCROLL|wx.LB_SINGLE )
		bSizer38.Add( self.m_listBox_in_files, 1, wx.ALL|wx.EXPAND, 5 )


		bSizer37.Add( bSizer38, 0, wx.EXPAND, 5 )

		self.m_staticline30 = wx.StaticLine( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_VERTICAL )
		bSizer37.Add( self.m_staticline30, 0, wx.EXPAND |wx.ALL, 5 )

		bSizer39 = wx.BoxSizer( wx.VERTICAL )

		self.m_bitmap_show = wx.StaticBitmap( self, wx.ID_ANY, wx.ArtProvider.GetBitmap( wx.ART_MISSING_IMAGE, wx.ART_BUTTON ), wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer39.Add( self.m_bitmap_show, 1, wx.ALL|wx.EXPAND, 5 )


		bSizer37.Add( bSizer39, 1, wx.EXPAND, 5 )


		bSizer36.Add( bSizer37, 1, wx.EXPAND, 5 )

		self.m_staticline32 = wx.StaticLine( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		bSizer36.Add( self.m_staticline32, 0, wx.EXPAND |wx.ALL, 5 )

		bSizer41 = wx.BoxSizer( wx.HORIZONTAL )

		m_sdbSizer3 = wx.StdDialogButtonSizer()
		self.m_sdbSizer3Save = wx.Button( self, wx.ID_SAVE )
		m_sdbSizer3.AddButton( self.m_sdbSizer3Save )
		self.m_sdbSizer3Cancel = wx.Button( self, wx.ID_CANCEL )
		m_sdbSizer3.AddButton( self.m_sdbSizer3Cancel )
		m_sdbSizer3.Realize();

		bSizer41.Add( m_sdbSizer3, 0, 0, 5 )

		self.m_staticline33 = wx.StaticLine( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL|wx.LI_VERTICAL )
		bSizer41.Add( self.m_staticline33, 0, wx.EXPAND |wx.ALL, 5 )

		self.m_staticText_info = wx.StaticText( self, wx.ID_ANY, _("Ready..."), wx.DefaultPosition, wx.DefaultSize, wx.ST_ELLIPSIZE_START )
		self.m_staticText_info.Wrap( -1 )

		bSizer41.Add( self.m_staticText_info, 1, wx.ALL|wx.EXPAND, 5 )


		bSizer36.Add( bSizer41, 0, wx.EXPAND, 5 )


		self.SetSizer( bSizer36 )
		self.Layout()

		self.Centre( wx.BOTH )

		# Connect Events
		self.Bind( wx.EVT_KEY_DOWN, self.on_key_down )
		self.m_textCtrl_id.Bind( wx.EVT_TEXT_ENTER, self.clear_ID )
		self.m_listBox_in_files.Bind( wx.EVT_LISTBOX_DCLICK, self.view_pic )
		self.m_sdbSizer3Save.Bind( wx.EVT_BUTTON, self.save_all )

		

	# Virtual event handlers, overide them in your derived class
	def on_key_down( self, event ):
		event.Skip()

	def clear_ID( self, event ):
		event.Skip()

	def view_pic( self, event ):
		event.Skip()

	def save_all( self, event ):
		event.Skip()
