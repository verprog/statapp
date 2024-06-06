with dictviews as (select *from public."DictionariesView" dv where dv."Id" between 122523 and 154269 and right(dv."Code",1) in ('�','M'))
select 
uv."LegalForm",
left(dv."Code",19) as CATOTTG_REGION,
uv."Region",
al."Name",
al."SexName", 
case 
when trim(al."SexName") in ('������','����','����','������','³��������','������','������','����������','������ (�������)',
'³��������',
'������',
'����',
'������',
'������',
'������ (�������)',
'����������',
'���������� (�������)',
'������',
'����',
) then '������'
when trim(al."SexName") in ('����, �������','��������','������,�����','����, �������','������, ���������',
'��������',
'����, �������',
'����, ������� ',
'����, ������� (�������)',
'������, ���������',
'������,�����',
'������',
'�����',
'����, �������') then '�����' end "AnimalGender",
sum(coalesce(al."Quantity",0)) as "animal"
FROM 
public."AnimalsView" al 
left join (select uv."Id",coalesce(uv."LegalForm",'�� ���������') "LegalForm",coalesce(uv."Region",'�� ���������') as "Region" 
from public."UsersView" uv group by uv."Id", uv."LegalForm",uv."Region" ) uv on uv."Id"=al."Id"
left join dictviews dv on dv."Name"=uv."Region"
group by uv."LegalForm",left(dv."Code",19),uv."Region",al."Name",al."SexName"