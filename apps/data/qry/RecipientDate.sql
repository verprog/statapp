SELECT  
pv."Name" as "NameProgram",
pv."type" as "TypeProgram",
uv."LegalForm",
uv."Id",
uv."Region",
uv."District",
uv."DrfoCode",
to_char(uav."CreateAt",'yyyy-mm-dd') "CreateAt",
pv.organization,
sum(coalesce(uav."DesiredAmount",0)) "DesiredAmount",
sum(coalesce(uav."Amount",0)) "ProvidedAmount",
uv."Area",
sum(coalesce(uav."LandParcelCount",0)) "LandParcelCount",
av."QuantityAnimal",
sum(coalesce(uav."AnimalCount",0)) "AnimalCount"
FROM 
public."ProgramsView" pv
join public."UserApplicationsView" uav on uav."ProgramId"=pv."Id" 
join (select uv."Id",coalesce(uv."LegalForm",'Не визначено') "LegalForm",coalesce(uv."Region",'Не визначений') as "Region",
coalesce(uv."District",'Не визначений') "District",uv."DrfoCode",max(uv."Group1LandParcelArea") "Area" 
		from public."UsersView" uv group by uv."Id", uv."LegalForm",uv."Region",uv."District",uv."DrfoCode" ) uv on uv."Id"=uav."Id"
left join (select av."Id",sum(av."Quantity") as "QuantityAnimal" from public."AnimalsView" av group by av."Id") av on av."Id"=uv."Id"
group by pv."Name",pv."type",uv."LegalForm",uv."Id",uv."Region",uv."District",uv."DrfoCode",to_char(uav."CreateAt",'yyyy-mm-dd'),
pv.organization,uv."Area",av."QuantityAnimal"