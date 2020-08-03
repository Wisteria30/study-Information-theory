import math
from heapq import heappush, heappop
from collections import OrderedDict


class Node:
    def __init__(self, left=None, right=None, item=None):
        self.left = left
        self.right = right
        self.item = item

    def __lt__(self, other):
        return 0

od = OrderedDict()


def init_od(item_name):
    global od
    for i in item_name:
        od[i] = ""


# 木の左を0, 右を1とする
def hafuman_decode(hafuman_tree, sign):
    if hafuman_tree.left:
        hafuman_decode(hafuman_tree.left, sign+"0")
    if hafuman_tree.right:
        hafuman_decode(hafuman_tree.right, sign+"1")
    if hafuman_tree.item:
        global od
        od[hafuman_tree.item] = sign
        

def hafuman_sign(item_name, pro):
    hq = []
    init_od(item_name)
    for i in range(len(item_name)):
        heappush(hq, (pro[i], Node(item=item_name[i])))

    while True:
        if len(hq) < 2:
            break
        q1_w, q1_n = heappop(hq)
        q2_w, q2_n = heappop(hq)
        heappush(hq, (q1_w + q2_w, Node(left=q2_n, right=q1_n)))

    _, hafuman_tree = heappop(hq)
    hafuman_decode(hafuman_tree, "")


def runlength_sign(item_name, fixed_runlength):
    init_od(item_name)
    for i in range(len(item_name)):
        od[item_name[i]] = bin(i)[2:].zfill(fixed_runlength)
        

def entropy(div, pro):
    ret = 0
    for i in pro:
        div_i = i/div
        ret += div_i*math.log2(div_i)
    
    return ret * -1


def redundancy(ent, pro):
    log2M = math.log2(len(pro))
    return 1 - (ent / log2M)


def create_expansion_info(expansion_level, div, item_name, pro):
    new_item_name = []
    new_pro = []
    n = len(item_name)
    for i in range(n ** expansion_level):
        tmp_list = []
        tmp_num = 1
        mask = i
        for j in range(expansion_level):
            tmp_list.append(item_name[mask % n])
            tmp_num *= pro[mask % n]
            mask = mask//n
        new_item_name.append("".join(list(reversed(tmp_list))))
        new_pro.append(tmp_num)

    return pow(div, expansion_level), new_item_name, new_pro


def create_runlength_info(runlength_level, div, item_name, pro):
    new_item_name = []
    new_pro = []
    for i in range(runlength_level):
        new_item_name.append(item_name[1]*i+item_name[0])
        new_pro.append(((pro[1]**i) * pro[0]) * (div**(runlength_level-i-1)))
    new_item_name.append(item_name[1]*runlength_level)
    new_pro.append(pro[1]**runlength_level)
    print(runlength_level, div**runlength_level)

    return pow(div, runlength_level), new_item_name, new_pro


def average_symbol_length(div, pro, runlength_level):
    return (1-pow(pro[1]/div, runlength_level))/(pro[0]/div)


def average_runlength_sign_length(div, pro, runlength_level, fixed_runlength):
    print("平均記号長: ", average_symbol_length(div, pro, runlength_level))
    return fixed_runlength / average_symbol_length(div, pro, runlength_level)


def average_sign_length(div, pro, sign_length, expansion_level):
    ret = 0
    for i in range(len(pro)):
        div_i = pro[i]/div
        ret += div_i * sign_length[i]
    return ret / expansion_level


def print_info(div, item_name, pro):
    print("============================")
    print("分母: ", div)
    print("-------------")
    print(*item_name, sep="\t")
    print(*pro, sep="\t")
    print("============================")


if __name__ == "__main__":
    # 入力
    # ---------------------------------
    # 拡大する次元数・ランレングス情報生成 2次拡大情報源なら2, 最大ランレングスN=4なら0 4のように0 ?を空白区切りで順番に
    # 分母
    # 各アイテムの名前
    # 分子を空白区切りで順番
    # 平均符号長を計算するかどうか、符号の長さを入力で取るなら1、ハフマン符号をするなら2、固定長ランレングス符号なら3、計算しないなら0
    # 符号の長さを取るなら、符号の長さを空白区切りで順番に、固定長ランレングス符号なら固定長Lを整数で

    expansion_level = list(map(int, input().split()))
    if len(expansion_level) == 2:
        runlength_level = expansion_level[1]
        expansion_level = 1
    else:
        expansion_level = expansion_level[0]
    div = int(input())
    item_name = list(input().split())
    pro = list(map(int, input().split()))
    is_sign = int(input())

    if "runlength_level" in locals():
        original_pro = pro
        original_div = div
        div, item_name, pro = create_runlength_info(runlength_level, div, item_name, pro)
    else:
        div, item_name, pro = create_expansion_info(expansion_level, div, item_name, pro)
    print_info(div, item_name, pro)

    ent = entropy(div, pro)
    red = redundancy(ent, pro)

    if is_sign == 1:
        sign_length = list(map(int , input().split()))
    elif is_sign == 2:
        hafuman_sign(item_name, pro)
        print("\nHafuman Sign\n", od, "\n")
        sign_length = [len(od[i]) for i in od]
    elif is_sign == 3:
        fixed_runlength = int(input())
        runlength_sign(item_name, fixed_runlength)
        print("\nRunlength Sign\n", od, "\n")
        sign_length = [len(od[i]) for i in od]
        
    if is_sign:
        ave_sign_len = average_sign_length(div, pro, sign_length, expansion_level)
        if is_sign == 3:
            ave_sign_len = average_runlength_sign_length(original_div, original_pro, runlength_level, fixed_runlength)
        elif "runlength_level" in locals():
            print("平均符号長: ", ave_sign_len / average_symbol_length(original_div, original_pro, runlength_level))
        print("average sign length: ", ave_sign_len)


    print("entoropy: ", ent)
    print("redundancy: ", red)

