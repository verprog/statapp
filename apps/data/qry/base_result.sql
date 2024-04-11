with 
userdata as
(SELECT 
coalesce(to_char(uv."RegistrationDate",'yyyy-mm-dd'),'2017-01-01') REGISTRATIONDATE,
uv."Id" as ID,
coalesce(uv."Region",'Не визначений') as REGION,
coalesce(uv."LegalForm",'Не визначено') as LEGALFORM,
coalesce(uv."Gender",'Не визначено') as GENDER
FROM 
public."UsersView" uv 
group by coalesce(to_char(uv."RegistrationDate",'yyyy-mm-dd'),'2017-01-01'),uv."Id",uv."Region",uv."LegalForm",uv."Gender"),
landdata as (SELECT lpl."Id" as ID, sum(coalesce(lpl."Area",0)) as AREA
FROM public."LandParcelsView" lpl 
group by lpl."Id"),
animaldata as (SELECT al."Id" as ID, sum(coalesce(al."Quantity",0)) as ANIMAL
FROM public."AnimalsView" al 
group by al."Id"),
userprogdata as (
SELECT 
/*coalesce(to_char(uac."CreateAt",'yyyy-mm-dd'),'2017-01-01') DATEAPPLICATION,*/
uac."Id" as ID,
sum(coalesce(uac."Amount",0)) as GIFTAMOUNT
FROM public."UserApplicationsView" uac
group by uac."Id"),
region as (
SELECT left(dv."Code",19) as CATOTTG_REGION,dv."Name" 
from public."DictionariesView" dv where dv."Id" between 122523 and 154269 and right(dv."Code",1) in ('О','M'))
select 
ud.REGISTRATIONDATE,rg.CATOTTG_REGION,ud.REGION,ud.LEGALFORM,
sum(coalesce(AREA,0)) AREA,sum(coalesce(ad.ANIMAL,0)) ANIMAL,sum(coalesce(up.GIFTAMOUNT,0)) GIFTAMOUNT,count(ud.ID) cntuser
from 
userdata as ud
left join landdata as ld on ld.ID=ud.ID
left join animaldata as ad on ad.ID=ud.ID
left join userprogdata as up on up.ID=ud.ID
left join region as rg on rg."Name"=ud.REGION
group by ud.REGISTRATIONDATE,rg.CATOTTG_REGION,ud.REGION,ud.LEGALFORM
order by 1 desc