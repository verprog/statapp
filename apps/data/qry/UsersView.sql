with dictviews as (select *from public."DictionariesView" dv where dv."Id" between 122523 and 154269 and right(dv."Code",1) in ('�','M','P'))
SELECT uv."Id",uv."RegNumber",coalesce(to_char(uv."RegistrationDate",'yyyy-mm-dd'),'2017-01-01') REGISTRATIONDATE,
uv."Gender",uv."LegalForm",uv."DrfoCode",uv."KindName",left(dv."Code",19) as CATOTTG_REGION,coalesce(uv."Region",'�� ����������') as "Region",
left(dv2."Code",19) as CATOTTG_DISTRICT,coalesce(uv."District",'�� ����������') "District",uv."Group1LandParcelArea"
FROM public."UsersView" uv 
	left join dictviews dv on dv."Name"=uv."Region"
	left join dictviews dv2 on dv2."Name"=uv."District"