# Copyright (c) 2010 Aldo Cortesi
# Copyright (c) 2010, 2014 dequis
# Copyright (c) 2012 Randall Ma
# Copyright (c) 2012-2014 Tycho Andersen
# Copyright (c) 2012 Craig Barnes
# Copyright (c) 2013 horsik
# Copyright (c) 2013 Tao Sauvage
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from libqtile import bar, layout, widget, hook
from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal
import subprocess
import os

mod = "mod4"
terminal = guess_terminal()
from libqtile.lazy import lazy 



@lazy.function
def changevol(qtile, increment):
    #Helper function to change volume up to a max. Uses wireplumber.
    maximum = 1.00 #Max vol percentage
    vol = float(subprocess.run(["wpctl", "get-volume", "@DEFAULT_SINK@"], capture_output=True).stdout.strip().split()[1])
    vol += increment
    if vol > maximum: vol = 1
    if vol < 0: vol = 0
    subprocess.run(["wpctl", "set-volume", "@DEFAULT_SINK@", str(vol)])

@hook.subscribe.startup_once
def autostart():
    x = os.path.expanduser('~/.config/qtile/autostart.sh')
    subprocess.run([x])

keys = [
    # A list of available commands that can be bound to keys can be found
    # at https://docs.qtile.org/en/latest/manual/config/lazy.html
    Key([mod], "d", lazy.spawn(os.path.expanduser("~/.config/rofi/scripts/launcher_t2"))),
    Key([], "XF86AudioRaiseVolume", changevol(0.05)),
    Key([], "XF86AudioLowerVolume", changevol(-0.05)),
    Key([mod], "f", lazy.window.toggle_floating()),
    Key([mod, "shift"], "s", lazy.spawn("flameshot gui")),
    # Switch between windows
    Key([mod], "h", lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "l", lazy.layout.right(), desc="Move focus to right"),
    Key([mod], "j", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "k", lazy.layout.up(), desc="Move focus up"),
    Key([mod], "space", lazy.layout.next(), desc="Move window focus to other window"),
    # Move windows between left/right columns or move up/down in current stack.
    # Moving out of range in Columns layout will create new column.
    Key([mod, "shift"], "h", lazy.layout.shuffle_left(), desc="Move window to the left"),
    Key([mod, "shift"], "l", lazy.layout.shuffle_right(), desc="Move window to the right"),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down(), desc="Move window down"),
    Key([mod, "shift"], "k", lazy.layout.shuffle_up(), desc="Move window up"),
    # Grow windows. If current window is on the edge of screen and direction
    # will be to screen edge - window would shrink.
    Key([mod, "control"], "h", lazy.layout.grow_left(), desc="Grow window to the left"),
    Key([mod, "control"], "l", lazy.layout.grow_right(), desc="Grow window to the right"),
    Key([mod, "control"], "j", lazy.layout.grow_down(), desc="Grow window down"),
    Key([mod, "control"], "k", lazy.layout.grow_up(), desc="Grow window up"),
    Key([mod], "n", lazy.layout.normalize(), desc="Reset all window sizes"),
    # Toggle between split and unsplit sides of stack.
    # Split = all windows displayed
    # Unsplit = 1 window displayed, like Max layout, but still with
    # multiple stack panes
    Key(
        [mod, "shift"],
        "Return",
        lazy.layout.toggle_split(),
        desc="Toggle between split and unsplit sides of stack",
    ),
    Key([mod], "Return", lazy.spawn(terminal), desc="Launch terminal"),
    # Toggle between different layouts as defined below
    Key([mod], "Tab", lazy.next_layout(), desc="Toggle between layouts"),
    Key([mod], "w", lazy.window.kill(), desc="Kill focused window"),
    Key([mod, "control"], "r", lazy.reload_config(), desc="Reload the config"),
    Key([mod, "control"], "q", lazy.shutdown(), desc="Shutdown Qtile"),
    Key([mod], "r", lazy.spawncmd(), desc="Spawn a command using a prompt widget"),
]

groups = [
    Group("  \uf269   ", layout="monadtall"),
    Group("     ", layout = "monadtall"),
    Group("     ", layout = "monadtall"),
    Group("     ", layout = "floating"),
]

for i in range(len(groups)):
    keys.extend(
        [
            # mod1 + letter of group = switch to group
            Key(
                [mod],
                str(i + 1),
                lazy.group[groups[i].name].toscreen(),
                desc="Switch to group {}".format(groups[i].name),
            ),
            # mod1 + shift + letter of group = switch to & move focused window to group
            Key(
                [mod, "shift"],
                str(i + 1),
                lazy.window.togroup(groups[i].name, switch_group=True),
                desc="Switch to & move focused window to group {}".format(groups[i].name),
            ),
            # Or, use below if you prefer not to switch to that group.
            # # mod1 + shift + letter of group = move focused window to group
            # Key([mod, "shift"], i.name, lazy.window.togroup(i.name),
            #     desc="move focused window to group {}".format(i.name)),
        ]
    )

layouts = [
    layout.MonadTall(
        margin = 10,
        border_focus = "#50477B"
    ),
    layout.Columns(border_focus_stack=["#d75f5f", "#8f3d3d"], border_width=4),
    layout.Max(),
    layout.Floating(),
    # Try more layouts by unleashing below layouts.
    # layout.Stack(num_stacks=2),
    layout.Bsp(),
    # layout.Matrix(),
    # layout.MonadWide(),
    # layout.RatioTile(),
    # layout.Tile(),
    # layout.TreeTab(),
    # layout.VerticalTile(),
    # layout.Zoomy(),
    layout.Spiral()
]

widget_defaults = dict(
    font="Hack Nerd Font Mono",
    fontsize=18,
)
extension_defaults = widget_defaults.copy()

screens = [
    Screen(
        bottom=bar.Bar(
            [
                widget.Sep(
                    linewidth=0,
                    padding=6
                ),
                widget.Image(
                    filename="~/.config/qtile/Archlinux-icon.png",
                    scale="False",
                    padding=6,
                    mouse_callbacks = {
                        "Button1" : lazy.spawn(os.path.expanduser("~/.config/rofi/scripts/powermenu_t1"))
                    }
                ),
                widget.Sep(
                    linewidth=0,
                    padding=10
                ),
                widget.GroupBox(
                    active="#ffffff",
                    rounded=False,
                    highlight_color="#c4a7e7",
                    highlight_method="line",
                    borderwidth=0,
                    padding=6,
                    font = "Hack Nerd Font",
                ),
                widget.WindowName(
                    foreground="#eb6f92",
                    markup=True,
                    font="Hack Nerd Font",
                    fontsize=15,
                    max_chars=63,
                    padding=6,
                ),
                widget.TextBox(
                    text='',
                    foreground="#f6c177",
                    padding=0,
                    fontsize=25
                ),
                widget.Backlight(
                    background = "#f6c177",
                    foreground="191724",
                    font = "Hack Nerd Font",
                    backlight_name="intel_backlight",
                    format = " {percent:2.0%}"
                ),
                widget.TextBox(
                    text='',
                    background="#f6c177",
                    foreground="#0bda51",
                    padding=0,
                    fontsize=25
                ),
                widget.TextBox(
                    text='墳',
                    background="#0bda51",
                    font = "Hack Nerd Font",
                    foreground="#191724",
                ),
                widget.PulseVolume(
                    background="#0bda51",
                    foreground="#191724"
                ),
                widget.TextBox(
                    text='',
                    background="#0bda51",
                    foreground="#e0def4",
                    padding=0,
                    fontsize=25
                ),
                widget.Battery(
                    foreground="#191724",
                    background="#e0def4",
                    font = "Hack Nerd Font",
                    format="{char} {percent:2.0%}",
                    charge_char = '',
                    discharge_char = '',
                    empty_char=''
                ),
                widget.TextBox(
                    text='',
                    foreground="#9ccfd8",
                    background="#e0def4",
                    padding=0,
                    fontsize=25
                ),
                widget.TextBox(
                    background="#9ccfd8",
                    foreground="#191724",
                    text = "",
                    font = "Hack Nerd Font",
                    mouse_callbacks = {
                        "Button1" : lazy.spawn("rofi-bluetooth")
                    }
                ),
                widget.TextBox(
                    text='',
                    background="#9ccfd8",
                    foreground="#eb6f92",
                    padding=0,
                    fontsize=25
                ),
                widget.Wlan(
                    interface="wlp9s0",
                    format="  {essid} {percent:2.0%}",
                    background="#eb6f92",
                    font = "Hack Nerd Font",
                    foreground="#191724",
                    update_interval=1.0,
                    mouse_callbacks = {
                        "Button1" : lazy.spawn(terminal + " nmtui")
                    }
                ),
                widget.TextBox(
                    text='',
                    background="#eb6f92",
                    foreground="#c4a7e7",
                    padding=0,
                    fontsize=25
                ),
                widget.Clock(
                    background="#c4a7e7",
                    foreground="#191724",
                    font = "Hack Nerd Font",
                    format=" %H:%M - %d/%m/%Y",
                    update_interval=60.0,
                    padding=0
                ),
                widget.TextBox(
                    text='',
                    background="#c4a7e7",
                    foreground="#232136",
                    padding=0,
                    fontsize=25
                ),
                widget.Systray(),
            ],
            25,
            background="#232136",
        ),
    ),
]

# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(), start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front()),
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: list
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False
floating_layout = layout.Floating(
    float_rules=[
        # Run the utility of `xprop` to see the wm class and name of an X client.
        *layout.Floating.default_float_rules,
        Match(wm_class="confirmreset"),  # gitk
        Match(wm_class="makebranch"),  # gitk
        Match(wm_class="maketag"),  # gitk
        Match(wm_class="ssh-askpass"),  # ssh-askpass
        Match(title="branchdialog"),  # gitk
        Match(title="pinentry"),  # GPG key password entry
    ]
)
auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True

# If things like steam games want to auto-minimize themselves when losing
# focus, should we respect this or not?
auto_minimize = True

# When using the Wayland backend, this can be used to configure input devices.
wl_input_rules = None

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"
