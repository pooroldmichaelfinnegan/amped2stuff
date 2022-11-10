struct PGF_SIZES {
	u32 TotalFileSize;
	u32 TotalDataSize;
	u32 TextureDataSize;
	u32 NumTextures;
	u32 ShaderDataSize;
};

struct PGF_HEADER {
	u32 VBDataSize;
	u32 IBDataSize;
	u32 PBDataSize;
	u32 BVDataSize;
	u32 MiscDataSize;
	u32 InfluenceDataSize;
	u32 LIMDataSize;
	u32 CollisionDataSize;
	u32 StringTableSize;
	u32 NumShaders;
	u32 NumVertexBuffers;
	u32 NumIndexBuffers;
	u32 NumPushBuffers;
	u32 NumPrimLists;
	u32 NumVBGeomData;
	u32 NumJoints;
	u32 CheskSum;
};

PGF_HEADER model_header @ 3952332;
