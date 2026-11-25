
from database import getConnection
import json


def saveMovie(movie_name: str, genre: str, duration: int) -> str:
    """Save new movie details"""

    con, cursor = getConnection()

    cursor.execute("""
        INSERT INTO movie(movie_name, genre, duration)
        VALUES(?,?,?)
    """, (movie_name, genre, duration))

    row = cursor.rowcount
    con.commit()

    cursor.close()
    con.close()

    if row == 1:
        return "new movie created successfully"
    return "unable to add a new movie"


def getAllMovies() -> str:
    """Get all movie records"""

    con, cursor = getConnection()

    cursor.execute("SELECT * FROM movie")
    rows = cursor.fetchall()

    movies = []

    for row in rows:
        movies.append({
            "movie_id": row[0],
            "movie_name": row[1],
            "genre": row[2],
            "duration": row[3]
        })

    cursor.close()
    con.close()

    return json.dumps(movies, indent=1)


def getMovieById(movie_id: int) -> str:
    """Get movie record by movie_id"""

    con, cursor = getConnection()

    cursor.execute("""
        SELECT * FROM movie WHERE movie_id = ?
    """, (movie_id,))

    row = cursor.fetchone()

    cursor.close()
    con.close()

    if row:
        movie = {
            "movie_id": row[0],
            "movie_name": row[1],
            "genre": row[2],
            "duration": row[3]
        }

        return json.dumps(movie, indent=1)

    return "movie not found"


def updateMovie(movie_id: int, movie_name: str,
                genre: str, duration: int) -> str:
    """Update movie details"""

    con, cursor = getConnection()

    cursor.execute("""
        UPDATE movie
        SET movie_name = ?, genre = ?, duration = ?
        WHERE movie_id = ?
    """, (movie_name, genre, duration, movie_id))

    row = cursor.rowcount
    con.commit()

    cursor.close()
    con.close()

    if row == 1:
        return "Movie updated successfully"

    return "unable to update movie"


def deleteMovie(movie_id: int) -> str:
    """Delete movie by movie_id"""

    con, cursor = getConnection()

    cursor.execute("""
        DELETE FROM movie WHERE movie_id = ?
    """, (movie_id,))

    row = cursor.rowcount
    con.commit()

    cursor.close()
    con.close()

    if row == 1:
        return "movie deleted successfully"

    return "unable to delete movie"


def saveMultiplex(multiplex_name: str, location: str) -> str:
    """Save new multiplex details"""

    con, cursor = getConnection()

    cursor.execute("""
        INSERT INTO multiplex(multiplex_name, location)
        VALUES(?,?)
    """, (multiplex_name, location))

    row = cursor.rowcount
    con.commit()

    cursor.close()
    con.close()

    if row == 1:
        return "new multiplex created successfully"

    return "unable to add multiplex"


def getAllMultiplex() -> str:
    """Get all multiplex records"""

    con, cursor = getConnection()

    cursor.execute("SELECT * FROM multiplex")
    rows = cursor.fetchall()

    multiplexes = []

    for row in rows:
        multiplexes.append({
            "multiplex_id": row[0],
            "multiplex_name": row[1],
            "location": row[2]
        })

    cursor.close()
    con.close()

    return json.dumps(multiplexes, indent=1)


def saveHall(hall_name: str, multiplex_id: int) -> str:
    """Save new hall details"""

    con, cursor = getConnection()

    cursor.execute("""
        INSERT INTO hall(hall_name, multiplex_id)
        VALUES(?,?)
    """, (hall_name, multiplex_id))

    row = cursor.rowcount
    con.commit()

    cursor.close()
    con.close()

    if row == 1:
        return "new hall created successfully"

    return "unable to add hall"


def getAllHalls() -> str:
    """Get all hall records with multiplex details"""

    con, cursor = getConnection()

    cursor.execute("""
        SELECT
            h.hall_id,
            h.hall_name,
            mx.multiplex_name,
            mx.location
        FROM hall h
        JOIN multiplex mx
        ON h.multiplex_id = mx.multiplex_id
    """)

    rows = cursor.fetchall()
    halls = []

    for row in rows:
        halls.append({
            "hall_id": row[0],
            "hall_name": row[1],
            "multiplex_name": row[2],
            "location": row[3]
        })

    cursor.close()
    con.close()

    return json.dumps(halls, indent=1)


def getMovieMultiplex(multiplex_name: str) -> str:
    """Get movie details by multiplex name"""

    con, cursor = getConnection()

    cursor.execute("""
        SELECT
            m.movie_id,
            m.movie_name,
            m.genre,
            m.duration,
            h.hall_id,
            h.hall_name,
            s.show_time,
            mx.multiplex_name,
            mx.location

        FROM shows s

        JOIN movie m
        ON s.movie_id = m.movie_id

        JOIN hall h
        ON s.hall_id = h.hall_id

        JOIN multiplex mx
        ON h.multiplex_id = mx.multiplex_id

        WHERE mx.multiplex_name = ?
    """, (multiplex_name,))

    rows = cursor.fetchall()
    movies = []

    for row in rows:
        movies.append({
            "movie_id": row[0],
            "movie_name": row[1],
            "genre": row[2],
            "duration": row[3],
            "hall_id": row[4],
            "hall_name": row[5],
            "show_time": row[6],
            "multiplex_name": row[7],
            "location": row[8]
        })

    cursor.close()
    con.close()

    return json.dumps(movies, indent=1)
