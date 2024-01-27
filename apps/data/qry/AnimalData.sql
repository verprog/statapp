select 
uv."LegalForm",
uv."Region",
al."Name",
al."SexName", 
case 
when trim(al."SexName") in ('Свинка','Коза','Ярка','Телиця','Вівцематка','Кобила','Корова','Свиноматка','Свинка (товарна)') then 'Самиці'
when trim(al."SexName") in ('Цапи, козлики','Жеребець','Бугаєць,бугай','Кнур, кнурець','Барани, баранчики') then 'Самці' end "AnimalGender",
sum(coalesce(al."Quantity",0)) as "animal"
FROM 
public."AnimalsView" al 
left join (select uv."Id",coalesce(uv."LegalForm",'Не визначено') "LegalForm",coalesce(uv."Region",'Не визначено') as "Region" 
from public."UsersView" uv group by uv."Id", uv."LegalForm",uv."Region" ) uv on uv."Id"=al."Id"
-- where uv."Id"=4
group by uv."LegalForm",uv."Region",al."Name",al."SexName"