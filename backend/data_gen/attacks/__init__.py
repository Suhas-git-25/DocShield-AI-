from .copy_move import apply_copy_move_attack
from .splicing import apply_splicing_attack
from .font_tamper import apply_font_tamper_attack
from .recompression import apply_recompression_attack
from .metadata_tamper import apply_metadata_tamper_attack
from .geometric_tamper import apply_geometric_tamper_attack

ATTACK_DISPATCHER = {
    "copy_move": apply_copy_move_attack,
    "splicing": apply_splicing_attack,
    "font_tamper": apply_font_tamper_attack,
    "recompression": apply_recompression_attack,
    "metadata_tamper": apply_metadata_tamper_attack,
    "geometric_tamper": apply_geometric_tamper_attack,
}

__all__ = [
    "apply_copy_move_attack",
    "apply_splicing_attack",
    "apply_font_tamper_attack",
    "apply_recompression_attack",
    "apply_metadata_tamper_attack",
    "apply_geometric_tamper_attack",
    "ATTACK_DISPATCHER"
]
