-- SQLite
select 
    --directory,
    --'exiftool -diff "' || digikam_path || '" "' || standard_path || '"' as exiftoll_diff
    --'exiftool -wm cg -TagsFromFile "' || digikam_path || '" -all:all "' || standard_path || '"' as exiftoll_TagsFromFile,
    'ren "' || digikam_path || '" "' || digikam_filename || '_old"' as rename_cmd
from xmp_duplicates;



-- SQLite
select
    --cr2.file_path as cr2_path,
    --cr2.file_name as cr2_filename,
    --xmp.file_path as xmp_path,
    --'exiftool -diff "' || cr2.file_path || '" "' || xmp.file_path || '"' as exiftoll_diff
    --'exiftool -wm cg -TagsFromFile "' || cr2.file_path || '" -all:all "' || xmp.file_path || '"' as exiftoll_TagsFromFile
    'ren "' || cr2.file_path || '" "' || cr2.file_name || '_old"' as rename_cmd
from digikam_xmp as cr2
inner join digikam_xmp as xmp on cr2.renamed_xmp_file = xmp.renamed_xmp_file and lower(xmp.file_name) not like '%.cr2.%'
where lower(cr2.file_name) like '%.cr2.%';


