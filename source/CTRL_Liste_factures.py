#!/usr/bin/env python
# -*- coding: iso-8859-15 -*-
#------------------------------------------------------------------------
# Application :    Noethys, gestion multi-activit�s
# Site internet :  www.noethys.com
# Auteur:           Ivan LUCAS
# Copyright:       (c) 2010-13 Ivan LUCAS
# Licence:         Licence GNU GPL
#------------------------------------------------------------------------

import wx
import wx.lib.agw.hyperlink as Hyperlink

import OL_Factures
import DLG_Filtres_factures
import UTILS_Utilisateurs


class Hyperlien(Hyperlink.HyperLinkCtrl):
    def __init__(self, parent, id=-1, label="", infobulle="", URL="", size=(-1, -1), pos=(0, 0)):
        Hyperlink.HyperLinkCtrl.__init__(self, parent, id, label, URL=URL, size=size, pos=pos)
        self.parent = parent
        self.URL = URL
        self.AutoBrowse(False)
        self.SetColours("BLUE", "BLUE", "BLUE")
        self.SetUnderlines(False, False, True)
        self.SetBold(False)
        self.EnableRollover(True)
        self.SetToolTip(wx.ToolTip(infobulle))
        self.UpdateLink()
        self.DoPopup(False)
        self.Bind(Hyperlink.EVT_HYPERLINK_LEFT, self.OnLeftLink)
    
    def OnLeftLink(self, event):
        if self.URL == "tout" :
            self.parent.ctrl_factures.CocheTout()
        if self.URL == "rien" :
            self.parent.ctrl_factures.CocheRien()
        self.UpdateLink()
        
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

class CTRL(wx.Panel):
    def __init__(self, parent, filtres=[], codesColonnes = ["IDfacture", "date", "numero", "famille", "prelevement", "email", "total", "solde", "solde_actuel", "date_echeance", "nom_lot"], checkColonne = True, triColonne = "numero"):
        wx.Panel.__init__(self, parent, id=-1, name="CTRL_Liste_factures", style=wx.TAB_TRAVERSAL)
        self.parent = parent
        
        # Liste des factures
        self.ctrl_factures = OL_Factures.ListView(self, id=-1, codesColonnes=codesColonnes, checkColonne=checkColonne, triColonne=triColonne, 
                                                                    style=wx.LC_HRULES|wx.LC_VRULES|wx.LC_REPORT|wx.SUNKEN_BORDER|wx.LC_SINGLE_SEL)
        self.ctrl_factures.SetMinSize((100, 100)) 
        
        # Ctrl des filtres de s�lection
        self.ctrl_filtres = DLG_Filtres_factures.CTRL_Filtres(self, filtres=filtres, ctrl_factures=self.ctrl_factures)
        
        # Commandes de liste
        self.bouton_apercu = wx.BitmapButton(self, -1, wx.Bitmap(u"Images/16x16/Apercu.png", wx.BITMAP_TYPE_ANY))
        self.bouton_email = wx.BitmapButton(self, -1, wx.Bitmap(u"Images/16x16/Emails_exp.png", wx.BITMAP_TYPE_ANY))
        self.bouton_supprimer = wx.BitmapButton(self, -1, wx.Bitmap(u"Images/16x16/Supprimer.png", wx.BITMAP_TYPE_ANY))
        self.bouton_liste_apercu = wx.BitmapButton(self, -1, wx.Bitmap(u"Images/16x16/Apercu.png", wx.BITMAP_TYPE_ANY))
        self.bouton_liste_imprimer = wx.BitmapButton(self, -1, wx.Bitmap(u"Images/16x16/Imprimante.png", wx.BITMAP_TYPE_ANY))
        self.bouton_liste_export_texte = wx.BitmapButton(self, -1, wx.Bitmap(u"Images/16x16/Texte2.png", wx.BITMAP_TYPE_ANY))
        self.bouton_liste_export_excel = wx.BitmapButton(self, -1, wx.Bitmap(u"Images/16x16/Excel.png", wx.BITMAP_TYPE_ANY))
        
        # Options de liste
        self.ctrl_recherche = OL_Factures.BarreRecherche(self, listview=self.ctrl_factures)
        self.hyper_tout = Hyperlien(self, label=u"Tout cocher", infobulle=u"Cliquez ici pour tout cocher", URL="tout")
        self.label_separation = wx.StaticText(self, -1, "|")
        self.hyper_rien = Hyperlien(self, label=u"Tout d�cocher", infobulle=u"Cliquez ici pour tout d�cocher", URL="rien")

        self.__set_properties()
        self.__do_layout()

        self.Bind(wx.EVT_BUTTON, self.OnBoutonApercu, self.bouton_apercu)
        self.Bind(wx.EVT_BUTTON, self.OnBoutonEmail, self.bouton_email)
        self.Bind(wx.EVT_BUTTON, self.OnBoutonSupprimer, self.bouton_supprimer)
        self.Bind(wx.EVT_BUTTON, self.OnBoutonListeApercu, self.bouton_liste_apercu)
        self.Bind(wx.EVT_BUTTON, self.OnBoutonListeImprimer, self.bouton_liste_imprimer)
        self.Bind(wx.EVT_BUTTON, self.OnBoutonListeExportTexte, self.bouton_liste_export_texte)
        self.Bind(wx.EVT_BUTTON, self.OnBoutonListeExportExcel, self.bouton_liste_export_excel)
        
    def __set_properties(self):
        self.bouton_apercu.SetToolTipString(u"Cliquez ici pour afficher un aper�u de la facture s�lectionn�e")
        self.bouton_email.SetToolTipString(u"Cliquez ici envoyer la facture s�lectionn�e par Email")
        self.bouton_supprimer.SetToolTipString(u"Cliquez ici pour supprimer la facture s�lectionn�e ou les factures coch�es")
        self.bouton_liste_apercu.SetToolTipString(u"Cliquez ici pour afficher un aper�u avant impression de cette liste")
        self.bouton_liste_imprimer.SetToolTipString(u"Cliquez ici pour imprimer cette liste")
        self.bouton_liste_export_texte.SetToolTipString(u"Cliquez ici pour exporter cette liste au format Texte")
        self.bouton_liste_export_excel.SetToolTipString(u"Cliquez ici pour exporter cette liste au format Excel")

    def __do_layout(self):
        grid_sizer_base = wx.FlexGridSizer(rows=2, cols=1, vgap=5, hgap=5)
        grid_sizer_base.Add(self.ctrl_filtres, 0, wx.EXPAND | wx.BOTTOM, 5)
        
        grid_sizer_liste = wx.FlexGridSizer(rows=2, cols=2, vgap=5, hgap=5)
        grid_sizer_liste.Add(self.ctrl_factures, 1, wx.EXPAND, 0)
        
        # Commandes de liste
        grid_sizer_commandes = wx.FlexGridSizer(rows=10, cols=1, vgap=5, hgap=5)
        grid_sizer_commandes.Add(self.bouton_apercu, 0, 0, 0)
        grid_sizer_commandes.Add(self.bouton_email, 0, 0, 0)
        grid_sizer_commandes.Add((5, 5), 0, wx.EXPAND, 0)

        grid_sizer_commandes.Add(self.bouton_supprimer, 0, 0, 0)
        grid_sizer_commandes.Add((5, 5), 0, wx.EXPAND, 0)

        grid_sizer_commandes.Add(self.bouton_liste_apercu, 0, 0, 0)
        grid_sizer_commandes.Add(self.bouton_liste_imprimer, 0, 0, 0)
        grid_sizer_commandes.Add((5, 5), 0, wx.EXPAND, 0)
        
        grid_sizer_commandes.Add(self.bouton_liste_export_texte, 0, 0, 0)
        grid_sizer_commandes.Add(self.bouton_liste_export_excel, 0, 0, 0)
        grid_sizer_liste.Add(grid_sizer_commandes, 1, wx.EXPAND, 0)
        
        # Options de liste
        grid_sizer_options_liste = wx.FlexGridSizer(rows=1, cols=5, vgap=5, hgap=5) 
        grid_sizer_options_liste.Add(self.ctrl_recherche, 0, wx.EXPAND, 0)
        grid_sizer_options_liste.Add((40, 5), 0, wx.EXPAND, 0)
        grid_sizer_options_liste.Add(self.hyper_tout, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        grid_sizer_options_liste.Add(self.label_separation, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        grid_sizer_options_liste.Add(self.hyper_rien, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        grid_sizer_options_liste.AddGrowableCol(0)
        grid_sizer_liste.Add(grid_sizer_options_liste, 1, wx.EXPAND, 0)
        
        grid_sizer_liste.AddGrowableRow(0)
        grid_sizer_liste.AddGrowableCol(0)
        grid_sizer_base.Add(grid_sizer_liste, 1, wx.EXPAND, 0)
        
        grid_sizer_base.AddGrowableRow(1)
        grid_sizer_base.AddGrowableCol(0)

        self.SetSizer(grid_sizer_base)
        grid_sizer_base.Fit(self)
        self.Layout()

    def OnBoutonApercu(self, event): 
        self.ctrl_factures.Reedition(None)

    def OnBoutonEmail(self, event): 
        self.ctrl_factures.EnvoyerEmail(None)

    def OnBoutonSupprimer(self, event): 
        self.ctrl_factures.Supprimer(None)

    def OnBoutonListeApercu(self, event): 
        self.ctrl_factures.Apercu(None)

    def OnBoutonListeImprimer(self, event): 
        self.ctrl_factures.Imprimer(None)

    def OnBoutonListeExportTexte(self, event): 
        self.ctrl_factures.ExportTexte(None)

    def OnBoutonListeExportExcel(self, event): 
        self.ctrl_factures.ExportExcel(None)
    
    def GetTracksCoches(self):
        return self.ctrl_factures.GetTracksCoches()

    def GetTracksTous(self):
        return self.ctrl_factures.GetTracksTous()

    def MAJ(self):
        self.ctrl_factures.MAJ() 
        
    def SetFiltres(self, filtres=[]):
        self.ctrl_factures.SetFiltres(filtres)






class MyFrame(wx.Frame):
    def __init__(self, *args, **kwds):
        wx.Frame.__init__(self, *args, **kwds)
        panel = wx.Panel(self, -1)
        sizer_1 = wx.BoxSizer(wx.VERTICAL)
        sizer_1.Add(panel, 1, wx.ALL|wx.EXPAND)
        self.SetSizer(sizer_1)        
        self.ctrl = CTRL(panel)
        self.ctrl.MAJ() 
        self.boutonTest = wx.Button(panel, -1, u"Bouton de test")
        sizer_2 = wx.BoxSizer(wx.VERTICAL)
        sizer_2.Add(self.ctrl, 1, wx.ALL|wx.EXPAND, 4)
        sizer_2.Add(self.boutonTest, 0, wx.ALL|wx.EXPAND, 4)
        panel.SetSizer(sizer_2)
        self.Layout()
        self.CentreOnScreen()
        self.Bind(wx.EVT_BUTTON, self.OnBoutonTest, self.boutonTest)
        
    def OnBoutonTest(self, event):
        """ Bouton Test """
        pass

if __name__ == '__main__':
    app = wx.App(0)
    #wx.InitAllImageHandlers()
    frame_1 = MyFrame(None, -1, u"TEST", size=(700, 500))
    app.SetTopWindow(frame_1)
    frame_1.Show()
    app.MainLoop()


