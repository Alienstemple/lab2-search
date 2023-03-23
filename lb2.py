from yargy.tokenizer import MorphTokenizer
from IPython.display import display
from yargy import Parser, rule, and_, not_, or_
from yargy.interpretation import fact
from yargy import interpretation as interp
from yargy.predicates import gram, in_, eq
from yargy.relations import gnc_relation
from yargy.pipelines import morph_pipeline

moto_text = """
Классика
Мотоцикл классической компоновки. Наиболее универсальные мотоциклы, исторически 
предшествовали всем остальным. Мотоциклы этого типа обеспечивают прямую посадку. 
В отличие от мотоциклов спортивного стиля лишены аэродинамических обтекателей
Спортивные
Пример «спортбайка» — Suzuki Hayabusa (1999), Япония
Мотоциклы этого типа проектируются в расчёте на максимальные динамические качества
 при езде по дорогам с качественным твёрдым покрытием.
По сравнению с классической компоновкой имеют худшие показатели экономичности, 
безопасности и удобства управления. Для снижения аэродинамического сопротивления 
на больших скоростях, как правило, имеют обтекатель двигателя и лобовой обтекатель.
Круизер
Keeway Cruiser-250
Харлей-Дэвидсон Heritage Softail
Название происходит от английского слова «круиз» (англ. cruise — круиз, дальнее 
путешествие). Характеризуется низким сиденьем, удобной вертикальной посадкой, 
мощным двигателем, усиленными тормозами и подвеской. Появился в США в 1930-е годы 
и сохранял популярность до 1960-х. Наиболее известные производители Харлей-Дэвидсон,
 Индиан и Excelsior-Henderson[en].
Круизер не предназначен для быстрой езды или езды по пересечённой местности, его 
предназначение — дальние поездки, вплоть до кругосветных. 
Эндуро
Мотоциклы для внедорожного туризма. Тяжелее кроссовых и менее мощные. Мотоциклы 
эндуро пришли с трасс ралли-рейдов. Потеряв в «болотной» и «пустынной» проходимости, 
они стали комфортней для езды по городским улицам и шоссе, позволяя водителю съехать 
с асфальта и не бояться достаточно серьёзных ухабов, колдобин, бордюров, лестниц 
и прочих сюрпризов. Основные преимущества мотоциклов эндуро: малый вес, большие 
ходы подвесок, минимум облицовки и ремонтопригодность.
Honda CRF250F/450F
Honda XR250/400/650
Yamaha TT250R Open Enduro
Suzuki DR-Z400
KTM EX-C250
Минибайк
Mаленький мотоцикл. При своём небольшом весе и размерах он достаточно быстро 
разгоняется и неплохо управляется. Самое трудное в минибайке — научиться держать 
равновесие. Дороги общего пользования для езды на минибайках не очень пригодны, 
зато на картодроме можно отлично погонять.
Тяжёлые мотоциклы
Мотоциклы с боковым прицепом. Большая масса, низкооборотистый и мощный мотор. 
Идеально подходят для езды по бездорожью и перевозки крупногабаритных предметов. 
В ВОВ применялись даже для перевозки небольших пушек. Для дорог общего пользования 
малопригодны из-за небольшой скорости и плохой устойчивости на высоких скоростях. 
Могут оснащаться приводом как на заднее колесо, так и приводом на заднее и колесо 
бокового прицепа, что повышает проходимость на бездорожье, но ограничивает 
максимальную скорость. 
"""

text_lines = moto_text.splitlines()

tokenizer = MorphTokenizer()

print(list(tokenizer('скорость')))


Motocharacteristic = fact(
    'Motocharacteristic',
    ['key', 'value']
)

KEY = morph_pipeline([
    'мощность',
    'управляемость',
    'сидение',
    'посадка',
    'показатели',
    'качества',
    'двигатель',
    'тормоза',
    'скорость',
    'вес',
    'масса',
    'мотор',
    'руль',
    'фары',
    'крылья',
    'топливный бак'
]).interpretation(
    interp.normalized()
)

VALUE = or_(
    gram('ADVB'),
    gram('ADJF')
)

MOTO_CHARACTERISTIC = rule(
    VALUE.interpretation(
        Motocharacteristic.value
    ),
    KEY.interpretation(
        Motocharacteristic.key
    )
).interpretation(
    Motocharacteristic
)

VENDOR = morph_pipeline([
'Suzuki',
'Kawasaki',
'BMW',
'Honda',
'YAMAHA',
'Харлей-Дэвидсон'
]).interpretation(
    interp.normalized()
)

Moto = fact(
    'Moto',
    ['vendor', 'model']
)


INT = type('INT')
LATIN = type('LATIN')
SLASH = eq('/')
DASH = eq('-')

MODEL = rule(  
    rule(LATIN).repeatable(min=1),
    rule(SLASH).optional(),
    rule(DASH).optional(),
    rule(LATIN).optional(),
    rule(INT).repeatable(min=0).optional()
).repeatable(min=1).interpretation(
    Moto.model
)

# MODEL = rule(  # FIXME Suzuki 1
#     INT
# ).interpretation(
#     Moto.model
# )


MOTO = rule(
    VENDOR.interpretation(
        Moto.vendor
    ),
    MODEL.optional().interpretation(
        Moto.model
    ),
).interpretation(
    Moto
)


parser1 = Parser(MOTO_CHARACTERISTIC)
parser2 = Parser(MOTO)

matches1 = []
matches2 = []
for elem in text_lines:
    for match in parser1.findall(elem):
            matches1.append(match.fact)
    for match in parser2.findall(elem):
            matches2.append(match.fact)

print(matches1)
print(matches2)
