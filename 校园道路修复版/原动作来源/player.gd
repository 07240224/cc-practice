extends BaseCharacter
class_name PaintedCampusPlayer

@export var controls_enabled: bool = true

const WALK_SPEED: float = 112.0
const RUN_SPEED: float = 175.0
const BICYCLE_SPEED: float = 300.0
const BicycleScript = preload("res://locations/campus_map/painted/scripts/bicycle.gd")
const SPRITE_SCALE: float = 0.235
const ANIMATION_RATE: float = 7.0
const WALK_FRAMES: Array[int] = [0, 1, 2, 1]

var _shared_rig: Node2D
var last_direction: Vector2 = Vector2(0.0, -1.0)
var _sprite: Sprite2D
var _frames: Array = []
var _texture: Texture2D
var _animation_step: float = 0.0
var _facing_row: int = 1
var _has_focus: bool = true
var _web_keyboard: JavaScriptObject
var surface_height := 0.0
var riding := false
var bicycle: Node2D
var climbing := false
var climb_moving := false
var climb_offset := Vector2.ZERO

func set_climbing(value: bool) -> void:
	climbing=value
	climb_moving=value
	if value:
		set_riding(false)
		last_direction=Vector2.UP
		_update_facing()
	else:
		climb_offset=Vector2.ZERO
		set_surface_height(0.0)

func set_climb_offset(value: Vector2) -> void:
	climb_offset=value
	set_surface_height(-value.y)

func set_facing(direction: GameConstants.FacingDirection) -> void:
	super.set_facing(direction)
	last_direction=[Vector2.UP,Vector2.DOWN,Vector2.LEFT,Vector2.RIGHT][direction]
	_update_facing()
	_apply_frame(1)

func set_riding(value: bool) -> void:
	riding=value
	if is_instance_valid(bicycle): bicycle.visible=riding
	_apply_frame(1)
	queue_redraw()

func set_surface_height(value: float) -> void:
	if climbing: value=-climb_offset.y
	# Physics stays on the map plane; only the drawing rises over an arched deck.
	if value<0.0 and riding: set_riding(false)
	if is_equal_approx(surface_height,value): return
	surface_height=value
	if is_instance_valid(_sprite): _sprite.position=Vector2(climb_offset.x,-value)
	queue_redraw()

func visual_foot_position() -> Vector2:
	return position+Vector2(climb_offset.x,-surface_height)


# Accept either four rows of three dictionaries, or twelve row-major dictionaries.
func setup(texture: Texture2D, frames: Array) -> void:
	_ensure_nodes()
	_frames.clear()
	_texture = null
	_sprite.texture = null
	_sprite.visible = false
	if texture == null:
		push_error("CampusPlayer.setup: student texture is missing.")
		return

	var flat_frames: Array = []
	if frames.size() == 4 and frames[0] is Array:
		for row_index in range(4):
			if not (frames[row_index] is Array):
				push_error("CampusPlayer.setup: animation row %d must be an Array." % row_index)
				return
			var row: Array = frames[row_index]
			if row.size() != 3:
				push_error("CampusPlayer.setup: animation row %d must contain three frames." % row_index)
				return
			flat_frames.append_array(row)
	elif frames.size() == 12:
		flat_frames = frames.duplicate(true)
	else:
		push_error("CampusPlayer.setup: expected four rows of three frames, or twelve flat frames.")
		return

	for frame_index in range(flat_frames.size()):
		if not (flat_frames[frame_index] is Dictionary):
			push_error("CampusPlayer.setup: frame %d must be a Dictionary." % frame_index)
			return
		var frame: Dictionary = flat_frames[frame_index]
		for key in ["x", "y", "w", "h"]:
			if not frame.has(key) or not (typeof(frame[key]) == TYPE_INT or typeof(frame[key]) == TYPE_FLOAT):
				push_error("CampusPlayer.setup: frame %d requires numeric %s." % [frame_index, key])
				return
		if float(frame["w"]) <= 0.0 or float(frame["h"]) <= 0.0:
			push_error("CampusPlayer.setup: frame %d has an empty region." % frame_index)
			return

	_frames = flat_frames.duplicate(true)
	_texture = texture
	_sprite.texture = _texture
	_sprite.visible = true
	_apply_frame(1)


func _ready() -> void:
	_ensure_nodes()
	super._ready()
	if OS.has_feature("web") and JavaScriptBridge.eval("typeof window.campusKeyboard !== 'undefined'"):
		_web_keyboard = JavaScriptBridge.get_interface("campusKeyboard")
	_sprite.texture = _texture
	_sprite.visible = _texture != null and _frames.size() == 12
	_apply_frame(1)


func _ensure_nodes() -> void:
	motion_mode = CharacterBody2D.MOTION_MODE_FLOATING
	if is_instance_valid(_sprite):
		return

	bicycle=BicycleScript.new()
	bicycle.name="Bicycle"
	bicycle.visible=false
	add_child(bicycle)
	_sprite = Sprite2D.new()
	_sprite.name = "StudentSprite"
	_sprite.region_enabled = true
	_sprite.region_filter_clip_enabled = true
	_sprite.scale = Vector2.ONE * SPRITE_SCALE
	add_child(_sprite)

	var collision := CollisionShape2D.new()
	collision.name = "FootCollision"
	var circle := CircleShape2D.new()
	circle.radius = 8.0
	collision.shape = circle
	add_child(collision)
	var visual := Node2D.new()
	visual.name="Visual"
	add_child(visual)
	_sprite.reparent(visual)
	_shared_rig=load("res://characters/shared/campus_student_v1/human_visual.tscn").instantiate()
	_shared_rig.name="Rig"
	_shared_rig.scale=Vector2.ONE*0.07
	visual.add_child(_shared_rig)
	# Keep the shared character API for framework actions and saved presentation,
	# while the campus renders its original four-direction hand-painted sprite.
	_shared_rig.hide()
	_shared_rig.process_mode=Node.PROCESS_MODE_DISABLED
	walk_speed=WALK_SPEED
	run_speed=RUN_SPEED
	collision_layer=2
	collision_mask=1
	queue_redraw()


func _physics_process(delta: float) -> void:
	if climbing:
		velocity=Vector2.ZERO
		if controls_enabled and input_enabled and climb_moving:
			_animation_step=fmod(_animation_step+delta*5.0,float(WALK_FRAMES.size()))
		_apply_frame(WALK_FRAMES[int(_animation_step)] if climb_moving else 1)
		return
	var direction := Vector2.ZERO
	var focused: bool = bool(_web_keyboard.focused) if _web_keyboard != null else _has_focus
	if controls_enabled and input_enabled and focused:
		# Physical keys remain held when the browser changes Shift modifiers.
		# Keep action input for the touch controls as well.
		direction = movement_direction()

	var wants_run: bool = bool(_web_keyboard.run) if _web_keyboard != null else Input.is_key_pressed(KEY_SHIFT) or Input.is_action_pressed("run")
	var running := update_stamina(delta,wants_run and not riding and direction.length_squared()>0.0)
	if direction.length_squared() > 0.0:
		direction = direction.normalized()
		last_direction = direction
		_update_facing()
		var speed: float = BICYCLE_SPEED if riding else RUN_SPEED if running else WALK_SPEED
		velocity = direction * speed
		_animation_step = fmod(_animation_step + delta * ANIMATION_RATE, float(WALK_FRAMES.size()))
		_apply_frame(1 if riding else WALK_FRAMES[int(_animation_step)])
	else:
		velocity = Vector2.ZERO
		_animation_step = 0.0
		_apply_frame(1)

	move_and_slide()
	if is_instance_valid(bicycle): bicycle.update_pose(last_direction,velocity.length(),delta,surface_height)


func movement_direction() -> Vector2:
	if _web_keyboard != null:
		var keyboard := Vector2(float(bool(_web_keyboard.right))-float(bool(_web_keyboard.left)),float(bool(_web_keyboard.down))-float(bool(_web_keyboard.up)))
		# Actions also support the touch pad; prefer physical browser keys when held.
		return keyboard.normalized() if keyboard != Vector2.ZERO else Input.get_vector("touch_left","touch_right","touch_up","touch_down")
	var left := Input.is_physical_key_pressed(KEY_A) or Input.is_physical_key_pressed(KEY_LEFT) or Input.is_action_pressed("move_left") or Input.is_action_pressed("touch_left")
	var right := Input.is_physical_key_pressed(KEY_D) or Input.is_physical_key_pressed(KEY_RIGHT) or Input.is_action_pressed("move_right") or Input.is_action_pressed("touch_right")
	var up := Input.is_physical_key_pressed(KEY_W) or Input.is_physical_key_pressed(KEY_UP) or Input.is_action_pressed("move_up") or Input.is_action_pressed("touch_up")
	var down := Input.is_physical_key_pressed(KEY_S) or Input.is_physical_key_pressed(KEY_DOWN) or Input.is_action_pressed("move_down") or Input.is_action_pressed("touch_down")
	return Vector2(float(right)-float(left),float(down)-float(up)).normalized()


func _update_facing() -> void:
	if absf(last_direction.x) > absf(last_direction.y):
		_facing_row = 3 if last_direction.x > 0.0 else 2
	else:
		_facing_row = 0 if last_direction.y > 0.0 else 1


func _apply_frame(column: int) -> void:
	if not is_instance_valid(_sprite):
		return
	var index: int = _facing_row * 3 + column
	if index < 0 or index >= _frames.size():
		return
	if not (_frames[index] is Dictionary):
		return
	var frame: Dictionary = _frames[index]
	var frame_width: float = float(frame.get("w", 0))
	var frame_height: float = float(frame.get("h", 0))
	var visible_height: float=frame_height*0.68 if riding else frame_height
	_sprite.region_rect = Rect2(float(frame.get("x", 0)), float(frame.get("y", 0)), frame_width, visible_height)
	# Each cropped frame stays centered horizontally, with its feet at this body's origin.
	_sprite.offset = Vector2(0.0, -frame_height+visible_height*0.5)


func _notification(what: int) -> void:
	if what == NOTIFICATION_WM_WINDOW_FOCUS_OUT:
		_has_focus = false
		velocity = Vector2.ZERO
		_animation_step = 0.0
		_apply_frame(1)
	elif what == NOTIFICATION_WM_WINDOW_FOCUS_IN:
		_has_focus = true


func _draw() -> void:
	if climbing: return
	draw_set_transform(Vector2(0.0, -1.0-surface_height), 0.0, Vector2(1.0, 0.35))
	if riding:
		draw_set_transform(Vector2(0,-surface_height),0,Vector2(1.0,0.22))
		draw_circle(Vector2.ZERO,32.0,Color(0.17,0.25,0.19,0.16))
	else:
		draw_circle(Vector2.ZERO, 12.0, Color(0.17, 0.25, 0.19, 0.19))
	draw_set_transform(Vector2.ZERO, 0.0, Vector2.ONE)
