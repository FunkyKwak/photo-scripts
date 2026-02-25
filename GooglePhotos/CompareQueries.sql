-- Fichiers Google absents sur le NAS
with approx as (
    SELECT
        google.id as google_id,
        (select nas_approx.id
        from files nas_approx
        WHERE google.filename = nas_approx.filename
        AND nas_approx.source = 'nas'
        LIMIT 1
        ) as nas_approx_id,
        (select count(distinct nas_approx.id)
        from files nas_approx
        WHERE google.filename = nas_approx.filename
        AND nas_approx.source = 'nas'
        ) as nas_approx_count
    FROM files google
    LEFT JOIN files nas_exact
        ON google.filename = nas_exact.filename
        AND google.date_taken = nas_exact.date_taken
        AND google.size <= nas_exact.size
        AND nas_exact.source = 'nas'
    WHERE google.source = 'google'
    AND nas_exact.id IS NULL
), googlenasdiff as (
    SELECT
        google.id as google_id, google.filename as google_filename, google.size as google_size, google.date_taken as google_date_taken, google.path as google_path,
        approx.nas_approx_count,
        nas.id    as nas_id   , nas.filename    as nas_filename   , nas.size    as nas_size   , nas.date_taken    as nas_date_taken   , nas.path as nas_path
    FROM approx
    LEFT JOIN files nas ON approx.nas_approx_id = nas.id
    INNER JOIN files google ON approx.google_id = google.id
)
select * 
from googlenasdiff
where nas_approx_count = 0
and google_path NOT LIKE '%\Archiver\%'
;



with approx as (
    SELECT
        google.id as google_id,
        (select nas_approx.id
        from files nas_approx
        WHERE google.filename = nas_approx.filename
        AND nas_approx.source = 'nas'
        LIMIT 1
        ) as nas_approx_id,
        (select count(distinct nas_approx.id)
        from files nas_approx
        WHERE google.filename = nas_approx.filename
        AND nas_approx.source = 'nas'
        ) as nas_approx_count
    FROM files google
    LEFT JOIN files nas_exact
        ON google.filename = nas_exact.filename
        AND google.date_taken = nas_exact.date_taken
        AND google.size <= nas_exact.size
        AND nas_exact.source = 'nas'
    WHERE google.source = 'google'
    AND nas_exact.id IS NULL
), googlenasdiff as (
    SELECT
        google.id as google_id, google.filename as google_filename, google.size as google_size, google.date_taken as google_date_taken, google.path as google_path,
        approx.nas_approx_count,
        nas.id    as nas_id   , nas.filename    as nas_filename   , nas.size    as nas_size   , nas.date_taken    as nas_date_taken   , nas.path as nas_path
    FROM approx
    LEFT JOIN files nas ON approx.nas_approx_id = nas.id
    INNER JOIN files google ON approx.google_id = google.id
)
select * 
from googlenasdiff
where nas_approx_count = 0
and google_path NOT LIKE '%\\Archiver\\%'