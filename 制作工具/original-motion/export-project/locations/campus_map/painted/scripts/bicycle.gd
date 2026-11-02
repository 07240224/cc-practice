extends Node2D
## Bike geometry stays attached to the same collision body as the student.
var direction := Vector2(0,-1)
var phase := 0.0
var speed := 0.0

func update_pose(facing: Vector2, travel_speed: float, delta: float, height: float) -> void:
	direction=facing
	speed=travel_speed
	phase=fmod(phase+delta*travel_speed/15.0,TAU)
	position.y=-height
	queue_redraw()

func stroke(points: Array, tint: Color, width: float) -> void:
	draw_polyline(PackedVector2Array(points),Color("34453c"),width+1.6,true)
	draw_polyline(PackedVector2Array(points),tint,width,true)

func wheel(at: Vector2, radii: Vector2) -> void:
	var rim := PackedVector2Array()
	for i in range(33):
		var angle := float(i)*TAU/32.0
		rim.append(at+Vector2(cos(angle),sin(angle))*radii)
	draw_colored_polygon(rim,Color(0.81,0.84,0.75,0.23))
	draw_polyline(rim,Color("36443f"),3.4,true)
	draw_polyline(rim,Color("b9c4b7"),1.0,true)
	for i in range(4):
		var angle := phase+float(i)*PI/4.0
		var p := Vector2(cos(angle),sin(angle))*radii*0.83
		draw_line(at-p,at+p,Color(0.61,0.70,0.64,0.75),0.8,true)
	draw_circle(at,1.8,Color("e6d9ad"))

func _draw() -> void:
	if absf(direction.x)>absf(direction.y):
		var side := 1.0 if direction.x>0 else -1.0
		draw_set_transform(Vector2.ZERO,0,Vector2(side,1))
		wheel(Vector2(-20,-7),Vector2(12,12))
		wheel(Vector2(20,-7),Vector2(12,12))
		stroke([Vector2(-20,-7),Vector2(-6,-26),Vector2(5,-8),Vector2(-20,-7)],Color("4e9381"),2.5)
		stroke([Vector2(-6,-26),Vector2(12,-27),Vector2(5,-8)],Color("66aa95"),2.3)
		stroke([Vector2(20,-7),Vector2(11,-32),Vector2(16,-35),Vector2(20,-35)],Color("8aa99a"),2.1)
		stroke([Vector2(-6,-26),Vector2(-8,-32)],Color("98aaa0"),2.0)
		stroke([Vector2(-15,-32),Vector2(-3,-32)],Color("6e5742"),3.1)
		# Knees and shoes pedal independently of the walking sprite.
		for i in range(2):
			var angle := phase+float(i)*PI
			var pedal := Vector2(3+cos(angle)*7,-9+sin(angle)*5)
			var knee := Vector2(5+cos(angle)*6,-22+sin(angle)*3)
			stroke([Vector2(-5,-32),knee,pedal],Color("30465c") if i==0 else Color("42596a"),4.2)
			stroke([pedal-Vector2(3,0),pedal+Vector2(4,0)],Color("584e42"),2.7)
		stroke([Vector2(1,-39),Vector2(10,-35),Vector2(18,-34)],Color("edc89d"),2.4)
	else:
		wheel(Vector2(0,-24),Vector2(5.5,11))
		wheel(Vector2(0,1),Vector2(5.5,12))
		stroke([Vector2(0,-27),Vector2(0,-1)],Color("529b86"),4.0)
		stroke([Vector2(-12,-22),Vector2(12,-22)],Color("9fb8a5"),2.2)
		for i in range(2):
			var side := -1.0 if i==0 else 1.0
			var pedal := Vector2(side*8,-8+sin(phase+float(i)*PI)*5)
			stroke([Vector2(side*5,-32),Vector2(side*10,-20),pedal],Color("354d62"),4.2)
			stroke([pedal-Vector2(3,0),pedal+Vector2(3,0)],Color("625443"),2.8)
		stroke([Vector2(-10,-31),Vector2(-12,-23)],Color("efcba2"),2.5)
		stroke([Vector2(10,-31),Vector2(12,-23)],Color("efcba2"),2.5)
	draw_set_transform(Vector2.ZERO,0,Vector2.ONE)
