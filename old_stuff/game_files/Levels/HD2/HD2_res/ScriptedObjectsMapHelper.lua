LuaP		ζ[‘°Ή²A2   @../Image/Levels/HD2/ScriptedObjectsMapHelper.lua                                                    "   "   #   #   $   $   %   %   H   '   j   J      l   €      Η   ¦   Η         UNKNOWN_AUDIO_EVENT       π?      πΏ   AUDIO_EVENT_SNOWMAN_TAUNT            AUDIO_EVENT_SNOWMAN_FOUND 
   DecVarRef 
   DecVarVal    DecVar    liftChairCount    liftObserverCount    snowmanCount 	   busCount    PlantLiftChair    PlantSnowCat    PlantLiftObserver    PlantSnowman 	   PlantBus                   VType           VName           VRef              	   
                     Name    Type    Value       π?      πΏ
   Reference        Κ  I }	}?~                  VType           VName           VValue                                      Name    Type    Value 
   Reference            Κ  I }	} ~Ώ~                  VType           VName           VValue           VRef                                       Name    Type    Value 
   Reference        Κ  I }	} ~Ι~       '            table '   +   ,   (   )   )   )   )   *   +   -   .   /   0   0   0   0   0   0   1   2   3   3   3   3   4   5   7   8   9   :   ;   =   >   ?   @   @   @   @   B   B   C   F   F   F   G   H         Name 
   LiftChair    liftChairCount    Type    LiftChairInstance    TypeSpecificData    PGFName    MM_LiftChair_Quad    MainAniName    ParentObject        Pos         
   YRotation    TriggerVolumeRadius       π?   ScriptName    LiftChairStateMachine 
   Variables    varLiftChairAnimation 
   animation    Value       πΏ
   Reference    varLiftChairObject    object     ,      A     I } Ώ~ 
 I@I@	Α
     ΑIBA   Σ  
 Κ  IC}Γ~	ΔIΐΚ  D}ΙΔ~	ΔA    I_   I   LΒ           J            table           K   L   M   N   P   Q   R   S   T   T   T   T   T   T   U   V   W   X   Z   [   \   ]   ^   `   a   b   c   e   e   f   i   j         Name 	   Snow_Cat    Type    SnowCatInstance    TypeSpecificData    PGFName    MainAniName    ScriptName    AutoRunAnimationStateMachine    ParentObject        Pos         
   YRotation    TriggerVolumeRadius       @
   Variables 
   animation    varAnimation    Value       π?      πΏ
   Reference    object 
   varObject            Ι>} I?~ 
 ΙΎΙ>ΐ	Α
     ΑIB
 Κ  ΙB~	C}ΙΓΙ>Κ  ID~D}ΙΓΙ>_   I          l           liftChairIndex     %      seatPosition     %      table !   %   &   m   n   n   n   n   o   p   r   s   t   t   t   t   u   v   v   v   v   v   v   w   x   y   z   |   }   ~                                          Name    LiftObserver    liftObserverCount    Type    ScriptedObjectInstance    TypeSpecificData    PGFName    M_Observer_Lift    MainAniName        ParentObject 
   LiftChair    AttachPosition    Pos         
   YRotation    TriggerVolumeRadius       4@   ScriptName    DoNothingStateMachine 
   Variables    object 
   varObject    Value       π?      πΏ
   Reference     &     A    Ι }Ώ~
 I@Ι@Α    S	I 
     		ΒΙBICΚ  ΙΓ~	D}ΙΔA    I	Ι  Δ                    x     =      y     =      z     =      yRot     =      challengeName     =      table 9   =   >                                                                                                                                                                              ’   ’   ’   £   €   $      Name    Snowman    snowmanCount    Type    ScriptedObjectInstance    TypeSpecificData    PGFName    MainAniName        ParentObject    Pos 
   YRotation    TriggerVolumeRadius       @   ObjectScale            ScriptName    ExplorationItemStateMachine 
   Variables 
   DecVarRef    object 
   varObject 
   animation    varIdleAnimation 	   Snow_Cat    varFoundAnimation 
   DecVarVal    soundID    varFoundSound    AUDIO_EVENT_SNOWMAN_FOUND    userStringValue    varChallengeID    userIntValue    varChallengePartIndex        @      π?    >     A    Σ}Ώ~
 Ι>ΐΐ
     	  
  ΙΙΙAIBΙB
 Ε  	A 
A     Ε 	 
Α   	Ε 
 A   
 Α  E  Ε  Α      A   G ` Ι  LG         ¦           AnimationName     (      table $   (   )   §   ¨   ¨   ¨   ¨   ©   ͺ   ¬   ­   ?   ―   °   °   °   °   °   °   ±   ²   ³   ΄   Ά   ·   Έ   Ή   Ί   Ό   ½   Ύ   Ώ   Ώ   Ώ   Ώ   Α   Α   Β   Ε   Ε   Ε   Ζ   Η         Name    Bus 	   busCount    Type    ScriptedObjectInstance    TypeSpecificData    PGFName    MB_Bus_Lower    MainAniName    ScriptName    AutoRunAnimationStateMachine    ParentObject        Pos         
   YRotation    TriggerVolumeRadius       @
   Variables 
   animation    varAnimation    Value       π?      πΏ
   Reference    object 
   varObject     )     A    Σ  }Ώ~
 I@	 	ΑΑ
     Ι	ΒΙB
 Κ  IΓ~C}IΔ	 Κ  ΙΔ~	E}IΔA    Σ_  Ι   D                Η   A   G  "     b   Η  ’     A   G  A     A   Η  A     β   G  "    b  Η  ’    β  G    