// amped 2 level boundaries

struct Vec3f {
	float x [[color("cce6ff")]];
	float y [[color("f7e6ff")]];
	float z [[color("ccffe6")]];
};

// lineloop mesh primitive
struct LineLoop {
	u32 num [[name("num of vertices"), color("ffff4d")]];
	Vec3f lineLoop[num];
};

// polyline mesh primitive, dont know why the vertex count is double
struct Lines {
	u32 num [[name("num of vertices"), color("ffff4d")]];
	Vec3f lineStrip[num * 2];
};

LineLoop endZone @ 0 [[comment("run finished zone")]];
LineLoop innerKill @ endZone.num*12 + 4 [[comment("kill zone warning")]];
LineLoop outerKill @ (endZone.num + innerKill.num)*12 + 8 [[comment("kill zone")]];
Lines resetPos @ (endZone.num + innerKill.num + outerKill.num)*12 + 12 [[comment("reset positions")]];

