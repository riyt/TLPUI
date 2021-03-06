import sys
from gi.repository import Gtk
from shutil import which
from subprocess import check_output
from . import language
from . import settings
from .uihelper import get_graphical_sudo, sudomissing


tlpstatmissing = language.ST_('tlp-stat executable not found.')  # type: str


def fetch_simple_stats(self, textbuffer):
    tlpstat_cmd = which("tlp-stat")

    if tlpstat_cmd is None:
        textbuffer.set_text(tlpstatmissing)
        return

    simple_stat_command = ["tlp-stat", "-g", "-r", "-t", "-c", "-s", "-u"]
    if settings.get_installed_tlp_version().startswith("0_"):
        simple_stat_command = ["tlp-stat", "-r", "-t", "-c", "-s", "-u"]

    tlpstat = check_output(simple_stat_command).decode(sys.stdout.encoding)
    textbuffer.set_text(tlpstat)


def fetch_complete_stats(self, textbuffer):
    sudo_cmd = get_graphical_sudo()
    tlpstat_cmd = which("tlp-stat")

    if sudo_cmd is None:
        textbuffer.set_text(sudomissing)
        return

    if tlpstat_cmd is None:
        textbuffer.set_text(tlpstatmissing)
        return

    tlpstat = check_output([sudo_cmd, "tlp-stat"]).decode(sys.stdout.encoding)
    textbuffer.set_text(tlpstat)


def create_stat_box() -> Gtk.Box:
    scrolledwindow = Gtk.ScrolledWindow()
    scrolledwindow.set_hexpand(True)
    scrolledwindow.set_vexpand(True)

    textbuffer = Gtk.TextBuffer()
    textbuffer.set_text(language.ST_('Click fetch button to receive results'))

    textview = Gtk.TextView()
    textview.set_buffer(textbuffer)
    textview.set_editable(False)

    scrolledwindow.add(textview)

    emptylabel = Gtk.Label()

    fetchsimplebutton = Gtk.Button(label=' {}'.format(language.ST_('Simple')), image=Gtk.Image(stock=Gtk.STOCK_INFO))
    fetchsimplebutton.connect('clicked', fetch_simple_stats, textbuffer)

    fetchcompletebutton = Gtk.Button(label=' {}'.format(language.ST_('Complete')), image=Gtk.Image(stock=Gtk.STOCK_INDEX))
    fetchcompletebutton.connect('clicked', fetch_complete_stats, textbuffer)

    buttonbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=12)
    buttonbox.pack_start(emptylabel, True, True, 0)
    buttonbox.pack_start(fetchsimplebutton, False, False, 0)
    buttonbox.pack_start(fetchcompletebutton, False, False, 0)

    statbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=12)
    statbox.set_margin_top(18)
    statbox.set_margin_bottom(18)
    statbox.set_margin_left(18)
    statbox.set_margin_right(18)
    statbox.pack_start(buttonbox, False, False, 0)
    statbox.pack_start(scrolledwindow, True, True, 0)

    return statbox
