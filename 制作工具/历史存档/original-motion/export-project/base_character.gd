class_name BaseCharacter
extends CharacterBody2D
# Offscreen export host only. Original player/bicycle drawing scripts stay byte-identical.
var walk_speed: float = 112.0
var run_speed: float = 175.0
var input_enabled: bool = false
func _ready() -> void: pass
func set_facing(_value: GameConstants.FacingDirection) -> void: pass
func update_stamina(_delta: float, wants_run: bool) -> bool: return wants_run
