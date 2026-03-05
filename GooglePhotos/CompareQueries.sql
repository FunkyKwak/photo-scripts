with approx as (
    SELECT
        google.id as google_id,
        (select nas_approx.id
        from files nas_approx
        WHERE google.filename = nas_approx.filename
        AND nas_approx.source in ('nas', 'syncthings')
        LIMIT 1
        ) as nas_approx_id,
        (select count(distinct nas_approx.id)
        from files nas_approx
        WHERE google.filename = nas_approx.filename
        AND nas_approx.source in ('nas', 'syncthings')
        ) as nas_approx_count
    FROM files google
    LEFT JOIN files nas_exact
        ON google.filename = nas_exact.filename
        AND (google.date_taken = nas_exact.date_taken or google.date_taken LIKE '2026-02-25%')
        AND google.size <= nas_exact.size
        AND nas_exact.source in ('nas', 'syncthings')
    WHERE google.source = 'google'
    AND nas_exact.id IS NULL
), googlenasdiff as (
    SELECT
        google.id as google_id, google.filename as google_filename, google.size as google_size, google.date_taken as google_date_taken, google.path as google_path,
        approx.nas_approx_count,
        nas.id    as nas_id   , nas.filename    as nas_filename   , nas.size    as nas_size   , nas.date_taken    as nas_date_taken   , nas.path as nas_path
    FROM approx
    LEFT JOIN files nas ON approx.nas_approx_id = nas.id and nas.source in ('nas', 'syncthings')
    INNER JOIN files google ON approx.google_id = google.id and google.source = 'google'
), statuses as (
select *
    ,case
        when nas_approx_count = 1 then 'Approximative Match'
        when nas_approx_count > 1 then 'Multiple matches'
        else 'Missings'
    end as status
from googlenasdiff
)
select status, count(*) as count
from statuses
group by status
order by count desc;


select source, count(*) as count
from files
GROUP BY source;