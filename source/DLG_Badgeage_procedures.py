#!/usr/bin/env python
# -*- coding: iso-8859-15 -*-
#------------------------------------------------------------------------
# Application :    Noethys, gestion multi-activit�s
# Site internet :  www.noethys.com
# Auteur:           Ivan LUCAS
# Copyright:       (c) 2010-12 Ivan LUCAS
# Licence:         Licence GNU GPL
#------------------------------------------------------------------------

import wx
import CTRL_Bandeau
import OL_Badgeage_procedures



class Dialog(wx.Dialog):
    def __init__(self, parent):
        wx.Dialog.__init__(self, parent, -1, style=wx.DEFAULT_DIALOG_STYLE|wx.RESIZE_BORDER|wx.MAXIMIZE_BOX|wx.MINIMIZE_BOX|wx.THICK_FRAME)
        self.parent = parent
        
        intro = u"Vous pouvez ici saisir, modifier ou supprimer des proc�dures de badgeage."
        titre = u"Gestion des proc�dures de badgeage"
        self.SetTitle(titre)
        self.ctrl_bandeau = CTRL_Bandeau.Bandeau(self, titre=titre, texte=intro, hauteurHtml=30, nomImage="Images/32x32/Badgeage.png")
        self.ctrl_listview = OL_Badgeage_procedures.ListView(self, id=-1, style=wx.LC_REPORT|wx.SUNKEN_BORDER|wx.LC_SINGLE_SEL|wx.LC_HRULES|wx.LC_VRULES)
        self.ctrl_listview.MAJ()
        self.ctrl_recherche = OL_Badgeage_procedures.BarreRecherche(self)
        
        self.bouton_ajouter = wx.BitmapButton(self, -1, wx.Bitmap("Images/16x16/Ajouter.png", wx.BITMAP_TYPE_ANY))
        self.bouton_modifier = wx.BitmapButton(self, -1, wx.Bitmap("Images/16x16/Modifier.png", wx.BITMAP_TYPE_ANY))
        self.bouton_supprimer = wx.BitmapButton(self, -1, wx.Bitmap("Images/16x16/Supprimer.png", wx.BITMAP_TYPE_ANY))
        self.bouton_dupliquer = wx.BitmapButton(self, -1, wx.Bitmap(u"Images/16x16/Dupliquer.png", wx.BITMAP_TYPE_ANY))
        self.bouton_defaut = wx.BitmapButton(self, -1, wx.Bitmap("Images/16x16/Ok.png", wx.BITMAP_TYPE_ANY))
        
        self.bouton_aide = wx.BitmapButton(self, -1, wx.Bitmap("Images/BoutonsImages/Aide_L72.png", wx.BITMAP_TYPE_ANY))
        self.bouton_vocal = wx.BitmapButton(self, -1, wx.Bitmap(u"Images/BoutonsImages/Synthese_vocale.png", wx.BITMAP_TYPE_ANY))
        self.bouton_fermer = wx.BitmapButton(self, wx.ID_CANCEL, wx.Bitmap("Images/BoutonsImages/Fermer_L72.png", wx.BITMAP_TYPE_ANY))

        self.__set_properties()
        self.__do_layout()
        
        self.Bind(wx.EVT_BUTTON, self.Ajouter, self.bouton_ajouter)
        self.Bind(wx.EVT_BUTTON, self.Modifier, self.bouton_modifier)
        self.Bind(wx.EVT_BUTTON, self.Supprimer, self.bouton_supprimer)
        self.Bind(wx.EVT_BUTTON, self.OnBoutonDupliquer, self.bouton_dupliquer)
        self.Bind(wx.EVT_BUTTON, self.SetDefaut, self.bouton_defaut)
        self.Bind(wx.EVT_BUTTON, self.OnBoutonVocal, self.bouton_vocal)
        self.Bind(wx.EVT_BUTTON, self.OnBoutonAide, self.bouton_aide)

    def __set_properties(self):
        self.bouton_ajouter.SetToolTipString(u"Cliquez ici pour ajouter une proc�dure")
        self.bouton_modifier.SetToolTipString(u"Cliquez ici pour modifier la proc�dure s�lectionn�e dans la liste")
        self.bouton_supprimer.SetToolTipString(u"Cliquez ici pour supprimer la proc�dure s�lectionn�e dans la liste")
        self.bouton_dupliquer.SetToolTipString(u"Cliquez ici pour dupliquer la proc�dure s�lectionn�e dans la liste")
        self.bouton_defaut.SetToolTipString(u"Cliquez ici pour d�finir la proc�dure s�lectionn�e comme celle par d�faut")
        self.bouton_aide.SetToolTipString(u"Cliquez ici pour obtenir de l'aide")
        self.bouton_vocal.SetToolTipString(u"Cliquez ici pour acc�der au param�trage de la synth�se vocale")
        self.bouton_fermer.SetToolTipString(u"Cliquez ici pour fermer")
        self.SetMinSize((650, 550))

    def __do_layout(self):
        grid_sizer_base = wx.FlexGridSizer(rows=3, cols=1, vgap=10, hgap=10)
        grid_sizer_boutons = wx.FlexGridSizer(rows=1, cols=6, vgap=10, hgap=10)
        grid_sizer_contenu = wx.FlexGridSizer(rows=1, cols=2, vgap=5, hgap=5)
        grid_sizer_droit = wx.FlexGridSizer(rows=6, cols=1, vgap=5, hgap=5)
        grid_sizer_gauche = wx.FlexGridSizer(rows=3, cols=1, vgap=10, hgap=10)
        grid_sizer_base.Add(self.ctrl_bandeau, 0, wx.EXPAND, 0)
        grid_sizer_gauche.Add(self.ctrl_listview, 0, wx.EXPAND, 0)
        grid_sizer_gauche.Add(self.ctrl_recherche, 0, wx.EXPAND, 0)
        grid_sizer_gauche.AddGrowableRow(0)
        grid_sizer_gauche.AddGrowableCol(0)
        grid_sizer_contenu.Add(grid_sizer_gauche, 1, wx.EXPAND, 0)
        grid_sizer_droit.Add(self.bouton_ajouter, 0, 0, 0)
        grid_sizer_droit.Add(self.bouton_modifier, 0, 0, 0)
        grid_sizer_droit.Add(self.bouton_supprimer, 0, 0, 0)
        grid_sizer_droit.Add( (5, 5), 0, 0, 0)
        grid_sizer_droit.Add(self.bouton_dupliquer, 0, 0, 0)
        grid_sizer_droit.Add(self.bouton_defaut, 0, 0, 0)
        grid_sizer_contenu.Add(grid_sizer_droit, 1, wx.EXPAND, 0)
        grid_sizer_contenu.AddGrowableRow(0)
        grid_sizer_contenu.AddGrowableCol(0)
        grid_sizer_base.Add(grid_sizer_contenu, 1, wx.LEFT|wx.RIGHT|wx.EXPAND, 10)
        grid_sizer_boutons.Add(self.bouton_aide, 0, 0, 0)
        grid_sizer_boutons.Add(self.bouton_vocal, 0, 0, 0)
        grid_sizer_boutons.Add((20, 20), 0, wx.EXPAND, 0)
        grid_sizer_boutons.Add(self.bouton_fermer, 0, 0, 0)
        grid_sizer_boutons.AddGrowableCol(2)
        grid_sizer_base.Add(grid_sizer_boutons, 1, wx.LEFT|wx.RIGHT|wx.BOTTOM|wx.EXPAND, 10)
        self.SetSizer(grid_sizer_base)
        grid_sizer_base.Fit(self)
        grid_sizer_base.AddGrowableRow(1)
        grid_sizer_base.AddGrowableCol(0)
        self.Layout()
        self.CenterOnScreen()

    def Ajouter(self, event):
        self.ctrl_listview.Ajouter(None)
        
    def Modifier(self, event):
        self.ctrl_listview.Modifier(None)

    def Supprimer(self, event):
        self.ctrl_listview.Supprimer(None)

    def OnBoutonDupliquer(self, event): 
        self.ctrl_listview.Dupliquer(None)

    def SetDefaut(self, event):
        self.ctrl_listview.SetDefaut(None)

    def OnBoutonVocal(self, event):
        import DLG_Vocal
        dlg = DLG_Vocal.Dialog(self)
        dlg.ShowModal() 
        dlg.Destroy()

    def OnBoutonAide(self, event): 
        import UTILS_Aide
        UTILS_Aide.Aide("Procduresdebadgeage")
        
        

if __name__ == "__main__":
    app = wx.App(0)
    #wx.InitAllImageHandlers()
    dialog_1 = Dialog(None)
    app.SetTopWindow(dialog_1)
    dialog_1.ShowModal()
    app.MainLoop()
