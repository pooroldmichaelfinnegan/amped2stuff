LuaP		ๆ[กฐนฒA2   @../Image/Levels/HD2/ScriptedObjectsMapHelper.lua                                                    "   "   #   #   $   $   %   %   H   '   j   J      l   ค      ว   ฆ   ว         UNKNOWN_AUDIO_EVENT       ๐?      ๐ฟ   AUDIO_EVENT_SNOWMAN_TAUNT            AUDIO_EVENT_SNOWMAN_FOUND 
   DecVarRef 
   DecVarVal    DecVar    liftChairCount    liftObserverCount    snowmanCount 	   busCount    PlantLiftChair    PlantSnowCat    PlantLiftObserver    PlantSnowman 	   PlantBus                   VType           VName           VRef              	   
                     Name    Type    Value       ๐?      ๐ฟ
   Reference        ส  I }	}?~                  VType           VName           VValue                                      Name    Type    Value 
   Reference            ส  I }	} ~ฟ~                  VType           VName           VValue           VRef                                       Name    Type    Value 
   Reference        ส  I }	} ~ษ~       '            table '   +   ,   (   )   )   )   )   *   +   -   .   /   0   0   0   0   0   0   1   2   3   3   3   3   4   5   7   8   9   :   ;   =   >   ?   @   @   @   @   B   B   C   F   F   F   G   H         Name 
   LiftChair    liftChairCount    Type    LiftChairInstance    TypeSpecificData    PGFName    MM_LiftChair_Quad    MainAniName    ParentObject        Pos         
   YRotation    TriggerVolumeRadius       ๐?   ScriptName    LiftChairStateMachine 
   Variables    varLiftChairAnimation 
   animation    Value       ๐ฟ
   Reference    varLiftChairObject    object     ,      A     I } ฟ~ 
 I@I@	ม
     มIBA   ำ  
 ส  IC}ร~	ฤIภส  D}ษฤ~	ฤA    I_   I   Lย           J            table           K   L   M   N   P   Q   R   S   T   T   T   T   T   T   U   V   W   X   Z   [   \   ]   ^   `   a   b   c   e   e   f   i   j         Name 	   Snow_Cat    Type    SnowCatInstance    TypeSpecificData    PGFName    MainAniName    ScriptName    AutoRunAnimationStateMachine    ParentObject        Pos         
   YRotation    TriggerVolumeRadius       @
   Variables 
   animation    varAnimation    Value       ๐?      ๐ฟ
   Reference    object 
   varObject            ษ>} I?~ 
 ษพษ>ภ	ม
     มIB
 ส  ษB~	C}ษรษ>ส  ID~D}ษรษ>_   I          l           liftChairIndex     %      seatPosition     %      table !   %   &   m   n   n   n   n   o   p   r   s   t   t   t   t   u   v   v   v   v   v   v   w   x   y   z   |   }   ~                                          Name    LiftObserver    liftObserverCount    Type    ScriptedObjectInstance    TypeSpecificData    PGFName    M_Observer_Lift    MainAniName        ParentObject 
   LiftChair    AttachPosition    Pos         
   YRotation    TriggerVolumeRadius       4@   ScriptName    DoNothingStateMachine 
   Variables    object 
   varObject    Value       ๐?      ๐ฟ
   Reference     &     A    ษ }ฟ~
 I@ษ@ม    S	I 
     		ยษBICส  ษร~	D}ษฤA    I	ษ  ฤ                    x     =      y     =      z     =      yRot     =      challengeName     =      table 9   =   >                                                                                                                                                                              ข   ข   ข   ฃ   ค   $      Name    Snowman    snowmanCount    Type    ScriptedObjectInstance    TypeSpecificData    PGFName    MainAniName        ParentObject    Pos 
   YRotation    TriggerVolumeRadius       @   ObjectScale            ScriptName    ExplorationItemStateMachine 
   Variables 
   DecVarRef    object 
   varObject 
   animation    varIdleAnimation 	   Snow_Cat    varFoundAnimation 
   DecVarVal    soundID    varFoundSound    AUDIO_EVENT_SNOWMAN_FOUND    userStringValue    varChallengeID    userIntValue    varChallengePartIndex        @      ๐?    >     A    ำ}ฟ~
 ษ>ภภ
     	  
  ษษษAIBษB
 ล  	A 
A     ล 	 
ม   	ล 
 A   
 ม  E  ล  ม      A   G ` ษ  LG         ฆ           AnimationName     (      table $   (   )   ง   จ   จ   จ   จ   ฉ   ช   ฌ   ญ   ฎ   ฏ   ฐ   ฐ   ฐ   ฐ   ฐ   ฐ   ฑ   ฒ   ณ   ด   ถ   ท   ธ   น   บ   ผ   ฝ   พ   ฟ   ฟ   ฟ   ฟ   ม   ม   ย   ล   ล   ล   ฦ   ว         Name    Bus 	   busCount    Type    ScriptedObjectInstance    TypeSpecificData    PGFName    MB_Bus_Lower    MainAniName    ScriptName    AutoRunAnimationStateMachine    ParentObject        Pos         
   YRotation    TriggerVolumeRadius       @
   Variables 
   animation    varAnimation    Value       ๐?      ๐ฟ
   Reference    object 
   varObject     )     A    ำ  }ฟ~
 I@	 	มม
     ษ	ยษB
 ส  Iร~C}Iฤ	 ส  ษฤ~	E}IฤA    ำ_  ษ   D                ว   A   G  "     b   ว  ข     A   G  A     A   ว  A     โ   G  "    b  ว  ข    โ  G    