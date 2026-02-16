# -*- coding: utf-8 -*-
# @Time    : 2026/02/15 10:00:00

# 【下一步】 增加 “我的防御策略” 模块


"""
隐性自恋型人格障碍（Covert / Vulnerable NPD）母亲 — 内在程序模型

【疗愈用途说明】
本模块不模拟具体伤害性对话，而是将隐性NPD母亲的行为模式抽象为可命名、可预测的
「程序逻辑」。当你能够把「她又在运行哪一段程序」认出来，就能：
  - 去个人化：不是因为你不够好，而是她的内在程序被触发了；
  - 预测：知道触发条件与常见反应，减少措手不及的恐慌；
  - 命名：用专业术语给经历命名，有助于从混乱中找回现实感。

【心理学依据】
- DSM-5 将隐性自恋归入 NPD 的「脆弱型/敏感型」表现，与显性自恋同一诊断，表现方式不同。
- 隐性NPD：外表羞怯、焦虑、自我贬低，内在仍存在优越感、特权感与对崇拜的渴求；
  对批评极度敏感，常用被动攻击、扮演受害者、道德绑架等方式维持自恋供给。
- 自恋供给（narcissistic supply）：自恋者赖以维持自我形象的外部关注，形式包括
  崇拜、钦佩、恐惧、怜悯等。子女常被置于「血包」角色以持续提供供给。

核心程序围绕三条需求运转（见 CoreNeed 枚举）：
  1. 扩张需求：维护自恋与优越感（让自己看起来永远正确、高人一等，整合地位与重要性）
  2. 生存需求：控制血包在身边（确保有人提供情感反馈、劳动力或作为情绪垃圾桶，防止孤立）
  3. 防御需求：避免羞耻与暴露（掩盖内在虚弱，绝不认错，对外维持完美体面）
"""

from enum import Enum
from typing import List, Tuple, Optional
from dataclasses import dataclass, field


# ---------------------------------------------------------------------------
# 一、供给类型与升级层级（自恋供给的形态与获取策略）
# ---------------------------------------------------------------------------

class SupplyType(Enum):
    """自恋供给类型：自恋者会优先争取崇拜，不足时升级为恐惧或怜悯。"""
    崇拜 = "admiration"      # 默认：赞美、顺从、关注
    恐惧 = "fear"            # 当崇拜不足：威胁、吼叫、惩罚，用恐惧绑住对方
    怜悯 = "pity"            # 当恐惧失效：扮演受害者、哭诉、自怜，换取照顾与愧疚


class EscalationLevel(Enum):
    """供给获取的升级层级：程序会按此顺序尝试恢复供给。"""
    一级_崇拜 = 1   # 正常运转时依赖的供给
    二级_恐惧 = 2   # 当孩子质疑、疏远、不赞美时激活
    三级_怜悯 = 3   # 当恐惧也无法控制时，转为「我才是受害者」


# ---------------------------------------------------------------------------
# 二、程序核心需求（驱动所有行为的底层目标）
# ---------------------------------------------------------------------------
# 三条：扩张需求（自恋与优越感）、生存需求（控制血包）、防御需求（避免羞耻与暴露）。

class CoreNeed(Enum):
    """隐性NPD母亲行为程序的三条核心需求。"""
    # 1. 扩张需求：维护自恋与优越感（整合了原地位与重要性）
    # 目标：让自己看起来像神，永远正确，高人一等。
    维护自恋与优越感 = "maintain_narcissism"

    # 2. 生存需求：控制血包
    # 目标：确保有人提供情感反馈、劳动力或作为情绪垃圾桶，防止孤立。
    控制血包在身边 = "control_supply"

    # 3. 防御需求：避免羞耻与暴露
    # 目标：掩盖内在的虚弱，绝不认错，对外维持完美体面。
    避免羞耻与暴露 = "avoid_shame_exposure"


def get_core_need_description(need: CoreNeed) -> str:
    """返回该核心需求在行为上的表现简述（用于自我觉察与命名）。"""
    descriptions = {
        CoreNeed.维护自恋与优越感: (
            "表现：打压、贬低、挑剔、否认你的感受、颠倒黑白、必须她最好/最对、比较与嫉妒、三角化以维持中心；"
            "本质：扩张需求——让自己看起来像神，永远正确，高人一等（含地位与重要性）。"
        ),
        CoreNeed.控制血包在身边: (
            "表现：道德绑架、guilt-tripping、制造愧疚、破坏边界、惩罚‘不听话’、爱的撤回、扮演受害者；"
            "本质：生存需求——确保你继续提供情感反馈、劳动力或情绪垃圾桶，不逃离，防止孤立。"
        ),
        CoreNeed.避免羞耻与暴露: (
            "表现：对批评/否定极度敏感、否认事实与感受、反击‘揭发者’、回避可能失败的情境；"
            "本质：防御需求——不能承受羞耻与负面评价，绝不认错，用否认与攻击维持完美体面。"
        ),
    }
    return descriptions.get(need, "")


# ---------------------------------------------------------------------------
# 三、常见触发情境（什么会激活程序的防御或攻击）
# ---------------------------------------------------------------------------

class TriggerType(Enum):
    """会激活隐性NPD母亲防御或控制行为的典型情境。"""
    被批评或否定 = "criticism"
    孩子独立或疏远 = "independence"
    设立边界 = "boundary"
    孩子成就超过或脱离 = "outshine"
    未被关注或忽视 = "ignored"
    被质疑或要求负责 = "accountability"
    孩子获得他人关注 = "others_attention"
    暴露缺点或失败 = "exposed_flaw"


def get_trigger_description(trigger: TriggerType) -> str:
    """返回该触发类型的简要说明。"""
    descriptions = {
        TriggerType.被批评或否定: "任何暗示她不够好、错了、不如人的信号",
        TriggerType.孩子独立或疏远: "你减少联系、自己做决定、不依赖她",
        TriggerType.设立边界: "你说不、要求隐私、拒绝被控制",
        TriggerType.孩子成就超过或脱离: "你成功、被认可、不再需要她",
        TriggerType.未被关注或忽视: "焦点不在她身上、没人赞美/照顾她",
        TriggerType.被质疑或要求负责: "你指出她的伤害行为、要求道歉或改变",
        TriggerType.孩子获得他人关注: "别人被夸奖、被爱，她不是中心",
        TriggerType.暴露缺点或失败: "她的错误、无能、不堪被看见",
    }
    return descriptions.get(trigger, "")


# ---------------------------------------------------------------------------
# 四、行为模式 / 战术（程序输出的可命名模式）
# ---------------------------------------------------------------------------

class BehaviorPattern(Enum):
    """隐性NPD母亲常见的行为模式/战术名称。命名它们有助于从‘一团乱’中找回现实感。"""
    贬低与挑剔 = "devaluation"
    否认感受 = "deny_feelings"
    煤气灯 = "gaslighting"
    DARVO = "darvo"                    # Deny, Attack, Reverse Victim and Offender
    道德绑架 = "moral_blackmail"
    惩罚与虐待 = "punishment"
    过度控制 = "over_control"
    被动攻击 = "passive_aggression"
    扮演受害者 = "play_victim"
    比较与嫉妒 = "compare_envy"
    爱的撤回 = "withdraw_love"
    三角化 = "triangulation"           # 拉第三方进来比较、传话、站队


@dataclass
class PatternCard:
    """单条行为模式的卡片：名称、属于哪个核心需求、典型表现、疗愈提示。"""
    pattern: BehaviorPattern
    serves_need: CoreNeed
    description: str
    healing_note: str


def get_pattern_cards() -> List[PatternCard]:
    """返回所有行为模式的疗愈用说明卡片。"""
    return [
        PatternCard(
            BehaviorPattern.贬低与挑剔,
            CoreNeed.维护自恋与优越感,
            "通过贬低你（外貌、能力、选择）来衬托她的优越或‘为你好’的正确性。",
            "她的贬低反映的是她内心的比较与不安全感，不是你的真实价值。",
        ),
        PatternCard(
            BehaviorPattern.否认感受,
            CoreNeed.避免羞耻与暴露,
            "否认你的感受（‘你没那么难受’‘你想多了’），让你怀疑自己的体验。",
            "你的感受是真实的。被否认的是她的共情能力，不是你的感受。",
        ),
        PatternCard(
            BehaviorPattern.煤气灯,
            CoreNeed.避免羞耻与暴露,
            "扭曲事实、否认说过的话、让你怀疑记忆与判断，从而逃避责任。",
            "记录、与可信的人核对，有助于稳住‘我的记忆是对的’。",
        ),
        PatternCard(
            BehaviorPattern.DARVO,
            CoreNeed.避免羞耻与暴露,
            "Deny否认→Attack攻击你→Reverse Victim and Offender 反转成她是受害者。",
            "这是她在面对问责时的程序反应，不是因为你‘不该提’。",
        ),
        PatternCard(
            BehaviorPattern.道德绑架,
            CoreNeed.控制血包在身边,
            "用‘我为你付出那么多’‘你不孝’等让你内疚，从而服从或留下。",
            "你的愧疚是被程序触发的，不等于你真的欠她无限服从。",
        ),
        PatternCard(
            BehaviorPattern.惩罚与虐待,
            CoreNeed.控制血包在身边,
            "用冷漠、吼叫、惩罚让你恐惧或顺从，确保控制力。",
            "恐惧是供给的一种；你感到的恐惧正是程序设计要制造的。",
        ),
        PatternCard(
            BehaviorPattern.过度控制,
            CoreNeed.控制血包在身边,
            "控制你的社交、选择、外表、行踪，削弱你的自主以维持依赖。",
            "你的边界与自主是正当的，不需要她的批准。",
        ),
        PatternCard(
            BehaviorPattern.被动攻击,
            CoreNeed.维护自恋与优越感,
            "不直接表达不满，用冷嘲热讽、拖延、‘忘了’、甩脸来惩罚你。",
            "识别为被动攻击后，可以少从自己身上找‘我哪里又错了’。",
        ),
        PatternCard(
            BehaviorPattern.扮演受害者,
            CoreNeed.控制血包在身边,
            "在冲突中变成‘最受伤的人’，哭诉、生病、自怜，换取你的照顾与愧疚。",
            "这是供给层级中的‘怜悯’策略；你可以选择不接这个角色。",
        ),
        PatternCard(
            BehaviorPattern.比较与嫉妒,
            CoreNeed.维护自恋与优越感,
            "拿你和别人比、或嫉妒你被夸/被爱，通过打压或抢夺关注恢复优越感。",
            "你的好不需要她认证；她的嫉妒属于她的内在程序。",
        ),
        PatternCard(
            BehaviorPattern.爱的撤回,
            CoreNeed.控制血包在身边,
            "用冷漠、疏远、‘不认你’威胁，让你为‘重新获得爱’而服从。",
            "爱被当作条件与筹码，是程序控制手段，不是你的错。",
        ),
        PatternCard(
            BehaviorPattern.三角化,
            CoreNeed.维护自恋与优越感,
            "拉兄弟姐妹、亲戚、外人进来比较、传话、站队，制造分裂与竞争。",
            "三角化是为了分而治之、维持中心地位；看清结构有助于不卷入。",
        ),
    ]


# ---------------------------------------------------------------------------
# 五、程序逻辑：触发 → 可能的行为模式（可预测性）
# ---------------------------------------------------------------------------

def get_likely_patterns_for_trigger(trigger: TriggerType) -> List[BehaviorPattern]:
    """
    根据触发类型，返回该「程序」可能激活的行为模式列表。
    用于：当某情境出现时，提前知道可能发生什么，减少「不知道会发生什么」的焦虑。
    """
    mapping = {
        TriggerType.被批评或否定: [
            BehaviorPattern.DARVO,
            BehaviorPattern.煤气灯,
            BehaviorPattern.否认感受,
            BehaviorPattern.被动攻击,
        ],
        TriggerType.孩子独立或疏远: [
            BehaviorPattern.道德绑架,
            BehaviorPattern.扮演受害者,
            BehaviorPattern.爱的撤回,
            BehaviorPattern.过度控制,
        ],
        TriggerType.设立边界: [
            BehaviorPattern.道德绑架,
            BehaviorPattern.惩罚与虐待,
            BehaviorPattern.否认感受,
            BehaviorPattern.过度控制,
        ],
        TriggerType.孩子成就超过或脱离: [
            BehaviorPattern.贬低与挑剔,
            BehaviorPattern.比较与嫉妒,
            BehaviorPattern.被动攻击,
            BehaviorPattern.扮演受害者,
        ],
        TriggerType.未被关注或忽视: [
            BehaviorPattern.扮演受害者,
            BehaviorPattern.被动攻击,
            BehaviorPattern.三角化,
        ],
        TriggerType.被质疑或要求负责: [
            BehaviorPattern.DARVO,
            BehaviorPattern.煤气灯,
            BehaviorPattern.扮演受害者,
            BehaviorPattern.道德绑架,
        ],
        TriggerType.孩子获得他人关注: [
            BehaviorPattern.比较与嫉妒,
            BehaviorPattern.贬低与挑剔,
            BehaviorPattern.三角化,
        ],
        TriggerType.暴露缺点或失败: [
            BehaviorPattern.DARVO,
            BehaviorPattern.煤气灯,
            BehaviorPattern.否认感受,
            BehaviorPattern.被动攻击,
        ],
    }
    return mapping.get(trigger, [])


def get_escalation_path(current_supply_failing: bool) -> List[SupplyType]:
    """
    当当前供给不足时，程序可能采取的升级路径（崇拜→恐惧→怜悯）。
    了解这一点有助于理解：她突然变凶或突然变可怜，都是同一套程序的不同阶段。
    """
    if not current_supply_failing:
        return [SupplyType.崇拜]
    return [SupplyType.崇拜, SupplyType.恐惧, SupplyType.怜悯]


# ---------------------------------------------------------------------------
# 六、疗愈向工具：按名称查模式、列出所有模式等
# ---------------------------------------------------------------------------

def find_patterns_by_need(need: CoreNeed) -> List[PatternCard]:
    """按核心需求筛选行为模式，便于理解「这段行为是在满足哪个需求」。"""
    cards = get_pattern_cards()
    return [c for c in cards if c.serves_need == need]


def format_core_need_summary() -> List[str]:
    """返回 CoreNeed 三条核心需求的摘要（多行），用于放在 trigger 输出前面。"""
    lines = []
    for need in CoreNeed:
        lines.append(f"  · {need.name}")
        lines.append(f"    {get_core_need_description(need)}")
        lines.append("")
    return lines


def format_escalation_level_summary() -> List[str]:
    """返回 EscalationLevel 供给升级路径的摘要（多行），用于放在 trigger 输出前面。"""
    return [
        "  崇拜（一级）→ 恐惧（二级）→ 怜悯（三级）",
        "  当崇拜不足时程序会升级为恐惧（威胁、惩罚）；恐惧失效则转为怜悯（扮演受害者、自怜）。",
        "",
    ]


def describe_trigger_and_patterns(trigger: TriggerType) -> str:
    """返回一段可读的疗愈向描述：该触发是什么 + 可能出现的模式。"""
    desc = get_trigger_description(trigger)
    patterns = get_likely_patterns_for_trigger(trigger)
    pattern_names = [p.name for p in patterns]
    return (
        f"触发情境：{trigger.name}\n"
        f"含义：{desc}\n"
        f"程序可能激活的行为模式：{', '.join(pattern_names)}\n"
        f"→ 这些行为是可预测的程序输出，不是因为你做错了什么。"
    )


def get_cards_for_trigger(trigger: TriggerType) -> List[PatternCard]:
    """
    根据触发类型，返回该触发可能激活的所有行为模式的完整卡片（含表现与疗愈提示），
    顺序与「可能出现的模式」一致，便于只查看与当前情境相关的部分。
    """
    patterns = get_likely_patterns_for_trigger(trigger)
    all_cards = {c.pattern: c for c in get_pattern_cards()}
    return [all_cards[p] for p in patterns if p in all_cards]


def print_cards_for_trigger(trigger: TriggerType) -> List[str]:
    """
    根据触发类型，先总结 CoreNeed 与 EscalationLevel，再输出该触发对应的行为模式卡片（可读格式）。
    返回字符串列表，便于打印或保存；也可直接遍历打印。
    """
    lines = []
    # 1. CoreNeed 总结
    lines.append("【CoreNeed 三条核心需求】")
    lines.extend(format_core_need_summary())
    # 2. EscalationLevel 总结
    lines.append("【EscalationLevel 供给升级路径】")
    lines.extend(format_escalation_level_summary())
    lines.append("---")
    lines.append("")
    # 3. 触发情境 + PatternCard 全部内容
    desc = describe_trigger_and_patterns(trigger)
    cards = get_cards_for_trigger(trigger)
    lines.append(desc)
    lines.append("")
    for c in cards:
        lines.append(f"【{c.pattern.name}】")
        lines.append(f"  表现：{c.description}")
        lines.append(f"  疗愈提示：{c.healing_note}")
        lines.append("")
    return lines


def list_all_patterns_with_healing_notes() -> List[str]:
    """列出所有行为模式及其疗愈提示，便于一次性阅读或打印。"""
    cards = get_pattern_cards()
    return [
        f"【{c.pattern.name}】\n  表现：{c.description}\n  疗愈提示：{c.healing_note}"
        for c in cards
    ]


# ---------------------------------------------------------------------------
# 七、执行示例
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    trigger = TriggerType.被质疑或要求负责
    for line in print_cards_for_trigger(trigger):
        print(line)
