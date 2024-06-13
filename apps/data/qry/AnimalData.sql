with dictviews as (select *from public."DictionariesView" dv where dv."ParentId"=122523)
select 
uv."LegalForm",
left(dv."Code",19) as CATOTTG_REGION,
uv."Region",
al."Name",
al."SexName", 
case 
when trim(al."SexName") in ('Свинка','Коза','Ярка','Телиця','Вівцематка','Кобила','Корова','Свиноматка','Свинка (товарна)',
'Вівцематка',
'Кобила',
'Коза',
'Корова',
'Свинка',
'Свинка (товарна)',
'Свиноматка',
'Свиноматка (товарна)',
'Телиця',
'Ярка'
) then 'Самиці'
when trim(al."SexName") in ('Цапи, козлики','Жеребець','Бугаєць,бугай','Кнур, кнурець','Барани, баранчики',
'Жеребець',
'Кнур, кнурець',
'Кнур, кнурець ',
'Кнур, кнурець (товарна)',
'Барани, баранчики',
'Бугаєць,бугай',
'Валухи',
'Мерин',
'Цапи, козлики') then 'Самці' end "AnimalGender",
sum(coalesce(al."Quantity",0)) as "animal"
FROM 
public."AnimalsView" al 
left join (select uv."Id",coalesce(uv."LegalForm",'Не визначено') "LegalForm",coalesce(uv."Region",'Не визначено') as "Region" 
from public."UsersView" uv group by uv."Id", uv."LegalForm",uv."Region" ) uv on uv."Id"=al."Id"
left join dictviews dv on dv."Name"=uv."Region"
group by uv."LegalForm",left(dv."Code",19),uv."Region",al."Name",al."SexName"