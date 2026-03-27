import hashlib
import html
import re
from typing import TYPE_CHECKING, Any, Dict, Iterable

from django.utils.html import strip_tags

if TYPE_CHECKING:
    from ..core import BaseRenderer, BlockState
    from ..markdown import Markdown

__all__ = ["clicker"]


clicker_item = re.compile(r"^(\[[ xX]\])\s+")


def clicker_hook(md: "Markdown", *args: Any) -> Any:
    """
    Support both Mistune hook signatures:
    - v3-style: hook(md, state)
    - older/custom: hook(md, tokens, state)
    """
    if len(args) == 1:
        state = args[0]
        tokens = getattr(state, "tokens", None)
        if tokens is not None:
            _rewrite_all_list_items(tokens)
        return state

    if len(args) >= 2:
        tokens = args[0]
        return _rewrite_all_list_items(tokens)

    return None


def render_clicker(renderer: "BaseRenderer", text: str, checked: bool = False) -> str:
    safe_text = html.escape(strip_tags(text))
    renderer_uniq_id = renderer.uniq_id if hasattr(renderer, "uniq_id") else ""
    clicker_id = hashlib.sha1(f"{renderer_uniq_id}{safe_text}".encode()).hexdigest()
    return f'<clicker clicker-id="{clicker_id}" text="{safe_text}"></clicker>'


def clicker(md: "Markdown") -> None:
    """A mistune plugin to support clickers. Spec defined by:
        - [ ] click me
        - [x] click me
    """
    md.before_render_hooks.append(clicker_hook)
    if md.renderer and md.renderer.NAME == "html":
        md.renderer.register("clicker_item", render_clicker)


def _rewrite_all_list_items(tokens: Iterable[Dict[str, Any]]) -> Iterable[Dict[str, Any]]:
    for tok in tokens:
        if tok["type"] == "list_item":
            _rewrite_list_item(tok)
        if "children" in tok:
            _rewrite_all_list_items(tok["children"])
    return tokens


def _rewrite_list_item(tok: Dict[str, Any]) -> None:
    children = tok["children"]
    if children:
        first_child = children[0]
        text = first_child.get("text", "")
        m = clicker_item.match(text)
        if m:
            mark = m.group(1)
            first_child["text"] = text[m.end() :]

            tok["type"] = "clicker_item"
            tok["attrs"] = {"checked": mark != "[ ]"}
