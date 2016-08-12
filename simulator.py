from collections import namedtuple
import itertools

Rune = namedtuple('Rune', '符文类型 部位 稀有等级 防御 防百 体力 体百 攻击 攻百 攻速 暴击 暴伤 命中 抵抗')
Improvement = namedtuple('Improvement', '防御 防百 体力 体百 攻击 攻百 攻速 暴击 暴伤 命中 抵抗')
Monster = namedtuple('Monster', '属性 魔灵 觉醒魔灵 体力 攻击力 防御力 攻击速度 暴击率 暴击伤害 效果抵抗 效果命中')

prop_list = ['防御', '防百', '体力', '体百', '攻击', '攻百', '攻速', '暴击', '暴伤', '命中', '抵抗']

防御值 = 0
防百值 = 1
体力值 = 2
体百值 = 3
攻击值 = 4
攻百值 = 5
攻速值 = 6
暴击值 = 7
暴伤值 = 8
命中值 = 9
抵抗值 = 10

属性表 = [防御值,防百值,体力值,体百值,攻击值,攻百值,攻速值,暴击值,暴伤值,命中值,抵抗值]

def csv_import(path: str) -> list:
    '''
    读取csv符文数据库
    '''
    result_list = []
    file = open(path, 'r')
    skip_first_line = file.readline()
    text_list = file.readlines()
    for line in text_list:
        if line != "":
            result_list.append(line.rstrip('\n').split(','))
    return result_list

def generate_collection(input_list : list) -> list:
    '''
    单数据列表转换Rune型数据或Monster型数据
    '''    
    C = []
    for item in input_list:
        if item[0] not in ['水', '火', '风', '光', '暗']:
            temp = Rune._make(item)
        else:
            temp = Monster._make(item)
        C.append(temp)
    return C

def get_position(rune_combine: list) -> list:
    '''
    获取已取得符文的符文位置
    '''
    position_list = []
    for rune in rune_combine:
        position_list.append(rune.部位)
    return position_list

def rune_set_choose_four(rune_list : list) -> list:
    '''
    返回所有选定4件套的可能搭配合集
    '''
    RC = []
    for rune_combine in itertools.combinations(rune_list, 4):
        position_list = get_position(rune_combine)
        if len(set(position_list)) == 4:
            RC.append(rune_combine)
    return RC

def get_position_for_two(position_list: list) -> list:
    '''
    获取剩余2个位置的位置数据
    '''
    result = []
    full_position = ['1','2','3','4','5','6']
    for p in full_position:
        if p not in position_list:
            result.append(p)
    return result

def get_rune_by_type(rune_list: list, t: str) -> list:
    '''
    根据符文类型筛选符文
    '''
    result = []
    for rune in rune_list:
        if rune.符文类型 == t:
            result.append(rune)
    return result

def get_rune_by_position(rune_list: list, p: str) -> list:
    '''
    根据位置筛选符文
    '''
    result = []
    for rune in rune_list:
        if rune.部位 == p:
            result.append(rune)
    return result

def set_effect_for_two(rune1: Rune, rune2: Rune) -> list:
    '''
    获取2件套效果
    '''
    if rune1.符文类型 == rune2.符文类型:
        if rune1.符文类型 == "祝福":
            return [体百值, 15]
        elif rune1.符文类型 == "守护":
            return [防百值, 15]
        elif rune1.符文类型 == "刀刃":
            return [暴击值, 12]
        elif rune1.符文类型 == "忍耐":
            return [抵抗值, 20]
        elif rune1.符文类型 == "集中":
            return [命中值, 20]
        else:
            return [66, 66]
    else:
        return [66, 66]

def get_value(rune:Rune, prop:str) -> int:
    '''
    获取Rune数据中属性数值
    '''
    if prop == "防御":
        return int(rune.防御)
    elif prop == "防百":
        return int(rune.防百)
    elif prop == "体力":
        return int(rune.体力)
    elif prop == "体百":
        return int(rune.体百)
    elif prop == "攻击":
        return int(rune.攻击)
    elif prop == "攻百":
        return int(rune.攻百)
    elif prop == "攻速":
        return int(rune.攻速)
    elif prop == "暴击":
        return int(rune.暴击)
    elif prop == "暴伤":
        return int(rune.暴伤)
    elif prop == "命中":
        return int(rune.命中)
    elif prop == "抵抗":
        return int(rune.抵抗)


def total_improvement(four_set: list, other_two: list, spd: int) -> Improvement:
    '''
    计算总体提升值
    '''
    #Rune = namedtuple('Rune', '符文类型 部位 稀有等级 防御 防百 体力 体百 攻击 攻百 攻速 暴击 暴伤 命中 抵抗')
    #Improvement = namedtuple('Improvement', '防御 防百 体力 体百 攻击 攻百 攻速 暴击 暴伤 命中 抵抗')
    improve_data = [0,0,0,0,0,0,0,0,0,0,0]
    for rune in four_set:
        for 属性 in 属性表:
            improve_data[属性] += get_value(rune, prop_list[属性])
    if four_set[0].符文类型 == "激怒":
        four_set_effect = [暴伤值, 40]
    elif four_set[0].符文类型 == "猛攻":
        four_set_effect = [攻百值, 35]
    elif four_set[0].符文类型 == "迅速":
        four_set_effect = [攻速值, round(spd/100*25)]
    else:
        four_set_effect = [66, 66]
    
    for rune in other_two:
        for 属性 in 属性表:
            improve_data[属性] += get_value(rune, prop_list[属性])

    two_set_effect = set_effect_for_two(other_two[0], other_two[1])

    if 66 not in two_set_effect:
        improve_data[two_set_effect[0]] += two_set_effect[1]

    if 66 not in four_set_effect:
        improve_data[four_set_effect[0]] += four_set_effect[1]
        
    result = Improvement._make(improve_data)
    
    return result

def get_monster(monster_list: list, att: str, name: str) -> Monster:
    for m in monster_list:
        if m.属性 == att and m.魔灵 == name:
            return m

def get_monster_name(m:Monster)->str:
    return m.魔灵

def get_monster_attr(m:Monster)->str:
    return m.属性


def main():
    '''
    主体程序
    '''
    print( '''
|----------------------------------------|
|summoners war runes simulator BETA v1.0 |
|                                        |
|         WHO USE WHO KNOW~ 233          |
|                                        |
| 01. 目标魔灵属性 （水,火,风,光,暗）    |
| 02. 目标魔灵名字 （觉醒前）            |
| 03. 4件套符文种类 ( 暴走, 迅速.... )   |
| 04. 理想体力（默认10000）              |
| 05. 理想攻击 （默认  0）               |
| 06. 理想防御 （默认  0）               |
| 07. 理想攻速 （默认  0）               |
| 08. 理想暴击 （默认  0）               |
| 09. 理想暴伤 （默认  0）               |
| 10. 理想抵抗 （默认  0）               |
| 11. 理想命中 （默认  0）               |
|----------------------------------------|
           ''')
    
    rune_list = generate_collection(csv_import("runes.csv"))
    monster_list = generate_collection(csv_import("monsters.csv"))

    attr_list = []
    name_list = []
    
    for m in monster_list:
        attr_list.append(get_monster_attr(m))
        name_list.append(get_monster_name(m))

    while True:
        monster_attribute = input("目标魔灵属性： ")
        if monster_attribute in attr_list:
            break
        else:
            print("错误： 输入的属性有错误。")
            
    while True:        
        monster_name = input("目标魔灵名字： ")
        if monster_name in name_list:
            break
        else:
            print("错误", monster_name,"不在当前数据库中，请重试。")

    while True:
        rune_type = input("4件套符文类型： ")
        if rune_type in ["暴走","迅速","吸血","绝望","激怒","猛攻"]:
            break
        else:
            print("错误： 输入需要计算的4件套属性。")


    理想体力 = int(input("默认10000  理想体力：") or "10000")
    理想攻击 = int(input("默认    0  理想攻击：") or "0")
    理想防御 = int(input("默认    0  理想防御：") or "0")
    理想攻速 = int(input("默认    0  理想攻速：") or "0")
    理想暴击 = int(input("默认    0  理想暴击：") or "0")
    理想暴伤 = int(input("默认    0  理想暴伤：") or "0")
    理想抵抗 = int(input("默认    0  理想抵抗：") or "0")
    理想命中 = int(input("默认    0  理想命中：") or "0")

    target_monster = get_monster(monster_list, monster_attribute, monster_name)
    monster_data = [int(target_monster.体力),int(target_monster.攻击力),int(target_monster.防御力),int(target_monster.攻击速度),int(target_monster.暴击率),int(target_monster.暴击伤害),int(target_monster.效果抵抗),int(target_monster.效果命中)]
    print("\n\n符文数量较多，计算量略大，请耐心等候片刻.........\n\n")
    
    rune_type_list = get_rune_by_type(rune_list, rune_type)
    four_set = rune_set_choose_four(rune_type_list)

    full_combine_list = []

    
    for subset in four_set:
        rest_two_position =  get_position_for_two(get_position(subset))
        first_position = get_rune_by_position(rune_list, rest_two_position[0])
        second_position = get_rune_by_position(rune_list, rest_two_position[1])
        combination = list(itertools.product(first_position, second_position))
        for other_two in combination:
            improve_data = total_improvement(subset, other_two, int(target_monster.攻击速度))
            full_set = list(subset)
            full_set.extend(list(other_two))
            full_combine_list.append([full_set, improve_data, []])


            
    for choice in full_combine_list:
        final_state = []
        final_state.append(round(monster_data[0] + choice[1].体力+ (monster_data[0]/100)*choice[1].体百))   #体力      
        final_state.append(round(monster_data[1] + choice[1].攻击+ (monster_data[1]/100)*choice[1].攻百))   #攻击力
        final_state.append(round(monster_data[2] + choice[1].防御+ (monster_data[2]/100)*choice[1].防百))   #防御力
        final_state.append(round(monster_data[3] + choice[1].攻速))   #攻击速度
        final_state.append(round(monster_data[4] + choice[1].暴击))   #暴击率
        final_state.append(round(monster_data[5] + choice[1].暴伤))   #暴击伤害
        final_state.append(round(monster_data[6] + choice[1].抵抗))   #效果抵抗
        final_state.append(round(monster_data[7] + choice[1].命中))   #效果命中
        choice[2] = final_state
        
    index = 1
    final_result = []
    for i in range(0, len(full_combine_list)):
        if full_combine_list[i][2][0] >= 理想体力 and full_combine_list[i][2][1] >= 理想攻击 and full_combine_list[i][2][2] >= 理想防御 and full_combine_list[i][2][3] >= 理想攻速 and full_combine_list[i][2][4] >= 理想暴击 and full_combine_list[i][2][5] >= 理想暴伤 and full_combine_list[i][2][6] >= 理想抵抗 and full_combine_list[i][2][7] >= 理想命中:
            print("搭配方案", index, "强化结果 : ==>")
            print(target_monster.属性, target_monster.魔灵," ： ","体力",full_combine_list[i][2][0],"攻击力",full_combine_list[i][2][1],"防御力",full_combine_list[i][2][2],"攻击速度",full_combine_list[i][2][3],"暴击率",full_combine_list[i][2][4],"暴击伤害",full_combine_list[i][2][5],"效果抵抗",full_combine_list[i][2][6],"效果命中",full_combine_list[i][2][7],'\n')
            index += 1
            final_result.append(full_combine_list[i][0])

    if index == 1:
        print("无法搭配当前输入的参数")
    else:
        while True:
            user_choose = input("需要查看的方案序号( 输入 0 退出)： ")
            if int(user_choose) <= index-1 and int(user_choose) >= 1:
                print("搭配方案",user_choose , " ==>")
                slot = ['1','2','3','4','5','6']
                for s in slot:
                    for rune in final_result[int(user_choose)-1]:
                        if rune.部位 == s:
                            print("///>", s,"号位：", rune)
            elif user_choose == 'q' or user_choose == 'Q':
                break
            else:
                print("错误：该序号方案不存在。")

    return

def TOP_LEVEL_ARCHITECTURE():
    while True:
        main()
        flag = input("\n(Q)uit? >")
        if flag == 'q' or flag == 'Q':
            break
        else:
            continue
    return


TOP_LEVEL_ARCHITECTURE()

