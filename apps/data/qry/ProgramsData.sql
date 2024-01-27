SELECT  
to_char(uav."CreateAt",'yyyy-mm-dd') "CreateAt",
uv."LegalForm",
uv."Region",
pv."type" as "TypeProgram",
pv."Name" as "NameProgram",
pv.organization as "organization",
pv."TotalAmount",
sum(coalesce(uav."DesiredAmount",0)) "DesiredAmount",
sum(coalesce(uav."Amount",0)) "ProvidedAmount",
sum(coalesce(uav."LandParcelCount",0)) "LandParcelCount",
sum(coalesce(uav."AnimalCount",0)) "AnimalCount"
FROM 
public."ProgramsView" pv
join public."UserApplicationsView" uav on uav."ProgramId"=pv."Id" 
join (select uv."Id",coalesce(uv."LegalForm",'Не визначено') "LegalForm",coalesce(uv."Region",'Не визначений') as "Region" 
from public."UsersView" uv group by uv."Id", uv."LegalForm",uv."Region" ) uv on uv."Id"=uav."Id"
group by to_char(uav."CreateAt",'yyyy-mm-dd'),uv."LegalForm",uv."Region",pv."type",pv."Name",pv.organization,pv."TotalAmount" 