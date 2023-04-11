import random
# pomocne premenne
size = 0
index = 0
column_size = 3
number_of_road_types = 2
# premenne popisujuce panacika A
# panacik A
figure_A = 'A'
# startova pozicia
start_coord_A = [0, 0]
# aktualna pozicia, ktora sa bude menit
act_coord_A = []
# aktualna pozicia pohybu v ramci mapy
act_moves_index_A = [0]
# pocet krokov ktory zostal panacikovi v ramci mapovania krokov
steps_left_A = [0]
# pomocne pole domcekov panacika
house_A = []
# pole ktore obsahuje pozicie domcekov v ramci celeho hracieho pola
coords_house_A = list()
# pole ktore obsahuje iba jednu hodnotu, a to pocet
# kol ktore presiel panacik
count_winner_A = [0]
# mapa krokov panacika
moves_A = []

# premenne popisujuce panacika B (to iste co v bloku pred tym)
figure_B = 'B'
start_coord_B = [0, 0]
act_coord_B = []
act_moves_index_B = [0]
steps_left_B = [0]
house_B = []
coords_house_B = []
count_winner_B = [0]
moves_B = []


# tlacshachovnica
def print_game(field):
    # ulohou tejto funkcie je vytlacit
    # priebezny stav hry(pola), vsetkych jeho panacikov
    # ktory su na ceste, a aj tych ktore su v domcekoch

    for row_index in range(len(field)):
        for column_index in range(len(field)):
            # ked panacik A presiel uz cele kolo,
            # daj ho do domceku
            if coords_house_A:
                # ked prechadzame cez poziciu, kde stoji panacik
                if row_index == coords_house_A[0][0] and column_index == coords_house_A[0][1]:
                    # ked pomocne pole house_A je neprazdne
                    if house_A:
                        # vytiahneme panacika z house_A a dame ho do field
                        # na poziciu domceka, vymazav prislusne koordinaty
                        # z coords_house
                        field[row_index][column_index] = house_A.pop()
                        coords_house_A.pop(0)
            # ked panacik B presiel uz cele kolo,
            # daj ho do domceku
            if coords_house_B:
                # ked prechadzame cez poziciu, kde stoji panacik
                if row_index == coords_house_B[0][0] and column_index == coords_house_B[0][1]:
                    # ked pomocne pole house_B je neprazdne
                    if house_B:
                        # vytiahneme panacika z house a dame ho do field
                        # na poziciu domceka, vymazav prislusne koordinaty
                        # z coords_house
                        field[row_index][column_index] = house_B.pop()
                        coords_house_B.pop(0)
            # vytlac aktualnu poziciu panacika A
            if act_coord_A[0] == row_index and act_coord_A[1] == column_index:
                print(figure_A + ' ', end='')
            # vytlac aktualnu poziciu panacika B
            elif act_coord_B[0] == row_index and act_coord_B[1] == column_index:
                print(figure_B + ' ', end='')
            # vytlac ostatne znaky z pola
            else:
                if len(field[row_index][column_index]) == 1:
                    print(field[row_index][column_index] + ' ', end='')
                else:
                    print(field[row_index][column_index], end='')

        print('\n', end='')


def create_road(type_of_road, index):
    # generuju sa šablony ciest z ktorych sa
    # potom sklada cele pole
    if type_of_road == 1:
        road = ['*'] * (index + 2) + ['D'] + ['*'] * (index + 1)
    else:
        road = ['*', '*'] + ['D'] * index + ['X'] + ['D'] * index + ['*']
    return road


def assign_road_to_field(field, road, size, index, type_of_road):
    # šablony vygenerovane funkciou create_road
    # podla ich typu priraduju sa do pola

    if type_of_road == 1:
        # prirad dve horizontalne šablony
        field[index + 1] = road
        field[index + 3] = road[:]
        # prirad dve vertikalne šablony
        for row_index in range(size):
            for column_index in range(size):
                if column_index == index + 1 or column_index == index + 3:
                    field[row_index][column_index] = road[row_index]
    else:
        # prirad šablonu do riadku
        field[index + 2] = road
        # prirad šablonu do stlpca
        for row_index in range(size):
            for column_index in range(size):
                if column_index == index + 2:
                    field[row_index][column_index] = road[row_index]


def map_the_road(field):
    # vytvorit šablonu cesty a zapisat ju do pola
    # podla toho aky typ cesty bol vygenerovany
    for i in range(1, number_of_road_types + 1):
        road = create_road(i, index)
        assign_road_to_field(field, road, size, index, i)


def index_the_field(field):
    # vytvara sa indexovanie pola
    # co znamena, ze indexy budu sucastou
    # pola
    for row_index in range(size):
        for column_index in range(size):
            # podmienky popisujuce specificky
            # posun indexovania riadkov dole o jeden,
            # a indexovania stlpcov doprava o jeden
            # aby indexovanie bolo nazorne spravne
            if row_index == 0 and column_index >= 1:
                field[row_index][column_index] = str(column_index - 1)
            if column_index == 0 and row_index >= 1:
                field[row_index][column_index] = str(row_index - 1)


# genshachovnica
def create_field(n):
    # generuje sa prazdne pole rozmeru n*n
    field = []
    for r in range(n):
        field.append([' '] * (n))
    return field


def get_size_from_user():
    # ziada usera o rozmer pola a robi
    # to dovtedy, kym user nezada spravne cislo(neparne)
    # pri zadani parneho cisla vrati warning
    global size
    while True:
        size = int(input("Enter the size of field: ")) + 1
        if (size - 1) % 2 == 1:
            break
        else:
            print("WARNING: Size of field must be odd!")


def set_game_config():
    # nastavuju sa do globalnych premennych
    # configuracie hry, ako napriklad
    # startova a aktualna pozicia kazdeho hraca,
    # mapa ich krokov.

    global index
    global moves_A
    global moves_B
    global start_coord_A
    global start_coord_B
    global coords_house_A
    global coords_house_B
    global act_coord_A
    global act_coord_B

    index = int((size - 4) / 2)

    # startova a aktualna pozicia panacika A
    start_coord_A = [1, index + 3]
    act_coord_A = start_coord_A[:]

    # naplna sa pole pozicii domcekov A
    for i in range(2, index+2):
        coords_house_A.append([i, index+2])

    # naplna sa pole pozicii domcekov B
    for i in range(size-2, size-2-index, -1):
        coords_house_B.append([i, index+2])

    # startova a aktualna pozicia panacika B
    start_coord_B = [size - 1, index + 1]
    act_coord_B = start_coord_B[:]

    # mapa krokov panacikov A a B
    moves_A = [['row', '+', index],
               ['column', '+', index],
               ['row', '+', column_size - 1],
               ['column', '-', index],
               ['row', '+', index],
               ['column', '-', column_size - 1],
               ['row', '-', index],
               ['column', '-', index],
               ['row', '-', column_size - 1],
               ['column', '+', index],
               ['row', '-', index],
               ['column', '+', column_size - 1]]
    moves_B = moves_A[6:]+moves_A[:6]


def prepare_field():
    # pripravi nastavenia hry a vytvori hracie pole
    global size
    # ziskaj od usera rozmery pola
    get_size_from_user()
    # nastav potrebne na hranie premenne
    set_game_config()
    # vytvor prazdne pole rozmeru ktory poziadal user
    field = create_field(size)
    # napln pole cestami pre panacikov
    map_the_road(field)
    # indexuj pole cislami stlpcov a riadkov
    index_the_field(field)
    return field


def step(act_coord, move):
    # urobi jeden krok v smere danom parametrom move
    direction = move[0]
    sign = move[1]
    # ked sa hybeme vertikalne a dole
    if direction == 'row' and sign == '+':
        act_coord[0] += 1
    # ked sa hybeme horizontalne a dolava
    elif direction == 'row' and sign == '-':
        act_coord[0] -= 1
    # ked sa hybeme vertikalne a hore
    elif direction == 'column' and sign == '+':
        act_coord[1] += 1
    # ked sa hybeme horizontalne a doprava
    elif direction == 'column' and sign == '-':
        act_coord[1] -= 1


def check_position(figure, act_coord, start_coord, house, count_winner):
    # skontroluje po kazdom kroku panacika, ci nie je uz nahodou
    # naspat v startovom mieste
    if act_coord == start_coord:
        # pridame panacika do pomocneho pola
        house.append(figure)
        # a inkrementujeme pocet prejdenych kol panacikom
        count_winner[0] += 1
        return True
    else:
        return False


def make_steps(rand_int, steps_left, moves, act_moves_index, act_coord, figure, start_coord, house, count_winner):
    # funkcia urobi potrebny pocet krokov panacikom
    while True:
        # ked nemas kroky, zober kroky v smere danom dalsim
        # mapovanim krokov
        if steps_left[0] == 0:
            steps_left[0] = moves[act_moves_index[0]][2]

        while True:
            # urobi sa krok a skontroluje sa
            # ci nie je panacik v startovej pozicii
            # ked je a zaroven vsetky domceky su obsadene,
            # tak mozeme vyskocit z cyklu

            step(act_coord, moves[act_moves_index[0]])
            if check_position(figure=figure,
                              act_coord=act_coord,
                              start_coord=start_coord,
                              house=house,
                              count_winner=count_winner):
                if count_winner[0] >= index:
                    rand_int = 0
                    break
            rand_int -= 1
            steps_left[0] -= 1
            # ked sme v rohu, ale este nie sme tam kde sme chceli byt
            if steps_left[0] == 0 and rand_int != 0:
                act_moves_index[0] += 1
                act_moves_index[0] = act_moves_index[0] % len(moves)
                break
            # ked sme v rohu a uz sme prisli
            elif steps_left[0] == 0 and rand_int == 0:
                act_moves_index[0] += 1
                act_moves_index[0] = act_moves_index[0] % len(moves)
                break
            # ked sme v strede hrany a uz sme prisli
            elif steps_left[0] != 0 and rand_int == 0:
                break
        if rand_int <= 0:
            break


def main():
    # hlavna funkcia programu,
    # kde bezi cela hra v cykle
    # striedaju sa panaciky
    # cize chodia po jednom
    # a po kazdom tahu sa vytlaci stav hry a
    # pred kazdym vypisom pola vypise sa
    # panack, ktory ma chodit a randome cislo tahu
    # Na konci simulacie sa vypise vitaz.

    global steps_left_A
    global act_coord_A
    global act_moves_index_A
    global moves_A
    global figure_A
    global house_A
    global count_winner_A
    global start_coord_A
    # vytvorime indexovane pole s panacikami
    field = prepare_field()
    # vytlacime vysledok
    print_game(field=field)
    counter = 0
    # kym ani jeden z panacikov nema obsadene domceky
    while count_winner_A[0] < index and count_winner_B[0] < index:
        # vygeneruje sa nahodne cislo
        rand_int = random.randint(1, 6)
        # ked counter je parne cislo, chodi A
        if counter % 2 == 0:
            print("\nRandom move: "+figure_A, rand_int)
            make_steps(rand_int=rand_int,
                       steps_left=steps_left_A,
                       act_coord=act_coord_A,
                       act_moves_index=act_moves_index_A,
                       moves=moves_A,
                       figure=figure_A,
                       house=house_A,
                       count_winner=count_winner_A,
                       start_coord=start_coord_A
                       )
        # ked nie je counter neparne cislo, chodi B
        else:
            print("\nRandom move: "+figure_B, rand_int)
            make_steps(rand_int=rand_int,
                       steps_left=steps_left_B,
                       act_coord=act_coord_B,
                       act_moves_index=act_moves_index_B,
                       moves=moves_B,
                       figure=figure_B,
                       house=house_B,
                       count_winner=count_winner_B,
                       start_coord=start_coord_B,
                       )
        # po kazdom tahu vytlaci sa vysledok
        print_game(field=field)
        counter += 1
    # podla toho kto ma viac obsadenych domcekov
    # ten je vitaz
    if count_winner_A > count_winner_B:
        print("Player A win!")
    elif count_winner_B > count_winner_A:
        print(f"Player B win!")


main()
