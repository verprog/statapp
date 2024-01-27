select 
coalesce(uv."LegalForm",'�� ���������') "LegalForm",
coalesce(dv."Name",'�� ����������') "Region",
coalesce(lpv."PropRight",'�� ����������') "PropRight",
coalesce(lpv."Purpose",'�� ����������') "Purpose",
sum(coalesce(lpv."Area",0)) "Area",
count(lpv."RegionId") "Subject"
FROM 
public."LandParcelsView" lpv
left join (select uv."Id", uv."LegalForm" from public."UsersView" uv group by uv."Id", uv."LegalForm" ) uv on uv."Id"=lpv."Id"
left join public."DictionariesView" dv on dv."Id"= lpv."RegionId"
group by coalesce(uv."LegalForm",'�� ���������'),coalesce(dv."Name",'�� ����������'),coalesce(lpv."PropRight",'�� ����������'),
coalesce(lpv."Purpose",'�� ����������')