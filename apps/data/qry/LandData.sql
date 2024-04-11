with dictviews as (select *from public."DictionariesView" dv where dv."Id" between 122523 and 154269)
select 
coalesce(uv."LegalForm",'Не визначено') "LegalForm",
left(dv."Code",19) as CATOTTG_REGION,
coalesce(dv."Name",'Не визначений') "Region",
left(dv2."Code",19) as CATOTTG_DISTRICT,
coalesce(dv2."Name",'Не визначений') "District",
left(dv3."Code",19) as CATOTTG_COMMUNITY,
coalesce(dv3."Name",'Не визначений') "Community",
coalesce(lpv."PropRight",'Не визначений') "PropRight",
coalesce(lpv."Purpose",'Не визначений') "Purpose",
sum(coalesce(lpv."Area",0)) "Area",
count(lpv."RegionId") "Subject"
FROM 
public."LandParcelsView" lpv
left join (select uv."Id", uv."LegalForm" from public."UsersView" uv group by uv."Id", uv."LegalForm" ) uv on uv."Id"=lpv."Id"
left join dictviews dv on dv."Id"= lpv."RegionId"
left join dictviews dv2 on dv2."Id"= lpv."DistrictId"
left join dictviews dv3 on dv3."Id"= lpv."LocalCommunityId"
group by coalesce(uv."LegalForm",'Не визначено'),coalesce(dv."Name",'Не визначений'),coalesce(lpv."PropRight",'Не визначений'),
coalesce(lpv."Purpose",'Не визначений'),left(dv."Code",19)
,left(dv2."Code",19),coalesce(dv2."Name",'Не визначений')
,left(dv3."Code",19),coalesce(dv3."Name",'Не визначений')