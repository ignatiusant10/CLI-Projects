import logging
import sys
import click

from journal.operations import add_entry, view_entries, delete_entry, search_entries
from journal.exceptions import journalError

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger("journal_cli")

@click.group()
def cli():
    pass
@cli.command()
@click.option("--content", required =True, help ="The journal entry text")
@click.option("--date", "entry_date", default =None, help = "Date in YYYY-MM-DD format. Defaults to today.")
def add(content , entry_date):
    try:
        entry = add_entry(content=content , entry_date=entry_date)
        click.secho(f"✔️ Entry added sucessfully! (id: {entry.id})", fg="green")
    except journalError as e:
        click.secho(f"❌ Error: {e}", fg ="red")
        sys.exit(1)

@cli.command()
def view():
    try:
        entries = view_entries()
        if not entries:
            click.echo("No entries yet. Add one with: python main.py add --content \"...\"")
            return

        for e in entries:
            click.echo("-"*50)
            click.secho(f"[{e.entry_date}]", fg = "cyan", nl=False)
            click.echo(f"(ID: {e.id})")
            click.echo(e.content)

        click.echo("-"*50)
    except journalError as e:
        click.secho(f"❌ Error: {e}", fg = "red")
        sys.exit(1)

@cli.command()
@click.option("--keyword",  required=True, help="Keyword to search for entry content")
def search(keyword):
    try:
        results = search_entries(keyword)
        if not results:
            click.echo(f"No entries found containing '{keyword}'.")
            return
        click.echo(f"Found {len(results)} matching entr{'y' if len(results)== 1 else 'ies'}:")
        for e in results:
            click.echo("-"*50)
            click.secho(f"[{e.entry_date}]", fg="cyan", nl=False)
            click.echo(f"(Id: {e.id})")
            click.echo(e.content)
    except journalError as e:
        click.secho(f"❌ Error: {e}", fg="red")
        sys.exit(1)

@cli.command()
@click.option("--id", "entry_id", required=True, help="ID of the entry to delete")
def delete(entry_id):
    try:
        delete_entry(entry_id)
        click.secho(f"✔️ Entry {entry_id} deleted.", fg="green")
    except journalError as e:
        click.secho(f"❌ Error: {e}", fg ="red")
        sys.exit(1)

if __name__ == "__main__":
    cli()
        



