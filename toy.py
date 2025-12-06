#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import sys
import sre_parse  # internal but stable enough for introspection
from typing import Dict

# ===== ANSI styling helpers =====

ANSI_RESET = "\033[0m"
ANSI_BOLD = "\033[1m"
ANSI_UNDERLINE = "\033[4m"
ANSI_RED = "\033[31m"
ANSI_GREEN = "\033[32m"
ANSI_YELLOW = "\033[33m"
ANSI_CYAN = "\033[36m"
ANSI_INVERT = "\033[7m"


def supports_color() -> bool:
    """Best-effort check for ANSI color support."""
    if not sys.stdout.isatty():
        return False
    return True


COLOR_ENABLED = supports_color()


def color(text: str, style: str) -> str:
    if not COLOR_ENABLED:
        return text
    return style + text + ANSI_RESET


# ===== i18n / l10n (EN + zh_CN) =====

LANG = "en"

I18N: Dict[str, Dict[str, str]] = {
    "en": {
        "TITLE": "=== Regex Visualizer (CUI) ===",
        "SUBTITLE": "Self-designed visualization engine on top of Python's re module.",
        "SUBTITLE2": "Uses internal parser to cover (almost) all regex features. Bilingual UI (EN/zh_CN).",
        "CURRENT_STATE": "Current state:",
        "STATE_PATTERN": "  Pattern: {pattern!r}  Flags: {flags!r}",
        "STATE_TEXT_LEN": "  Text length: {length} chars",
        "MENU_TITLE": "Menu:",
        "MENU_1": "1) Set / change pattern",
        "MENU_2": "2) Set / change flags (e.g. imsx)",
        "MENU_3": "3) Set / change test text",
        "MENU_4": "4) Show pattern structure (all features)",
        "MENU_5": "5) Find & visualize all matches",
        "MENU_6": "6) Simulate search process",
        "MENU_7": "7) Quit",
        "MENU_8": "8) Switch language (EN/zh_CN)",
        "PROMPT_CHOICE": "Choose an option [1-8]: ",
        "PROMPT_PATTERN": "Enter regex pattern: ",
        "PROMPT_FLAGS": "Enter flags (any of i m s x): ",
        "PROMPT_TEXT_HEADER": "Enter test text",
        "TEXT_END_HINT": "(End with an empty line.)",
        "PROMPT_LANG": "Choose language / 选择语言:",
        "PROMPT_LANG_INPUT": "1) English  2) 简体中文 [1/2]: ",
        "MSG_SET_PATTERN_FIRST": "Set a pattern first.",
        "STRUCTURE_HEADER": "Pattern structure (parsed with Python's regex engine):",
        "MSG_TEXT_WITH_MATCHES": "Text with matches highlighted:",
        "MSG_NO_MATCHES": "No matches found.",
        "MSG_GROUPS_HEADER": "Groups:",
        "MSG_NAMED_GROUPS_HEADER": "Named groups:",
        "MSG_SIMULATION_HEADER": "Search simulation (like re.search):",
        "MSG_SIMULATION_DESC": "Trying pattern against text starting at each position until first success.",
        "MSG_PATTERN_ERROR": "Pattern error: {error}",
        "MSG_CANNOT_SIMULATE": "Cannot simulate, pattern error: {error}",
        "MSG_INVALID_CHOICE": "Invalid choice.",
        "MSG_GOODBYE": "Bye!",
        "LABEL_MATCH_PREFIX": "Match",
        "LABEL_NO_MATCH_AT_POS": "No match at this position.",
        "LABEL_NO_MATCH_ANY": "No match found at any position.",
        "SIM_START_PREFIX": "Start at index",
        "SIM_MATCH_FROM": "Match from",
        "SIM_TO": "to",
    },
    "zh_CN": {
        "TITLE": "=== 正则表达式可视化工具（命令行） ===",
        "SUBTITLE": "基于 Python re 模块的自定义可视化引擎。",
        "SUBTITLE2": "通过内部解析器支持几乎所有正则特性；支持中英文界面。",
        "CURRENT_STATE": "当前状态：",
        "STATE_PATTERN": "  模式: {pattern!r}  标志: {flags!r}",
        "STATE_TEXT_LEN": "  测试文本长度: {length} 个字符",
        "MENU_TITLE": "菜单：",
        "MENU_1": "1) 设置 / 修改 正则模式",
        "MENU_2": "2) 设置 / 修改 标志（如 imsx）",
        "MENU_3": "3) 设置 / 修改 测试文本",
        "MENU_4": "4) 显示模式结构（几乎所有特性）",
        "MENU_5": "5) 查找并可视化所有匹配",
        "MENU_6": "6) 模拟 search 搜索过程",
        "MENU_7": "7) 退出",
        "MENU_8": "8) 切换语言（EN/zh_CN）",
        "PROMPT_CHOICE": "请选择操作 [1-8]: ",
        "PROMPT_PATTERN": "请输入正则模式：",
        "PROMPT_FLAGS": "请输入标志（i m s x 任意组合）：",
        "PROMPT_TEXT_HEADER": "请输入测试文本",
        "TEXT_END_HINT": "（空行结束输入）",
        "PROMPT_LANG": "选择语言 / Choose language:",
        "PROMPT_LANG_INPUT": "1) English  2) 简体中文 [1/2]: ",
        "MSG_SET_PATTERN_FIRST": "请先设置正则模式。",
        "STRUCTURE_HEADER": "模式结构（使用 Python 正则解析）：",
        "MSG_TEXT_WITH_MATCHES": "高亮显示匹配的文本：",
        "MSG_NO_MATCHES": "未找到任何匹配。",
        "MSG_GROUPS_HEADER": "捕获组：",
        "MSG_NAMED_GROUPS_HEADER": "命名组：",
        "MSG_SIMULATION_HEADER": "搜索模拟（类似 re.search）：",
        "MSG_SIMULATION_DESC": "从文本中每个起始位置尝试匹配，直到第一次成功。",
        "MSG_PATTERN_ERROR": "模式错误：{error}",
        "MSG_CANNOT_SIMULATE": "无法模拟，模式错误：{error}",
        "MSG_INVALID_CHOICE": "无效的选项。",
        "MSG_GOODBYE": "再见！",
        "LABEL_MATCH_PREFIX": "匹配",
        "LABEL_NO_MATCH_AT_POS": "该位置没有匹配。",
        "LABEL_NO_MATCH_ANY": "在任何起始位置都没有匹配。",
        "SIM_START_PREFIX": "从索引",
        "SIM_MATCH_FROM": "匹配从",
        "SIM_TO": "到",
    },
}


def tr(key: str) -> str:
    """Translate a short key to the current language."""
    lang_map = I18N.get(LANG, I18N["en"])
    return lang_map.get(key, I18N["en"].get(key, key))


def choose_language_interactive() -> None:
    """Ask user for language at startup or when switching."""
    global LANG
    print()
    print(tr("PROMPT_LANG"))
    choice = input(I18N["en"]["PROMPT_LANG_INPUT"]).strip()  # show both langs prompt
    if choice == "2":
        LANG = "zh_CN"
    else:
        LANG = "en"
    print()


# ===== Regex structure visualization (using sre_parse) =====

def flags_to_str(flags: int) -> str:
    mapping = [
        (re.IGNORECASE, "i"),
        (re.MULTILINE, "m"),
        (re.DOTALL, "s"),
        (re.VERBOSE, "x"),
    ]
    parts = [ch for bit, ch in mapping if flags & bit]
    return "".join(parts) or "0"


def describe_category(cat) -> str:
    """Human-ish description of \d, \w, \s etc., with a tiny bit of l10n."""
    name = str(cat)  # e.g. 'category_digit'
    mapping_en = {
        "category_digit": r"\d (digit)",
        "category_not_digit": r"\D (non-digit)",
        "category_space": r"\s (whitespace)",
        "category_not_space": r"\S (non-whitespace)",
        "category_word": r"\w (word char)",
        "category_not_word": r"\W (non-word char)",
    }
    mapping_zh = {
        "category_digit": r"\d （数字）",
        "category_not_digit": r"\D （非数字）",
        "category_space": r"\s （空白字符）",
        "category_not_space": r"\S （非空白字符）",
        "category_word": r"\w （单词字符）",
        "category_not_word": r"\W （非单词字符）",
    }
    if LANG == "zh_CN":
        return mapping_zh.get(name, name)
    else:
        return mapping_en.get(name, name)


def describe_anchor(at) -> str:
    """Human-ish description of ^, $, \b, etc."""
    name = str(at)  # e.g. 'at_beginning', 'at_boundary'
    mapping_en = {
        "at_beginning": "^ (start of string)",
        "at_beginning_string": r"\A (start of string)",
        "at_beginning_line": "^ (start of line, MULTILINE)",
        "at_end": "$ (end of string or before final \\n)",
        "at_end_string": r"\Z (end of string)",
        "at_end_line": "$ (end of line, MULTILINE)",
        "at_boundary": r"\b (word boundary)",
        "at_non_boundary": r"\B (non-word boundary)",
    }
    mapping_zh = {
        "at_beginning": "^（字符串开头）",
        "at_beginning_string": r"\A（字符串开头）",
        "at_beginning_line": "^（行首，MULTILINE）",
        "at_end": "$（字符串末尾或最后换行前）",
        "at_end_string": r"\Z（字符串末尾）",
        "at_end_line": "$（行尾，MULTILINE）",
        "at_boundary": r"\b（单词边界）",
        "at_non_boundary": r"\B（非单词边界）",
    }
    if LANG == "zh_CN":
        return mapping_zh.get(name, name)
    else:
        return mapping_en.get(name, name)


def format_repeat(minr: int, maxr: int) -> str:
    if maxr == sre_parse.MAXREPEAT:
        max_repr = "∞"
    else:
        max_repr = str(maxr)

    # try to map to common quantifiers
    if minr == 0 and maxr == sre_parse.MAXREPEAT:
        return "* (0 or more)"
    if minr == 1 and maxr == sre_parse.MAXREPEAT:
        return "+ (1 or more)"
    if minr == 0 and maxr == 1:
        return "? (0 or 1)"
    return f"{{{minr},{max_repr}}}"


def format_repeat_zh(minr: int, maxr: int) -> str:
    if maxr == sre_parse.MAXREPEAT:
        max_repr = "∞"
    else:
        max_repr = str(maxr)

    if minr == 0 and maxr == sre_parse.MAXREPEAT:
        return "*（0 次或更多）"
    if minr == 1 and maxr == sre_parse.MAXREPEAT:
        return "+（1 次或更多）"
    if minr == 0 and maxr == 1:
        return "?（0 或 1 次）"
    return f"{{{minr},{max_repr}}}（重复区间）"


def print_charset(charset, indent: int) -> None:
    ind = "  " * indent
    negate = any(op is sre_parse.NEGATE for op, _ in charset)
    if negate:
        if LANG == "zh_CN":
            print(ind + "- [^...] (取反字符集)")
        else:
            print(ind + "- [^...] (negated character set)")
    else:
        if LANG == "zh_CN":
            print(ind + "- [...] (字符集)")
        else:
            print(ind + "- [...] (character set)")

    for op, av in charset:
        if op is sre_parse.NEGATE:
            continue
        if op is sre_parse.LITERAL:
            ch = chr(av)
            if LANG == "zh_CN":
                print(ind + f"    - 字符: {repr(ch)} (code {av})")
            else:
                print(ind + f"    - char: {repr(ch)} (code {av})")
        elif op is sre_parse.RANGE:
            lo, hi = av
            if LANG == "zh_CN":
                print(ind + f"    - 范围: {repr(chr(lo))} - {repr(chr(hi))}")
            else:
                print(ind + f"    - range: {repr(chr(lo))} - {repr(chr(hi))}")
        elif op is sre_parse.CATEGORY:
            if LANG == "zh_CN":
                print(ind + f"    - 类别: {describe_category(av)}")
            else:
                print(ind + f"    - category: {describe_category(av)}")
        elif op is sre_parse.IN:
            # nested charset (rare but possible)
            print_charset(av, indent + 1)
        elif op is sre_parse.NOT_LITERAL:
            ch = chr(av)
            if LANG == "zh_CN":
                print(ind + f"    - 非字符: 非 {repr(ch)}")
            else:
                print(ind + f"    - not char: not {repr(ch)}")
        else:
            if LANG == "zh_CN":
                print(ind + f"    - 其他: {op} {av}")
            else:
                print(ind + f"    - other: {op} {av}")


def print_subpattern(subpattern: sre_parse.SubPattern, group_names, indent: int = 0) -> None:
    ind = "  " * indent
    for op, av in subpattern.data:
        if op is sre_parse.LITERAL:
            ch = chr(av)
            if LANG == "zh_CN":
                print(ind + f"- LITERAL 字面量: {repr(ch)} (code {av})")
            else:
                print(ind + f"- LITERAL: {repr(ch)} (code {av})")

        elif op is sre_parse.NOT_LITERAL:
            ch = chr(av)
            if LANG == "zh_CN":
                print(ind + f"- NOT_LITERAL 非字面量: 非 {repr(ch)}")
            else:
                print(ind + f"- NOT_LITERAL: not {repr(ch)}")

        elif op is sre_parse.IN:
            print_charset(av, indent)

        elif op in (sre_parse.MAX_REPEAT, sre_parse.MIN_REPEAT):
            minr, maxr, inner = av
            if LANG == "zh_CN":
                label = "MAX_REPEAT（贪婪重复）" if op is sre_parse.MAX_REPEAT else "MIN_REPEAT（非贪婪重复）"
                print(ind + f"- {label}: {format_repeat_zh(minr, maxr)}")
            else:
                label = "MAX_REPEAT (greedy)" if op is sre_parse.MAX_REPEAT else "MIN_REPEAT (lazy)"
                print(ind + f"- {label}: {format_repeat(minr, maxr)}")
            print_subpattern(inner, group_names, indent + 1)

        elif op is sre_parse.SUBPATTERN:
            # (group_num, add_flags, del_flags, inner)
            if len(av) == 4:
                group_num, add_flags, del_flags, inner = av
            else:
                # Fallback, older versions
                group_num, add_flags, inner = av[0], av[1], av[-1]
                del_flags = 0

            name = group_names.get(group_num)
            if LANG == "zh_CN":
                if group_num:
                    if name:
                        print(ind + f"- GROUP 组 #{group_num} (命名：{name})")
                    else:
                        print(ind + f"- GROUP 组 #{group_num}")
                else:
                    print(ind + "- 非捕获组 / 内联标志组")
            else:
                if group_num:
                    if name:
                        print(ind + f"- GROUP #{group_num} (name: {name})")
                    else:
                        print(ind + f"- GROUP #{group_num}")
                else:
                    print(ind + "- non-capturing / inline-flags group")

            if add_flags or del_flags:
                if LANG == "zh_CN":
                    print(ind + f"    +标志: {flags_to_str(add_flags)}  -标志: {flags_to_str(del_flags)}")
                else:
                    print(ind + f"    +flags: {flags_to_str(add_flags)}  -flags: {flags_to_str(del_flags)}")
            print_subpattern(inner, group_names, indent + 1)

        elif op is sre_parse.BRANCH:
            _, branches = av
            if LANG == "zh_CN":
                print(ind + "- BRANCH 分支（|）")
            else:
                print(ind + "- BRANCH (alternation |)")
            for i, b in enumerate(branches, 1):
                if LANG == "zh_CN":
                    print(ind + f"  |-- 备选 {i}")
                else:
                    print(ind + f"  |-- Alternative {i}")
                print_subpattern(b, group_names, indent + 2)

        elif op is sre_parse.ANY:
            if LANG == "zh_CN":
                print(ind + "- DOT .（除了换行以外的任意字符）")
            else:
                print(ind + "- DOT . (any character except newline)")

        elif op is sre_parse.AT:
            desc = describe_anchor(av)
            if LANG == "zh_CN":
                print(ind + f"- ANCHOR 锚点: {desc}")
            else:
                print(ind + f"- ANCHOR: {desc}")

        elif op is sre_parse.CATEGORY:
            desc = describe_category(av)
            if LANG == "zh_CN":
                print(ind + f"- CATEGORY 类别: {desc}")
            else:
                print(ind + f"- CATEGORY: {desc}")

        elif op is sre_parse.ASSERT:
            direction, inner, width = av
            if direction < 0:
                if LANG == "zh_CN":
                    print(ind + f"- ASSERT 向后查找（宽度 {width}）")
                else:
                    print(ind + f"- ASSERT lookbehind (width {width})")
            else:
                if LANG == "zh_CN":
                    print(ind + f"- ASSERT 向前查找（宽度 {width}）")
                else:
                    print(ind + f"- ASSERT lookahead (width {width})")
            print_subpattern(inner, group_names, indent + 1)

        elif op is sre_parse.ASSERT_NOT:
            direction, inner, width = av
            if direction < 0:
                if LANG == "zh_CN":
                    print(ind + f"- ASSERT_NOT 负向向后查找（宽度 {width}）")
                else:
                    print(ind + f"- ASSERT_NOT negative lookbehind (width {width})")
            else:
                if LANG == "zh_CN":
                    print(ind + f"- ASSERT_NOT 负向向前查找（宽度 {width}）")
                else:
                    print(ind + f"- ASSERT_NOT negative lookahead (width {width})")
            print_subpattern(inner, group_names, indent + 1)

        elif op is sre_parse.GROUPREF:
            if LANG == "zh_CN":
                print(ind + f"- GROUPREF 组引用: \\{av}")
            else:
                print(ind + f"- GROUPREF: \\{av}")

        elif op is sre_parse.GROUPREF_EXISTS:
            # (group_num, yes, no)
            group_num, yes_pat, no_pat = av
            if LANG == "zh_CN":
                print(ind + f"- GROUPREF_EXISTS 条件组: 若组 #{group_num} 存在")
            else:
                print(ind + f"- GROUPREF_EXISTS conditional: if group #{group_num}")
            if yes_pat is not None:
                if LANG == "zh_CN":
                    print(ind + "  ? 分支 YES：")
                else:
                    print(ind + "  ? YES branch:")
                print_subpattern(yes_pat, group_names, indent + 2)
            if no_pat is not None:
                if LANG == "zh_CN":
                    print(ind + "  : 分支 NO：")
                else:
                    print(ind + "  : NO branch:")
                print_subpattern(no_pat, group_names, indent + 2)

        else:
            # Fallback for rarer internal opcodes
            if LANG == "zh_CN":
                print(ind + f"- 其他内部节点: {op} {av}")
            else:
                print(ind + f"- other internal opcode: {op} {av}")


def print_pattern_structure(pattern: str, flags: int) -> None:
    """Parse pattern with sre_parse and pretty-print the structure."""
    try:
        compiled = re.compile(pattern, flags)
    except re.error as e:
        print(color(tr("MSG_PATTERN_ERROR").format(error=e), ANSI_RED))
        return

    group_names = {num: name for name, num in compiled.groupindex.items()}
    parsed = sre_parse.parse(compiled.pattern, compiled.flags)

    print()
    print(color(tr("STRUCTURE_HEADER"), ANSI_BOLD))
    print()
    print_subpattern(parsed, group_names, indent=0)
    print()


# ===== Match visualization helpers =====

def highlight_matches(text: str, matches) -> str:
    """Highlight all matches in the text using inverse video (or plain text)."""
    matches = list(matches)
    if not matches:
        return text

    result = []
    last = 0
    for m in matches:
        s, e = m.span()
        if s < last:
            # Skip overlapping / zero-length already covered
            continue
        result.append(text[last:s])
        segment = text[s:e]
        result.append(color(segment, ANSI_INVERT))
        last = e
    result.append(text[last:])
    return "".join(result)


def print_match_details(text: str, matches) -> None:
    matches = list(matches)
    if not matches:
        print(color(tr("MSG_NO_MATCHES"), ANSI_RED))
        return

    print()
    for idx, m in enumerate(matches, start=1):
        s, e = m.span()
        prefix = tr("LABEL_MATCH_PREFIX")
        header = f"{prefix} #{idx}: span=({s}, {e})  text={m.group(0)!r}"
        print(color(header, ANSI_GREEN))
        # Show text with a caret line underneath the match
        print(" " * 4 + text)
        print(" " * 4 + " " * s + color("^" * max(1, e - s), ANSI_CYAN))

        # Capturing groups (by index)
        if m.re.groups:
            print(" " * 4 + tr("MSG_GROUPS_HEADER"))
            for gidx in range(1, m.re.groups + 1):
                try:
                    gval = m.group(gidx)
                except IndexError:
                    gval = None
                print(f"      ${gidx}: {gval!r}")

        # Named groups
        if m.re.groupindex:
            print(" " * 4 + tr("MSG_NAMED_GROUPS_HEADER"))
            for name, gidx in m.re.groupindex.items():
                print(f"      {name}: {m.group(gidx)!r}")
        print()


# ===== Simple search simulation engine =====

def simulate_search(pattern: str, flags: int, text: str) -> None:
    """
    Very high-level visualization of how search() scans for a match:
    we try match() at each position until it works.
    """
    print()
    print(color(tr("MSG_SIMULATION_HEADER"), ANSI_BOLD))
    print(tr("MSG_SIMULATION_DESC"))
    print()

    try:
        compiled = re.compile(pattern, flags)
    except re.error as e:
        print(color(tr("MSG_CANNOT_SIMULATE").format(error=e), ANSI_RED))
        return

    for start in range(len(text) + 1):
        prefix = tr("SIM_START_PREFIX")
        label = f"{prefix} {start}: "
        sys.stdout.write(label)
        sys.stdout.flush()
        # Visualize current start position
        prefix_text = text[:start]
        rest = text[start:]
        sys.stdout.write(color("|", ANSI_YELLOW) + prefix_text + color("▶", ANSI_CYAN) + rest + "\n")

        m = compiled.match(text, start)
        if m:
            s, e = m.span()
            match_from = tr("SIM_MATCH_FROM")
            to_word = tr("SIM_TO")
            print(color(f"  ✔ {match_from} {s} {to_word} {e}: {m.group(0)!r}", ANSI_GREEN))
            print("  " + text)
            print("  " + " " * s + color("^" * max(1, e - s), ANSI_CYAN))
            break
        else:
            print(color("  ✖ " + tr("LABEL_NO_MATCH_AT_POS") + "\n", ANSI_RED))
    else:
        print(color(tr("LABEL_NO_MATCH_ANY"), ANSI_RED))


# ===== Utility: flags & input =====

def parse_flags(flag_string: str) -> int:
    mapping = {
        "i": re.IGNORECASE,
        "m": re.MULTILINE,
        "s": re.DOTALL,
        "x": re.VERBOSE,
    }
    flags = 0
    for ch in flag_string:
        if ch.lower() in mapping:
            flags |= mapping[ch.lower()]
    return flags


def read_multiline(prompt: str) -> str:
    print(prompt)
    print(tr("TEXT_END_HINT"))
    lines = []
    while True:
        try:
            line = input()
        except EOFError:
            break
        if line == "":
            break
        lines.append(line)
    return "\n".join(lines)


# ===== Main CUI loop =====

def main():
    choose_language_interactive()

    print(color(tr("TITLE"), ANSI_BOLD))
    print(tr("SUBTITLE"))
    print(tr("SUBTITLE2"))
    print()

    pattern = ""
    flag_string = ""
    text = ""

    while True:
        print(color(tr("CURRENT_STATE"), ANSI_BOLD))
        print(tr("STATE_PATTERN").format(pattern=pattern, flags=flag_string))
        print(tr("STATE_TEXT_LEN").format(length=len(text)))
        print()

        print(color(tr("MENU_TITLE"), ANSI_UNDERLINE))
        print("  " + tr("MENU_1"))
        print("  " + tr("MENU_2"))
        print("  " + tr("MENU_3"))
        print("  " + tr("MENU_4"))
        print("  " + tr("MENU_5"))
        print("  " + tr("MENU_6"))
        print("  " + tr("MENU_7"))
        print("  " + tr("MENU_8"))

        choice = input("\n" + tr("PROMPT_CHOICE")).strip()
        print()

        if choice == "1":
            pattern = input(tr("PROMPT_PATTERN"))
        elif choice == "2":
            flag_string = input(tr("PROMPT_FLAGS"))
        elif choice == "3":
            text = read_multiline(tr("PROMPT_TEXT_HEADER"))
        elif choice == "4":
            if not pattern:
                print(color(tr("MSG_SET_PATTERN_FIRST"), ANSI_RED))
            else:
                flags = parse_flags(flag_string)
                print_pattern_structure(pattern, flags)
        elif choice == "5":
            if not pattern:
                print(color(tr("MSG_SET_PATTERN_FIRST"), ANSI_RED))
                continue
            flags = parse_flags(flag_string)
            try:
                compiled = re.compile(pattern, flags)
            except re.error as e:
                print(color(tr("MSG_PATTERN_ERROR").format(error=e), ANSI_RED))
                continue
            matches = list(compiled.finditer(text))
            print()
            print(color(tr("MSG_TEXT_WITH_MATCHES"), ANSI_BOLD))
            print(highlight_matches(text, matches))
            print_match_details(text, matches)
        elif choice == "6":
            if not pattern:
                print(color(tr("MSG_SET_PATTERN_FIRST"), ANSI_RED))
                continue
            flags = parse_flags(flag_string)
            simulate_search(pattern, flags, text)
        elif choice == "7":
            print(tr("MSG_GOODBYE"))
            break
        elif choice == "8":
            choose_language_interactive()
        else:
            print(color(tr("MSG_INVALID_CHOICE"), ANSI_RED))

        print("\n" + "-" * 60 + "\n")


if __name__ == "__main__":
    main()
