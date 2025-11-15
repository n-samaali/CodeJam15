import csv
import io
from math import sin

from textual.app import App, ComposeResult
from rich.syntax import Syntax
from rich.table import Table
from rich.traceback import Traceback
from textual.containers import Horizontal, Vertical

from textual import containers, events, lazy, on
from textual.app import ComposeResult
from textual.binding import Binding
from textual.demo.data import COUNTRIES, DUNE_BIOS, MOVIES, MOVIES_TREE
from textual.demo.page import PageScreen
from textual.reactive import reactive, var
from textual.suggester import SuggestFromList
from textual.theme import BUILTIN_THEMES
from textual.widgets import (
    Button,
    Checkbox,
    DataTable,
    Digits,
    Footer,
    Input,
    Label,
    ListItem,
    ListView,
    Log,
    Markdown,
    MaskedInput,
    OptionList,
    RadioButton,
    RadioSet,
    RichLog,
    Select,
    Sparkline,
    Static,
    Switch,
    TabbedContent,
    TextArea,
    Tree,
)



class ActionButtons(containers.VerticalGroup):
    """Buttons demo."""

    ALLOW_MAXIMIZE = True
    DEFAULT_CLASSES = "column"
    DEFAULT_CSS = """
    ActionButtons {
        ItemGrid { margin-bottom: 0;}
        Button { width: 1fr; }
    }
    """
    
    def compose(self) -> ComposeResult:
        with containers.HorizontalGroup():
            yield Button(
                "Strength",
                variant="success",
                #tooltip="",
                #action="notify('You chose Strength')",
            )
            yield Button(
                "Dexterity",
                variant="primary",
                #tooltip="The primary button style - carry out the core action of the dialog",
                #action="notify('You chose Dexterity')",
            )
            yield Button(
                "Intelligence",
                variant="warning",
                #tooltip="The warning button style - warn the user that this isn't a typical button",
                #action="notify('You chose Intelligence')",
            )
            yield Button(
                "Charisma",
                variant="error",
                #tooltip="The error button style - clicking is a destructive action",
                #action="notify('You chose Charisma')",                
            )
            
        # with containers.ItemGrid(min_column_width=20, regular=True):
        #     yield Button("Default", disabled=True)
        #     yield Button("Primary", variant="primary", disabled=True)
        #     yield Button("Warning", variant="warning", disabled=True)
        #     yield Button("Error", variant="error", disabled=True)
        
class Logs(containers.VerticalGroup):

    DEFAULT_CLASSES = "column"
    
    DEFAULT_CSS = """
    Logs {
        height: 1fr;
    }
    Logs RichLog {
        width: 1fr;
        height: 1fr;
        padding: 1;
        overflow-x: auto;
        border: wide transparent;
        &:focus {
            border: wide $border;
        }
    }
    Logs TabPane { padding: 0; }
    Logs TabbedContent.-maximized {
        height: 1fr;
        Log, RichLog { height: 1fr; }
    }
    """

    CSV = """lane,swimmer,country,time
                4,Joseph Schooling,Singapore,50.39
                2,Michael Phelps,United States,51.14
                5,Chad le Clos,South Africa,51.14
                6,László Cseh,Hungary,51.14
                3,Li Zhuhao,China,51.26
                8,Mehdy Metella,France,51.58
                7,Tom Shields,United States,51.73
                1,Aleksandr Sadovnikov,Russia,51.84"""
    CSV_ROWS = list(csv.reader(io.StringIO(CSV)))

    CODE = '''\
def loop_first_last(values: Iterable[T]) -> Iterable[tuple[bool, bool, T]]:
    """Iterate and generate a tuple with a flag for first and last value."""
    iter_values = iter(values)
    try:
        previous_value = next(iter_values)
    except StopIteration:
        return
    first = True
    for value in iter_values:
        yield first, False, previous_value
        first = False
        previous_value = value
    yield first, True, previous_value\
'''
    rich_log_count = var(0)

    def compose(self) -> ComposeResult:
        yield RichLog(max_lines=10_000, wrap=True, markup=True)

    def on_mount(self) -> None:
        rich_log = self.query_one(RichLog)
        rich_log.write("I am a Rich Log Widget")
        self.set_interval(1, self.update_rich_log)

    def update_rich_log(self) -> None:
        """Update the Rich Log with content."""
        rich_log = self.query_one(RichLog)
        if self.is_scrolling:
            return
        if (
            not self.app.screen.can_view_entire(rich_log)
            and not rich_log.is_in_maximized_view
        ):
            return
        self.rich_log_count += 1
        log_option = self.rich_log_count % 3
        if log_option == 0:
            rich_log.write("Syntax highlighted code", animate=True)
            rich_log.write(Syntax(self.CODE, lexer="python"), animate=True)
        elif log_option == 1:
            rich_log.write("A Rich Table", animate=True)
            table = Table(*self.CSV_ROWS[0])
            for row in self.CSV_ROWS[1:]:
                table.add_row(*row)
            rich_log.write(table, animate=True)
        elif log_option == 2:
            rich_log.write("A Rich Traceback", animate=True)
            try:
                1 / 0
            except Exception:
                traceback = Traceback()
                rich_log.write(traceback, animate=True)
        
class SidePanel(containers.VerticalGroup) :
    
    DEFAULT_CSS="""
    
    #user_stats {
        height: 1fr;
    }
    
    #card_description {
        height: 1fr;
    }
    
    #card_display {
        height: 2fr;
    }
    
    """
    
    def compose(self) -> ComposeResult:
        with containers.Container():
            yield TextArea("This text area will present user stats.", language=None, id="user_stats")
            yield TextArea("This text area will show card scription.", language=None, id="card_description")
            yield TextArea("This are will display card ASCII art.", language=None, id="card_display")
            
class MainPanel(containers.VerticalGroup) :
    
    def compose(self) -> ComposeResult:
        yield Logs()
        yield ActionButtons()
        
class GameApp(App[None]):
    
    DEFAULT_CSS = """
    #side_panel {
        width: 2fr;
    }
    #main_panel {
        width: 5fr; 
    }
    """

    def compose(self) -> ComposeResult:
        self.app.theme = "gruvbox"
        with containers.HorizontalGroup():
            with containers.VerticalGroup(id="side_panel"):
                yield SidePanel()
            with containers.VerticalGroup(id="main_panel"):
                yield MainPanel()

if __name__ == "__main__":
    app = GameApp()
    app.run()