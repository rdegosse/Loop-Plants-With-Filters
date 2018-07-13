# Loop-Plants-With-Filters
NO WARRANTY, AS IS, NO SUPPORT... unless you are nice


-- Farmware for farmbot --

Loop plants with filters, execute sequences and save meta data (FARMBOT_OS 6 minimum)


-- Do ---

- Load all plants for current device
- Filter plants with Plant name, Openfarm Slug Name, Plant Age in day range, Meta data key/value, Coordinates
- Sort plants by X,Y
- Execute Init Sequences
- Loop all filtered plants
    - Execute 'Before Move' Sequences
    - Move to plant coordinate (X,Y) with Offset X, Offset Y, Default Z and Default speed
    - Execute 'After Move' Sequences
    - Save meta data key/value if required
    - Save plant_stage value if required
- Execute End Sequences



-- input ---


  {"name": "title", "label": "Title", "value": "-"},
-> Title used for description only

  {"name": "pointname", "label": "Filter by plant name", "value": "*"}
-> Filter by plant name (equal/Not case sensitive)
-> default : * -> all plant name 
  
  {"name": "openfarm_slug", "label": "Filter by Openfarm slug name", "value": "*"}
-> Filter by Openfarm type (equal/Not case sensitive)
-> default : * -> all openfarm_slug

  {"name": "age_min_day", "label": "Filter by plant age (minimum days)", "value": "-1"}
-> Filter by minimum plant age in days
-> default : -1 -> to be sure with time zone and large range..
  
  {"name": "age_max_day", "label": "Filter by plant age (maximum days)", "value": "36500"}
-> Filter by maximum plant age in days
-> default : 36500 -> a plant of a century...

  {"name": "filter_meta_key", "label": "Filter by meta data : key", "value": "None"}
-> Filter by meta data - KEY
-> default : None -> no meta filter

 {"name": "filter_meta_op", "label": "Filter by meta data : operator (==,!=,>,<,>=,<=,regex,daysmin,daysmax,minutesmin,minutesmax)", "value": "=="},
-> Filter by meta data - OPERATOR
-> default : == 
-> ==    : equals (numeric/string)
-> !=    : different (numeric/string)
-> >     : superior (numeric)
-> <     : inferior (numeric)
-> >=    : superior or equal (numeric)
-> <=    : inferior or equal (numeric)
-> regex : regular expression
-> daysmin : minimum days number from now to include plant (datetime)
-> daysmax : maximum days number from now to include plant (datetime)
-> minutesmin : minimum minutes number from now to include plant (datetime)
-> minutesmax : maximum minutes number from now to include plant (datetime)

  {"name": "filter_meta_value", "label": "Filter by meta data : value", "value": "None"}
-> Filter by meta data - VALUE (Not case sensitive)
-> default : None -> no meta filter

  {"name": "filter_plant_stage", "label": "Filter by plant stage (none,planned,planted,harvested)", "value": "None"},
-> Filter by plant stage - none,planned,planted or harvested
-> default : None -> no plant_stage filter

  {"name": "filter_min_x", "label": "Filter by coordinates - Min X", "value": "None"},
-> Filter by coordinates - X minimum
-> default : None -> no coordinates filter

  {"name": "filter_max_x", "label": "Filter by coordinates - Max X", "value": "None"},
-> Filter by coordinates - X maximum
-> default : None -> no coordinates filter

  {"name": "filter_min_y", "label": "Filter by coordinates - Min Y", "value": "None"},
-> Filter by coordinates - Y minimum
-> default : None -> no coordinates filter

  {"name": "filter_max_y", "label": "Filter by coordinates - Max Y", "value": "None"},
-> Filter by coordinates - Y maximum
-> default : None -> no coordinates filter

  {"name": "sequence_init", "label": "Init Sequences Name - one time - (multiple: Seq1,Seq2,...)", "value": "None"},
-> Execute sequences one time, on start. Sequences Name (equal/Not case sensitive)
-> Can be an ordered list of sequences with , seperator : Seq1,Seq2,...
-> default : None -> no execute sequence

  {"name": "sequence_beforemove", "label": "Sequences Name Before Next Move - for each plant - (multiple: Seq1,Seq2,...)", "value": "None"},
-> Execute sequences before each move. Sequence Name (equal/Not case sensitive)
-> Can be an ordered list of sequences with , seperator : Seq1,Seq2,...
-> default : None -> no execute sequence
  
  {"name": "sequence_aftermove", "label": "Sequences Name After Move - for each plant - (multiple: Seq1,Seq2,...)", "value": "None"},
-> Execute sequences after each move. Sequence Name (equal/Not case sensitive)
-> Can be an ordered list of sequences with , seperator : Seq1,Seq2,...
-> default : None -> no execute sequence

  {"name": "sequence_end", "label": "End Sequences Name - one time - (multiple: Seq1,Seq2,...)", "value": "None"},
-> Execute sequences one time, at the end. Sequence Name (equal/Not case sensitive)
-> Can be an ordered list of sequences with , seperator : Seq1,Seq2,...
-> default : None -> no execute sequence

  {"name": "save_meta_key", "label": "Save in meta data : key", "value": "None"}
-> Save meta data after sequence_aftermove - KEY
-> default : None -> no save meta data

  {"name": "save_meta_value", "label": "Save in meta data : value", "value": "None"}
-> Save meta data after sequence_aftermove - VALUE
-> default : None -> no save meta data

  {"name": "save_plant_stage", "label": "Set plant stage (none,planned,planted,harvested)", "value": "None"},
-> Save plant stage to : planned, planted or harvested
-> default : None -> no plant stage change
-> /!\ if planted : planted_at property is changed to now utc (like web app)

  {"name": "offset_x", "label": "Offset X value when moving", "value": 0},
-> add offset X value to each plant
-> default : 0 -> no offset

  {"name": "offset_y", "label": "Offset Y value when moving", "value": 0},
-> add offset Y value to each plant
-> default : 0 -> no offset

  {"name": "default_z", "label": "default Z axis value when moving", "value": 0}
-> default z axis coordinate when moving
-> default : 0 -> Z axis coordinate

  {"name": "default_speed", "label": "default speed value when moving", "value": 800}
-> default speed when moving
-> default : 800 -> default value in celery script

  {"name": "debug", "label": "Debug (0-> No FW debug msg, 1-> FW debug msg, 2-> No Move/exec and FW debug msg only)", "value": 1}
-> debug mode : 0 -> no farmware debug log, 1 -> farmware debug log, 2 -> simulation : no move, no execute sequence, no save meta data AND only farmware debug log
-> default : 1 -> move/exec and debug log


