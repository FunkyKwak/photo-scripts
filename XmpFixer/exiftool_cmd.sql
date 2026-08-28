-- SQLite
select 
    --directory,
    --'exiftool -diff "' || digikam_path || '" "' || standard_path || '"' as exiftoll_diff
    --'exiftool -wm cg -TagsFromFile "' || digikam_path || '" -all:all "' || standard_path || '"' as exiftoll_TagsFromFile,
    'ren "' || digikam_path || '" "' || digikam_filename || '_old"' as rename_cmd
from xmp_duplicates;



-- Renamed files
select
    --cr2.file_path as cr2_path,
    --cr2.file_name as cr2_filename,
    --xmp.file_path as xmp_path,
    --'exiftool -diff "' || cr2.file_path || '" "' || xmp.file_path || '"' as exiftoll_diff
    --'exiftool -wm cg -TagsFromFile "' || cr2.file_path || '" -all:all "' || xmp.file_path || '"' as exiftoll_TagsFromFile
    'ren "' || cr2.file_path || '" "' || cr2.file_name || '_old"' as rename_cmd
from xmp_files as cr2
inner join xmp_files as xmp on cr2.renamed_xmp_file = xmp.renamed_xmp_file and lower(xmp.file_name) not like '%.cr2.%'
where lower(cr2.file_name) like '%.cr2.%';



-- Vérification des doublons
select *, 
    (select count(*) from xmp_files as xm2 where replace(xm2.file_path, xm2.file_name, '') = replace(xm1.file_path, xm1.file_name, '') and xm2.base_name = xm1.base_name) as duplicate_count
from xmp_files as xm1
where duplicate_count > 1


-- XMP par type et propriétaire
select xmp_type, xmp_owner, count(*) as count
from xmp_files
group by xmp_type, xmp_owner


-- XMP sans fichier image correspondant
select *
from xmp_files
where image_file_path LIKE '(%)'

-- Standard XMP restants
select *
from xmp_files
where xmp_type = 'std'


-- Fichiers renommés
select *
from xmp_files
where renamed_xmp_file IS NOT NULL

