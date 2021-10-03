from textual.app import App
from textual import events
from textual.widgets import Placeholder
from rich.align import Align
from rich.console import Console, ConsoleOptions, RenderResult, RenderableType
from rich.padding import Padding
from rich.panel import Panel
from rich.text import Text
from textual.widget import Widget
from textual.reactive import Reactive
from rich import box

import asyncio
from pyfiglet import Figlet
import obd_gateway

import argparse

FIGLET_RENDERER = Figlet(font="roman")

class FigletText:
    """A renderable to generate figlet text that adapts to fit the container."""

    def __init__(self, text: str) -> None:
        self.text = text

    def __rich_console__(
        self, console: Console, options: ConsoleOptions
    ) -> RenderResult:
        """Build a Rich renderable to render the Figlet text."""
        yield Text(FIGLET_RENDERER.renderText(self.text).rstrip("\n"), style="bold")


class Numbers(Widget):
    """The digital display of the calculator."""

    def __init__(self, value_, title_):
        super().__init__(title_)
        self.value = str(value_)
        self.title = str(title_)

    def render(self) -> RenderableType:
        """Build a Rich renderable to render the calculator display."""
        return Panel(
            Align.center(FigletText(self.value), vertical="middle"),
            title=self.title
        )
    
async def broadcast(q):
    while True:
        msg = await q.get()
        widget = msg[0]
        widget.value = str(msg[3])
        widget.refresh()
        q.task_done()

WIDGETS = [
    [obd_gateway.ENGINE_RPM, obd_gateway.SPEED],
    [obd_gateway.ENGINE_LOAD]
]
        
class GridTest(App):
    async def on_mount(self, event: events.Mount) -> None:
        parser = argparse.ArgumentParser()
        parser.add_argument("--rs232_port", required=True)

        args = parser.parse_args()
        
        grid = await self.view.dock_grid()


        grid.add_column("col", fraction=1, max_size=70, min_size=45)
        for x in range(len(WIDGETS)):
            grid.add_row("row", fraction=1)

        grid.set_repeat(True, True)
        
        gw = obd_gateway.ObdGateway(args.rs232_port)

        def put_to_eventloop_(widget, cmd, value_type, msg, loop, q):
            loop.call_soon_threadsafe(q.put_nowait, (widget, cmd, value_type, msg))
        Q = asyncio.Queue()
        loop = asyncio.get_running_loop()

        widgets = {}
        for r in range(len(WIDGETS)):
            for c in range(len(WIDGETS[r])):
                cmd = WIDGETS[r][c]
                widget_area_name = "widget_%d_%d" % (r, c)
                area = {widget_area_name: "col-%d-start|col-%d-end,row-%d-start|row-%d-end" % (c+1, c+1, r+1, r+1)}
                grid.add_areas(**area)
                self.log(area)
                widget = Numbers(0, cmd.get_cmd().desc)
                cb = lambda x, y, z, widget=widget: put_to_eventloop_(widget, x, y, z, loop, Q)
                gw.subscribe_for(cmd, cb)
                widgets[widget_area_name] = widget
        
        grid.set_align("stretch", "center")

        grid.place(**widgets)

        asyncio.create_task(broadcast(Q))
        
        await loop.run_in_executor(None, gw.start)


GridTest.run(title="OBD dashboard", log="dashboard.log")
