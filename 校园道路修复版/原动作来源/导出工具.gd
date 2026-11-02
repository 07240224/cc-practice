extends SceneTree
const PLAYER = preload("res://locations/campus_map/painted/scripts/player.gd")
const BIKE = preload("res://locations/campus_map/painted/scripts/bicycle.gd")
const PHASES = 128
const CELL = 192
const COLS = 32
const ROWS = 17
var viewport: SubViewport
var actor: Node2D
var atlas: Image
var metadata := {"cell":192,"columns":32,"rows":17,"origin":[96,160],"renderScale":2,"phaseCount":128,"walkOffset":0,"bikeOffset":12,"directions":["down","up","left","right"],"sequence":[0,1,2,1],"animationRate":7.0,"spriteScale":0.235,"sourceSpeeds":{"walk":112.0,"run":175.0,"bike":300.0},"frames":[]}
func _initialize() -> void:
	call_deferred("export_all")
func export_all() -> void:
	viewport=SubViewport.new()
	viewport.size=Vector2i(CELL,CELL)
	viewport.transparent_bg=true
	viewport.disable_3d=true
	viewport.render_target_update_mode=SubViewport.UPDATE_ALWAYS
	viewport.canvas_item_default_texture_filter=Viewport.DEFAULT_CANVAS_ITEM_TEXTURE_FILTER_LINEAR
	root.add_child(viewport)
	actor=PLAYER.new()
	var cycle=BIKE.new()
	cycle.name="Bicycle"
	cycle.visible=false
	actor.add_child(cycle)
	actor.bicycle=cycle
	var visual=Node2D.new()
	visual.name="Visual"
	actor.add_child(visual)
	var sprite=Sprite2D.new()
	sprite.name="StudentSprite"
	sprite.region_enabled=true
	sprite.region_filter_clip_enabled=true
	sprite.scale=Vector2.ONE*PLAYER.SPRITE_SCALE
	visual.add_child(sprite)
	actor._sprite=sprite
	actor.position=Vector2(96,160)
	actor.scale=Vector2(2,2)
	viewport.add_child(actor)
	actor.set_physics_process(false)
	actor.set_process(false)
	var source=Image.load_from_file("res://locations/campus_map/painted/assets/student-walk-v2.png")
	var frames=JSON.parse_string(FileAccess.get_file_as_string("res://locations/campus_map/painted/data/frames.json"))
	actor.setup(ImageTexture.create_from_image(source),frames)
	atlas=Image.create(COLS*CELL,ROWS*CELL,false,Image.FORMAT_RGBA8)
	atlas.fill(Color.TRANSPARENT)
	var dirs=[Vector2.DOWN,Vector2.UP,Vector2.LEFT,Vector2.RIGHT]
	for row in 4:
		actor.set_riding(false)
		actor.last_direction=dirs[row]
		actor._update_facing()
		for column in 3:
			actor._apply_frame(column)
			await capture(row*3+column)
	for row in 4:
		actor.last_direction=dirs[row]
		actor._update_facing()
		actor.set_riding(true)
		for phase in PHASES:
			cycle.phase=float(phase)*TAU/float(PHASES)
			cycle.update_pose(dirs[row],PLAYER.BICYCLE_SPEED,0.0,0.0)
			await capture(12+row*PHASES+phase)
		print("exported riding row ",row)
	var target="/workspace/scratch/original-motion/original-motion-atlas.png"
	var code=atlas.save_png(target)
	assert(code==OK)
	var f=FileAccess.open("/workspace/scratch/original-motion/atlas.json",FileAccess.WRITE)
	f.store_string(JSON.stringify(metadata,"\t"))
	print("ORIGINAL_MOTION_EXPORT_OK ",target)
	quit(0)
func capture(index:int) -> void:
	actor.queue_redraw()
	await process_frame
	await RenderingServer.frame_post_draw
	var img=viewport.get_texture().get_image()
	assert(img!=null and not img.is_empty())
	img.convert(Image.FORMAT_RGBA8)
	atlas.blit_rect(img,Rect2i(0,0,CELL,CELL),Vector2i((index%COLS)*CELL,(index/COLS)*CELL))
