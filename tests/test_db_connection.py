# Third party imports
import pytest
import random
import sqlite3

# import InstaPy modules
from instapy.database_engine import INSERT_INTO_PROFILE
from instapy.database_engine import SELECT_FROM_PROFILE_WHERE_NAME
from instapy.database_engine import SQL_CREATE_PROFILE_TABLE
from instapy.database_engine import SQL_CREATE_RECORD_ACTIVITY_TABLE
from instapy.database_engine import SQL_CREATE_FOLLOW_RESTRICTION_TABLE
from instapy.database_engine import SQL_CREATE_SHARE_WITH_PODS_RESTRICTION_TABLE
from instapy.database_engine import SQL_CREATE_COMMENT_RESTRICTION_TABLE
from instapy.database_engine import SQL_CREATE_ACCOUNTS_PROGRESS_TABLE
from instapy.database_engine import SQL_CREATE_BLOCK_ON_LIKES_TABLE


SAMPLE_USERS = ["USER1", "USER2", "USER3"]
USERNAME = random.choice(SAMPLE_USERS)
ID = random.randint(1, 1000)
POSTID = random.randint(1, 1000)
FOLLOWERS = random.randint(1, 1000)
FOLLOWING = random.randint(1, 1000)
POSTS = random.randint(1, 1000)


@pytest.fixture
def setup_database():
    """ Fixture to set up the in-memory database with test data """
    sample_data = [
        ("USER1",),
        ("USER2",),
        ("USER3",),
    ]

    conn = sqlite3.connect(":memory:")
    cursor = conn.cursor()

    cursor.execute(SQL_CREATE_PROFILE_TABLE)
    cursor.execute(SQL_CREATE_RECORD_ACTIVITY_TABLE)
    cursor.execute(SQL_CREATE_FOLLOW_RESTRICTION_TABLE)
    cursor.execute(SQL_CREATE_SHARE_WITH_PODS_RESTRICTION_TABLE)
    cursor.execute(SQL_CREATE_COMMENT_RESTRICTION_TABLE)
    cursor.execute(SQL_CREATE_ACCOUNTS_PROGRESS_TABLE)
    cursor.execute(SQL_CREATE_BLOCK_ON_LIKES_TABLE)
    cursor.executemany(INSERT_INTO_PROFILE, sample_data)

    yield conn


def test_db_user(setup_database):
    # Test to make sure that there exist User* in the DB

    cursor = setup_database
    assert (
        len(list(cursor.execute(SELECT_FROM_PROFILE_WHERE_NAME, {"name": USERNAME})))
        == 1
    )


def test_db_activity(setup_database):
    """ Check there is only one row per user """

    cursor = setup_database

    cursor.execute(
        "INSERT INTO recordActivity VALUES "
        "(?, 0, 0, 0, 0, 1, STRFTIME('%Y-%m-%d %H:%M:%S', "
        "'now', 'localtime'))",
        (ID,),
    )

    assert (
        len(
            list(
                cursor.execute(
                    "SELECT * FROM recordActivity WHERE profile_id=:var AND "
                    "STRFTIME('%Y-%m-%d %H', created) == STRFTIME('%Y-%m-%d "
                    "%H', 'now', 'localtime')",
                    {"var": ID},
                )
            )
        )
        == 1
    )


def test_db_restriction(setup_database):
    """ Check there is only one row per user """

    cursor = setup_database

    cursor.execute(
        "INSERT INTO followRestriction (profile_id, "
        "username, times) VALUES (?, ?, ?)",
        (ID, USERNAME, 1),
    )

    assert (
        len(
            list(
                cursor.execute(
                    "SELECT * FROM followRestriction WHERE profile_id=:var", {"var": ID}
                )
            )
        )
        == 1
    )


def test_db_pods_restriction(setup_database):
    """ Check there is only one row per user """

    cursor = setup_database

    cursor.execute(
        "INSERT INTO shareWithPodsRestriction (profile_id, "
        "postid, times) VALUES (?, ?, ?)",
        (ID, POSTID, 1),
    )

    assert (
        len(
            list(
                cursor.execute(
                    "SELECT * FROM shareWithPodsRestriction WHERE profile_id=:id_var "
                    "AND postid=:name_var",
                    {"id_var": ID, "name_var": POSTID},
                )
            )
        )
        == 1
    )


def test_db_comment_restriction(setup_database):
    """ Check there is only one row per user """

    cursor = setup_database

    cursor.execute(
        "INSERT INTO commentRestriction (profile_id, "
        "postid, times) VALUES (?, ?, ?)",
        (ID, POSTID, 1),
    )

    assert (
        len(
            list(
                cursor.execute(
                    "SELECT * FROM commentRestriction WHERE profile_id=:id_var "
                    "AND postid=:name_var",
                    {"id_var": ID, "name_var": POSTID},
                )
            )
        )
        == 1
    )


def test_db_accounts_progress(setup_database):
    """ Check there is only one row per user """

    cursor = setup_database

    cursor.execute(
        "INSERT INTO accountsProgress (profile_id, followers, "
        "following, total_posts, created, modified) "
        "VALUES (?, ?, ?, ?, strftime('%Y-%m-%d %H:%M:%S'), "
        "strftime('%Y-%m-%d %H:%M:%S'))",
        (ID, FOLLOWERS, FOLLOWING, POSTS),
    )

    assert (
        len(
            list(
                cursor.execute(
                    "SELECT * FROM accountsProgress WHERE profile_id=:id_var "
                    "AND total_posts=:name_var",
                    {"id_var": ID, "name_var": POSTS},
                )
            )
        )
        == 1
    )


def test_db_block_on_likes(setup_database):
    """ Check there is only one row per user """

    cursor = setup_database

    cursor.execute(
        "INSERT OR IGNORE INTO blockOnLikes (profile_id, created, "
        "block) VALUES (?, strftime('%Y-%m-%d %H:%M:%S'), ?)",
        (ID, random.randint(0, 2)),
    )

    cursor.execute(
        "INSERT OR IGNORE INTO blockOnLikes (profile_id, created, "
        "block) VALUES (?, strftime('%Y-%m-%d %H:%M:%S'), ?)",
        (ID, random.randint(0, 2)),
    )

    assert (
        len(
            list(
                cursor.execute(
                    "SELECT COUNT (block) FROM blockOnLikes WHERE profile_id=:id_var ",
                    {"id_var": ID},
                )
            )
        )
        == 1
    )
