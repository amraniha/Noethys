#!/usr/bin/env python
# -*- coding: iso-8859-15 -*-
#------------------------------------------------------------------------
# Application :    Noethys, gestion multi-activit�s
# Site internet :  www.noethys.com
# Auteur:           Ivan LUCAS
# Copyright:       (c) 2010-11 Ivan LUCAS
# Licence:         Licence GNU GPL
#------------------------------------------------------------------------

import wx

from ObjectListView import FastObjectListView, ColumnDefn, Filter

try: import psyco; psyco.full()
except: pass


class Track(object):
    def __init__(self, donnees):
        self.nom = donnees[0]
        self.exemple = donnees[1]
        self.code = donnees[2]       

    
class ListView(FastObjectListView):
    def __init__(self, *args, **kwds):
        # R�cup�ration des param�tres perso
        self.listeChamps = kwds.pop("listeChamps", None)
        # Initialisation du listCtrl
        FastObjectListView.__init__(self, *args, **kwds)
        # Binds perso
        self.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.OnItemActivated)
        self.Bind(wx.EVT_CONTEXT_MENU, self.OnContextMenu)
        
    def OnItemActivated(self,event):
        self.Inserer(None)
                
    def InitModel(self):
        self.donnees = self.GetTracks()

    def GetTracks(self):
        """ R�cup�ration des donn�es """
        listeListeView = []
        for item in self.listeChamps :
            track = Track(item)
            listeListeView.append(track)
            if self.selectionID == item[0] :
                self.selectionTrack = track
        return listeListeView
            
    def InitObjectListView(self):            
        # Couleur en alternance des lignes
        self.oddRowsBackColor = "#F0FBED" 
        self.evenRowsBackColor = wx.Colour(255, 255, 255)
        self.useExpansionColumn = True
            
        liste_Colonnes = [
            ColumnDefn(u"", 'left', 0, "" ),
            ColumnDefn(u"Nom du champ", 'left', 150, "nom", isSpaceFilling=True ),
            ColumnDefn(u"Valeur exemple", 'left', 150, "exemple"),
            ColumnDefn(u"Code", 'left', 140, "code"),
            ]
        
        self.SetColumns(liste_Colonnes)
        self.SetEmptyListMsg(u"Aucun champ disponible")
        self.SetEmptyListMsgFont(wx.FFont(11, wx.DEFAULT, face="Tekton"))
        self.SetSortColumn(self.columns[0])
        self.SetObjects(self.donnees)
       
    def MAJ(self, ID=None):
        if ID != None :
            self.selectionID = ID
            self.selectionTrack = None
        else:
            self.selectionID = None
            self.selectionTrack = None
        self.InitModel()
        self.InitObjectListView()
        # S�lection d'un item
        if self.selectionTrack != None :
            self.SelectObject(self.selectionTrack, deselectOthers=True, ensureVisible=True)
        self.selectionID = None
        self.selectionTrack = None
    
    def Selection(self):
        return self.GetSelectedObjects()

    def OnContextMenu(self, event):
        """Ouverture du menu contextuel """
        if len(self.Selection()) == 0:
            noSelection = True
        else:
            noSelection = False
                
        # Cr�ation du menu contextuel
        menuPop = wx.Menu()

        # Item Modifier
        item = wx.MenuItem(menuPop, 10, u"Ins�rer")
        bmp = wx.Bitmap("Images/16x16/Fleche_bas.png", wx.BITMAP_TYPE_PNG)
        item.SetBitmap(bmp)
        menuPop.AppendItem(item)
        self.Bind(wx.EVT_MENU, self.Inserer, id=10)
        
        menuPop.AppendSeparator()
    
        # Item Apercu avant impression
        item = wx.MenuItem(menuPop, 40, u"Aper�u avant impression")
        bmp = wx.Bitmap("Images/16x16/Apercu.png", wx.BITMAP_TYPE_PNG)
        item.SetBitmap(bmp)
        menuPop.AppendItem(item)
        self.Bind(wx.EVT_MENU, self.Apercu, id=40)
        
        # Item Imprimer
        item = wx.MenuItem(menuPop, 50, u"Imprimer")
        bmp = wx.Bitmap("Images/16x16/Imprimante.png", wx.BITMAP_TYPE_PNG)
        item.SetBitmap(bmp)
        menuPop.AppendItem(item)
        self.Bind(wx.EVT_MENU, self.Imprimer, id=50)
        
        self.PopupMenu(menuPop)
        menuPop.Destroy()

    def Apercu(self, event):
        import UTILS_Printer
        prt = UTILS_Printer.ObjectListViewPrinter(self, titre=u"Liste des champs", format="A", orientation=wx.PORTRAIT)
        prt.Preview()

    def Imprimer(self, event):
        import UTILS_Printer
        prt = UTILS_Printer.ObjectListViewPrinter(self, titre=u"Liste des champs", format="A", orientation=wx.PORTRAIT)
        prt.Print()

    def Inserer(self, event):
        if len(self.Selection()) == 0 :
            dlg = wx.MessageDialog(self, u"Vous n'avez s�lectionn� aucun champ � ins�rer !", u"Erreur de saisie", wx.OK | wx.ICON_EXCLAMATION)
            dlg.ShowModal()
            dlg.Destroy()
            return
        nom = self.Selection()[0].nom
        code = self.Selection()[0].code
        # Insertion dans le texte
        self.GetParent().InsertTexte(code)


class MyFrame(wx.Frame):
    def __init__(self, *args, **kwds):
        wx.Frame.__init__(self, *args, **kwds)
        panel = wx.Panel(self, -1, name="test1")
        sizer_1 = wx.BoxSizer(wx.VERTICAL)
        sizer_1.Add(panel, 1, wx.ALL|wx.EXPAND)
        self.SetSizer(sizer_1)
        listeChamps = [
            (u"Nom de l'individu", u"DUPOND", u"NOM_INDIVIDU"),
            (u"Pr�nom de l'individu", u"G�rard", u"PRENOM_INDIVIDU"),
            ]
        self.myOlv = ListView(panel, listeChamps=listeChamps, id=-1, name="OL_test", style=wx.LC_REPORT|wx.SUNKEN_BORDER|wx.LC_SINGLE_SEL|wx.LC_HRULES|wx.LC_VRULES)
        self.myOlv.MAJ() 
        sizer_2 = wx.BoxSizer(wx.VERTICAL)
        sizer_2.Add(self.myOlv, 1, wx.ALL|wx.EXPAND, 4)
        panel.SetSizer(sizer_2)
        self.Layout()

if __name__ == '__main__':
    app = wx.App(0)
    #wx.InitAllImageHandlers()
    frame_1 = MyFrame(None, -1, "OL TEST")
    app.SetTopWindow(frame_1)
    frame_1.Show()
    app.MainLoop()
