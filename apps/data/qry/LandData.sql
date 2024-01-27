select 
coalesce(uv."LegalForm",'Не визначено') "LegalForm",
coalesce(dv."Name",'Не визначений') "Region",
coalesce(lpv."PropRight",'Не визначений') "PropRight",
coalesce(lpv."Purpose",'Не визначений') "Purpose",
sum(coalesce(lpv."Area",0)) "Area",
count(lpv."RegionId") "Subject"
FROM 
public."LandParcelsView" lpv
left join (select uv."Id", uv."LegalForm" from public."UsersView" uv group by uv."Id", uv."LegalForm" ) uv on uv."Id"=lpv."Id"
left join public."DictionariesView" dv on dv."Id"= lpv."RegionId"
group by coalesce(uv."LegalForm",'Не визначено'),coalesce(dv."Name",'Не визначений'),coalesce(lpv."PropRight",'Не визначений'),
coalesce(lpv."Purpose",'Не визначений')