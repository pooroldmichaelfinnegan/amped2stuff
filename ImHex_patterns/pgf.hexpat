struct Vec3f { float x; float y; float z; };
struct RGBA { u8 red; u8 green; u8 blue; u8 alpha; };

struct PGFHeader {
	u32 fileSize;
	u32 size_from_vertexindex_header_to_eof;
	u32 xpr_data_size;
	u32 xpr_resource_count;
	u32 unk_section_size;
};

enum d3dResourceType {
	u32 xpr    0x00040001;
	u32 vertex 0x00800001;
	u32 index  0x00010001;
}
struct d3dResource {
	u32 d3dResourceType [[comment("0x00040001 = xpr, 0x00800001 = vertex buffer, 0x00010001 = index buffer"), color("a05050")]];
	u32 startIndex [[color("9090ff")]];
	u8 unk[0xC] [[name("unknown 12 bytes"), color("80a0b0")]];
};

struct VertexIndex_Section_Header {
	u32 vertexBufferSize;
	u32 indexBufferSize;
	u8 unk_22_bytes[0x14];
	u32 _0x18A1D0;
	u32 _0x400;
	u32 _unk_null_1;
	u32 vertex_or_index_section_count_1;
	u32 vertex_or_index_section_count_2;
	u32 _unk_null_2;
	u32 _unk_u32;
	u32 vertex_or_index_section_count_3;
	u32 _unk_null_3;
};

struct d3dVertex_0x1C {
	Vec3f position;
	RGBA color;
	Vec3f _2d_thing;
};

struct PGF {
	u32 magic_idk; //0x40400000 ;
	u32 x01_00_FF_0F_thing;
	PGFHeader pgf_header;
	u32 x01_00_FF_0F_thing2;
	XPR_Resource xpr_section[pgf_header.xpr_resource_count];
	u128 xpr_data[pgf_header.xpr_data_size/16];
	u32 x01_00_FF_0F_thing3;
	u8 unk_section[pgf_header.unk_section_size];
	u32 x01_00_FF_0F_thing4;
	VertexIndex_Section_Header vi_header;
	u32 x01_00_FF_0F_thing5;
	u8 vertex_buffer[vi_header.vertexBufferSize];
};

; // [[comment("0xF0FF0001 or  0x01_00_FF_0F  seperates all the sections")]];
PGF pgf @ $;
