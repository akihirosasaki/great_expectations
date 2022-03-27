select
  *
from
  {{ source('asasaki_data_infra_dataset', 'customer') }}
where
  gender_cd = "0" -- 0はgender="男性"