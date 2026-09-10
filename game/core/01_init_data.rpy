# 01_init_data.rpy

##################################### CHARACTERS #####################################

define artem = Character('Артём', color="#1e82b1", image='artem')
define mother_voice = Character('Голос мамы', color="#d39e61", image='default_char')


######################################## MOBS ########################################

## Для тестового поля боя
default cat = Mob(name="Кошка", current_health = 3, max_health = 3)
default dog = Mob(name="Собака", current_health = 5, max_health = 5)
default test_buttle = ButtleData(active_mobs = {cat.name, dog.name})