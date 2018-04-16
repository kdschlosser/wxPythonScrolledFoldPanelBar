# -*- coding: utf-8 -*-
#
# The code contained within this file also falls under the GNU license of
# EventGhost
#
# Copyright © 2005-2018 EventGhost Project <http://www.eventghost.net/>
#
# EventGhost is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation, either version 2 of the License, or (at your option)
# any later version.
#
# EventGhost is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for
# more details.
#
# You should have received a copy of the GNU General Public License along
# with EventGhost. If not, see <http://www.gnu.org/licenses/>.

# wxPython Scrolled Fold Panel Bar
#  ************** ADDS SCROLL BAR SUPPORT TO FOLD PANEL BAR ******************
# To use you can either add this code to a current code file and then create
# your fold panel bar instance. or i believe you can also add this file to your
# current project and import it. then import wx after that.

# in order to have scroll bars for each panel in the fold panel bar we have to
# override the FoldPanelItem class.
# Because we do not want to scroll the caption bar with all the rest of the
# widgets I have kept the wx.Panel that is used to house this and added a
# scrolled panel to it. I did this in a manner that will expose the scrolled
# panel so if you wanted to really get creative with the organization of the
# widgets you are able to through the use of sizers. You simply set a sizer
# just like you would normally for a panel. If you want to keep the boring
# single line of widgets you are able to do so by calling the standard
# AddWindow method.
# I have ditched the custom drawing of the lines as well as the
# absolute positioning for each of the widgets that are added to the panel.
# this needed to get done in order to allow for the addition os a sizer.

# Since FoldPanelItem is a subclass of wx.lib.scrolledpanel.ScrolledPanel
# you are able to access any of the methods that are available to the parent
# class

# I also added the ability to change the caption any time you want.


import wx
import cStringIO
import wx.lib.agw.foldpanelbar as fpb
import wx.lib.scrolledpanel as scrolled


# expand and collapse icons used in the wxPython demo
def collapsed_icon_data():
    return \
'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x10\x00\x00\x00\x10\x08\x06\
\x00\x00\x00\x1f\xf3\xffa\x00\x00\x00\x04sBIT\x08\x08\x08\x08|\x08d\x88\x00\
\x00\x01\x8eIDAT8\x8d\xa5\x93-n\xe4@\x10\x85?g\x03\n6lh)\xc4\xd2\x12\xc3\x81\
\xd6\xa2I\x90\x154\xb9\x81\x8f1G\xc8\x11\x16\x86\xcd\xa0\x99F\xb3A\x91\xa1\
\xc9J&\x96L"5lX\xcc\x0bl\xf7v\xb2\x7fZ\xa5\x98\xebU\xbdz\xf5\\\x9deW\x9f\xf8\
H\\\xbfO|{y\x9dT\x15P\x04\x01\x01UPUD\x84\xdb/7YZ\x9f\xa5\n\xce\x97aRU\x8a\
\xdc`\xacA\x00\x04P\xf0!0\xf6\x81\xa0\xf0p\xff9\xfb\x85\xe0|\x19&T)K\x8b\x18\
\xf9\xa3\xe4\xbe\xf3\x8c^#\xc9\xd5\n\xa8*\xc5?\x9a\x01\x8a\xd2b\r\x1cN\xc3\
\x14\t\xce\x97a\xb2F0Ks\xd58\xaa\xc6\xc5\xa6\xf7\xdfya\xe7\xbdR\x13M2\xf9\
\xf9qKQ\x1fi\xf6-\x00~T\xfac\x1dq#\x82,\xe5q\x05\x91D\xba@\xefj\xba1\xf0\xdc\
zzW\xcff&\xb8,\x89\xa8@Q\xd6\xaaf\xdfRm,\xee\xb1BDxr#\xae\xf5|\xddo\xd6\xe2H\
\x18\x15\x84\xa0q@]\xe54\x8d\xa3\xedf\x05M\xe3\xd8Uy\xc4\x15\x8d\xf5\xd7\x8b\
~\x82\x0fh\x0e"\xb0\xad,\xee\xb8c\xbb\x18\xe7\x8e;6\xa5\x89\x04\xde\xff\x1c\
\x16\xef\xe0p\xfa>\x19\x11\xca\x8d\x8d\xe0\x93\x1b\x01\xd8m\xf3(;x\xa5\xef=\
\xb7w\xf3\x1d$\x7f\xc1\xe0\xbd\xa7\xeb\xa0(,"Kc\x12\xc1+\xfd\xe8\tI\xee\xed)\
\xbf\xbcN\xc1{D\x04k\x05#\x12\xfd\xf2a\xde[\x81\x87\xbb\xdf\x9cr\x1a\x87\xd3\
0)\xba>\x83\xd5\xb97o\xe0\xaf\x04\xff\x13?\x00\xd2\xfb\xa9`z\xac\x80w\x00\
\x00\x00\x00IEND\xaeB`\x82'


def expanded_icon_data():
    return \
'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x10\x00\x00\x00\x10\x08\x06\
\x00\x00\x00\x1f\xf3\xffa\x00\x00\x00\x04sBIT\x08\x08\x08\x08|\x08d\x88\x00\
\x00\x01\x9fIDAT8\x8d\x95\x93\xa1\x8e\xdc0\x14EO\xb2\xc4\xd0\xd2\x12\xb7(mI\
\xa4%V\xd1lQT4[4-\x9a\xfe\xc1\xc2|\xc6\xc2~BY\x83:A3E\xd3\xa0*\xa4\xd2\x90H!\
\x95\x0c\r\r\x1fK\x81g\xb2\x99\x84\xb4\x0fY\xd6\xbb\xc7\xf7>=\'Iz\xc3\xbcv\
\xfbn\xb8\x9c\x15 \xe7\xf3\xc7\x0fw\xc9\xbc7\x99\x03\x0e\xfbn0\x99F+\x85R\
\x80RH\x10\x82\x08\xde\x05\x1ef\x90+\xc0\xe1\xd8\ryn\xd0Z-\\A\xb4\xd2\xf7\
\x9e\xfbwoF\xc8\x088\x1c\xbbae\xb3\xe8y&\x9a\xdf\xf5\xbd\xe7\xfem\x84\xa4\
\x97\xccYf\x16\x8d\xdb\xb2a]\xfeX\x18\xc9s\xc3\xe1\x18\xe7\x94\x12cb\xcc\xb5\
\xfa\xb1l8\xf5\x01\xe7\x84\xc7\xb2Y@\xb2\xcc0\x02\xb4\x9a\x88%\xbe\xdc\xb4\
\x9e\xb6Zs\xaa74\xadg[6\x88<\xb7]\xc6\x14\x1dL\x86\xe6\x83\xa0\x81\xba\xda\
\x10\x02x/\xd4\xd5\x06\r\x840!\x9c\x1fM\x92\xf4\x86\x9f\xbf\xfe\x0c\xd6\x9ae\
\xd6u\x8d \xf4\xf5\x165\x9b\x8f\x04\xe1\xc5\xcb\xdb$\x05\x90\xa97@\x04lQas\
\xcd*7\x14\xdb\x9aY\xcb\xb8\\\xe9E\x10|\xbc\xf2^\xb0E\x85\xc95_\x9f\n\xaa/\
\x05\x10\x81\xce\xc9\xa8\xf6><G\xd8\xed\xbbA)X\xd9\x0c\x01\x9a\xc6Q\x14\xd9h\
[\x04\xda\xd6c\xadFkE\xf0\xc2\xab\xd7\xb7\xc9\x08\x00\xf8\xf6\xbd\x1b\x8cQ\
\xd8|\xb9\x0f\xd3\x9a\x8a\xc7\x08\x00\x9f?\xdd%\xde\x07\xda\x93\xc3{\x19C\
\x8a\x9c\x03\x0b8\x17\xe8\x9d\xbf\x02.>\x13\xc0n\xff{PJ\xc5\xfdP\x11""<\xbc\
\xff\x87\xdf\xf8\xbf\xf5\x17FF\xaf\x8f\x8b\xd3\xe6K\x00\x00\x00\x00IEND\xaeB\
`\x82'


def convert_icon(icon_data):
    stream = cStringIO.StringIO(icon_data)
    image = wx.ImageFromStream(stream)
    stream.close()
    return wx.BitmapFromImage(image)


class ExpandedIcon:

    @staticmethod
    def GetBitmap():
        return convert_icon(expanded_icon_data())


_expanded_icon = fpb.ExpandedIcon
fpb.ExpandedIcon = ExpandedIcon


class CollapsedIcon:

    @staticmethod
    def GetBitmap():
        return convert_icon(collapsed_icon_data())


_collapsed_icon = fpb.CollapsedIcon
fpb.CollapsedIcon = CollapsedIcon


class FoldPanelItem(scrolled.ScrolledPanel):

    def __init__(
        self,
        parent,
        id=wx.ID_ANY,
        caption="",
        foldIcons=None,
        collapsed=False,
        cbstyle=None
    ):
        self.__panel = wx.Panel(
            parent,
            id,
            wx.Point(0, 0),
            style=wx.CLIP_CHILDREN
        )

        self._controlCreated = False
        self._UserSize = 0
        self._PanelSize = 0
        self._LastInsertPos = 0
        self._itemPos = 0
        self._userSized = False

        if foldIcons is None:
            foldIcons = wx.ImageList(16, 16)

            bmp = fpb.ExpandedIcon.GetBitmap()
            foldIcons.Add(bmp)
            bmp = fpb.CollapsedIcon.GetBitmap()
            foldIcons.Add(bmp)

        self._foldIcons = foldIcons
        if cbstyle is None:
            cbstyle = fpb.EmptyCaptionBarStyle

        self._captionBar = fpb.CaptionBar(
            self.__panel,
            wx.ID_ANY,
            wx.Point(0, 0),
            size=wx.DefaultSize,
            caption=caption,
            foldIcons=foldIcons,
            cbstyle=cbstyle
        )

        if collapsed:
            self._captionBar.Collapse()
        self._controlCreated = True

        size = self._captionBar.GetSize()

        if self.IsVertical():
            scrolled.ScrolledPanel.__init__(
                self,
                self.__panel,
                -1,
                style=wx.VSCROLL
            )
            self.SetupScrolling(scroll_x=False)
            sizer = wx.BoxSizer(wx.VERTICAL)
            self.__main_sizer = wx.BoxSizer(wx.VERTICAL)
            self._PanelSize = size.GetHeight()
        else:
            scrolled.ScrolledPanel.__init__(
                self,
                self.__panel,
                -1,
                style=wx.HSCROLL
            )
            self.SetupScrolling(scroll_y=False)
            sizer = wx.BoxSizer(wx.HORIZONTAL)
            self.__main_sizer = wx.BoxSizer(wx.HORIZONTAL)
            self._PanelSize = size.GetWidth()

        sizer.Add(self._captionBar, 0, wx.EXPAND)
        sizer.Add(self, 1, wx.EXPAND)
        self.__panel.SetSizer(sizer)
        self.SetSizer(self.__main_sizer)

        self._LastInsertPos = self._PanelSize
        self._items = []

        self.__panel.Bind(fpb.EVT_CAPTIONBAR, self.OnPressCaption)
        self.Expand()

        if collapsed:
            self.Collapse()

        self.__panel.Bind(wx.EVT_SIZE, self.OnSize)
        self.OnSize()

    def OnSize(self, event=None):
        pnl_size = self.__panel.GetSize()
        vsize = self.GetVirtualSize()
        size = self.GetSize()

        if self.IsVertical():
            self.SetSize((pnl_size[0], size[1]))
            self.SetVirtualSize((pnl_size[0] - 40, vsize[1]))
        else:
            self.SetSize((size[0], pnl_size[1]))
            self.SetVirtualSize((vsize[0], pnl_size[1] - 40))
        if event is not None:
            event.Skip()

    def AddWindow(
        self,
        window,
        flags=fpb.FPB_ALIGN_WIDTH,
        spacing=fpb.FPB_DEFAULT_SPACING,
        leftSpacing=fpb.FPB_DEFAULT_LEFTSPACING,
        rightSpacing=fpb.FPB_DEFAULT_RIGHTSPACING
    ):
        sizer1 = wx.BoxSizer(wx.HORIZONTAL)
        sizer2 = wx.BoxSizer(wx.VERTICAL)

        if flags | fpb.FPB_ALIGN_WIDTH == flags:
            sizer1.AddStretchSpacer(1)

        sizer2.Add(window, 1, wx.EXPAND | wx.LEFT, leftSpacing)
        sizer1.Add(sizer2, 1, wx.EXPAND | wx.ALL, spacing)

        sizer1.AddStretchSpacer(1)
        self.__main_sizer.Add(sizer1, wx.EXPAND | wx.RIGHT, rightSpacing)

    def AddSeparator(
        self,
        colour=wx.BLACK,
        spacing=fpb.FPB_DEFAULT_SPACING,
        leftSpacing=fpb.FPB_DEFAULT_LEFTSPACING,
        rightSpacing=fpb.FPB_DEFAULT_RIGHTSPACING
    ):
        sizer1 = wx.BoxSizer(wx.HORIZONTAL)
        sizer2 = wx.BoxSizer(wx.VERTICAL)

        if self.IsVertical():
            line = wx.StaticLine(self, -1, style=wx.LI_HORIZONTAL)
        else:
            line = wx.StaticLine(self, -1, style=wx.LI_VERTICAL)

        sizer2.Add(line, 1, wx.EXPAND | wx.LEFT, leftSpacing)
        sizer1.Add(sizer2, 1, wx.EXPAND | wx.ALL, spacing)

        self.__main_sizer.Add(sizer1, wx.EXPAND | wx.RIGHT, rightSpacing)

    def Reposition(self, pos):
        self.__panel.Freeze()

        vertical = self.IsVertical()
        xpos = (vertical and [-1] or [pos])[0]
        ypos = (vertical and [pos] or [-1])[0]

        self.__panel.SetDimensions(xpos, ypos, -1, -1, wx.SIZE_USE_EXISTING)
        self._itemPos = pos

        self.__panel.Thaw()
        return self.GetPanelLength()

    def OnPressCaption(self, event):
        event.SetTag(self)
        event.Skip()

    def ResizePanel(self):
        self.__panel.Freeze()

        vertical = self.IsVertical()

        if self._captionBar.IsCollapsed():
            size = self._captionBar.GetSize()
            self._PanelSize = (
                vertical and [size.GetHeight()] or [size.GetWidth()]
            )[0]
        else:
            size = self.__panel.GetBestSize()
            self._PanelSize = (
                vertical and [size.GetHeight()] or [size.GetWidth()]
            )[0]

            if self._UserSize:
                if vertical:
                    size.SetHeight(self._UserSize)
                else:
                    size.SetWidth(self._UserSize)

        pnlsize = self.__panel.GetParent().GetSize()

        if vertical:
            size.SetWidth(pnlsize.GetWidth())
        else:
            size.SetHeight(pnlsize.GetHeight())

        xsize = (vertical and [size.GetWidth()] or [-1])[0]
        ysize = (vertical and [-1] or [size.GetHeight()])[0]

        self._captionBar.SetSize((xsize, ysize))

        self.__panel.SetSize(pnlsize)
        self.__panel.Thaw()
        self.__panel.Refresh()
        self.__panel.Update()

    def IsVertical(self):
        if isinstance(self.__panel.GetGrandParent(), fpb.FoldPanelBar):
            return self.__panel.GetGrandParent().IsVertical()
        else:
            raise Exception(
                "ERROR: Wrong Parent " + repr(
                    self.__panel.GetGrandParent())
            )

    def IsExpanded(self):
        return not self._captionBar.IsCollapsed()

    def GetItemPos(self):
        return self._itemPos

    def Collapse(self):
        self._captionBar.Collapse()
        self.Show(False)
        self.ResizePanel()

    def Expand(self):
        self._captionBar.Expand()
        self.Show(True)
        self.ResizePanel()

    def GetPanelLength(self):
        if self._captionBar.IsCollapsed():
            return self.GetCaptionLength()
        elif self._userSized:
            return self._UserSize

        if self.IsVertical():
            return self.__panel.GetSize()[1]

        return self.__panel.GetSize()[0]

    def GetCaptionLength(self):
        size = self._captionBar.GetSize()
        return (
            self.IsVertical() and [size.GetHeight()] or [size.GetWidth()]
        )[0]

    def ApplyCaptionStyle(self, cbstyle):
        self._captionBar.SetCaptionStyle(cbstyle)

    def GetCaptionStyle(self):
        return self._captionBar.GetCaptionStyle()

    def SetCaptionLabel(self, label):
        self._captionBar._caption = label
        self._captionBar.Refresh()
        self._captionBar.Update()

    def GetCaptionLabel(self):
        return self._captionBar._caption


_fold_panel_item = fpb.FoldPanelItem
fpb.FoldPanelItem = FoldPanelItem
