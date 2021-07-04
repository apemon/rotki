import logging
from sqlite3 import Cursor
from typing import TYPE_CHECKING, List, Optional

from pysqlcipher3 import dbapi2 as sqlcipher

from rotkehlchen.accounting.ledger_actions import LedgerAction
from rotkehlchen.db.utils import form_query_to_filter_timestamps
from rotkehlchen.errors import DeserializationError, UnknownAsset
from rotkehlchen.typing import Location, Timestamp
from rotkehlchen.user_messages import MessagesAggregator

log = logging.getLogger(__name__)

if TYPE_CHECKING:
    from rotkehlchen.db.dbhandler import DBHandler


def _add_gitcoin_extra_data(cursor: Cursor, actions: List[LedgerAction]) -> None:
    """May raise sqlcipher.IntegrityError"""
    db_tuples = []
    for action in actions:
        if action.extra_data is not None:
            db_tuples.append(
                action.extra_data.serialize_for_db(parent_id=action.identifier),
            )

    if len(db_tuples) == 0:
        return

    query = """INSERT INTO ledger_actions_gitcoin_data(
        parent_id, tx_id, grant_id, clr_round, tx_type
    )
    VALUES (?, ?, ?, ?, ?);"""
    cursor.executemany(query, db_tuples)


class DBLedgerActions():

    def __init__(self, database: 'DBHandler', msg_aggregator: MessagesAggregator):
        self.db = database
        self.msg_aggregator = msg_aggregator

    def get_ledger_actions(
            self,
            from_ts: Optional[Timestamp],
            to_ts: Optional[Timestamp],
            location: Optional[Location],
            link: Optional[str] = None,
            notes: Optional[str] = None,
    ) -> List[LedgerAction]:
        bindings = []
        cursor = self.db.conn.cursor()
        query_selection = 'SELECT * '
        query = 'FROM ledger_actions '
        if location is not None:
            query += f'WHERE location="{location.serialize_for_db()}" '

        if link is not None:
            if 'WHERE' not in query:
                query += ' WHERE '
            else:
                query += ' AND '
            query += 'link=? '
            bindings.append(link)

        if notes is not None:
            if 'WHERE' not in query:
                query += ' WHERE '
            else:
                query += ' AND '
            query += 'notes=? '
            bindings.append(notes)

        query, time_bindings = form_query_to_filter_timestamps(query, 'timestamp', from_ts, to_ts)
        full_query = query_selection + query
        results = cursor.execute(full_query, bindings + list(time_bindings)).fetchall()  # type: ignore  # noqa: E501

        original_query = 'SELECT identifier ' + query[:-1]
        gitcoin_query = f'SELECT * from ledger_actions_gitcoin_data WHERE parent_id IN ({original_query});'  # noqa: E501
        gitcoin_results = cursor.execute(gitcoin_query, bindings + list(time_bindings))  # type: ignore  # noqa: E501
        gitcoin_map = {x[0]: x for x in gitcoin_results}

        actions = []
        for result in results:
            try:
                action = LedgerAction.deserialize_from_db(result, gitcoin_map)
            except DeserializationError as e:
                self.msg_aggregator.add_error(
                    f'Error deserializing Ledger Action from the DB. Skipping it.'
                    f'Error was: {str(e)}',
                )
                continue
            except UnknownAsset as e:
                self.msg_aggregator.add_error(
                    f'Error deserializing Ledger Action from the DB. Skipping it. '
                    f'Unknown asset {e.asset_name} found',
                )
                continue

            actions.append(action)

        return actions

    def add_ledger_action(self, action: LedgerAction) -> int:
        """Adds a new ledger action to the DB and returns its identifier for success

        May raise:
        - sqlcipher.IntegrityError if there is a conflict at addition in  _add_gitcoin_extra_data.
         If this error is raised connection needs to be rolled back by the caller.
        """
        cursor = self.db.conn.cursor()
        query = """
        INSERT INTO ledger_actions(
            timestamp, type, location, amount, asset, rate, rate_asset, link, notes
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);"""
        cursor.execute(query, action.serialize_for_db())
        identifier = cursor.lastrowid
        action.identifier = identifier
        _add_gitcoin_extra_data(cursor, [action])
        self.db.conn.commit()
        return identifier

    def add_ledger_actions(self, actions: List[LedgerAction]) -> None:
        """Adds multiple ledger action to the DB

        Is slow due to not using executemany since the ledger actions table
        utilized an auto generated primary key.
        """
        for action in actions:
            try:
                self.add_ledger_action(action)
            except sqlcipher.IntegrityError:  # pylint: disable=no-member
                self.db.msg_aggregator.add_warning('Did not add ledger action to DB due to it already existing')  # noqa: E501
                log.warning(f'Did not add ledger action {action} to the DB due to it already existing')  # noqa: E501
                self.db.conn.rollback()  # undo the addition and rollack to last commit

    def remove_ledger_action(self, identifier: int) -> Optional[str]:
        """Removes a ledger action from the DB by identifier

        Returns None for success or an error message for error
        """
        error_msg = None
        cursor = self.db.conn.cursor()
        cursor.execute(
            'DELETE from ledger_actions WHERE identifier = ?;', (identifier,),
        )
        if cursor.rowcount < 1:
            error_msg = (
                f'Tried to delete ledger action with identifier {identifier} but '
                f'it was not found in the DB'
            )
        self.db.conn.commit()
        return error_msg

    def edit_ledger_action(self, action: LedgerAction) -> Optional[str]:
        """Edits a ledger action from the DB by identifier

        Does not edit the extra data at the moment

        Returns None for success or an error message for error
        """
        error_msg = None
        cursor = self.db.conn.cursor()
        query = """
        UPDATE ledger_actions SET timestamp=?, type=?, location=?, amount=?,
        asset=?, rate=?, rate_asset=?, link=?, notes=? WHERE identifier=?"""
        db_action_tuple = action.serialize_for_db()
        cursor.execute(query, (*db_action_tuple, action.identifier))
        if cursor.rowcount != 1:
            error_msg = (
                f'Tried to edit ledger action with identifier {action.identifier} '
                f'but it was not found in the DB'
            )
        self.db.conn.commit()
        return error_msg
