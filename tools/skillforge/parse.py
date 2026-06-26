from __future__ import annotations

from pathlib import Path
from typing import Any


class ParseError(ValueError):
    pass


def parse_scalar(value: str) -> Any:
    value = value.strip()
    if value == "":
        return ""
    if value in {"true", "True"}:
        return True
    if value in {"false", "False"}:
        return False
    if value in {"null", "None", "~"}:
        return None
    if value.startswith('"') and value.endswith('"'):
        return value[1:-1]
    if value.startswith("'") and value.endswith("'"):
        return value[1:-1]
    if value.startswith("[") and value.endswith("]"):
        inner = value[1:-1].strip()
        if not inner:
            return []
        return [parse_scalar(part.strip()) for part in inner.split(",")]
    if value.isdigit() or (value.startswith("-") and value[1:].isdigit()):
        try:
            return int(value)
        except ValueError:
            return value
    return value


def parse_yaml(text: str) -> Any:
    raw_lines = []
    for line_number, line in enumerate(text.splitlines(), start=1):
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        if "\t" in line[: len(line) - len(line.lstrip())]:
            raise ParseError(f"Tabs are not supported in YAML indentation at line {line_number}")
        indent = len(line) - len(line.lstrip(" "))
        raw_lines.append((indent, stripped, line_number))

    if not raw_lines:
        return {}

    def parse_block(index: int, indent: int) -> tuple[Any, int]:
        if index >= len(raw_lines):
            return {}, index
        current_indent, current_text, _ = raw_lines[index]
        if current_indent < indent:
            return {}, index
        if current_text.startswith("- "):
            return parse_list(index, current_indent)
        return parse_map(index, current_indent)

    def parse_list(index: int, indent: int) -> tuple[list[Any], int]:
        items: list[Any] = []
        while index < len(raw_lines):
            current_indent, text, line_number = raw_lines[index]
            if current_indent != indent or not text.startswith("- "):
                break
            value_text = text[2:].strip()
            index += 1
            if value_text == "":
                value, index = parse_block(index, indent + 2)
                items.append(value)
                continue
            if is_inline_mapping(value_text):
                key, value = split_key_value(value_text, line_number)
                item: dict[str, Any] = {key: parse_scalar(value) if value else {}}
                if value == "":
                    nested, index = parse_block(index, indent + 2)
                    item[key] = nested
                while index < len(raw_lines):
                    next_indent, next_text, next_line = raw_lines[index]
                    if next_indent <= indent:
                        break
                    if next_indent != indent + 2 or next_text.startswith("- "):
                        nested, index = parse_block(index, next_indent)
                        if isinstance(nested, dict):
                            item.update(nested)
                        else:
                            raise ParseError(f"Unexpected nested list at line {next_line}")
                        continue
                    nested_key, nested_value = split_key_value(next_text, next_line)
                    index += 1
                    if nested_value == "":
                        child, index = parse_block(index, indent + 4)
                        item[nested_key] = child
                    else:
                        item[nested_key] = parse_scalar(nested_value)
                items.append(item)
            else:
                items.append(parse_scalar(value_text))
        return items, index

    def parse_map(index: int, indent: int) -> tuple[dict[str, Any], int]:
        result: dict[str, Any] = {}
        while index < len(raw_lines):
            current_indent, text, line_number = raw_lines[index]
            if current_indent < indent:
                break
            if current_indent > indent:
                raise ParseError(f"Unexpected indentation at line {line_number}")
            if text.startswith("- "):
                break
            key, value = split_key_value(text, line_number)
            index += 1
            if value == "":
                child, index = parse_block(index, indent + 2)
                result[key] = child
            else:
                result[key] = parse_scalar(value)
        return result, index

    parsed, final_index = parse_block(0, raw_lines[0][0])
    if final_index != len(raw_lines):
        _, _, line_number = raw_lines[final_index]
        raise ParseError(f"Could not parse YAML at line {line_number}")
    return parsed


def split_key_value(text: str, line_number: int) -> tuple[str, str]:
    if ":" not in text:
        raise ParseError(f"Expected key/value pair at line {line_number}")
    key, value = text.split(":", 1)
    key = key.strip()
    if not key:
        raise ParseError(f"Empty key at line {line_number}")
    return key, value.strip()


def is_inline_mapping(value_text: str) -> bool:
    if ":" not in value_text:
        return False
    key = value_text.split(":", 1)[0].strip()
    return bool(key) and all(character.isalnum() or character in {"_", "-"} for character in key)


def parse_yaml_file(path: Path) -> Any:
    try:
        return parse_yaml(path.read_text(encoding="utf-8"))
    except ParseError:
        raise
    except OSError as exc:
        raise ParseError(str(exc)) from exc


def parse_skill_markdown(path: Path) -> tuple[dict[str, Any], str]:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        raise ParseError("SKILL.md must start with YAML frontmatter")
    end = text.find("\n---", 4)
    if end == -1:
        raise ParseError("SKILL.md frontmatter must end with ---")
    frontmatter_text = text[4:end].strip()
    body = text[end + 4 :].strip()
    frontmatter = parse_yaml(frontmatter_text)
    if not isinstance(frontmatter, dict):
        raise ParseError("SKILL.md frontmatter must be a mapping")
    return frontmatter, body
