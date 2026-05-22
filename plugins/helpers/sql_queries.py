class SqlQueries:
    songplay_table_insert = ("""
        INSERT INTO songplays
        SELECT
            md5(events.sessionid || events.start_time) AS songplay_id,
            events.start_time, 
            CAST(events.userid AS INTEGER),
            events.level, 
            songs.song_id, 
            songs.artist_id, 
            events.sessionid, 
            events.location, 
            events.useragent
        FROM (
            SELECT 
                TIMESTAMP 'epoch' + ts/1000 * interval '1 second' AS start_time,
                userid,
                level,
                song,
                artist,
                length,
                sessionid,
                location,
                useragent
            FROM staging_events
            WHERE page = 'NextSong'
            AND TRIM(userid) ~ '^[0-9]+$'
        ) events
        JOIN staging_songs songs
        ON events.song = songs.title
        AND events.artist = songs.artist_name
        AND events.length = songs.duration;
    """)

    user_table_insert = ("""
        INSERT INTO users (userid, first_name, last_name, gender, level)
        SELECT DISTINCT CAST(userid AS INTEGER), firstname, lastname, gender, level
        FROM staging_events
        WHERE page = 'NextSong'
        AND TRIM(userid) ~ '^[0-9]+$';
    """)



    song_table_insert = ("""
        INSERT INTO songs (songid, title, artistid, year, duration)
        SELECT DISTINCT song_id, title, artist_id, year, duration
        FROM staging_songs;
    """)


    artist_table_insert = ("""
        INSERT INTO artists (artistid, name, location, lattitude, longitude)
        SELECT DISTINCT artist_id, artist_name, artist_location, artist_latitude, artist_longitude
        FROM staging_songs;
    """)


    time_table_insert = ("""
        INSERT INTO time (start_time, hour, day, week, month, year, weekday)
        SELECT DISTINCT start_time,
            EXTRACT(hour FROM start_time),
            EXTRACT(day FROM start_time),
            EXTRACT(week FROM start_time),
            EXTRACT(month FROM start_time),
            EXTRACT(year FROM start_time),
            EXTRACT(weekday FROM start_time)
        FROM songplays;

    """)