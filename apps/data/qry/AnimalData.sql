select 
uv."LegalForm",
uv."Region",
al."Name",
al."SexName", 
case 
when trim(al."SexName") in ('������','����','����','������','³��������','������','������','����������','������ (�������)') then '������'
when trim(al."SexName") in ('����, �������','��������','������,�����','����, �������','������, ���������') then '�����' end "AnimalGender",
sum(coalesce(al."Quantity",0)) as "animal"
FROM 
public."AnimalsView" al 
left join (select uv."Id",coalesce(uv."LegalForm",'�� ���������') "LegalForm",coalesce(uv."Region",'�� ���������') as "Region" 
from public."UsersView" uv group by uv."Id", uv."LegalForm",uv."Region" ) uv on uv."Id"=al."Id"
-- where uv."Id"=4
group by uv."LegalForm",uv."Region",al."Name",al."SexName"